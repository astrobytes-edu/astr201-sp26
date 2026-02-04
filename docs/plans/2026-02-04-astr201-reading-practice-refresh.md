# ASTR 201 Reading Practice Problems Refresh Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite and add reading practice problems in ASTR 201 lecture readings to comply with the new Problems & Solutions contract (labels, tools, O→M→I, CGS units, structured solutions).

**Architecture:** Each reading gets a contract-compliant Practice Problems section with hidden labels and tool tags. **Solutions live in separate `*-solutions.qmd` files** (marked `draft: true` for now) following the ASTR 101 pattern. Existing quick practice can be preserved as an optional "Legacy Quick Practice" subsection if it remains useful.

**Tech Stack:** Quarto `.qmd`, Markdown, callout blocks.

## References (must read before editing)
- `docs/contracts/astr201-problems-solutions-contract.md`
- `docs/contracts/astr201-pedagogical-contract.md`
- `docs/contracts/astr201-pedagogical-elements.md`
- `handouts/formula-sheets/astr201-math-cheatsheet.qmd`

## Target Files (reading practice)
- `modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd`
- `modules/module-01/readings/lecture-02-foundations-reading.qmd`
- `modules/module-01/readings/lecture-03-gravity-and-orbits.qmd`
- `modules/module-01/readings/lecture-04-light-as-information.qmd`

---

### Task 1: Define a standard Practice Problems section template

**Files:**
- Modify: `modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd`

**Step 1: Write the failing test**
Create a placeholder checklist comment at the top of the Practice Problems section indicating required counts (8–12 total, 3+ O→M→I, tool balance).

```markdown
<!-- PRACTICE-PROBLEMS-AUDIT: MISSING LABELS + O→M→I + TOOL BALANCE -->
```

**Step 2: Run test to verify it fails**
Run:

```bash
rg -n "PRACTICE-PROBLEMS-AUDIT" modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd
```

Expected: The placeholder appears (audit failing by design).

**Step 3: Write minimal implementation**
Replace placeholder with a real template section:
- `## Practice Problems` heading
- Subheadings for Conceptual / Calculation / Synthesis (optional)
- Each problem preceded by a hidden label comment
- **No solutions in the reading** (solutions go in a separate `*-solutions.qmd` file)

```markdown
::: {.callout-note title="Answers" collapse="true"}
[Structured solutions]
:::
```

**Step 4: Run test to verify it passes**
Run:

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd
```

Expected: Hidden labels appear for every problem.

**Step 5: Commit**
(Handled in batch commit at end of plan execution.)

---

### Task 2: Rewrite practice problems in Lecture 01 (Spoiler Alerts)

**Files:**
- Modify: `modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd`

**Step 1: Write the failing test**
Identify current problems lacking labels and O→M→I tags.

```bash
rg -n "Practice Problems" -n modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd
```

**Step 2: Run test to verify it fails**
Confirm there are no hidden labels:

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd
```

Expected: No matches (failure condition).

**Step 3: Write minimal implementation**
- Replace or rewrite problems to hit 8–12 total.
- Add hidden labels with Tools, O→M→I, and ⭐ ratings.
- Ensure at least 3 O→M→I.
- **Remove any answers from the reading.**
- Create `modules/module-01/readings/lecture-01-spoiler-alerts-solutions.qmd` with full structured solutions (mark `draft: true`).
- Keep any prior quick practice in a clearly marked optional subsection if needed.

**Step 4: Run test to verify it passes**
Run:

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd
```

Expected: Labels present for every problem.

**Step 5: Commit**
(Handled in batch commit.)

---

### Task 3: Rewrite practice problems in Lecture 02 (Foundations)

**Files:**
- Modify: `modules/module-01/readings/lecture-02-foundations-reading.qmd`

**Step 1: Write the failing test**
Locate existing practice problems.

```bash
rg -n "Practice Problems" modules/module-01/readings/lecture-02-foundations-reading.qmd
```

**Step 2: Run test to verify it fails**
Confirm there are no hidden labels.

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-02-foundations-reading.qmd
```

Expected: No matches.

**Step 3: Write minimal implementation**
- Rewrite to 8–12 total problems.
- Add labels with tools and O→M→I tags.
- Ensure CGS units by default.
- **Remove any answers from the reading.**
- Create `modules/module-01/readings/lecture-02-foundations-solutions.qmd` with full structured solutions (mark `draft: true`).

**Step 4: Run test to verify it passes**

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-02-foundations-reading.qmd
```

Expected: Labels present for every problem.

**Step 5: Commit**
(Handled in batch commit.)

---

### Task 4: Add new practice problems to Lecture 03 (Gravity & Orbits)

**Files:**
- Modify: `modules/module-01/readings/lecture-03-gravity-and-orbits.qmd`

**Step 1: Write the failing test**
Verify no practice problems section exists.

```bash
rg -n "Practice Problems" modules/module-01/readings/lecture-03-gravity-and-orbits.qmd
```

Expected: No matches.

**Step 2: Run test to verify it fails**
Confirm there are no hidden labels.

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-03-gravity-and-orbits.qmd
```

Expected: No matches.

**Step 3: Write minimal implementation**
- Add a new `## Practice Problems` section.
- Create 8–12 problems covering: orbital speed, escape speed, Kepler scaling, energy/bound vs unbound, misconceptions about centripetal force.
- Add labels with tools and O→M→I.
- Create `modules/module-01/readings/lecture-03-gravity-and-orbits-solutions.qmd` with full structured solutions (mark `draft: true`).

**Step 4: Run test to verify it passes**

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-03-gravity-and-orbits.qmd
```

Expected: Labels present for every problem.

**Step 5: Commit**
(Handled in batch commit.)

---

### Task 5: Add new practice problems to Lecture 04 (Light as Information)

**Files:**
- Modify: `modules/module-01/readings/lecture-04-light-as-information.qmd`

**Step 1: Write the failing test**
Verify no practice problems section exists.

```bash
rg -n "Practice Problems" modules/module-01/readings/lecture-04-light-as-information.qmd
```

Expected: No matches.

**Step 2: Run test to verify it fails**
Confirm there are no hidden labels.

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-04-light-as-information.qmd
```

Expected: No matches.

**Step 3: Write minimal implementation**
- Add a new `## Practice Problems` section.
- Create 8–12 problems covering: spectra, Wien's law, Stefan–Boltzmann, Doppler, observational inference.
- Add labels with tools and O→M→I.
- Create `modules/module-01/readings/lecture-04-light-as-information-solutions.qmd` with full structured solutions (mark `draft: true`).

**Step 4: Run test to verify it passes**

```bash
rg -n "<!-- Problem:" modules/module-01/readings/lecture-04-light-as-information.qmd
```

Expected: Labels present for every problem.

**Step 5: Commit**
(Handled in batch commit.)

---

### Task 6: Global audit and render

**Files:**
- Modify: `modules/module-01/readings/*.qmd`

**Step 1: Write the failing test**
Ensure each reading has the required counts and O→M→I minimums using a manual checklist.

**Step 2: Run test to verify it fails**
Expect at least one reading to be out of balance before final pass.

**Step 3: Write minimal implementation**
Adjust counts and labels so each reading meets:
- 8–12 total
- 3–4 conceptual
- 3–4 calculation
- 2–3 synthesis
- 3+ O→M→I
- at least 3 distinct tools

**Step 4: Run test to verify it passes**
Run:

```bash
quarto render modules/module-01/readings/lecture-01-spoiler-alerts-reading.qmd
quarto render modules/module-01/readings/lecture-02-foundations-reading.qmd
quarto render modules/module-01/readings/lecture-03-gravity-and-orbits.qmd
quarto render modules/module-01/readings/lecture-04-light-as-information.qmd
```

Expected: Render succeeds for each reading.

**Step 5: Commit**

```bash
git add modules/module-01/readings/*.qmd
git commit -m "refresh ASTR201 reading practice problems"
```

---

## Execution Handoff

Plan complete and saved to `docs/plans/2026-02-04-astr201-reading-practice-refresh.md`.

Two execution options:

1. Subagent-Driven (this session)
2. Parallel Session (separate)

Which approach?
