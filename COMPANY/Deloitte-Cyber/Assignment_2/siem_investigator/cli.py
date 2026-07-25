"""Command-line entry point — the agentic loop an analyst drives.

    ingest -> detect -> correlate -> enrich (ATT&CK) -> assess -> synthesise -> answer

Default run executes the whole pipeline, prints the terminal report, and writes
the machine-readable IR + the interactive HTML report. Sub-commands expose the
same Incident for targeted questions (`ask`), the full example-query set
(`questions`), or JSON export. The optional `--llm` flag adds a Claude-narrated,
citation-verified brief; without a key it degrades to a one-line notice.
"""

from __future__ import annotations

import argparse
import os
import sys

from . import pipeline, report, synthesize
from .llm import narrate

_DEF_LOGS = os.path.join(os.path.dirname(__file__), "..", "data", "siem_logs.json")


def _reconfigure_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m siem_investigator",
        description="Agentic SIEM incident-investigation prototype — reconstruct a multi-stage attack "
                    "from raw logs with full ATT&CK mapping and per-claim traceability.")
    p.add_argument("command", nargs="?", default="run",
                   help="run (default) | ask [QUESTION] | questions | timeline | report | json")
    p.add_argument("query", nargs="*", help="question text for `ask`")
    p.add_argument("--logs", default=_DEF_LOGS, help="path to SIEM logs JSON (default: data/siem_logs.json)")
    p.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "out"),
                   help="output directory for artifacts (default: out/)")
    p.add_argument("--llm", action="store_true", help="append a Claude-narrated, citation-verified brief")
    p.add_argument("--refresh-attack", action="store_true", help="reconcile ATT&CK catalogue vs the live STIX feed")
    p.add_argument("--no-html", action="store_true", help="skip HTML report generation on a default run")
    p.add_argument("--json", action="store_true", help="print the machine-readable investigation IR and exit")
    p.add_argument("-v", "--verbose", action="store_true", help="show pipeline stage logs")
    return p


KNOWN = {"run", "ask", "questions", "timeline", "report", "json"}


def main(argv=None) -> int:
    _reconfigure_stdout()
    args = build_parser().parse_args(argv)

    # UX nicety (mirrors round 1): if the first token isn't a known command,
    # treat the whole invocation as an `ask` query — paste a question directly.
    command, query = args.command, list(args.query)
    if command not in KNOWN:
        query = [command] + query
        command = "ask"

    incident = pipeline.run(args.logs, refresh_attack=args.refresh_attack, verbose=args.verbose)

    if args.json or command == "json":
        print(incident.dumps())
        return 0

    if command == "timeline":
        print(synthesize.q_timeline(incident))
        return 0

    if command == "questions":
        for i, (q, a) in enumerate(synthesize.all_answers(incident), 1):
            print("\n[{}] {}\n{}\n{}".format(i, q, "-" * 78, a))
        return 0

    if command == "ask":
        if query:
            print(synthesize.answer(incident, " ".join(query)))
            return 0
        return _interactive(incident)

    if command == "report":
        _write_artifacts(incident, args, html_only=True)
        return 0

    # default: full run -> terminal report + artifacts
    llm_brief = _maybe_llm(incident, args.llm)
    print(report.render_cli(incident))
    if llm_brief:
        print("\n" + "=" * 78 + "\n AI-NARRATED BRIEF (Claude, grounded + citation-verified)\n" + "=" * 78)
        print(llm_brief)
    _write_artifacts(incident, args, llm_brief=llm_brief)
    return 0


def _maybe_llm(incident, enabled):
    if not enabled:
        return None
    text, reason = narrate(incident)
    if text is None:
        print("[--llm] {}".format(reason), file=sys.stderr)
    return text


def _write_artifacts(incident, args, llm_brief=None, html_only=False):
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    if not html_only:
        ir_path = os.path.join(out, "investigation.json")
        with open(ir_path, "w", encoding="utf-8") as fh:
            fh.write(incident.dumps())
        print("\n[artifact] machine-readable IR  -> {}".format(os.path.relpath(ir_path)))
    if not args.no_html:
        if llm_brief is None and args.llm:
            llm_brief = _maybe_llm(incident, True)
        html_path = os.path.join(out, "incident_report.html")
        report.write_html(incident, html_path, llm_brief)
        print("[artifact] interactive report  -> {}".format(os.path.relpath(html_path)))


def _interactive(incident) -> int:
    print("Interactive investigation session. Ask about the incident; 'help' for examples, 'quit' to exit.\n"
          "Loaded: {} findings, {} techniques, {} hosts.".format(
              incident.stats["findings"], incident.stats["techniques_count"], len(incident.hosts)))
    while True:
        try:
            q = input("\ninvestigate> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not q:
            continue
        if q.lower() in ("quit", "exit", "q"):
            return 0
        if q.lower() == "help":
            print("Examples:")
            for ex, _ in synthesize.CANONICAL:
                print("  - " + ex)
            continue
        print(synthesize.answer(incident, q))


if __name__ == "__main__":
    raise SystemExit(main())
