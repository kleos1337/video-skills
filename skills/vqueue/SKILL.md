---
name: vqueue
description: Processes a queue of YouTube videos in batch. Extracts each link's transcript in sequence, stores everything in one folder, and writes an index with a short summary of each. Use when the user sends a list or playlist of links to study later, or says "vqueue".
---

# vqueue: list of videos to transcript library

## 1. Build the queue

Collect the URLs from the request, one per line. For a playlist, list its items with `yt-dlp --flat-playlist --print url "<playlist>"`, using the venv Python (`-m yt_dlp`). Show the item count and the estimated total duration. If the queue has more than 2 hours of video or more than 10 items, wait for the user's OK.

## 2. Extract in sequence

Output folder: `queue\<YYYY-MM-DD>\` in the current folder, or the one the user names. For each URL, one at a time:

```powershell
& "$HOME\.claude\skills\yt-shared\.venv\Scripts\python.exe" "$HOME\.claude\skills\yt-shared\extract_video.py" "<URL>" --out "queue\<date>\<NN>-<id>"
```

A failure on one item doesn't stop the queue. Record the error and continue.

## 3. Index

Write `queue\<date>\INDEX.md`. For each item, include the number, title, URL, duration, word count, source (captions or whisper), status (ok or error), and a 2 to 3 line summary based on the start and end of the transcript. Don't read whole transcripts here. Full reading belongs to `/vdo`, `/vsteps`, `/vcompare`, and `/vrefine`.

## 4. Wrap up

Report how many items succeeded and which failed. Suggest a next step: `/vcompare` for items on the same topic, or `/vdo` for one item. The transcripts stay on disk on purpose, so don't delete the queue folder.
