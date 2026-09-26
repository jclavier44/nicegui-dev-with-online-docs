# nicegui-dev-with-online-docs

An agent skill for building **NiceGUI** apps that stay correct over time: every API,
prop, event, and styling question is grounded in NiceGUI's **live documentation
index**, never in stale model memory.

[![skills.sh](https://skills.sh/b/jclavier44/nicegui-dev-with-online-docs)](https://skills.sh/jclavier44/nicegui-dev-with-online-docs)

## Why this skill

NiceGUI's API drifts between releases, and its UI bugs surface as *layout* bugs
(gaps that break on Ubuntu, scroll areas that collapse to zero height) rather than
exceptions. This skill pairs hard-won NiceGUI styling rules with a helper that
queries the current upstream docs, so the agent verifies instead of guesses.

## Main features

### 1. Live documentation index — no hallucinated APIs

NiceGUI publishes its entire documentation as machine-readable JSON. The bundled
`scripts/nicegui_docs.py` downloads, caches (7-day TTL), and regex-filters that
index so the whole ~158k-token sitewide dump never enters context.

```bash
DOCS=scripts/nicegui_docs.py

python3 $DOCS "ui.table"                 # content + demos (sitewide index)
python3 $DOCS "ui.table" --demo          # include runnable Python demos
python3 $DOCS "gap" --index search       # broader index, includes GitHub examples
python3 $DOCS "auth" --index examples    # GitHub example apps only
python3 $DOCS --refresh                  # force re-download
```

Three indices are available: `sitewide` (791 entries, demo code), `search`
(850 entries, GitHub examples), and `examples` (59 full example apps). The skill
also instructs the agent to reconcile doc entries against the **installed**
NiceGUI version, and to let the installed version win on disagreement.

### 2. NiceGUI styling pitfalls, encoded

Rules that prevent the classic NiceGUI layout failures:

- Use **inline `style("gap: …")`**, never Tailwind `gap-*` classes (NiceGUI #2171).
- Never put `height: 100%` inside a `max-height` container (it collapses to 0).
- Add `min-width: 0` to flex children in side-by-side chart layouts.
- Dock modal/dialog action buttons so primary actions stay visible while content scrolls.

### 3. Product-thinking guardrails

Before building any data display, the skill forces the questions that prevent
copy-pasted UI: *Where else does this data appear? Should this be one component with
modes? Can the user navigate from a reference to its source?* The same data is
required to look the same everywhere.

### 4. UI architecture discipline

Business logic lives in **controllers**, not in UI event handlers. Handlers stay
thin, data fetching returns Pydantic models, actions are logged, and controllers are
integration-tested. State is modeled with enums rather than implicit boolean flags.

### 5. Checklists for review

Built-in checklists cover data display components, UI architecture, NiceGUI styling,
and "staying current", so the agent (or you) can self-review before shipping.

## Install

```bash
npx skills add jclavier44/nicegui-dev-with-online-docs
```

Works with **OpenCode**, **Claude Code**, **Cursor**, **Codex**, **GitHub Copilot**,
**Gemini CLI**, and [70+ other agents](https://github.com/vercel-labs/skills#supported-agents).

Install globally to a specific agent:

```bash
npx skills add jclavier44/nicegui-dev-with-online-docs -g -a opencode -y
```

## Repository layout

```
skills/nicegui-dev-with-online-docs/
├── SKILL.md                       # the instructions the agent follows
└── scripts/
    └── nicegui_docs.py            # query the live NiceGUI docs index
```

## Requirements

- Python 3 (only for `scripts/nicegui_docs.py`)
- Network access on first run (the index is cached locally afterward)

## License

MIT — see [LICENSE](LICENSE).
