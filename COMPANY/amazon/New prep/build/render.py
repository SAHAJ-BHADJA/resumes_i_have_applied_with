# -*- coding: utf-8 -*-
"""Builds the combined PDF source: the 5-day plan + all 32 problems, each
written in the fixed 12-section interview answer format."""
import html, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SECTIONS = [
    ("Clarification communication",              "clarify"),
    ("Understanding of the question",            "understand"),
    ("Brute-force approach in English",          "brute_en"),
    ("Data structures used",                     "brute_ds"),
    ("Step-by-step algorithm",                   "brute_algo"),
    ("Time & space complexity with explanation", "brute_cx"),
    ("Fully commented brute-force code",         "brute_code"),
    ("Limitation of brute force",                "brute_limit"),
    ("Optimal approach in English",              "opt_en"),
    ("Optimal data structures",                  "opt_ds"),
    ("Step-by-step optimal algorithm",           "opt_algo"),
    ("Fully commented optimal code",             "opt_code"),
]

CODE_KEYS = {"brute_code", "opt_code"}
LIST_KEYS = {"clarify", "brute_algo", "opt_algo"}


def esc(t):
    return html.escape(t, quote=False)


def inline(t):
    """Tiny markup pass: `code` and **bold**."""
    out = esc(t)
    parts = out.split("`")
    out = "".join(p if i % 2 == 0 else "<code>" + p + "</code>"
                  for i, p in enumerate(parts))
    parts = out.split("**")
    out = "".join(p if i % 2 == 0 else "<strong>" + p + "</strong>"
                  for i, p in enumerate(parts))
    return out


def render_code(src):
    return '<pre class="code">' + esc(src.strip("\n")) + "</pre>"


def render_list(items):
    return '<ol class="steps">' + "".join(
        "<li>" + inline(i) + "</li>" for i in items) + "</ol>"


def render_para(text):
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    out = []
    for b in blocks:
        if b.startswith("- "):
            items = [ln[2:].strip() for ln in b.split("\n")
                     if ln.strip().startswith("- ")]
            out.append("<ul>" + "".join("<li>" + inline(i) + "</li>"
                                        for i in items) + "</ul>")
        else:
            out.append("<p>" + inline(b.replace("\n", " ")) + "</p>")
    return "".join(out)


def render_problem(p):
    o = []
    o.append('<section class="problem">')
    o.append('<h2 class="ptitle"><span class="pnum">' + esc(str(p["num"]))
             + "</span> " + esc(p["title"])
             + ' <span class="stars">' + esc(p.get("stars", "")) + "</span></h2>")
    o.append('<div class="meta">' + esc(p["day"])
             + " &nbsp;&middot;&nbsp; Pattern: " + inline(p["pattern"])
             + " &nbsp;&middot;&nbsp; Optimal: <strong>"
             + inline(p["opt_cx_short"]) + "</strong></div>")
    for n, (label, key) in enumerate(SECTIONS, start=1):
        val = p[key]
        o.append('<div class="sec"><h3><span class="sn">' + str(n) + "</span>"
                 + esc(label) + "</h3>")
        if key in CODE_KEYS:
            o.append(render_code(val))
        elif key in LIST_KEYS:
            o.append(render_list(val))
        else:
            o.append(render_para(val))
        o.append("</div>")
    o.append('<div class="sec closing"><h3><span class="sn">+</span>'
             "Optimal complexity, and what to say out loud</h3>")
    o.append(render_para(p["opt_cx"]))
    o.append("</div></section>")
    return "\n".join(o)


CSS = """
@page { size: A4; margin: 15mm 14mm 16mm 14mm; }
* { box-sizing: border-box; }
body { margin:0; font-family:"Charter","Georgia","Times New Roman",serif;
       font-size:9.7pt; line-height:1.46; color:#16181d; }
h1,h2,h3,h4 { font-family:"Helvetica Neue",Arial,sans-serif; }
code, pre { font-family:"Cascadia Mono","Consolas","DejaVu Sans Mono",monospace; }
code { font-size:0.88em; background:#f1f2f5; padding:0.5px 3px; border-radius:3px; }
pre.code { font-size:8.1pt; line-height:1.36; background:#fbfbfd;
  border:0.6pt solid #d8dae2; border-left:2.4pt solid #3f4a5a;
  border-radius:3px; padding:7px 9px; margin:6px 0 0;
  white-space:pre-wrap; word-wrap:break-word; }

.cover { height:252mm; display:flex; flex-direction:column; justify-content:center;
         page-break-after:always; }
.cover .kicker { font-family:Arial,sans-serif; letter-spacing:.22em; font-size:8.6pt;
   text-transform:uppercase; color:#7a8090; }
.cover h1 { font-size:30pt; line-height:1.08; margin:12px 0 6px; letter-spacing:-0.8px; }
.cover h2 { font-size:12.5pt; font-weight:400; color:#4a505e; margin:0 0 24px; }
.cover .rule { height:2.6pt; background:#1d2430; width:74px; margin:0 0 24px; }
.cover .fmt { border:0.8pt solid #d8dae2; border-radius:5px; padding:14px 18px;
   background:#fafbfc; }
.cover .fmt h3 { margin:0 0 8px; font-size:9pt; letter-spacing:.1em;
   text-transform:uppercase; color:#5b6273; }
.cover ol { margin:0; padding-left:20px; column-count:2; column-gap:26px; font-size:9.4pt; }
.cover ol li { margin:1.5px 0; break-inside:avoid; }
.cover .foot { margin-top:24px; font-size:9pt; color:#6b7280; }

h1.part { font-size:19pt; margin:0 0 4px; letter-spacing:-0.4px; }
.partsub { color:#5b6273; font-size:10pt; margin:0 0 16px;
   border-bottom:1.6pt solid #1d2430; padding-bottom:10px; }
.pagebreak { page-break-before:always; }

section.problem { page-break-before:always; }
.ptitle { font-size:15pt; margin:0 0 3px; letter-spacing:-0.3px; }
.pnum { display:inline-block; background:#1d2430; color:#fff; border-radius:4px;
   padding:1px 7px; font-size:12pt; margin-right:6px; }
.stars { color:#c08a1e; font-size:12pt; }
.meta { font-size:8.6pt; color:#5b6273; background:#f5f6f8; border-radius:4px;
   padding:4px 8px; margin:0 0 10px; }

.sec { margin:0 0 9px; page-break-inside:avoid; }
.sec h3 { font-size:9.6pt; margin:0 0 3px; color:#1d2430;
   border-bottom:0.6pt solid #e3e5ea; padding-bottom:2.5px; }
.sn { display:inline-block; width:15px; height:15px; line-height:15px;
   text-align:center; background:#e7eaf0; color:#39404f; border-radius:3px;
   font-size:7.6pt; margin-right:6px; vertical-align:1px; }
.sec p { margin:3px 0; }
.sec ul, .sec ol { margin:3px 0; padding-left:19px; }
.sec li { margin:1.5px 0; }
ol.steps li { margin:2px 0; }
.closing { background:#f7f8fa; border-radius:4px; padding:7px 9px 8px;
   border:0.6pt solid #e3e5ea; }
.closing h3 { border-bottom:0.6pt solid #c9cdd6; }

table { width:100%; border-collapse:collapse; margin:8px 0 14px; font-size:9pt;
  page-break-inside:avoid; }
th { background:#1d2430; color:#fff; text-align:left; padding:5px 7px;
  font-family:Arial,sans-serif; font-size:8.4pt; letter-spacing:.04em; }
td { border-bottom:0.6pt solid #e3e5ea; padding:4.5px 7px; vertical-align:top; }
tr:nth-child(even) td { background:#fafbfc; }
.day { page-break-before:always; }
.day h2 { font-size:15pt; margin:0 0 2px; }
.day .roundtype { font-size:10pt; color:#5b6273; margin:0 0 10px;
   border-bottom:1.2pt solid #d8dae2; padding-bottom:8px; }
.callout { border-left:2.6pt solid #3f4a5a; background:#f7f8fa; padding:7px 11px;
   margin:9px 0; border-radius:0 4px 4px 0; page-break-inside:avoid; }
.callout p:first-child { margin-top:0; }
.callout p:last-child { margin-bottom:0; }
.idx { column-count:2; column-gap:22px; font-size:9pt; }
.idx div { break-inside:avoid; margin:1.5px 0; }
"""


def build(problems, plan_html, out_path):
    body = io.StringIO()
    body.write("<style>" + CSS + "</style>\n")
    body.write(plan_html)
    body.write('<div class="pagebreak"></div>')
    body.write('<h1 class="part">Part II &mdash; The 32 Problems</h1>')
    body.write('<p class="partsub">Every problem below is written in the same '
               "twelve-section order. That order <em>is</em> the answer &mdash; an "
               "Amazon interviewer scores the sequence you follow, not only the "
               "final code you type.</p>")
    body.write('<div class="idx">')
    for p in problems:
        body.write("<div><strong>" + esc(str(p["num"])) + ".</strong> "
                   + esc(p["title"]) + ' <span style="color:#7a8090">&middot; '
                   + esc(p["day"].split(" ·")[0]) + "</span></div>")
    body.write("</div>")
    for p in problems:
        body.write(render_problem(p))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("<!doctype html><html><head><meta charset='utf-8'>"
                "<title>Amazon SDE-I Prep</title></head><body>")
        f.write(body.getvalue())
        f.write("</body></html>")
