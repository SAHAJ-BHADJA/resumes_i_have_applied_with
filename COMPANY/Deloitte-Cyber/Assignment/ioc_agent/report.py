"""Rendering: analyst-facing cards, batch summaries, stats tables, JSON output.

Uses `rich` for colour panels/tables when available and falls back to plain
ASCII otherwise - the content is identical either way, so nothing analyst-
facing depends on the pretty renderer. JSON mode emits a machine-readable
audit record that includes the raw feed responses (trust & traceability).
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone

from . import feeds
from .verdict import (
    LEVEL_INCONCLUSIVE,
    LEVEL_MALICIOUS,
    LEVEL_NO_RECORDS,
    LEVEL_TEST,
)

try:
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    _console = Console(highlight=False)
    _err_console = Console(stderr=True, highlight=False)
except ImportError:  # plain-text fallback keeps the tool runnable anywhere
    _console = None
    _err_console = None

_force_plain = False

LEVEL_HEADLINE = {
    LEVEL_MALICIOUS: "MALICIOUS",
    LEVEL_TEST: "TEST FILE (EICAR) - not a real threat",
    LEVEL_NO_RECORDS: "UNKNOWN - no records in the queried feeds",
    LEVEL_INCONCLUSIVE: "ERROR - one or more sources could not be checked",
}
LEVEL_SHORT = {
    LEVEL_MALICIOUS: "malicious",
    LEVEL_TEST: "test artifact",
    LEVEL_NO_RECORDS: "unknown",
    LEVEL_INCONCLUSIVE: "error",
}

_SOURCE_ORDER = ("ThreatFox", "URLhaus", "MalwareBazaar")
LEVEL_COLOR = {
    LEVEL_MALICIOUS: "red",
    LEVEL_TEST: "yellow",
    LEVEL_NO_RECORDS: "cyan",
    LEVEL_INCONCLUSIVE: "magenta",
}

DEMO_BANNER = (
    "DEMO MODE - responses below are canned fixtures shaped like real abuse.ch "
    "replies (no network calls were made). Remove --demo for live lookups."
)

EXAMPLE_QUERIES = [
    'python -m ioc_agent "Is 185.220.101.45 a known malicious IP? What is it associated with?"',
    'python -m ioc_agent "Look up the hash 44d88612fea8a8f36de82e1278abb02f - is this malware?"',
    'python -m ioc_agent "Check the URL http://194.165.16.11/bins/tsunami.arm7 and tell me what you find."',
    'python -m ioc_agent "I have these 3 IPs from our proxy logs - which ones are malicious? 185.220.101.45, 8.8.8.8, 1.2.3.4"',
    'python -m ioc_agent "What malware families have been most active in ThreatFox in the last 7 days?"',
    'python -m ioc_agent "Is emotet-c2-update.xyz a known bad domain, and how confident are you?"',
    "python -m ioc_agent --file sample_iocs.txt        (batch + overall threat picture)",
]


def _rich_on() -> bool:
    return _console is not None and not _force_plain


def set_plain(value: bool) -> None:
    global _force_plain
    _force_plain = value


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def notice(msg: str) -> None:
    """Meta-information for the user. Goes to stderr so --json stdout stays clean."""
    if _rich_on() and _err_console is not None:
        _err_console.print(Text("[!] " + msg, style="dim"))
    else:
        print("[!] " + msg, file=sys.stderr)


def _trunc(s: str, n: int) -> str:
    s = str(s)
    return s if len(s) <= n else s[: n - 2] + ".."


# ------------------------------------------------------------- per-IOC card

def _card_lines(e) -> list:
    v = e.verdict
    lines = []
    conf = ""
    if v.confidence != "n/a":
        conf = " - confidence {}".format(v.confidence.upper())
        if v.confidence_detail:
            conf += " ({})".format(v.confidence_detail)
    lines.append("Verdict : {}{}".format(LEVEL_HEADLINE.get(v.level, v.level), conf))
    if v.classification:
        lines.append("Class   : {}".format(v.classification))
    if v.families:
        fam = ", ".join(v.families)
        if v.aliases:
            fam += "  (aliases: {})".format(", ".join(v.aliases))
        lines.append("Malware : {}".format(fam))
    if v.first_seen or v.last_seen:
        seen = "first {}   last {}".format(v.first_seen or "?", v.last_seen or "?")
        if v.active:
            seen += "   [ACTIVE within 90d]"
        lines.append("Seen    : {}".format(seen))
    lines.append("Action  : {} - {}".format(v.priority, v.priority_detail))
    if v.evidence:
        lines.append("Evidence:")
        for b in v.evidence:
            lines.append("  - {}".format(b))
    if v.context_note:
        lines.append("Context : {} (local analyst note, not a feed verdict)".format(v.context_note))
    for c in v.caveats:
        lines.append("Caveat  : {}".format(c))
    queried = e.results[0].queried_at if e.results else _stamp()
    lines.append("Sources : {}   (queried {})".format(v.sources_line, queried))
    return lines


def _print_card(e) -> None:
    title = "{}  [{}]".format(e.ioc.value, e.ioc.label)
    body = "\n".join(_card_lines(e))
    if _rich_on():
        _console.print(
            Panel(
                Text(body),
                title=Text(title, style="bold"),
                border_style=LEVEL_COLOR.get(e.verdict.level, "white"),
                box=box.ROUNDED,
            )
        )
    else:
        print("=" * 78)
        print(title)
        print("-" * 78)
        print(body)
        print()


# --------------------------------------------------------- batch summarising

def summary_data(enrichments, invalid_inputs=None) -> dict:
    levels = Counter(e.verdict.level for e in enrichments)
    families = Counter(f for e in enrichments for f in e.verdict.families)
    consulted = [
        s for s in _SOURCE_ORDER
        if any(r.source == s for e in enrichments for r in e.results)
    ]
    return {
        "total_submitted": len(enrichments) + len(invalid_inputs or []),
        "total": len(enrichments),
        "counts": {LEVEL_SHORT[k]: n for k, n in levels.items()},
        "invalid_count": len(invalid_inputs or []),
        "invalid_inputs": list(invalid_inputs or []),
        "families": dict(families.most_common()),
        "p1_act_now": [e.ioc.value for e in enrichments if e.verdict.priority == "P1"],
        "p2_investigate": [e.ioc.value for e in enrichments if e.verdict.priority == "P2"],
        "no_records": [e.ioc.value for e in enrichments if e.verdict.level == LEVEL_NO_RECORDS],
        "errors": [e.ioc.value for e in enrichments if e.verdict.level == LEVEL_INCONCLUSIVE],
        "test_artifacts": [e.ioc.value for e in enrichments if e.verdict.level == LEVEL_TEST],
        "sources_consulted": consulted,
    }


def _threat_picture_lines(enrichments, invalid_inputs=None) -> list:
    d = summary_data(enrichments, invalid_inputs=invalid_inputs)
    counts = ", ".join("{} {}".format(n, name) for name, n in d["counts"].items())
    head = "{} indicator(s) triaged: {}".format(d["total"], counts)
    if d["invalid_count"]:
        head += " (+{} invalid input(s) skipped)".format(d["invalid_count"])
    lines = [head + "."]
    if d["families"]:
        fams = ", ".join("{} ({})".format(f, n) for f, n in d["families"].items())
        lines.append("Malware families in play: {}.".format(fams))
    if d["p1_act_now"]:
        lines.append("P1 - act now: {}.".format(", ".join(d["p1_act_now"])))
    if d["p2_investigate"]:
        lines.append("P2 - investigate: {}.".format(", ".join(d["p2_investigate"])))
    if d["test_artifacts"]:
        lines.append("Test artifacts (not threats): {}.".format(", ".join(d["test_artifacts"])))
    if d["no_records"]:
        lines.append(
            "Unknown (no feed evidence): {} - verify with additional sources before closing.".format(
                ", ".join(d["no_records"])
            )
        )
    if d["errors"]:
        lines.append(
            "Errors (could not check): {} - treat as unknown, not clean; re-run when feeds are reachable.".format(
                ", ".join(d["errors"])
            )
        )
    if d["invalid_inputs"]:
        lines.append(
            "Invalid input skipped (never queried): {}.".format(", ".join(d["invalid_inputs"]))
        )
    if d["sources_consulted"]:
        lines.append("Sources consulted: {}.".format(", ".join(d["sources_consulted"])))
    steps = []
    if d["p1_act_now"]:
        steps.append("push P1 indicators to egress/proxy blocklists now")
    if d["p1_act_now"] or d["p2_investigate"]:
        steps.append("retro-hunt proxy/email/EDR logs across each indicator's seen-window")
    steps.append("treat 'no records' as unverified, not clean - pivot to VT/AbuseIPDB/passive DNS")
    lines.append("Suggested next steps: {}.".format("; ".join(steps)))
    return lines


def _print_summary_table(enrichments) -> None:
    if _rich_on():
        table = Table(box=box.SIMPLE_HEAVY, title="Batch triage summary")
        table.add_column("Indicator", max_width=42, overflow="fold")
        table.add_column("Type")
        table.add_column("Verdict")
        table.add_column("Conf")
        table.add_column("Malware")
        table.add_column("Prio")
        for e in enrichments:
            v = e.verdict
            table.add_row(
                e.ioc.value,
                e.ioc.type,
                Text(LEVEL_SHORT[v.level], style=LEVEL_COLOR.get(v.level, "white")),
                v.confidence,
                _trunc(", ".join(v.families) or "-", 24),
                v.priority,
            )
        _console.print(table)
    else:
        print("BATCH TRIAGE SUMMARY")
        header = "{:<42} {:<7} {:<13} {:<7} {:<24} {:<4}".format(
            "Indicator", "Type", "Verdict", "Conf", "Malware", "Prio"
        )
        print(header)
        print("-" * len(header))
        for e in enrichments:
            v = e.verdict
            print(
                "{:<42} {:<7} {:<13} {:<7} {:<24} {:<4}".format(
                    _trunc(e.ioc.value, 42),
                    e.ioc.type,
                    LEVEL_SHORT[v.level],
                    v.confidence,
                    _trunc(", ".join(v.families) or "-", 24),
                    v.priority,
                )
            )
        print()


def _print_threat_picture(enrichments, invalid_inputs=None) -> None:
    body = "\n".join(
        "- {}".format(line) for line in _threat_picture_lines(enrichments, invalid_inputs=invalid_inputs)
    )
    if _rich_on():
        _console.print(
            Panel(Text(body), title=Text("Overall threat picture", style="bold"), border_style="blue", box=box.ROUNDED)
        )
    else:
        print("OVERALL THREAT PICTURE")
        print(body)
        print()


def _print_llm_panel(text: str) -> None:
    title = "Claude analyst brief (generated from the evidence above - verdicts remain deterministic)"
    if _rich_on():
        _console.print(Panel(Text(text), title=Text(title, style="bold"), border_style="green", box=box.ROUNDED))
    else:
        print(title.upper())
        print(text)
        print()


def _print_demo_banner() -> None:
    if _rich_on():
        _console.print(Text(DEMO_BANNER, style="bold yellow"))
    else:
        print("*** " + DEMO_BANNER + " ***")


# -------------------------------------------------------------- entry points

def print_enrichments(enrichments, llm_text=None, json_mode=False, invalid_inputs=None) -> None:
    if json_mode:
        print(
            json.dumps(
                to_json_payload(enrichments, llm_text=llm_text, invalid_inputs=invalid_inputs),
                indent=2,
                default=str,
            )
        )
        return
    if feeds.demo_enabled():
        _print_demo_banner()
    for e in enrichments:
        _print_card(e)
    if len(enrichments) > 1 or invalid_inputs:
        _print_summary_table(enrichments)
        _print_threat_picture(enrichments, invalid_inputs=invalid_inputs)
    if llm_text:
        _print_llm_panel(llm_text)


def print_summary_only(enrichments, llm_text=None) -> None:
    _print_summary_table(enrichments)
    _print_threat_picture(enrichments)
    if llm_text:
        _print_llm_panel(llm_text)


def print_stats(days: int, feed_result, json_mode=False) -> None:
    if not feed_result.ok:
        notice("ThreatFox stats unavailable: {}".format(feed_result.error))
        if json_mode:
            print(json.dumps({"error": feed_result.error, "source": "ThreatFox"}, indent=2))
        return
    families = Counter(
        str(rec.get("malware_printable") or rec.get("malware") or "unknown")
        for rec in feed_result.records
    )
    total = len(feed_result.records)
    note = (
        "Window: IOCs submitted to ThreatFox in the last {} day(s) ({} IOCs). "
        "Counts reflect reporting volume on abuse.ch, not global prevalence.".format(days, total)
    )
    if json_mode:
        print(
            json.dumps(
                {
                    "source": "ThreatFox get_iocs",
                    "window_days": days,
                    "total_iocs": total,
                    "families": dict(families.most_common()),
                    "generated_at": _stamp(),
                    "mode": "demo" if feeds.demo_enabled() else "live",
                },
                indent=2,
            )
        )
        return
    if feeds.demo_enabled():
        _print_demo_banner()
    if _rich_on():
        table = Table(
            box=box.SIMPLE_HEAVY,
            title="ThreatFox - most active malware families (last {} day(s))".format(days),
        )
        table.add_column("#", justify="right")
        table.add_column("Malware family")
        table.add_column("New IOCs", justify="right")
        table.add_column("Share", justify="right")
        for i, (fam, n) in enumerate(families.most_common(12), 1):
            table.add_row(str(i), fam, str(n), "{:.0f}%".format(100.0 * n / max(total, 1)))
        _console.print(table)
        _console.print(Text(note, style="dim"))
    else:
        print("THREATFOX - MOST ACTIVE MALWARE FAMILIES (last {} day(s))".format(days))
        for i, (fam, n) in enumerate(families.most_common(12), 1):
            print("{:>2}. {:<28} {:>4} IOCs  ({:.0f}%)".format(i, fam, n, 100.0 * n / max(total, 1)))
        print(note)
        print()


def print_banner() -> None:
    title = "IOC Enrichment & Threat Intelligence Agent  -  abuse.ch feeds (ThreatFox / URLhaus / MalwareBazaar)"
    hint = "Paste IOCs or a question. Commands: help, stats [days], summarise, quit."
    if _rich_on():
        _console.print(Panel(Text(title + "\n" + hint), border_style="blue", box=box.ROUNDED))
        if feeds.demo_enabled():
            _print_demo_banner()
    else:
        print(title)
        print(hint)
        if feeds.demo_enabled():
            _print_demo_banner()
        print()


def print_help_examples() -> None:
    lines = "\n".join("  " + q for q in EXAMPLE_QUERIES)
    body = "Example queries (from the assignment brief):\n" + lines + (
        "\nIn this interactive session just type the question part (no quotes needed)."
    )
    if _rich_on():
        _console.print(Panel(Text(body), border_style="blue", box=box.ROUNDED))
    else:
        print(body)
        print()


# ------------------------------------------------------------------- JSON

def to_json_payload(enrichments, llm_text=None, invalid_inputs=None) -> dict:
    payload = {
        "generated_at": _stamp(),
        "mode": "demo" if feeds.demo_enabled() else "live",
        "results": [
            {
                "ioc": {"value": e.ioc.value, "type": e.ioc.type},
                "verdict": asdict(e.verdict),
                "sources": [asdict(r) for r in e.results],
            }
            for e in enrichments
        ],
    }
    if invalid_inputs:
        payload["invalid_inputs"] = list(invalid_inputs)
    if len(enrichments) > 1 or invalid_inputs:
        payload["summary"] = summary_data(enrichments, invalid_inputs=invalid_inputs)
        payload["threat_picture"] = _threat_picture_lines(enrichments, invalid_inputs=invalid_inputs)
    if llm_text:
        payload["llm_summary"] = llm_text
    return payload


def llm_payload(enrichments) -> dict:
    """Compact, structured evidence digest handed to the (optional) LLM layer."""
    return {
        "generated_at": _stamp(),
        "mode": "demo-fixtures" if feeds.demo_enabled() else "live-feeds",
        "iocs": [
            {
                "value": e.ioc.value,
                "type": e.ioc.type,
                "verdict": e.verdict.level,
                "confidence": e.verdict.confidence,
                "confidence_detail": e.verdict.confidence_detail,
                "classification": e.verdict.classification,
                "families": e.verdict.families,
                "first_seen": e.verdict.first_seen,
                "last_seen": e.verdict.last_seen,
                "recently_active": e.verdict.active,
                "priority": "{} - {}".format(e.verdict.priority, e.verdict.priority_detail),
                "evidence": e.verdict.evidence,
                "caveats": e.verdict.caveats,
                "sources": e.verdict.sources_line,
            }
            for e in enrichments
        ],
        "summary": summary_data(enrichments),
    }
