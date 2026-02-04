# ASTR 201 Assessment Contracts + Formula Sheets Design

**Date:** 2026-02-04
**Owner:** Dr. Anna Rosen
**Status:** Draft (approved in conversation)

## Goal
Create a contract ecosystem for ASTR 201 that mirrors ASTR 101 where appropriate, but is tuned for ASTR 201 rigor, tool-based reasoning, and the "measurement → model → inference" throughline. The ecosystem must reduce authoring overhead, standardize quality, and enable rapid reuse (reading bank → HW subset → exam subset).

## Scope (Now)
- New contracts:
  - `docs/contracts/astr201-problems-solutions-contract.md`
  - `docs/contracts/astr201-activities-contract.md`
  - `docs/contracts/astr201-course-playbook.md`
- New assessment support artifacts (Quarto):
  - `handouts/formula-sheets/astr201-formula-sheet-exam.qmd`
  - `handouts/formula-sheets/astr201-formula-sheet-study.qmd`
  - `handouts/formula-sheets/astr201-math-cheatsheet.qmd`
- New Codex skill enforcing ASTR 201 problems + solutions workflow.

## Out of Scope (Deferred)
- Demo/data contracts (demo pedagogy, compute provider, physics library, spectra data). Activities contract will include optional demo touchpoints that reference cosmic-playground without formal contracts yet.

## Contract 1: Problems & Solutions (Unified)
**Purpose:** A single, enforceable standard for reading practice problems, homework, exams, and solution files.

### Taxonomy (ASTR 201 revision of ASTR 101)
Keep the ASTR 101 taxonomy and add an instructor-only Tools tag.

**Label format (hidden in HTML comment):**
```
Type / Depth / O→M→I / Tools: Dimensional, Scaling/Ratio, Energy / ⭐⭐
```

**Type:** Conceptual, Calculation, Synthesis

**Depth:** Recognition, Application, Connection

**O→M→I tag:** required for minimum counts

**Tools (multi-select, instructor-only):**
- Dimensional
- Scaling/Ratio
- Order-of-Magnitude
- Energy
- Force/Balance
- Model-Inversion
- Data/Graph
- Uncertainty/Assumptions
- Unit-Conversion

### Pipeline (Required)
Reading bank → HW subset → Exam subset (exams easier than HW).

### Recipes
- **Reading problems:** 8–12 total; balanced by type; 3+ O→M→I.
- **Homework:** 6–8 total; balanced by type; 2+ O→M→I.
- **Exams (recommended):** 40–50% conceptual, 40–50% calculation, max 1 synthesis; no ⭐⭐⭐ problems.

### Solution Standards
Retain ASTR 101 solution formats but enforce ASTR 201 math-grammar rigor:
- Conceptual: restatement, key insight, answer, common misconception.
- Calculation: given/find with units, equation, step-by-step, unit check, sanity check, boxed answer.
- Synthesis: restatement, key elements checklist, sample response, grading guidance.

## Contract 2: Activities
ASTR 201 activities contract mirrors ASTR 101 structure (worksheet, discussion, lab, demo-driven) but assumes higher math fluency and includes optional demo touchpoints. Each activity specifies type, duration, objective, and structure. Demos are referenced as optional add-ons from cosmic-playground.

## Contract 3: Course Playbook
Codifies course identity, math ceiling, and pacing guidance.

**Math ceiling:** Algebra + proportional reasoning + logs (when explained) + basic trig; no calculus required on HW or exams. Conceptual derivatives allowed for motivation/derivation context only.

## Formula Sheets (Quarto)
Two formula sheets plus a separate math cheatsheet.

- **Exam formula sheet (neutral):** equations and notation only, no "use when" hints.
- **Study/HW formula sheet (annotated):** brief scaffolds and reminders.
- **Math cheatsheet:** logs/exponents identities, unit conversion tips, and algebra reminders.

## New Codex Skill
Create a Codex skill that enforces the ASTR 201 problems & solutions contract, including taxonomy labels, pipeline workflow, solution formats, and tool balance checks. Follow the writing-skills TDD workflow (baseline failures → minimal skill → re-test).

## Success Criteria
- Contracts exist and align with ASTR 201 pedagogical contract.
- Formula sheets + math cheatsheet render cleanly in Quarto.
- Homework and exams can be designed by selecting from the reading bank without drift in style or rigor.

