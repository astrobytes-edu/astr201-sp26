# HW Solutions Visual QA + Formatting Fixes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Visually QA HW1/HW2 solutions pages, fix math rendering/overflow/list issues, and update the agent math-typing rule to prevent regressions.

**Architecture:** Render the specific solution pages to HTML, visually inspect each section for layout/LaTeX/list issues, then edit the source `.qmd` files to align with the problems/solutions contract and math‑grammar rules. Re‑render to confirm fixes.

**Tech Stack:** Quarto, Markdown/LaTeX, local file inspection (browser), `rg` for checks.

### Task 1: Render HW solution pages for visual QA

**Files:**
- Source: `homework/solutions/astr201-hw1-solutions.qmd`
- Source: `homework/solutions/astr201-hw2-solutions.qmd`

**Step 1: Render HW1 solutions**

Run: `quarto render homework/solutions/astr201-hw1-solutions.qmd`
Expected: Build completes without errors.

**Step 2: Render HW2 solutions**

Run: `quarto render homework/solutions/astr201-hw2-solutions.qmd`
Expected: Build completes without errors.

### Task 2: Visual inspection (page‑by‑page)

**Files:**
- Output HTML under `_site/homework/solutions/`

**Step 1: Open HW1 solutions page and scan each problem**

Check: list rendering, inline math, display math overflow, unit cancellation, boxed answers, and tool-label visibility (should be hidden).

**Step 2: Open HW2 solutions page and scan each problem**

Check: display math multi‑line formatting, `\` usage only in display math/YAML, `\approx` errors, list rendering, boxed answers with units.

### Task 3: Fix issues in source `.qmd`

**Files:**
- Modify: `homework/solutions/astr201-hw1-solutions.qmd`
- Modify: `homework/solutions/astr201-hw2-solutions.qmd`
- Modify: `AGENTS.md`

**Step 1: Edit to remove inline `\\` and convert long math to multi‑line display**

**Step 2: Ensure lists render (blank line after `Answer:`)**

**Step 3: Box final answers with units and show unit cancellation**

### Task 4: Re‑render and re‑inspect

**Step 1: Re‑render both solution pages**

Run: `quarto render homework/solutions/astr201-hw1-solutions.qmd`
Run: `quarto render homework/solutions/astr201-hw2-solutions.qmd`
Expected: Build completes without errors.

**Step 2: Re‑inspect HTML to confirm fixes**

### Task 5: Stage changes (commit only if requested)

**Step 1: Stage files**

Run: `git add AGENTS.md homework/solutions/astr201-hw1-solutions.qmd homework/solutions/astr201-hw2-solutions.qmd`

**Step 2: Commit**

Run: `git commit -m "fix: qa hw solutions math formatting"`

