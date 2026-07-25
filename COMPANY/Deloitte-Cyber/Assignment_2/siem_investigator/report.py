"""Stage: report. Two renderers over the same Incident IR:

  - render_cli(): a clean terminal report for the SOC analyst at a keyboard.
  - build_html(): a self-contained, interactive incident report — the artifact a
    CISO can open in any browser (no server, no network) and hand to the board.
    Every finding drills down to the untouched raw log events behind it, so the
    traceability is in the artifact itself, not just claimed in prose.
"""

from __future__ import annotations

import html
import json
import re

from .model import CONFIRMED, SUSPECTED, UNCERTAIN, Incident
from . import synthesize

# --------------------------------------------------------------------------- #
# terminal report
# --------------------------------------------------------------------------- #
def render_cli(incident: Incident) -> str:
    s = incident.stats
    bar = "=" * 78
    out = [bar,
           " SIEM INCIDENT INVESTIGATION — reconstructed attack report",
           " Northwind Health (synthetic)  |  window {}  ->  {}".format(
               s["first_malicious_activity"], s["last_malicious_activity"]),
           bar, "",
           " {} events analysed across {} sources  |  {} findings  |  {} techniques / {} tactics".format(
               s["events_ingested"], len(s.get("events_by_source", {})), s["findings"],
               s["techniques_count"], s["tactics_covered"]),
           " {} CONFIRMED  {} SUSPECTED  {} UNCERTAIN  |  attack duration {}h".format(
               s["confirmed_findings"], s["suspected_findings"], s["uncertain_findings"],
               s["attack_duration_hours"]),
           ""]
    out.append(synthesize.q_exec_summary(incident))
    out += ["", bar, ""]
    out.append(synthesize.q_timeline(incident))
    out += ["", bar, ""]
    out.append(synthesize.q_blast_radius(incident))
    out += ["", bar, ""]
    out.append(synthesize.q_gaps(incident))
    out += ["", bar, ""]
    out.append(synthesize.q_ir_actions(incident))
    if incident.benign_review:
        out += ["", bar, "", "ACTIVITY REVIEWED AND RULED BENIGN (precision — not every anomaly is an attack):", ""]
        for n in incident.benign_review:
            out.append("  • {} — {}".format(n["activity"], n["verdict"]))
            out.append("      {}".format(n["why"]))
    out += ["", bar,
            " Deterministic reconstruction. Every claim above cites the log event IDs behind it.",
            " Machine-readable IR: out/investigation.json  |  Interactive report: out/incident_report.html",
            bar]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# HTML report
# --------------------------------------------------------------------------- #
def esc(x) -> str:
    return html.escape(str(x if x is not None else ""))


_BADGE = {CONFIRMED: "conf", SUSPECTED: "susp", UNCERTAIN: "unc"}
_SEV = {"critical": "sev-c", "high": "sev-h", "medium": "sev-m", "low": "sev-l"}


def _linkify(text: str, techniques: dict) -> str:
    """Escape text, then linkify ATT&CK technique IDs and make event/finding IDs
    clickable (they open the evidence drawer via JS)."""
    out = esc(text)
    # technique IDs -> MITRE
    def tech(m):
        tid = m.group(0)
        meta = techniques.get(tid)
        url = meta.get("url") if meta else "https://attack.mitre.org/techniques/{}/".format(tid.replace(".", "/"))
        return '<a class="tid" href="{}" target="_blank" rel="noopener">{}</a>'.format(esc(url), tid)
    out = re.sub(r"\bT\d{4}(?:\.\d{3})?\b", tech, out)
    # event IDs -> evidence drawer
    out = re.sub(r"\b(?:EP|AU|NW|CS)-\d{3,4}\b",
                 lambda m: '<a class="evref" onclick="showEv(\'{0}\')">{0}</a>'.format(m.group(0)), out)
    # finding IDs -> scroll to finding
    out = re.sub(r"\bF-\d{3}\b",
                 lambda m: '<a class="fref" href="#{0}">{0}</a>'.format(m.group(0)), out)
    return out


def _stat(label, value):
    return '<div class="stat"><div class="v">{}</div><div class="l">{}</div></div>'.format(esc(value), esc(label))


def _evchip(incident: Incident, eid: str) -> str:
    """Evidence citation with a source·timestamp tooltip (traceability without a click)."""
    e = incident.store.get(eid)
    tip = "{} · {}".format(e.source, e.ts_str) if e else "raw event not embedded"
    return '<a class="evref" title="{tip}" onclick="showEv(\'{id}\')">{id}</a>'.format(tip=esc(tip), id=esc(eid))


def _timeline_html(incident: Incident) -> str:
    cards = []
    for f in incident.timeline:
        chips = " ".join(
            '<span class="tpair"><a class="tid" href="{url}" target="_blank" rel="noopener" '
            'title="{tactic}">{id}</a><span class="tname">{name}</span></span>'.format(
                url=esc(incident.techniques.get(t, {}).get("url", "https://attack.mitre.org/techniques/" + t.replace(".", "/") + "/")),
                id=esc(t), name=esc(incident.techniques.get(t, {}).get("name", "")),
                tactic=esc(incident.techniques.get(t, {}).get("tactic", "")))
            for t in f.technique_ids)
        ev = " ".join(_evchip(incident, e) for e in f.evidence)
        cav = '<div class="caveat"><b>Caveat:</b> {}</div>'.format(esc(f.caveats)) if f.caveats else ""
        cards.append(
            '<div class="tl-item {badge}" id="{fid}">'
            '<div class="tl-dot"></div>'
            '<div class="tl-card">'
            '<div class="tl-top"><span class="when">{when}</span>'
            '<span class="phase">{phase}</span>'
            '<span class="badge {badge}">{conf}</span>'
            '<span class="badge {sev}">{sevname}</span>'
            '<span class="fid">{fid}</span></div>'
            '<div class="tl-title">{title}</div>'
            '<div class="tl-why">{why}</div>'
            '<div class="chips">{chips}</div>'
            '<div class="evrow"><span class="evlabel">Evidence:</span> {ev}</div>'
            '{cav}</div></div>'.format(
                badge=_BADGE.get(f.confidence, "unc"), fid=esc(f.id),
                when=esc(f.ts.strftime("%b %d, %H:%M") if f.ts else "—"),
                phase=esc(f.phase), conf=esc(f.confidence),
                sev=_SEV.get(f.severity, "sev-m"), sevname=esc(f.severity.upper()),
                title=esc(f.title), why=_linkify(f.rationale, incident.techniques),
                chips=chips, ev=ev, cav=cav))
    return '<div class="timeline">' + "".join(cards) + "</div>"


def _attack_path_html(incident: Incident) -> str:
    if not incident.attack_path:
        return ""
    rows = []
    for e in incident.attack_path:
        rows.append(
            '<div class="hop {b}"><span class="node">{f}</span>'
            '<span class="arrow">&#8594;<small>{via}</small></span>'
            '<span class="node">{t}</span>'
            '<span class="hopmeta">{conf} &middot; {when}</span></div>'.format(
                b=_BADGE.get(e["confidence"], "unc"), f=esc(e["from"]), t=esc(e["to"]),
                via=esc(e["via"]), conf=esc(e["confidence"]),
                when=esc((e["when"] or "")[5:16].replace("T", " "))))
    return '<div class="apath">' + "".join(rows) + "</div>"


def _attack_matrix_html(incident: Incident) -> str:
    blocks = []
    for block in incident.attack_by_tactic:
        techs = "".join(
            '<tr><td class="tcell"><a class="tid" href="{url}" target="_blank" rel="noopener">{id}</a></td>'
            '<td>{name}</td><td class="fcell">{finds}</td></tr>'.format(
                url=esc(incident.techniques.get(t["id"], {}).get("url", "")),
                id=esc(t["id"]), name=esc(incident.techniques.get(t["id"], {}).get("name", t["name"])),
                finds=" ".join('<a class="fref" href="#{0}">{0}</a>'.format(esc(x)) for x in t["findings"]))
            for t in block["techniques"])
        blocks.append(
            '<div class="tactic-block"><h4>{tactic}</h4>'
            '<table class="ttable"><tbody>{rows}</tbody></table></div>'.format(
                tactic=esc(block["tactic"]), rows=techs))
    return '<div class="matrix">' + "".join(blocks) + "</div>"


def _blast_html(incident: Incident) -> str:
    def rows(d, first_label):
        r = []
        for name, rec in d.items():
            r.append(
                '<tr class="{b}"><td><span class="badge {b}">{s}</span></td><td class="mono">{n}</td>'
                '<td>{role}</td><td class="fcell">{finds}</td></tr>'.format(
                    b=_BADGE.get(rec["status"], "unc"), s=esc(rec["status"]), n=esc(name),
                    role=esc(rec.get("role") or rec.get("usage") or rec.get("type", "")),
                    finds=" ".join('<a class="fref" href="#{0}">{0}</a>'.format(esc(x)) for x in rec.get("findings", []))))
        return ('<table class="btable"><thead><tr><th>Status</th><th>{}</th><th>Role / usage</th>'
                '<th>Findings</th></tr></thead><tbody>{}</tbody></table>').format(first_label, "".join(r))
    return ('<h4>Hosts</h4>' + rows(incident.hosts, "Host")
            + '<h4>Accounts</h4>' + rows(incident.accounts, "Account")
            + ('<h4>Cloud resources</h4>' + rows(incident.cloud, "Resource") if incident.cloud else ""))


def _gaps_html(incident: Incident) -> str:
    items = "".join(
        '<li><div class="gaptxt">{g}</div><div class="gapimp">&rarr; {i} <span class="gapsrc">({s})</span></div></li>'.format(
            g=esc(x["gap"]), i=esc(x["impact"]), s=esc(x["source"])) for x in incident.gaps)
    return '<ul class="gaps">' + items + "</ul>"


def _benign_html(incident: Incident) -> str:
    if not incident.benign_review:
        return ""
    items = "".join(
        '<li><b>{v}</b> — {a}<div class="benwhy">{w}</div>'
        '<div class="evrow">{ev}</div></li>'.format(
            v=esc(n["verdict"]), a=esc(n["activity"]), w=esc(n["why"]),
            ev=" ".join('<a class="evref" onclick="showEv(\'{0}\')">{0}</a>'.format(esc(e)) for e in n.get("evidence", [])))
        for n in incident.benign_review)
    return '<ul class="benign">' + items + "</ul>"


def _qa_html(incident: Incident) -> str:
    items = []
    for i, (q, a) in enumerate(synthesize.all_answers(incident)):
        items.append(
            '<div class="qa" data-q="{ql}"><button class="qbtn" onclick="toggleQA(this)">{q}</button>'
            '<pre class="qans">{a}</pre></div>'.format(
                ql=esc(q.lower()), q=esc(q), a=_linkify(a, incident.techniques)))
    return "".join(items)


def _evidence_json(incident: Incident) -> str:
    """Embed the raw events the report can drill into so traceability works fully
    offline. Only cited events are ever clickable, so we embed exactly those."""
    cited = set()
    for f in incident.findings:
        cited.update(f.evidence)
    for n in incident.benign_review:
        cited.update(n.get("evidence", []))
    data = {}
    for eid in sorted(cited):
        e = incident.store.get(eid)
        if e:
            data[eid] = e.raw
    return json.dumps(data, ensure_ascii=False)


def build_html(incident: Incident, llm_brief: str | None = None) -> str:
    s = incident.stats
    gen = s.get("last_malicious_activity", "")
    stats_row = "".join([
        _stat("Events analysed", s["events_ingested"]),
        _stat("Findings", s["findings"]),
        _stat("ATT&CK techniques", s["techniques_count"]),
        _stat("Tactics", s["tactics_covered"]),
        _stat("Hosts in blast radius", len(incident.hosts)),
        _stat("Accounts", len(incident.accounts)),
        _stat("Duration (h)", s["attack_duration_hours"]),
        _stat("Confirmed / Uncertain", "{}/{}".format(s["confirmed_findings"], s["uncertain_findings"])),
    ])
    exec_summary = esc(synthesize.q_exec_summary(incident).split("\n\n", 1)[-1])
    llm_block = ""
    if llm_brief:
        llm_block = ('<section class="card llm"><h3>AI-narrated brief '
                     '<span class="tag">Claude — grounded &amp; citation-verified</span></h3>'
                     '<pre class="qans">{}</pre></section>').format(_linkify(llm_brief, incident.techniques))

    ir_actions = _linkify(synthesize.q_ir_actions(incident).split("\n\n", 1)[-1].split("\n\nEvery")[0], incident.techniques)

    return _TEMPLATE.format(
        stats=stats_row, exec_summary=exec_summary, llm_block=llm_block,
        attack_path=_attack_path_html(incident), timeline=_timeline_html(incident),
        matrix=_attack_matrix_html(incident), blast=_blast_html(incident),
        gaps=_gaps_html(incident), benign=_benign_html(incident), qa=_qa_html(incident),
        ir=ir_actions, evidence_json=_evidence_json(incident),
        window_start=esc(s["first_malicious_activity"]), window_end=esc(s["last_malicious_activity"]),
        n_events=s["events_ingested"],
    )


def write_html(incident: Incident, path: str, llm_brief: str | None = None) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build_html(incident, llm_brief))


# --------------------------------------------------------------------------- #
# self-contained HTML/CSS/JS template
# --------------------------------------------------------------------------- #
_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Incident Investigation Report — Northwind Health (synthetic)</title>
<style>
:root{{
  --bg:#f4f6f8; --card:#ffffff; --ink:#1a2230; --muted:#5b6673; --line:#e2e7ee;
  --accent:#0b7d4f; --accent2:#0a6ff0; --chip:#eef1f5;
  --conf:#0b7d4f; --susp:#b7791f; --unc:#b23b3b;
  --sevc:#b21f1f; --sevh:#d1660b; --sevm:#b7791f; --sevl:#5b6673;
}}
@media (prefers-color-scheme: dark){{
  :root{{--bg:#0f141b; --card:#161d27; --ink:#e7edf5; --muted:#95a1b2; --line:#26303d;
    --accent:#2fbe83; --accent2:#4c9dff; --chip:#1e2732;
    --conf:#2fbe83; --susp:#e0a13a; --unc:#e5716f;
    --sevc:#ef5350; --sevh:#f19334; --sevm:#e0a13a; --sevl:#95a1b2;}}
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:28px 20px 80px}}
header.top{{border-left:5px solid var(--accent);padding:6px 0 6px 16px;margin-bottom:6px}}
header.top h1{{margin:0;font-size:24px;letter-spacing:.2px}}
header.top .sub{{color:var(--muted);font-size:13.5px;margin-top:3px}}
.provenance{{font-size:12px;color:var(--muted);background:var(--chip);border:1px dashed var(--line);
  padding:8px 12px;border-radius:8px;margin:14px 0 20px}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0 26px}}
@media(max-width:720px){{.stats{{grid-template-columns:repeat(2,1fr)}}}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
.stat .v{{font-size:22px;font-weight:700}}
.stat .l{{font-size:12px;color:var(--muted);margin-top:2px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:16px 0}}
.card h3{{margin:0 0 12px;font-size:16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.card h4{{margin:16px 0 6px;font-size:13.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}}
.card h4:first-child{{margin-top:0}}
.tag{{font-size:11px;font-weight:600;color:#fff;background:var(--accent2);padding:2px 8px;border-radius:20px}}
.execsum{{font-size:15.5px;line-height:1.65}}
.badge{{font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:20px;color:#fff;letter-spacing:.3px}}
.badge.conf{{background:var(--conf)}} .badge.susp{{background:var(--susp)}} .badge.unc{{background:var(--unc)}}
.badge.sev-c{{background:var(--sevc)}} .badge.sev-h{{background:var(--sevh)}}
.badge.sev-m{{background:var(--sevm)}} .badge.sev-l{{background:var(--sevl)}}
/* attack path */
.apath{{display:flex;flex-direction:column;gap:8px}}
.hop{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:var(--chip);
  border-left:4px solid var(--conf);border-radius:8px;padding:8px 12px}}
.hop.unc{{border-left-color:var(--unc)}} .hop.susp{{border-left-color:var(--susp)}}
.node{{font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:700;font-size:13.5px}}
.arrow{{color:var(--muted);display:flex;flex-direction:column;align-items:center;font-size:15px;line-height:1}}
.arrow small{{font-size:10px}}
.hopmeta{{margin-left:auto;font-size:12px;color:var(--muted)}}
/* timeline */
.timeline{{position:relative;margin-left:8px}}
.tl-item{{position:relative;padding-left:26px;padding-bottom:14px;border-left:2px solid var(--line)}}
.tl-item:last-child{{border-left-color:transparent}}
.tl-dot{{position:absolute;left:-7px;top:6px;width:12px;height:12px;border-radius:50%;
  background:var(--conf);border:2px solid var(--card)}}
.tl-item.unc .tl-dot{{background:var(--unc)}} .tl-item.susp .tl-dot{{background:var(--susp)}}
.tl-card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
.tl-top{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:12px;color:var(--muted)}}
.tl-top .when{{font-weight:700;color:var(--ink)}}
.tl-top .phase{{background:var(--chip);padding:2px 8px;border-radius:6px;font-weight:600}}
.tl-top .fid{{margin-left:auto;font-family:ui-monospace,monospace;font-size:11px;color:var(--muted)}}
.tl-title{{font-weight:700;font-size:15px;margin:7px 0 4px}}
.tl-why{{font-size:14px;color:var(--ink)}}
.chips{{margin-top:8px;display:flex;gap:4px 10px;flex-wrap:wrap}}
.tpair{{display:inline-flex;align-items:center;gap:5px}}
.tname{{font-size:11.5px;color:var(--muted)}}
.tid{{font-family:ui-monospace,monospace;font-size:11.5px;background:var(--chip);color:var(--accent2);
  padding:2px 7px;border-radius:6px;text-decoration:none;border:1px solid var(--line)}}
.tid:hover{{text-decoration:underline}}
.evrow{{margin-top:8px;font-size:12px;color:var(--muted)}}
.evlabel{{font-weight:600}}
.evref{{font-family:ui-monospace,monospace;font-size:11.5px;color:var(--accent);cursor:pointer;
  border-bottom:1px dotted var(--accent);margin-right:5px}}
.fref{{font-family:ui-monospace,monospace;font-size:11.5px;color:var(--accent2);text-decoration:none;border-bottom:1px dotted}}
.caveat{{margin-top:8px;font-size:12.5px;background:var(--chip);border-left:3px solid var(--susp);
  padding:6px 10px;border-radius:0 6px 6px 0;color:var(--muted)}}
/* matrix */
.matrix{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
@media(max-width:720px){{.matrix{{grid-template-columns:1fr}}}}
.tactic-block h4{{margin:0 0 4px}}
.ttable,.btable{{width:100%;border-collapse:collapse;font-size:13px}}
.ttable td,.btable td,.btable th{{padding:5px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
.btable th{{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.3px}}
.tcell{{white-space:nowrap}} .fcell{{white-space:nowrap}} .mono{{font-family:ui-monospace,monospace;font-weight:700}}
/* gaps / benign */
.gaps,.benign{{list-style:none;padding:0;margin:0}}
.gaps li{{padding:9px 0;border-bottom:1px solid var(--line)}}
.gaptxt{{font-weight:600}} .gapimp{{font-size:13px;color:var(--muted);margin-top:2px}}
.gapsrc{{font-style:italic}}
.benign li{{padding:9px 0;border-bottom:1px solid var(--line)}}
.benwhy{{font-size:13px;color:var(--muted);margin-top:2px}}
/* Q&A */
.qa{{border:1px solid var(--line);border-radius:8px;margin-bottom:8px;overflow:hidden}}
.qbtn{{width:100%;text-align:left;background:var(--card);color:var(--ink);border:0;padding:11px 14px;
  font-size:14px;font-weight:600;cursor:pointer}}
.qbtn:hover{{background:var(--chip)}}
.qans{{display:none;margin:0;padding:12px 14px;background:var(--chip);white-space:pre-wrap;
  font:12.5px/1.5 ui-monospace,Menlo,Consolas,monospace;border-top:1px solid var(--line);overflow-x:auto}}
.qa.open .qans{{display:block}}
#ask{{width:100%;padding:11px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card);
  color:var(--ink);font-size:14px;margin-bottom:12px}}
.ir{{white-space:pre-wrap;font-size:14px;line-height:1.6}}
/* evidence drawer */
.drawer{{position:fixed;top:0;right:-460px;width:440px;max-width:92vw;height:100%;background:var(--card);
  border-left:1px solid var(--line);box-shadow:-8px 0 30px rgba(0,0,0,.18);transition:right .22s;z-index:50;
  padding:20px;overflow-y:auto}}
.drawer.open{{right:0}}
.drawer h3{{margin:0 0 4px}}
.drawer .close{{position:absolute;top:14px;right:16px;cursor:pointer;font-size:20px;color:var(--muted);border:0;background:0}}
.drawer pre{{background:var(--chip);padding:12px;border-radius:8px;font-size:12px;white-space:pre-wrap;overflow-x:auto}}
.evsub{{font-size:12px;color:var(--muted);margin-bottom:12px}}
.backdrop{{position:fixed;inset:0;background:rgba(0,0,0,.35);opacity:0;pointer-events:none;transition:opacity .2s;z-index:40}}
.backdrop.open{{opacity:1;pointer-events:auto}}
footer{{margin-top:30px;font-size:12px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}}
a{{color:var(--accent2)}}
h3 .anchor{{font-size:12px;color:var(--muted);font-weight:400}}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <h1>Incident Investigation Report</h1>
    <div class="sub">Reconstructed attack timeline &middot; Northwind Health (synthetic) &middot; window {window_start} &rarr; {window_end} UTC</div>
  </header>
  <div class="provenance">
    <b>Prototype output.</b> Generated by a deterministic correlation engine over {n_events} synthetic SIEM
    events. Every finding cites the raw log event IDs behind it — click any <span class="evref">EV-ID</span>
    to inspect the untouched source record. Technique IDs link to attack.mitre.org.
  </div>

  <div class="stats">{stats}</div>

  <section class="card">
    <h3>Executive summary <span class="anchor">— board briefing</span></h3>
    <div class="execsum">{exec_summary}</div>
  </section>

  {llm_block}

  <section class="card">
    <h3>Attack path</h3>
    {attack_path}
  </section>

  <section class="card">
    <h3>Attack timeline <span class="anchor">— initial access &rarr; last observed activity</span></h3>
    {timeline}
  </section>

  <section class="card">
    <h3>MITRE ATT&amp;CK coverage <span class="anchor">— techniques mapped to findings</span></h3>
    {matrix}
  </section>

  <section class="card">
    <h3>Blast radius</h3>
    {blast}
  </section>

  <section class="card">
    <h3>Immediate response — next 2 hours</h3>
    <div class="ir">{ir}</div>
  </section>

  <section class="card">
    <h3>Coverage gaps &amp; limits on confidence</h3>
    {gaps}
  </section>

  <section class="card">
    <h3>Activity reviewed and ruled benign <span class="anchor">— precision, not an alert cannon</span></h3>
    {benign}
  </section>

  <section class="card">
    <h3>Ask the investigation <span class="anchor">— the assignment's example queries, pre-answered &amp; cited</span></h3>
    <input id="ask" placeholder="Type a question (e.g. 'is there exfiltration?', 'blast radius', 'gaps') and press Enter…" onkeydown="if(event.key==='Enter')askQ()">
    {qa}
  </section>

  <footer>
    <b>How to trust this report.</b> The engine that finds and judges the attack is deterministic code — no
    language model decides what happened, so every conclusion is a reproducible function of the cited events.
    Confidence is explicit (CONFIRMED = multi-source corroboration; UNCERTAIN = access seen but actions
    unobservable). The report states what it <i>cannot</i> confirm as plainly as what it can. Data is
    synthetic; no real patient information is present.
  </footer>
</div>

<div class="backdrop" id="backdrop" onclick="closeEv()"></div>
<aside class="drawer" id="drawer">
  <button class="close" onclick="closeEv()">&times;</button>
  <h3 id="ev-id">Evidence</h3>
  <div class="evsub" id="ev-sub"></div>
  <pre id="ev-body"></pre>
</aside>

<script>
const EVIDENCE = {evidence_json};
function showEv(id){{
  const ev = EVIDENCE[id];
  document.getElementById('ev-id').textContent = id;
  if(!ev){{document.getElementById('ev-body').textContent='(raw event not embedded)';}}
  else{{
    document.getElementById('ev-sub').textContent =
      (ev.source||'')+' · '+(ev.host||ev.principal||ev.src_host||'')+' · '+(ev.timestamp||'');
    document.getElementById('ev-body').textContent = JSON.stringify(ev, null, 2);
  }}
  document.getElementById('drawer').classList.add('open');
  document.getElementById('backdrop').classList.add('open');
}}
function closeEv(){{
  document.getElementById('drawer').classList.remove('open');
  document.getElementById('backdrop').classList.remove('open');
}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape')closeEv();}});
function toggleQA(btn){{btn.parentElement.classList.toggle('open');}}
function askQ(){{
  const q=document.getElementById('ask').value.toLowerCase().trim();
  if(!q)return;
  const cards=[...document.querySelectorAll('.qa')];
  cards.forEach(c=>c.classList.remove('open'));
  const score=c=>{{const t=c.dataset.q;let s=0;q.split(/\s+/).forEach(w=>{{if(w.length>2&&t.includes(w))s++;}});return s;}};
  let best=cards[0],bs=-1;
  cards.forEach(c=>{{const s=score(c);if(s>bs){{bs=s;best=c;}}}});
  best.classList.add('open');
  best.scrollIntoView({{behavior:'smooth',block:'center'}});
}}
</script>
</body>
</html>"""
