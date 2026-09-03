# -*- coding: utf-8 -*-
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render, plan, day1, day2, day3, day4

PROBLEMS = day1.PROBLEMS + day2.PROBLEMS + day3.PROBLEMS + day4.PROBLEMS

REQUIRED = ["num", "title", "stars", "day", "pattern", "opt_cx_short",
            "clarify", "understand", "brute_en", "brute_ds", "brute_algo",
            "brute_cx", "brute_code", "brute_limit", "opt_en", "opt_ds",
            "opt_algo", "opt_code", "opt_cx"]

problems = []
for p in PROBLEMS:
    missing = [k for k in REQUIRED
               if k not in p or (k != "stars" and p[k] in (None, "", []))]
    if missing:
        raise SystemExit("Problem %s is missing: %s" % (p.get("num"), missing))
    problems.append(p)

nums = [p["num"] for p in problems]
if len(set(nums)) != len(nums):
    raise SystemExit("duplicate problem numbers: %s" % nums)

out = os.path.join(HERE, "prep.html")
render.build(problems, plan.PLAN_HTML, out)
print("problems:", len(problems))
print("numbers :", nums)
print("wrote   :", out, os.path.getsize(out), "bytes")
