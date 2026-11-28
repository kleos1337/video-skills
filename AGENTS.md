# AGENTS.md

> A short guide for AI agents working on this repository.

## Rules

1. **English only.** Code, comments, docs, commit messages, and PR text are in English.
2. **One skill, one folder.** Each skill is `skills/<name>/SKILL.md` with `name` and `description` in the frontmatter.
3. **Use the shared engine.** Skills call `~/.claude/skills/yt-shared/extract_video.py`. A skill belongs to the suite if its file mentions `yt-shared`, and `/vask` finds skills that way.
4. **Keep the engine contract.** Don't rename the flags or the stdout labels (`transcript`, `source`, `duration`, `words`, `slides`) or the output files (`transcript.txt`, `slide_NNN.png`). See [docs/engine.md](docs/engine.md).
5. **Don't invent facts.** README claims must match the files in the repo.

## Commands

| Task | Command |
|---|---|
| Install on Windows | `powershell -ExecutionPolicy Bypass -File install.ps1` |
| Install on Linux or macOS | `./install.sh` |
| Run the engine | `shared/.venv\Scripts\python.exe shared/extract_video.py <URL>` |
| Check the Whisper path | add `--langs zz` to force the fallback |

The repository has no automated test suite. Verify a change by running the engine on a short video.

## Layout

- `shared/extract_video.py`: the engine.
- `skills/`: `vask`, `vrefine`, `vdo`, `vqueue`, `vcompare`, and `vsteps`.
- `readme.source.md`: README source. `README.md` is generated from it by readme-aura (`npx readme-aura build`, or the workflow on push). Never edit `README.md` by hand.
- `assets/banner.svg` and `assets/architecture.svg`: hero and diagram. Hand-built Liquid Glass SVGs.
- `.github/workflows/readme-aura.yml`: rebuilds `README.md` when `readme.source.md` changes.
- `docs/engine.md`: engine reference.

## Notes

- The `SKILL.md` files use Windows paths (`.venv\Scripts\python.exe`, `%TEMP%`).
- Installers link the repo into `~/.claude/skills`, so edits to `skills/` take effect after a Claude Code restart.
