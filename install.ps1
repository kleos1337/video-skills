# Install the skills into ~/.claude/skills as junctions (no admin rights needed) and build the shared venv.
$ErrorActionPreference = "Stop"
$repo = $PSScriptRoot
$dest = Join-Path $HOME ".claude\skills"
New-Item -ItemType Directory -Force $dest | Out-Null

function Set-Junction($name, $target) {
    $link = Join-Path $dest $name
    if (Test-Path $link) {
        if (-not (Get-Item $link).LinkType) { Write-Warning "$link exists and is not a link; skipped"; return }
        (Get-Item $link).Delete()
    }
    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    Write-Host "ok  $name -> $target"
}

Set-Junction "yt-shared" "$repo\shared"
Get-ChildItem "$repo\skills" -Directory | ForEach-Object { Set-Junction $_.Name $_.FullName }

$py = "$repo\shared\.venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    python -m venv "$repo\shared\.venv"
    & $py -m pip install -q --upgrade pip yt-dlp faster-whisper "av>=14,<17"
}
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Warning "ffmpeg is not on PATH (the script finds the winget install on its own). If it fails: winget install Gyan.FFmpeg"
}
Write-Host "done. Restart Claude Code if the skills don't appear."
