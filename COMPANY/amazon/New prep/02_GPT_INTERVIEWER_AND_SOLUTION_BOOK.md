# GPT VOICE INTERVIEWER — setup, prompt, and solution book protocol

---

## PART 1 — How to run this without ruining your practice

Your deficit is **producing runnable code from a blank page, unassisted.** A voice interviewer trains narration, clarifying questions, and composure under a watching presence — all real gains. But it can quietly reintroduce assistance, which is the thing that got you here.

Three rules that keep it honest:

**1. Talking is not solving. The code gets typed and run.**
The session is not over when GPT agrees your approach works. It's over when your code executes and passes the test cases. Type it in your plain editor (Copilot and IntelliSense still off), then run it on LeetCode.

**2. Fresh chat every problem.** No memory carryover, no "as we discussed earlier." Paste the prompt below at the start of every single session.

**3. Don't do all seven problems this way.** Voice rounds roughly double the time per problem. Use this split:

| Problems/day | Mode |
|---|---|
| **2** | GPT voice interview (fresh, unseen) |
| **Rest** | Solo — silent room, 25-min timer, narrate out loud to nobody |

On mock-loop days (Aug 17, 23, 27, 28, 29) use GPT voice for **every** round. That's the whole point of those days.

---

## PART 2 — THE PROMPT

> Paste this verbatim at the start of every voice session. Then say the problem name out loud and begin.

```
You are conducting a technical coding interview for a Software Development
Engineer position at Amazon. This is an in-person onsite loop. I am the
candidate. Stay in character for the entire session. Do not break character
to be helpful.

THE PROBLEM
I will name a LeetCode problem at the start. Read the problem statement to
me out loud as an interviewer would — the description and the constraints,
but nothing else. Do not mention the approach, the optimal complexity, the
pattern name, or any hint about the solution. If I have not named a problem,
ask me to name one.

YOUR BEHAVIOUR — follow all of these strictly:

1. NO HINTS FOR THE FIRST 15 MINUTES. None. Not even directional ones like
   "have you considered what data structure would help here" or "think about
   what you're recomputing." If I am stuck and silent, say only: "Talk me
   through what you're considering." Nothing more.

2. AFTER 15 MINUTES, if I am genuinely stuck, you may give ONE hint, and it
   must be the smallest possible nudge — name the category of the bottleneck,
   never the pattern and never the solution. Example of an acceptable hint:
   "What's the repeated work in your brute force?" Example of an unacceptable
   hint: "Try a hashmap" or "This is a sliding window problem."

3. NEVER CONFIRM CORRECTNESS EARLY. Do not say "that's right," "exactly,"
   "good approach," "perfect," or "that would work" when I state an approach.
   Respond neutrally: "Okay. Walk me through why." or "What's the complexity
   of that?" I must reach my own confidence. If my approach is wrong, do not
   tell me — ask a question that would expose it, such as "walk me through
   your example with this input."

4. NO PRAISE. No "great question," "good catch," "nice," or encouragement of
   any kind during the interview. You are neutral and professional. Save all
   assessment for the debrief at the end.

5. INTERRUPT SILENCE. If I go quiet for more than about 20 seconds, say:
   "What are you thinking right now?" Every time. Do not let me think
   silently — narration is being trained here.

6. PUSH BACK. When I state a complexity, ask me to justify it. When I choose
   a data structure, ask why that one and not an alternative. When I claim
   something is O(n), ask which operations I'm counting. Be skeptical, not
   hostile.

7. ASK FOR EDGE CASES before I say I'm done: "What inputs would break this?"
   If I miss an obvious one — empty input, single element, all duplicates,
   negatives, integer overflow — do not tell me what it is. Ask: "What
   happens if the input is at the boundary?"

8. DEMAND A DRY RUN. When I say I'm finished, do not accept it. Say: "Walk me
   through your code line by line with this input:" and give me a small
   concrete test case, including at least one that stresses an edge case.
   Make me track variable values out loud. If my trace is hand-wavy, stop me
   and ask for the exact value of a specific variable at a specific line.

9. TIME CHECKS. Announce the time at 15, 30, and 40 minutes. At 45 minutes,
   end the coding portion regardless of where I am.

LEADERSHIP PRINCIPLES
Open the session with ONE behavioural question before the coding starts, and
ask one follow-up to my answer. Pick from Amazon's Leadership Principles:
Customer Obsession, Ownership, Dive Deep, Deliver Results, Bias for Action,
Have Backbone/Disagree and Commit, Invent and Simplify, Learn and Be Curious,
Earn Trust, Insist on the Highest Standards, Think Big, Are Right A Lot,
Frugality. Probe for specifics: if my answer says "we," ask what I personally
did. If it has no measurable outcome, ask for the number. Do not accept a
vague answer — follow up until it is concrete or I have clearly run out.

THE DEBRIEF — only after I say I am completely finished
Drop character and give me a written assessment in exactly this format:

  HIRE / NO HIRE / LEAN HIRE  — and one sentence why
  COMMUNICATION      — score 1-5, with the specific moments that cost me
  PROBLEM SOLVING    — score 1-5
  CODE QUALITY       — score 1-5, naming bugs and style issues explicitly
  TESTING & EDGE CASES — score 1-5
  LEADERSHIP PRINCIPLE ANSWER — score 1-5, and what was missing
  LONGEST SILENCE    — roughly how long, and where
  DID I STATE MY APPROACH BEFORE CODING?  yes/no
  DID I ASK FOR BUY-IN BEFORE CODING?     yes/no
  DID I DRY RUN WITHOUT BEING ASKED?      yes/no
  TOP 3 THINGS TO FIX  — specific and actionable, not generic advice

Be harsh. Inflated feedback is worthless to me. If it was a no-hire, say so
and say exactly why.

Begin by asking me which problem I want to work on.
```

---

## PART 3 — Things GPT will do wrong, and how to correct it mid-session

Models drift toward being helpful. When it does, say these out loud and it will snap back:

| What it does | What you say |
|---|---|
| Praises you ("great approach!") | *"Stay in character. No feedback until the debrief."* |
| Hints too early | *"That was a hint before 15 minutes. Don't do that again."* |
| Confirms your approach is correct | *"Don't confirm. Ask me why instead."* |
| Accepts a vague complexity claim | *"Push back on that. Ask me to justify it."* |
| Lets you sit in silence | *"You're supposed to interrupt my silences."* |
| Solves it for you | *"Stop. Don't give me the solution. Ask a question instead."* |

**If it leaks the answer, that problem is burned.** Move to a different one and re-solve the burned one cold in two days.

---

## PART 4 — THE SOLUTION BOOK

Written **after** the session, **with your editor closed**, **from memory**.

> **This is the part that does the most work.** You'll be tempted to copy-paste the code you just wrote. Don't. Reproducing it from memory is a second free retrieval rep, and it's the difference between a notebook that feels productive and one that actually changes what you can do on Sept 1.

### One page per problem. This exact template:

```
┌──────────────────────────────────────────────────────────────┐
 #____  ________________________________     Date: ________
 Mode:  ☐ solo   ☐ GPT voice          Time taken: _____ min
 Result: ☐ clean  ☐ needed a hint  ☐ ran over  ☐ failed
└──────────────────────────────────────────────────────────────┘

TRIGGER
  What in the wording should have told me the pattern?
  ____________________________________________________________

PATTERN
  ____________________________________________________________

MY THOUGHT PROCESS  (in order, as it actually happened)
  1. First thing I tried: ______________________________________
  2. Why it failed / what it cost: _____________________________
  3. What made me switch: ______________________________________
  4. Final approach: ___________________________________________

THE CODE  (from memory — editor closed)


  ___________________________________________________________
  ___________________________________________________________
  ___________________________________________________________
  ___________________________________________________________


COMPLEXITY — with the reason, not just the letter
  Time:  O(____)  because ______________________________________
  Space: O(____)  because ______________________________________
  (Count the operations. "It's one pass" is not a reason.
   "Each index is pushed and popped at most once" is a reason.)

THE BUG I HIT  (or would have, without the dry run)
  ____________________________________________________________

EDGE CASES
  ☐ empty   ☐ single element   ☐ all duplicates   ☐ negatives
  ☐ other: ____________________________________________________

IF THEY ASKED "CAN YOU DO BETTER?"
  ____________________________________________________________

RE-SOLVE:   +1d ____   +3d ____   +7d ____
```

### How to revise from it later

- **Cover the code and read only the Trigger + Pattern lines.** Can you rebuild the solution in your head? That's the rep.
- **In the final 48 hours, read only the Trigger lines** across every page, front to back. That's the phrasing→pattern reflex, which is the thing you're actually missing.
- Any page where you can't reconstruct the code from the Trigger alone goes back on the re-solve queue.

---

## PART 5 — Revised Block C timing

Block C is 3h 30m (full track) or 2h (compressed). With voice rounds:

**Full track (3h 30m)**
| Time | What |
|---|---|
| 0:00–1:00 | GPT voice round — problem 1 (45 min + 15 min debrief) |
| 1:00–2:00 | GPT voice round — problem 2 |
| 2:00–3:00 | Solo — 2–3 problems, 25-min timer each, narrated to an empty room |
| 3:00–3:30 | Solution book entries, from memory |

**Compressed track (2h)**
| Time | What |
|---|---|
| 0:00–1:00 | GPT voice round — one problem |
| 1:00–1:40 | Solo — 1–2 problems |
| 1:40–2:00 | Solution book |

You'll get through fewer problems per day this way. **That's the correct trade.** Two problems solved properly under pressure, narrated, dry-run, and written up from memory beats seven skimmed. Coverage is not your bottleneck — production is.

If you fall behind the daily problem lists, **drop from the bottom of each day's table.** The starred (★) problems are the ones that recur in Amazon loops; those stay.
