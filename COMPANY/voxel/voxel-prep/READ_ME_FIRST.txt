VOXEL AI — INTERVIEW PREP PACK
================================

You unzipped this correctly. Start with: 00_START_HERE_MASTER_PLAN.md

WHAT'S HERE
-----------
00_START_HERE_MASTER_PLAN.md   The 4-day plan (Fri-Mon). Read this first.
01_ROUND1_CODE_CREATION.md     Coding round: problem bank + narration script.
02_ROUND2_CODE_MODIFICATION.md Code Modification/Debugging round: the workflow.
03_ROUND3_SYSTEM_DESIGN.md     System design: both confirmed questions.
04_ROUND4_BEHAVIORAL.md        Behavioral: STAR stories, "why Voxel", the Card.
05_COMPANY_BRIEF.md            Everything about Voxel to have loaded.
06_LLD_INSURANCE.md            Hedge in case system design is low-level.

practice/                      TWO runnable mock codebases for Round 2:
  voxel_alerts/                  Do this one SATURDAY. 8 tasks.
  voxel_ingest/                  Save this one for MONDAY (cold read). 4 tasks.

HOW TO RUN THE PRACTICE CODEBASES (needs Python 3.10+)
------------------------------------------------------
Open a terminal (PowerShell) in this folder, then:

  cd practice\voxel_alerts
  pip install -r requirements.txt
  python -m pytest -q

You should see: 5 failed, 20 passed.
Those 5 failures are the planted bugs — your job is to fix them.
Each repo has a README.md (the tasks) and SOLUTIONS.md (check yourself AFTER).

Do NOT open SOLUTIONS.md until you've attempted the tasks.
