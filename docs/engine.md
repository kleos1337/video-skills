# Engine reference

`shared/extract_video.py` turns a video URL into a transcript and, optionally, slide frames.

## Usage

```powershell
shared/extract_video.py <URL> [--out DIR] [--slides] [--scene 0.3] [--model base|small] [--langs pt,en,es]
```

Run it with the venv Python, `shared/.venv\Scripts\python.exe` on Windows or `shared/.venv/bin/python` elsewhere.

## Options

| Option | Default | Description |
|---|---|---|
| `url` | required | Video URL. |
| `--out DIR` | `<temp>/yt_context_<id>` | Output folder. Created if missing. |
| `--slides` | off | Download the video at 720p or below, save a frame at each scene change, then delete the video file. |
| `--scene` | `0.3` | Scene-change threshold, 0 to 1. A lower value gives more frames. |
| `--model` | `base` | Whisper model size, `base` or `small`. |
| `--langs` | `pt,en,es` | Caption languages, in priority order. Variants such as `pt-BR` and `en-orig` match. |

## How it picks a transcript source

1. **Captions.** `yt-dlp` fetches manual or automatic captions as VTT. The engine removes the header, timestamps, HTML tags, and repeated lines, then joins the text. Caption transcripts have no time markers.
2. **Whisper fallback.** With no usable captions, or if the caption download fails, the engine downloads the audio as MP3 and transcribes it with `faster-whisper` on CPU (`int8`, voice-activity filter on). The transcript has a `[mm:ss]` marker every 2 minutes.

## Output

Files in the output folder:

| File | When |
|---|---|
| `transcript.txt` | Always. |
| `slide_NNN.png` | With `--slides`. |
| `sub.*.vtt` | Left behind if captions were downloaded. |
| `audio.mp3` | Left behind if Whisper ran. |

Stdout, one label per line:

```text
transcript: <path to transcript.txt>
source: captions | whisper
duration: <minutes> min
words: <word count>
slides: <count> in <folder>      (only with --slides)
```

The skills parse these labels. Keep them stable.

## ffmpeg

The engine uses `ffmpeg` from `PATH`. On Windows it also looks in the winget install folder. If it finds neither, it exits with `ffmpeg not found. Install it with: winget install Gyan.FFmpeg`.
