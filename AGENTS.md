# ASTR 201 (Spring 2026) — Agent Guide

This repo is a Quarto website + RevealJS slide system for **ASTR 201: Astronomy for Science Majors**. The agent supports course logistics, planning, writing, brainstorming, and website/CI maintenance.

## Prime Directive

**Correctness > invariants > reproducibility > clarity > elegance > speed.**

- Do not invent facts, citations, URLs, dates, policies, or numerical values.
- If something is unknown, stop and ask or mark it clearly as `VERIFY`/`[TBD]`.

## Typography Conventions

- **Emdashes:** Use spaces around emdashes: `x — y` not `x—y`

## Math Typesetting (Non‑Negotiable)

- Never use `\\` inside inline math (`$...$`) in Quarto body text.
- `\\` is allowed only when required in **YAML strings** (e.g., to preserve LaTeX line breaks in YAML metadata) or in **display math** environments.
- Long or multi-step equations must be in display math, split across multiple lines with `aligned`.
- Use `\frac{...}{...}` for fractions (no slash forms like `GM/r` in final work).
- Use `\text{...}` for **text subscripts** (e.g., `v_{\text{esc}}`, `T_{\text{eff}}`).
- Final numeric answers must be boxed with units, e.g. `\boxed{x = y\ \text{units}}`.
- Show unit cancellation explicitly in display math, not inline.
- Add a blank line between `Answer:` and any list so Quarto renders bullets correctly.

## Non‑Negotiables (Session Discipline)

- Activate the course conda environment before running repo commands: `conda activate astro`. If `conda`/`astro` isn’t available in this shell, stop and ask (don’t guess paths).
- Read relevant files before editing.
- Follow the phase separation in `docs/llm-lab-protocol.md` (understanding → assumptions → exploration → implementation).
- Treat `docs/software-engineering-playbook.md` as the general engineering checklist for repo changes.
- Run `quarto render` (or `make render`) before claiming success on any content/site change.
- Fix one root cause at a time when debugging; don’t bundle “drive-by” refactors.

## Skills (Autoload for ASTR201 Work)

At the start of any session in this repo, load the ASTR201 teaching skills; keep them active for the whole task and re-load as needed when switching contexts (writing vs auditing vs systems work).

- Codex skills (preferred, live outside repo):
  - `astr201-lecture-writing`
  - `lecture-audit`
  - `astr201-equations`
  - `astr201-figures`
  - `astr201-problems-solutions`
  - `voice-and-tone`
  - `math-grammar-rules`

Load with:

Superpowers are discovered from `~/.agents/skills/`.
Ensure the symlink exists: `~/.agents/skills/superpowers -> ~/.codex/superpowers/skills/`.

Optional one-command helper (auto-loads the course lecture-writing skill for this repo):
`~/.codex/bin/lecture-writing`

Repo-local Claude skills (reference docs under version control):
- `.claude/skills/creating-astr201-materials/`
- `.claude/skills/astr201-lecture-writing/`
- `.claude/skills/astr201-lecture-audit/`
- `.claude/skills/astr201-equations/`
- `.claude/skills/astr201-figures/`

## Repo Map (Where Things Live)

- Site config: `_quarto.yml`, `_quarto-student.yml`, `_quarto-instructor.yml`, `_brand.yml`
- Custom shortcodes/filters: `_extensions/course/shortcodes.lua`
- Reusable includes: `_includes/` (including `_includes/equations/`)
- Data registries:
  - Equations: `data/equations.yml`, `data/eqcards.yml`
  - Figures: `assets/figures.yml`
  - Schedule data: `data/schedule.yml` (generated/consumed by site tooling)
- Content:
  - `index.qmd` (home)
  - `course-info/` (syllabus, schedule, policies)
  - `modules/module-*/` (module hubs, slides, readings, `_prep/` instructor-only)
  - `handouts/`, `homework/`, `exams/`, `explore/`
- Docs system:
  - Contracts/specs: `docs/contracts/`, `docs/specs/`
  - Audits: `docs/audits/`
  - Plans: `docs/plans/` (preferred place for implementation plans)
  - Acceptance gate: `docs/acceptance/`

## Core Systems (Do This, Not Ad-Hoc)

### Figures

- Register figures in `assets/figures.yml`.
- Use shortcodes, not raw paths:
  - `{{< fig id >}}` (image + caption)
  - `{{< img id >}}` (image only; good for slides)

Implementation is in `_extensions/course/shortcodes.lua`; align registry fields with what the shortcode reads (`path`, `caption`, `alt`, optional `credit`).

### Equations

- Canonical equations use the equation system:
  - Registry: `data/equations.yml`
  - Meaning cards: `data/eqcards.yml`
  - LaTeX includes: `_includes/equations/*.qmd`
- Preferred pattern when introducing:
  - `{{< include _includes/equations/<name>.qmd >}}`
  - `{{< eqrefcard <equation-id> >}}`

### Assessments (Problems + Solutions)

- Required pipeline: **reading bank → homework subset → exam subset** (exams easier than HW).
- Use the problems contract: `docs/contracts/astr201-problems-solutions-contract.md`.
- Every problem must include a **hidden label** with type, depth, O→M→I tag, tools, and ⭐ rating.
- Tool tags are **instructor-only** and must remain hidden from students.
- Solutions live in separate `*-solutions.qmd` files (ASTR 101 pattern), typically `draft: true` while in development.

### Units Convention (ASTR 201)

- Default unit system: **CGS**.
- SI is allowed only if explicitly stated.

### Brand → SCSS tokens (CI enforced)

- `_brand.yml` is the source of truth.
- Generated file: `assets/theme/_tokens_generated.scss`
- Regenerate with `python scripts/brand_to_scss.py` or `make tokens`.

CI fails if `_tokens_generated.scss` is out of date.

### Student vs Instructor builds

- Student (default): `quarto render`
- Instructor: `quarto render --profile instructor` (outputs to `_site-instructor/`)

## Standard Commands

- `make preview` (generates tokens, runs `quarto preview`)
- `make render` (generates tokens, runs `quarto render`)
- `make tokens` (regen SCSS tokens)
- `python scripts/schedule_generator.py` (schedule tooling, if used)

## Assessment Artifacts

- Formula sheets and math support live in `handouts/formula-sheets/`:
  - `handouts/formula-sheets/astr201-formula-sheet-exam.qmd`
  - `handouts/formula-sheets/astr201-formula-sheet-study.qmd`
  - `handouts/formula-sheets/astr201-math-cheatsheet.qmd`
  - `handouts/formula-sheets/astr201-constants-sheet.qmd`

## CI Reality

- `.github/workflows/ci.yml` renders HTML (`quarto render --to html`) and runs link/image checks via `proof-html`.
- External URLs may be ignored (see `ignore_url_re` in the workflow); internal links and missing artifacts (e.g., `*.pdf`) can still fail CI.
  - Before merging changes that touch links/navigation, use `docs/ci-checklist.md` as the preflight checklist.

## What “Done” Means

- `quarto render` succeeds with no errors.
- For content work: narrative voice, equation meaning+units, figure registry usage, and retrieval practice meet `docs/contracts/astr201-pedagogical-contract.md`.
- For UI/brand changes: satisfy `docs/acceptance/course-site-acceptance-screenshots.md` (golden views) before declaring ready.
