# Contributing to video-skills

There are two ways to contribute:

1. **[Add a skill](#add-a-skill)**: a new command that works from a video transcript.
2. **[Change the engine](#change-the-engine)**: fixes and features in `shared/extract_video.py`.

---

## Add a skill

### Step 1: Create the folder

Make `skills/<name>/SKILL.md`. Use a short, `v`-prefixed name that says what it does, such as `vquiz`.

### Step 2: Write the frontmatter

```yaml
---
name: <name>
description: <what it does, then when to use it, ending with: or says "<name>".>
---
```

Write everything in English. The `description` is what routes Claude to the skill, so name the trigger phrases.

### Step 3: Call the shared engine

Run the engine from `~/.claude/skills/yt-shared`, the way the existing skills do. Reading `yt-shared` in the file is also what lets `/vask` find your skill, so don't skip it.

### Step 4: Follow the skill conventions

- Read the whole transcript, in parts if it has more than 15,000 words.
- Say whether the skill edits code. Most don't.
- End with a cleanup step that removes `yt_context_*` from the temp folder, unless the output is meant to stay.

### Step 5: Install and try it

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

Restart Claude Code, run your skill on a short video, and open a pull request that says what you ran.

---

## Change the engine

- Keep the flags and the stdout labels (`transcript`, `source`, `duration`, `words`, `slides`) stable. The skills parse them.
- Update [docs/engine.md](docs/engine.md) when you change behavior.
- Check both paths on a short video: one with captions, and one forced through Whisper with `--langs zz`.

---

## Pull requests

Keep each pull request to one change. Write code, comments, and docs in English.

To change the README, edit `readme.source.md` and run `npx readme-aura build`. Commit both files. `README.md` is generated, so edits made directly to it are overwritten.
