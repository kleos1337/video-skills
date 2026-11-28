---
name: vask
description: Router for the YouTube skill suite. Use whenever the user asks which video skill to use, describes a YouTube or video goal without naming a command, shares a video link with no instructions, or runs /vask. Recommends the right skill or sequence and hands back the exact command to run. Does not do the video work itself.
---

# vask: which video skill?

Route, don't work. Never run extraction, summaries, or edits here. End with a command for the user to run.

## 1. Read the suite

List the suite's skills and read each `SKILL.md` frontmatter. A skill belongs to the suite if it calls the shared engine `yt-shared`:

```powershell
Get-ChildItem "$HOME\.claude\skills\*\SKILL.md" | Where-Object { $_.Directory.Name -ne "vask" -and (Select-String -Path $_ -Pattern "yt-shared" -Quiet) } | ForEach-Object { $_.FullName; Get-Content $_ -TotalCount 4 }
```

Use each skill's real `name` and `description`. Don't rely on memory. The filter skips `vask` itself. A new skill that calls `yt-shared` is routable at once.

## 2. Read the project state (light)

Run a few cheap checks in the current folder. Skip any that don't apply:

- `git status --short` and the project stack (`package.json`, `pyproject.toml`, and similar).
- A `queue\*\INDEX.md`: transcripts are already extracted, so the user may want to compare or pick one.
- A `docs\specs\*.md` from `/vrefine`: a spec exists, so execution is the likely next step.
- A `steps-*.md` from `/vsteps`.

Treat what you find as a hint about where the user is, not as a decision.

## 3. Ask only if the goal is unclear

If the request already names a goal, skip this step. If the user ran `/vask` bare, or only dropped a link, ask **one or two** questions. Make each single-choice, give your recommended answer, and wait. Word them so that "yes" accepts the recommendation.

```
❓ **Q1** - **Goal**: What do you want from this video?
a) Build it into this codebase  b) Get a step-by-step checklist  c) Compare it with other videos  d) Save a whole playlist for later

➡️ a
```

Ask a second question only if the first answer leaves two skills in play, for example a vague "build it" where it is unclear whether the plan is settled. Don't ask about anything you can read from the project.

## 4. Recommend and hand off

Give the **single best** skill, or a sequence such as `/vrefine` then `/vdo`. Then:

- Give 2 or 3 bullets on why, tied to the goal and the project state you found.
- Give the exact command in a code block, with any URL the user already shared. Use `<URL>` only if there is none.
- If you recommend a sequence, give only the first command and name the next.

Don't start the skill yourself.
