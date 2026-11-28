---
name: vsteps
description: Converts a YouTube tutorial or talk into a numbered, executable step list with timestamps, commands, and prerequisites, without changing the project. Use when the user wants the steps, checklist, or recipe from a video, or says "vsteps".
---

# vsteps: video to steps

Read-only. Don't edit the project.

## 1. Extract

```powershell
& "$HOME\.claude\skills\yt-shared\.venv\Scripts\python.exe" "$HOME\.claude\skills\yt-shared\extract_video.py" "<URL>" --slides --scene 0.1
```

Keep `--slides` for tutorials that show code, a terminal, or screens. Read the whole transcript, in parts if it has more than 15,000 words. Check the slides near any command or configuration.

## 2. Output

Write `steps-<slug>.md` in the current folder, or show the steps in chat if the user prefers:

1. **Prerequisites:** tools, versions, accounts, and anything that must exist first.
2. **Numbered steps**, one action each. Give every step a `[mm:ss]` reference, the exact command or file when the video shows it, and how to tell it worked.
3. **Pitfalls** the speaker warned about.
4. **Gaps:** what the video skipped or left ambiguous. Mark these. Don't invent content.

Automatic transcription misspells names. Mark any command or package whose spelling is doubtful as "confirm". At the end, suggest `/vdo` to run the steps in the project.

## 3. Clean up

```powershell
Remove-Item -Recurse -Force "$env:TEMP\yt_context_*"
```
