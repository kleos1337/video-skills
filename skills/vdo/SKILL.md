---
name: vdo
description: Watches a YouTube video or talk (with or without captions) and applies what it teaches to the current project. Extracts the transcript, summarizes it, maps it onto the files, implements the change, and runs the tests. Use when the user shares a link and asks to apply, implement, or do what the video shows, or says "vdo".
---

# vdo: video to code

## 1. Extract

```powershell
& "$HOME\.claude\skills\yt-shared\.venv\Scripts\python.exe" "$HOME\.claude\skills\yt-shared\extract_video.py" "<URL>" [--slides] [--scene 0.1]
```

Add `--slides` if the video shows diagrams or code on screen. A lower `--scene` value gives more frames. If the user points to a spec from `/vrefine`, read the spec and use the video for reference only.

## 2. Read everything

Read all of `transcript.txt`. If it has more than 15,000 words, read it in sequential parts. Open only the relevant `slide_*.png` files.

## 3. Summarize before editing

State the video's thesis and the problem it solves, the tools, patterns, and architectures it recommends, and the trade-offs and warnings the speaker gives.

## 4. Resolve ambiguity

If the request has more than one reasonable reading and the choice changes files, data, or a public API, ask one short round of numbered questions. Give each a recommended answer, then wait. If the ambiguity is large, suggest `/vrefine`. Otherwise, don't ask.

## 5. Apply

Inspect the repository and propose a file-by-file plan. If the user already asked you to apply the change, execute it. Follow the project's CLAUDE.md and AGENTS.md. Run the project's tests and linters and report the real results.

## 6. Clean up

```powershell
Remove-Item -Recurse -Force "$env:TEMP\yt_context_*"
```
