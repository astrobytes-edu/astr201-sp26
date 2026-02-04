# ASTR 201 Assessment Contracts Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create the ASTR 201 assessment contract ecosystem, plus Quarto formula sheets and a math cheatsheet, and a Codex skill that enforces the problems + solutions workflow.

**Architecture:** Three new contracts in `docs/contracts`, four new handouts under `handouts/formula-sheets/`, and one new Codex skill under `~/.codex/skills/`.

**Tech Stack:** Quarto (`.qmd`), Markdown, and Codex skills.

## Task 1: ASTR 201 Problems & Solutions Contract

**Files:**
- Create: `docs/contracts/astr201-problems-solutions-contract.md`

**Step 1: Draft the contract**
- Base structure on `docs/contracts/astr101-problems-solutions-contract.md`.
- Add ASTR 201 taxonomy Tools tag and pipeline section.
- Encode reading/HW minimums and exam recommended mix and star cap.

**Step 2: Manual check**
- Verify labels format and tool list match the design doc.

## Task 2: ASTR 201 Activities Contract

**Files:**
- Create: `docs/contracts/astr201-activities-contract.md`

**Step 1: Draft the contract**
- Base structure on `docs/contracts/astr101-activities-contract.md`.
- Add optional demo touchpoints referencing cosmic-playground.

**Step 2: Manual check**
- Ensure activity types, duration categories, and headers are defined.

## Task 3: ASTR 201 Course Playbook

**Files:**
- Create: `docs/contracts/astr201-course-playbook.md`

**Step 1: Draft the playbook**
- Base structure on `docs/contracts/astr101-course-playbook.md`.
- Encode math ceiling (algebra/proportions/logs + conceptual derivatives only).
- Add ASTR 201 identity and assessment alignment notes.

**Step 2: Manual check**
- Ensure “no calculus required on HW/exams” is explicit.

## Task 4: Formula Sheets + Math Cheatsheet + Constants (Quarto)

**Files:**
- Create: `handouts/formula-sheets/astr201-formula-sheet-exam.qmd`
- Create: `handouts/formula-sheets/astr201-formula-sheet-study.qmd`
- Create: `handouts/formula-sheets/astr201-math-cheatsheet.qmd`
- Create: `handouts/formula-sheets/astr201-constants-sheet.qmd`

**Step 1: Create directory and scaffold files**
- Include YAML frontmatter and consistent section headings.

**Step 2: Populate content (CGS)**
- Convert the S25 LaTeX formula sheet equations into Quarto math blocks.
- Exam sheet: neutral, no “use when” hints.
- Study sheet: include brief scaffolds and tool reminders.
- Math cheatsheet: logs, exponents, scientific notation, unit conversion identity trick.
- Constants sheet: CGS values only.

**Step 3: Manual check**
- Ensure notation consistency and units are explicit (CGS).

## Task 5: ASTR 201 Problems + Solutions Codex Skill

**Files:**
- Create: `~/.codex/skills/astr201-problems-solutions/SKILL.md`

**Step 1: RED (baseline tests)**
- Run 3 pressure scenarios with agents without the skill.
- Record failures and rationalizations.

**Step 2: GREEN (write minimal skill)**
- Write skill with YAML frontmatter, workflow, labels, and solution format.

**Step 3: REFACTOR (close loopholes)**
- Add explicit counters for rationalizations.
- Re-test with agents until compliant.

## Task 6: Verification

**Step 1: Quarto render**
Run: `quarto render`
Expected: Render completes with no errors.

**Step 2: Report**
- Summarize what changed.
- List any tests not run.
