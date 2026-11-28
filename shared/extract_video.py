#!/usr/bin/env python3
"""Extract a transcript (captions or local Whisper) and, optionally, slides from a video.

Usage: extract_video.py <URL> [--out DIR] [--slides] [--scene 0.3] [--model base|small] [--langs pt,en,es]
Stdout: path to transcript.txt, transcript source, duration, and word count.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

import yt_dlp


def find_ffmpeg():
    """Return the directory that holds ffmpeg (PATH first, then the winget install)."""
    exe = shutil.which("ffmpeg")
    if exe:
        return os.path.dirname(exe)
    base = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages")
    hits = glob.glob(os.path.join(base, "Gyan.FFmpeg*", "**", "bin", "ffmpeg.exe"), recursive=True)
    if hits:
        return os.path.dirname(hits[0])
    sys.exit("ffmpeg not found. Install it with: winget install Gyan.FFmpeg")


def clean_vtt(text):
    """Drop the header, timestamps, HTML tags, and the repeated lines in auto-generated captions."""
    out, last = [], None
    for line in text.splitlines():
        line = line.strip()
        if (not line or line == "WEBVTT" or "-->" in line
                or line.startswith(("Kind:", "Language:", "NOTE"))):
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and line != last:
            out.append(line)
            last = line
    return " ".join(out)


def try_subs(url, out, langs):
    opts = {"skip_download": True, "writesubtitles": True, "writeautomaticsubtitles": True,
            "subtitleslangs": langs, "subtitlesformat": "vtt",
            "outtmpl": os.path.join(out, "sub.%(ext)s"), "quiet": True, "no_warnings": True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:  # captions are only the fast path; any failure falls back to Whisper
        print(f"caption download failed ({e}); using Whisper", file=sys.stderr)
        return None
    for lang in langs:  # honor the priority order; accept variants such as pt-BR and en-orig
        for f in sorted(glob.glob(os.path.join(out, f"sub.{lang}*.vtt"))):
            txt = clean_vtt(open(f, encoding="utf-8").read())
            if txt:
                return txt
    return None


def whisper_transcribe(url, out, ffdir, model_name):
    from faster_whisper import WhisperModel
    opts = {"format": "bestaudio/best", "outtmpl": os.path.join(out, "audio.%(ext)s"),
            "ffmpeg_location": ffdir, "quiet": True, "no_warnings": True,
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3",
                                "preferredquality": "5"}]}
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(os.path.join(out, "audio.mp3"), vad_filter=True)
    blocks, cur, block_start = [], [], 0
    for seg in segments:
        if seg.start >= block_start + 120 and cur:
            blocks.append((block_start, " ".join(cur)))
            cur, block_start = [], int(seg.start // 120) * 120
        cur.append(seg.text.strip())
    if cur:
        blocks.append((block_start, " ".join(cur)))
    return "\n\n".join(f"[{s // 60:02d}:{s % 60:02d}]\n{t}" for s, t in blocks)


def extract_slides(url, out, ffdir, scene):
    opts = {"format": "bestvideo[height<=720][ext=mp4]/best[height<=720]",
            "outtmpl": os.path.join(out, "video.%(ext)s"), "ffmpeg_location": ffdir,
            "quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    video = glob.glob(os.path.join(out, "video.*"))[0]
    subprocess.run([os.path.join(ffdir, "ffmpeg"), "-y", "-loglevel", "error", "-i", video,
                    "-vf", f"select='gt(scene,{scene})'", "-fps_mode", "vfr",
                    os.path.join(out, "slide_%03d.png")], check=True)
    os.remove(video)
    return len(glob.glob(os.path.join(out, "slide_*.png")))


def main():
    ap = argparse.ArgumentParser(description="Extract a transcript and optional slides from a video URL.")
    ap.add_argument("url")
    ap.add_argument("--out", help="output directory (default: <temp>/yt_context_<id>)")
    ap.add_argument("--slides", action="store_true", help="also extract slide frames")
    ap.add_argument("--scene", type=float, default=0.3,
                    help="scene-change threshold, 0 to 1; lower values give more slides")
    ap.add_argument("--model", default="base", help="Whisper model size (base or small)")
    ap.add_argument("--langs", default="pt,en,es", help="caption languages, in priority order")
    a = ap.parse_args()

    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        info = ydl.extract_info(a.url, download=False)
    out = a.out or os.path.join(tempfile.gettempdir(), f"yt_context_{info['id']}")
    os.makedirs(out, exist_ok=True)
    ffdir = find_ffmpeg()

    text = try_subs(a.url, out, a.langs.split(","))
    source = "captions"
    if not text:
        text, source = whisper_transcribe(a.url, out, ffdir, a.model), "whisper"
    path = os.path.join(out, "transcript.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"transcript: {path}")
    print(f"source: {source}")
    print(f"duration: {(info.get('duration') or 0) // 60} min")
    print(f"words: {len(text.split())}")
    if a.slides:
        print(f"slides: {extract_slides(a.url, out, ffdir, a.scene)} in {out}")


if __name__ == "__main__":
    main()
