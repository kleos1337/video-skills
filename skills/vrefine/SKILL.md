---
name: vrefine
description: Turns a video or talk into an approved spec or plan without writing code. Extracts the transcript, restates the goal in its own words, and interviews the user in rounds until no ambiguity is left. Use when the user shares a video and wants to settle what to apply before executing, or says "vrefine".
---

# vrefine: video to shared understanding to spec

Do not edit project code in this skill. The output is an approved spec file.

## 1. Extract

```powershell
& "$HOME\.claude\skills\yt-shared\.venv\Scripts\python.exe" "$HOME\.claude\skills\yt-shared\extract_video.py" "<URL>" [--slides] [--scene 0.1]
```

Add `--slides` if the video shows diagrams or code on screen. Read all of `transcript.txt`, in parts if it has more than 15,000 words. Explore the current repository with your tools. Don't ask about anything you can look up.

## 2. Say it in your own words

Before you ask any question, restate the following in your own words, in a few lines:

- **Goal:** what the user wants to achieve with this video in this project.
- **Problem:** the concrete pain this solves.
- **What the video teaches** that serves the goal, with `[mm:ss]` references.

Don't copy the user's wording or the speaker's. Stop and wait for the user to confirm or correct. If they correct you, restate again.

## 3. Interview in rounds

Map the plan as a **design tree**: every decision branches into the decisions that depend on it. The **frontier** is every decision whose prerequisites are already settled. Ask the whole frontier in one round, numbered, then wait for the answers before the next round. Use this format:

```
❓ **Q1** - **<title>**: <question, with options if there are any>

➡️ <your recommended answer>
```

- Word each question so that "yes" accepts your recommendation.
- Never ask about what you can find yourself (code, files, the video). Go look. Ask only about decisions.
- A question that depends on another open question waits for a later round.
- Each answer reshapes the tree. Recompute the frontier and ask the next round.
- Stop when the frontier is empty and nothing is assumed silently.

## 4. Write the spec

When the frontier is empty, write `docs/specs/<video-slug>.md` (or wherever the project says). Include the goal, the problem, the decisions made (each with its source question), a file-by-file plan, what is out of scope, and how to verify. Show it to the user. Don't call the work done until they confirm that you share the same understanding. To execute the spec, suggest `/vdo`.

## 5. Clean up

```powershell
Remove-Item -Recurse -Force "$env:TEMP\yt_context_*"
```
