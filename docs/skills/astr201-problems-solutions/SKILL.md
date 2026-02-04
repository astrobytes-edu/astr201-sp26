---
name: astr201-problems-solutions
description: Use when drafting or auditing ASTR 201 assessment problems or solutions and you must enforce the problems-and-solutions contract, taxonomy labels, tool tags, and exam/HW constraints.
---

# ASTR 201 Problems & Solutions

## Overview
Use this skill to enforce the ASTR 201 Problems & Solutions contract: every problem is labeled, tool-balanced, and paired with solutions that show reasoning, units, and sanity checks.

## When to Use
- Building reading problem banks
- Selecting homework subsets
- Writing exam questions
- Drafting solutions
- Auditing any assessment artifact (problems or solutions)

## When NOT to Use
- Lecture slides or readings (use lecture-writing)
- Purely administrative documents

## Core Pattern

**Problem label (hidden):**
```markdown
<!-- Problem: Calculation / Application / O→M→I / Tools: Scaling/Ratio, Unit-Conversion / ⭐⭐ -->
```

**Solution skeleton (calculation):**
```markdown
**Given:** ... (with units)
**Find:** ...
**Equation:** ...
**Steps:** ...
**Unit check:** ...
**Sanity check:** ...
**Answer:** ... (with units)
```

## Quick Reference

| Item | Required |
| --- | --- |
| Label format | Type / Depth / O→M→I / Tools: ... / ⭐ |
| Tool tags | Instructor-only; never visible to students |
| Unit system | CGS by default; label if SI appears |
| Pipeline | Reading bank -> HW subset -> Exam subset |
| Exams | No ⭐⭐⭐; 40-50% conceptual, 40-50% calculation, max 1 synthesis |
| O→M→I minimums | Reading: 3+; HW: 2+; Exams: 2+ |

## Implementation Checklist

1) **Label every problem** with Type, Depth, O→M→I, Tools, and Stars (hidden comment).
2) **Enforce the pipeline**: build reading bank first, then select HW, then select exams.
3) **Check recipe counts** (reading 8-12; HW 6-8; exam mix as above).
4) **Write solutions in full structure** (units, steps, sanity check, interpretation).
5) **Verify tool balance** (at least 3 tools; no single tool > 50%).

## Common Mistakes
- Skipping labels to save time
- Showing tool tags to students
- Using ⭐⭐⭐ on exams
- Solutions that only list final answers
- Missing unit checks or sanity checks

## Rationalizations and Counters

| Excuse | Reality |
| --- | --- |
| "I will add labels later" | Labels define the assessment; no label = not done. |
| "Exams can be harder since they are cumulative" | Contract says exams are easier than HW. |
| "All calculation problems are faster" | Balanced types are required by recipe. |
| "Tool tags are optional" | Tool tags enforce balance and must be included (hidden). |
| "I can show tool tags to students to help them" | Tool tags are instructor-only and must stay hidden. |

## Red Flags - Stop and Fix

- "Just post the answers"
- "No time for labels"
- "This exam problem is hard but fine"
- "O→M→I tagging is optional"
- "Show tool tags to students"

## Example (Conceptual)

```markdown
<!-- Problem: Conceptual / Connection / O→M→I / Tools: Model-Inversion, Uncertainty/Assumptions / ⭐⭐ -->
**Problem.** A star's spectrum shifts redward. What was measured, and what was inferred?
```
