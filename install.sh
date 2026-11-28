#!/usr/bin/env bash
# Link skills/* and shared/ into ~/.claude/skills and build the shared venv.
# On Windows, use install.ps1 (symlinks need Developer Mode or admin rights).
set -euo pipefail
repo="$(cd "$(dirname "$0")" && pwd)"
dest="$HOME/.claude/skills"
mkdir -p "$dest"

ln -sfn "$repo/shared" "$dest/yt-shared"
for d in "$repo"/skills/*/; do
  ln -sfn "${d%/}" "$dest/$(basename "$d")"
  echo "ok  $(basename "$d")"
done

if [ ! -x "$repo/shared/.venv/bin/python" ]; then
  python3 -m venv "$repo/shared/.venv"
  "$repo/shared/.venv/bin/python" -m pip install -q --upgrade pip yt-dlp faster-whisper "av>=14,<17"
fi
command -v ffmpeg >/dev/null || echo "warning: install ffmpeg (brew or apt)"
echo "done. Outside Windows, replace .venv\\Scripts\\python.exe with .venv/bin/python in the SKILL.md files."
