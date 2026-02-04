# HW2 + Lecture Problem Bank Updates Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update the ASTR 201 problem bank and contract for HW2 (Option A) and add the HW3 Option B synthesis problem to Lecture 4, then draft HW2 and update navigation.

**Architecture:** Content-only changes in Quarto `.qmd` files plus a contract tweak; no new tooling or data formats.

**Tech Stack:** Quarto, YAML front matter, ASTR 201 contracts/shortcodes.

---

### Task 1: Update HW recipe counts in the problems/solutions contract

**Files:**
- Modify: `docs/contracts/astr201-problems-solutions-contract.md`

**Step 1: Edit the HW recipe table**
- Update total problems to **8–10** and adjust conceptual/calculation/synthesis minimums to match.

**Step 2: Quick sanity pass**
- Ensure the new counts still align with “exams easier than HW” and tool-balance checklist.

**Step 3: Commit**
```bash
git add docs/contracts/astr201-problems-solutions-contract.md
git commit -m "docs: update HW recipe counts"
```

---

### Task 2: Update Lecture 3 reading + solutions (Virial capstone)

**Files:**
- Modify: `modules/module-01/readings/lecture-03-gravity-and-orbits.qmd`
- Modify: `modules/module-01/readings/lecture-03-gravity-and-orbits-solutions.qmd`

**Step 1: Remove the virial item from Quick Practice**
- Delete the virial quick-practice item and its quick-solution line.

**Step 2: Add a new synthesis problem (virial capstone)**
- Add Problem 11 with label, tool tags, and CGS units.

**Step 3: Add matching solution**
- Use the synthesis solution template (Restatement, Key elements, Sample response, Grading guidance).

**Step 4: Fix stray LaTeX escapes**
- Replace `\\dfrac`, `\\sqrt`, `\\mu`, `\\times` with single-backslash versions.

**Step 5: Commit**
```bash
git add modules/module-01/readings/lecture-03-gravity-and-orbits.qmd \
  modules/module-01/readings/lecture-03-gravity-and-orbits-solutions.qmd
git commit -m "content: add virial capstone and clean lecture 3 solutions"
```

---

### Task 3: Add HW3 Option B synthesis problem to Lecture 4

**Files:**
- Modify: `modules/module-01/readings/lecture-04-light-as-information.qmd`
- Modify: `modules/module-01/readings/lecture-04-light-as-information-solutions.qmd`

**Step 1: Add new synthesis problem (Problem 11)**
- Doppler → velocity dispersion → virial mass (order-of-magnitude, CGS-aware).

**Step 2: Add matching synthesis solution**
- Use restatement + key elements + sample response + grading guidance.

**Step 3: Fix stray LaTeX escapes**
- Replace `\\mu`, `\\times` in solution file.

**Step 4: Commit**
```bash
git add modules/module-01/readings/lecture-04-light-as-information.qmd \
  modules/module-01/readings/lecture-04-light-as-information-solutions.qmd
git commit -m "content: add L4 synthesis capstone and clean solutions"
```

---

### Task 4: Draft HW2 and update navigation

**Files:**
- Create: `homework/astr201-hw2.qmd`
- Modify: `homework/index.qmd`
- Modify: `_quarto.yml`

**Step 1: Draft HW2**
- Select 8–10 problems (mostly Lecture 3, limited Lecture 4) with no tool hints.
- Use TBD placeholders for dates.

**Step 2: Update homework index + sidebar**
- Add HW2 row and nav entry.

**Step 3: Commit**
```bash
git add homework/astr201-hw2.qmd homework/index.qmd _quarto.yml
git commit -m "content: add HW2 draft and nav updates"
```

---

### Task 5: QA pass

**Files:**
- Review all modified `.qmd` files

**Step 1: Check labels/tool tags/CGS**
- Confirm labels are hidden, tool balance is reasonable, and CGS units are consistent.

**Step 2: Spot-check math grammar**
- Ensure every equation in problems/solutions is readable with units and sanity checks.

**Step 3: Commit (if fixes applied)**
```bash
git add <files>
git commit -m "content: QA fixes for HW2 + lecture problems"
```
