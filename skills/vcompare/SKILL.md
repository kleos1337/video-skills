---
name: vcompare
description: Compares two or more YouTube videos or talks on the same topic. Shows where they agree, where they differ, and what each adds, with a recommendation for the current project. Use when the user shares several links and asks for a comparison, or says "vcompare".
---

# vcompare: N videos to one comparison

Read-only. Don't edit the project.

## 1. Extract each video

Run the command once per URL. Each video lands in `%TEMP%\yt_context_<id>`.

```powershell
& "$HOME\.claude\skills\yt-shared\.venv\Scripts\python.exe" "$HOME\.claude\skills\yt-shared\extract_video.py" "<URL>" [--slides]
```

Run them one at a time, because Whisper on CPU is heavy. Warn the user if the videos add up to more than about 2 hours.

## 2. Read and summarize each one

Read each transcript in full, in parts if it has more than 15,000 words. For each video, note the thesis, the recommended techniques and tools, the trade-offs, and the `[mm:ss]` of the key claims.

## 3. Compare

Deliver:

- A **table** with one row per topic (for example architecture, tool, when to use) and one column per video.
- **Agreements** and **real disagreements** (same topic, different conclusions), with the reason.
- **What only one video covers.**
- A **recommendation** for the current project. Inspect the repository first, then say which approach fits and why.

Attribute every claim to a video and a timestamp. Don't blend the speakers' voices, and don't invent consensus.

## 4. Clean up

```powershell
Remove-Item -Recurse -Force "$env:TEMP\yt_context_*"
```
