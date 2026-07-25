"""Command-line entry point and the outer agent loop.

The agentic loop, end to end:

    parse   - understand the analyst's free-text input (extract + classify
              IOCs, detect intents such as "most active families" or
              "summarise")
    plan    - choose which feeds/endpoints apply to each IOC (enrich.plan_for)
    act     - execute the feed lookups, tolerating per-source failures
    reason  - fold the evidence into deterministic, source-cited verdicts
    report  - render analyst cards, a batch threat picture, and optionally a
              Claude-written brief grounded in that same evidence
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from . import __version__, feeds, llm, report
from .enrich import enrich_many
from .iocs import extract_iocs, extract_with_invalid

STATS_INTENT = re.compile(r"most\s+active|trending|malware\s+famil|top\s+famil", re.IGNORECASE)
DAYS_RE = re.compile(r"last\s+(\d+)\s+days?|\b(\d+)\s+days?\b", re.IGNORECASE)
SUMMARY_INTENT = re.compile(r"summari[sz]e|summary|threat\s+picture|overall\s+picture", re.IGNORECASE)

KEY_FILENAME = "abusech_auth.key"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m ioc_agent",
        description=(
            "IOC Enrichment & Threat Intelligence Agent - grounded, source-cited "
            "triage of IPs, domains, URLs and file hashes against the abuse.ch "
            "feeds (ThreatFox, URLhaus, MalwareBazaar)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            '  python -m ioc_agent "Is 185.220.101.45 a known malicious IP?"\n'
            "  python -m ioc_agent --file sample_iocs.txt\n"
            "  python -m ioc_agent --stats 7\n"
            "  python -m ioc_agent --demo --file sample_iocs.txt   (offline demo)\n"
            "  python -m ioc_agent                                 (interactive session)\n"
        ),
    )
    parser.add_argument("query", nargs="*", help="free-text question and/or IOCs (quotes recommended)")
    parser.add_argument("-f", "--file", help="file of IOCs, one per line ('#' comments ignored; defanged OK)")
    parser.add_argument(
        "--stats", nargs="?", const=7, type=int, metavar="DAYS",
        help="most active malware families in ThreatFox over the last DAYS days (default 7, API max 7)",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output incl. raw feed responses (audit trail)")
    parser.add_argument("--demo", action="store_true", help="offline demo mode with canned fixture data (clearly labelled)")
    parser.add_argument("--llm", action="store_true", help="add a Claude-written brief grounded in the evidence (needs ANTHROPIC_API_KEY; optional)")
    parser.add_argument("--auth-key", help="abuse.ch Auth-Key (or set ABUSECH_AUTH_KEY, or an abusech_auth.key file)")
    parser.add_argument("--plain", action="store_true", help="plain ASCII output (no colour panels)")
    parser.add_argument("--timeout", type=float, default=15.0, help="per-request timeout in seconds (default 15)")
    parser.add_argument("--workers", type=int, default=4, help="parallel IOC lookups in batch mode (default 4)")
    parser.add_argument("--version", action="version", version="ioc-agent {}".format(__version__))
    return parser.parse_args(argv)


def resolve_auth_key(args) -> str | None:
    import os

    if args.auth_key:
        return args.auth_key
    for env_name in ("ABUSECH_AUTH_KEY", "ABUSE_CH_AUTH_KEY", "ABUSECH_API_KEY"):
        value = os.environ.get(env_name)
        if value:
            return value
    for base in (Path.cwd(), Path(__file__).resolve().parent.parent):
        candidate = base / KEY_FILENAME
        try:
            if candidate.exists():
                text = candidate.read_text(encoding="utf-8").strip()
                if text:
                    return text
        except OSError:
            continue
    return None


def finish_report(enrichments, args, invalid_inputs=None) -> None:
    llm_text = None
    if args.llm:
        text, reason = llm.narrate(report.llm_payload(enrichments))
        if reason:
            report.notice("Claude brief skipped: {}".format(reason))
        llm_text = text
    report.print_enrichments(
        enrichments, llm_text=llm_text, json_mode=args.json, invalid_inputs=invalid_inputs
    )


def run_stats(days: int, args) -> int:
    days = max(1, min(days or 7, 7))
    result = feeds.threatfox_recent(days)
    report.print_stats(days, result, json_mode=args.json)
    return 0 if result.ok else 1


def run_text(text: str, args, invalid_from_file=None) -> int:
    iocs, invalid_tokens = extract_with_invalid(text)
    if not iocs and not invalid_tokens and not invalid_from_file and STATS_INTENT.search(text):
        m = DAYS_RE.search(text)
        days = int(next((g for g in m.groups() if g), 7)) if m else 7
        return run_stats(days, args)

    # INVALID input is a distinct category: surfaced explicitly, never queried,
    # and never conflated with an UNKNOWN (no records) lookup result.
    invalids = list(invalid_from_file or [])
    for token in invalid_tokens:
        if not any(token in line for line in invalids):
            invalids.append(token)
    for item in invalids:
        report.notice("INVALID input skipped (failed validation, not queried): {!r}".format(item))

    if not iocs:
        if invalids:
            report.notice("No valid IOCs to look up - every candidate failed validation.")
            return 2
        report.notice(
            "No IOCs recognised in the input. I extract IPv4 addresses, domains, URLs "
            "and MD5/SHA1/SHA256 hashes (defanged forms like hxxp:// and [.] are fine)."
        )
        report.print_help_examples()
        return 2
    report.notice("Enriching {} IOC(s) across the abuse.ch feeds...".format(len(iocs)))
    enrichments = enrich_many(iocs, max_workers=args.workers)
    finish_report(enrichments, args, invalid_inputs=invalids)
    return 0


def interactive(args) -> int:
    report.print_banner()
    last_enrichments = []
    while True:
        try:
            # Strip BOM/zero-width characters too - they ride along when input
            # is piped through Windows shells or pasted from web pages.
            line = input("ioc-agent> ").strip().strip("\ufeff\u200b").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        lowered = line.lower()
        if lowered in ("quit", "exit", "q"):
            break
        if lowered in ("help", "?", "h"):
            report.print_help_examples()
            continue
        iocs_in_line, invalid_in_line = extract_with_invalid(line)
        if not iocs_in_line and not invalid_in_line and SUMMARY_INTENT.search(line):
            if last_enrichments:
                llm_text = None
                if args.llm:
                    text, reason = llm.narrate(report.llm_payload(last_enrichments))
                    if reason:
                        report.notice("Claude brief skipped: {}".format(reason))
                    llm_text = text
                report.print_summary_only(last_enrichments, llm_text=llm_text)
            else:
                report.notice("Nothing to summarise yet - look up some IOCs first.")
            continue
        if not iocs_in_line and not invalid_in_line and (STATS_INTENT.search(line) or lowered.startswith("stats")):
            m = DAYS_RE.search(line)
            days = int(next((g for g in m.groups() if g), 7)) if m else 7
            run_stats(days, args)
            continue
        for item in invalid_in_line:
            report.notice("INVALID input skipped (failed validation, not queried): {!r}".format(item))
        if not iocs_in_line:
            if not invalid_in_line:
                report.notice(
                    "No IOCs recognised. Paste IPs/domains/URLs/hashes, or try 'stats', "
                    "'summarise', 'help'."
                )
            continue
        report.notice("Enriching {} IOC(s) across the abuse.ch feeds...".format(len(iocs_in_line)))
        last_enrichments = enrich_many(iocs_in_line, max_workers=args.workers)
        finish_report(last_enrichments, args, invalid_inputs=invalid_in_line)
    return 0


def main(argv=None) -> int:
    args = parse_args(argv)

    if args.plain or args.json:
        report.set_plain(True)

    if args.demo:
        from .demo_fixtures import FIXTURES

        feeds.enable_demo(FIXTURES)
    else:
        key = resolve_auth_key(args)
        feeds.set_auth_key(key)
        if not key:
            report.notice("No abuse.ch Auth-Key configured - live lookups will fail. " + feeds.AUTH_HINT)
    feeds.set_timeout(args.timeout)

    if args.stats is not None:
        return run_stats(args.stats, args)

    text = ""
    file_invalid_lines: list = []
    if args.file:
        path = Path(args.file)
        if not path.exists():
            report.notice("File not found: {}".format(path))
            return 2
        raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        kept = [ln.strip() for ln in raw_lines if ln.strip() and not ln.strip().startswith("#")]
        # Whole lines that yield no valid IOC are INVALID input for a
        # one-indicator-per-line file; run_text surfaces and tracks them.
        file_invalid_lines = [ln for ln in kept if not extract_iocs(ln)]
        text = "\n".join(kept)
    if args.query:
        text = (text + "\n" + " ".join(args.query)).strip()

    if not text.strip():
        if args.file or args.query:
            report.notice(
                "No usable input - the file/arguments were empty after removing comments."
            )
            return 2
        return interactive(args)
    return run_text(text, args, invalid_from_file=file_invalid_lines)
