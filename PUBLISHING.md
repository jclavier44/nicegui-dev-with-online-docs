# Publishing `nicegui-dev-with-online-docs`

Two goals:

1. **Push** the skill to <https://github.com/jclavier44/nicegui-dev-with-online-docs>
2. **Publish** it so it is discoverable on [skills.sh](https://skills.sh)

> **Key fact about skills.sh:** there is **no submission form, PR, or approval step**.
> The registry is *telemetry-driven*: any **public** GitHub repo containing a valid
> `SKILL.md` becomes installable with `npx skills add owner/repo`, and the skill
> appears on skills.sh automatically once people install it. Ranking = install count.
> So "publishing to skills.sh" really means: **make the repo public, keep `SKILL.md`
> valid, and drive installs.**

---

## Part 0 — Fix the repository layout (do this first)

The `skills` CLI discovers a `SKILL.md` in the repo root or inside a
`skills/<name>/` container. Your skill currently lives in a bare top-level folder
(`nicegui-dev-with-online-docs/`), which only gets found by the slow recursive
fallback. Move it to the documented `skills/` layout so discovery is reliable:

```bash
cd ~/Documents/NiceGuiApps/NiceGuiDev_skill

mkdir -p skills
mv nicegui-dev-with-online-docs skills/

# Don't ship Python bytecode caches
rm -rf skills/nicegui-dev-with-online-docs/scripts/__pycache__
printf '__pycache__/\n*.pyc\n' > .gitignore
```

Resulting tree:

```
NiceGuiDev_skill/                 (= the git repo root)
├── .gitignore
├── PUBLISHING.md
└── skills/
    └── nicegui-dev-with-online-docs/
        ├── SKILL.md
        └── scripts/
            └── nicegui_docs.py
```

(If you prefer a single-skill repo, you can instead put `SKILL.md` at the repo root.
Both work; `skills/` keeps room for more skills later.)

---

## Part 1 — Push to GitHub

### 1. Set your git identity (not configured yet on this machine)

```bash
git config --global user.name  "jclavier44"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

### 2. Commit everything

```bash
cd ~/Documents/NiceGuiApps/NiceGuiDev_skill
git add -A
git commit -m "Add nicegui-dev-with-online-docs skill"
git branch -M main
```

### 3. Create the GitHub repo

The repo does **not** need to exist empty first — if `gh` is installed:

```bash
gh repo create jclavier44/nicegui-dev-with-online-docs \
  --public --source=. --remote=origin --push
```

`gh` is **not** installed here, so use the web UI instead:

1. Go to <https://github.com/new>
2. Owner: `jclavier44`, Repository name: `nicegui-dev-with-online-docs`
3. Visibility: **Public** (required for skills.sh discovery)
4. Do **not** initialize with a README/.gitignore (you already have commits)
5. Create, then push:

```bash
git remote add origin https://github.com/jclavier44/nicegui-dev-with-online-docs.git
git push -u origin main
```

---

## Part 2 — Verify the skill is installable

Before anything else, confirm the CLI can discover and parse the skill.

```bash
# From the repo root — list skills without installing
npx skills add . --list

# After it's on GitHub — this is what users will run
npx skills add jclavier44/nicegui-dev-with-online-docs --list
```

Expect to see `nicegui-dev-with-online-docs` listed. If you get **"No skills found"**:

- Confirm `SKILL.md` exists and its YAML frontmatter has both `name:` and `description:`
- Confirm the file is at `skills/nicegui-dev-with-online-docs/SKILL.md`
- Confirm the frontmatter is valid YAML (no tabs)

Install it end-to-end to be safe:

```bash
npx skills add jclavier44/nicegui-dev-with-online-docs -g -a opencode -y
```

---

## Part 3 — Publish / get listed on skills.sh

### 1. Make sure the repo is public

Private repos are not indexed. Confirm at
<https://github.com/jclavier44/nicegui-dev-with-online-docs/settings> →
Danger Zone → visibility.

### 2. Nothing to submit — it's automatic

Once the repo is public, the skill is already installable and eligible for the
skills.sh directory. Listing and ranking update from **install telemetry**
(`npx skills add …`). There is no dashboard, no waitlist, no PR.

Your page will live at:

```
https://skills.sh/jclavier44/nicegui-dev-with-online-docs
```

### 3. Add the skills.sh badge to your README

Create `README.md` at the repo root with a clear install block and the badge:

```markdown
# nicegui-dev-with-online-docs

A NiceGUI development skill that grounds every API question in the **live NiceGUI
documentation index** instead of model memory.

[![skills.sh](https://skills.sh/b/jclavier44/nicegui-dev-with-online-docs)](https://skills.sh/jclavier44/nicegui-dev-with-online-docs)

## Install

```bash
npx skills add jclavier44/nicegui-dev-with-online-docs
```

Works with OpenCode, Claude Code, Cursor, Codex, Copilot, Gemini CLI and
[70+ other agents](https://github.com/vercel-labs/skills#supported-agents).
```

Commit and push it:

```bash
git add README.md && git commit -m "Add README with install instructions" && git push
```

### 4. Drive installs (this is the only lever that matters)

skills.sh ranks purely by install count, so discovery follows usage:

- Post the `npx skills add jclavier44/nicegui-dev-with-online-docs` command in
  NiceGUI / Python / AI-coding communities (Discord, Reddit, X, LinkedIn).
- Add GitHub topics to the repo to help search:
  `agent-skill`, `opencode`, `claude-code`, `nicegui`, `python`.
- Keep `SKILL.md`'s `description` full of trigger keywords (it already is), since
  `skills find` and skills.sh search match on it.
- Ship updates with `npx skills update` in mind — keep the skill self-contained so
  updates don't break for users.

### 5. Optional: request a listing tweak or report issues

If the skill never shows up on skills.sh after real installs, file an issue at
<https://github.com/vercel-labs/skills/issues> with the repo URL.

---

## Ongoing maintenance checklist

- [ ] Repo is **public** and default branch is `main`
- [ ] `SKILL.md` at `skills/nicegui-dev-with-online-docs/SKILL.md`, valid frontmatter
- [ ] `npx skills add jclavier44/nicegui-dev-with-online-docs --list` shows the skill
- [ ] README has the install command and the skills.sh badge
- [ ] `scripts/nicegui_docs.py` path in `SKILL.md` matches the installed location
- [ ] No secrets, no `__pycache__`, no large binaries in the repo
