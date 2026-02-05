# ASTR 201 Problems & Solutions Contract

*Taxonomy, format, and quality standards for all ASTR 201 assessment problems and solutions.*

Version: v1.0 • Status: Active • Owner: Instructor

---

## 0) Purpose and Scope

This contract enforces consistency across all ASTR 201 assessment artifacts:
- Reading practice problem banks
- Homework assignments
- Exam questions
- Solution files

**Philosophy:** Problems should teach reasoning tools and reinforce the measurement → model → inference throughline, not reward memorization or plug-and-chug.

---

## 1) Assessment Pipeline (Required)

**Reading bank → Homework subset → Exam subset (easier than HW).**

- Reading problems are the canonical bank.
- Homework selects a balanced subset from the reading bank.
- Exams select a smaller, easier subset (no ⭐⭐⭐).

This pipeline is required to reduce authoring overhead and preserve consistency.

---

## 2) Problem Taxonomy (ASTR 201 Revision)

Each problem is labeled along five dimensions.

### 2.1 Type (format)

| Type | Description | Example |
| --- | --- | --- |
| **Conceptual** | No calculation; reasoning about ideas/models | "What was measured vs inferred?" |
| **Calculation** | Apply quantitative tool to get a number | "Estimate orbital period at 30 AU" |
| **Synthesis** | Combine multiple ideas across an inference chain | "Use observation + model to infer a property" |

### 2.2 Depth (thinking level)

| Depth | What It Demands | Indicator |
| --- | --- | --- |
| **Recognition** | Identify, recall, classify | "Which statement is correct?" |
| **Application** | Use a tool in a familiar context | "Compute v_orb from M and r" |
| **Connection** | Link ideas, justify reasoning, critique claims | "Explain why this interpretation fails" |

### 2.3 O→M→I tag (throughline)

| Tag | Meaning | Audit Use |
| --- | --- | --- |
| **O→M→I** | Requires observable → model → inference reasoning | Ensures course thesis is reinforced |
| **—** | No inference chain required | Tool drill or mechanics practice |

### 2.4 Tools (ASTR 201 instructor-only tag)

**Instructor-only. Do not show to students in the rendered output.**

Allowed tool tags (multi-select):
- Dimensional
- Scaling/Ratio
- Order-of-Magnitude
- Energy
- Force/Balance
- Model-Inversion
- Data/Graph
- Uncertainty/Assumptions
- Unit-Conversion

### 2.5 Difficulty (stars)

| Stars | Meaning | Typical Use |
| --- | --- | --- |
| ⭐ | Straightforward, builds confidence | Warmup, first exposure |
| ⭐⭐ | Standard ASTR 201 level | Most problems |
| ⭐⭐⭐ | Challenging synthesis or transfer | Stretch problems (not on exams) |

---

## 2.6 Units Convention (ASTR 201)

- Default unit system: **CGS**.
- If SI or mixed units are used, they must be stated explicitly.
- All conversions must show the identity trick (multiply by 1) and carry units through each step.

---

## 3) Required Label Format (Hidden)

Every problem must include a label in a hidden comment.

```
Type / Depth / O→M→I / Tools: Dimensional, Scaling/Ratio / ⭐⭐
```

**Placement:** in an HTML comment before the problem statement.

```markdown
<!-- Problem: Calculation / Application / O→M→I / Tools: Scaling/Ratio, Unit-Conversion / ⭐⭐ -->
**Problem 4.** ...
```

---

## 4) Calculation Sub-Types (Optional Scaffolding)

For calculation problems, optionally specify a sub-type:

| Sub-Type | Description | When to Use |
| --- | --- | --- |
| **Setup** | Identify equation and knowns/unknowns, no solve | Early practice |
| **Execute** | Carry out calculation | Mechanics practice |
| **Interpret** | Explain physical meaning of result | Diagnosis of understanding |
| **Full** | Setup + Execute + Interpret | Standard assessment |

Format with sub-type:
```
Calculation:Full / Application / O→M→I / Tools: Scaling/Ratio / ⭐⭐
```

---

## 5) Solution Format Requirements

Solutions must follow the math-grammar rules in the ASTR 201 Pedagogical Contract.

### 5.0 Formatting and Presentation (Non‑Negotiable)

- **Display math for multi‑step work.** Any derivation or multi‑line calculation must use display math (`$$ ... $$`) with line breaks and clear step separation.
- **No inline line breaks.** Never use `\\` inside inline math (`$...$`). Line breaks belong only in display math.
- **Blank line before lists.** If a label ends with a colon (e.g., `Answer:` or `Steps:`), add a blank line before the list so Quarto renders bullets correctly.
- **Use fraction form.** Use `\frac{...}{...}` (no slash forms like `GM/r` in final work).
- **Text subscripts.** Use `\text{...}` for text subscripts (e.g., `v_{\text{esc}}`, `T_{\text{eff}}`).
- **Box final answers.** Final numeric answers must be boxed with units, e.g. `\boxed{x = y\ \text{units}}`.
- **Show unit cancellation.** Unit cancellations must be shown explicitly in display math (not compressed into inline text).
- **Prefer ratio forms for scaling.** Use ratio/reference forms (e.g., $P/1\,\text{yr} = (a/1\,\text{AU})^{3/2}$) to avoid misleading “$P=a$” shortcuts.

### 5.1 Conceptual Problems
1) **Restatement** (1 sentence)
2) **Key insight** (core idea being tested)
3) **Answer** (clear, complete response)
4) **Common misconception** (if applicable)

### 5.2 Calculation Problems
1) **Given / Find** (with units)
2) **Equation** (identify relevant relation)
3) **Step-by-step solution** (no skipped steps)
4) **Unit check** (dimensional consistency)
5) **Sanity check** (order of magnitude or physical reasonableness)
6) **Answer summary** (boxed or bold, with units)

**Step-by-step standard:** show each algebraic transformation on its own display line (or aligned block) so the reasoning is visible and readable.

### 5.3 Synthesis Problems
1) **Restatement**
2) **Key elements** (checklist of points a complete answer must address)
3) **Sample response** (model answer at expected depth)
4) **Grading guidance** (full vs partial credit)

---

## 6) Recipes (Minimums and Recommendations)

### 6.1 Reading Problem Banks (Required)

| Requirement | Minimum |
| --- | --- |
| Total problems | 8–12 |
| Conceptual | 3–4 |
| Calculation | 3–4 |
| Synthesis | 2–3 |
| O→M→I tagged | 3+ |

### 6.2 Homework Assignments (Required)

| Requirement | Minimum |
| --- | --- |
| Total problems | 8–10 |
| Conceptual | 3–4 |
| Calculation | 3–4 |
| Synthesis | 2–3 |
| O→M→I tagged | 2+ |

### 6.3 Exams (Recommended)

- 40–50% conceptual
- 40–50% calculation
- Max 1 synthesis problem
- **No ⭐⭐⭐ problems**
- At least 2 O→M→I tagged problems

**Constraint:** Exams must be easier than homework in difficulty and reasoning chain length.

---

## 7) Tool Balance Checklist (Instructor Only)

Before finalizing an assessment, check:
- [ ] At least 3 distinct tools represented
- [ ] No single tool exceeds 50% of the problems
- [ ] At least 2 problems require interpretation (not just calculation)
- [ ] Tool tags are hidden from students

---

## 8) Anti-Patterns (Forbidden)

- Problems that test pure recall without reasoning
- Calculations without units or sanity checks
- Hidden assumptions not stated or discussed
- All problems at the same difficulty level
- Exams that include ⭐⭐⭐ problems
- Solutions that skip algebraic steps
- Tool tags shown to students

---

## 9) Audit Checklist

- [ ] Every problem has a hidden taxonomy label
- [ ] O→M→I minimums satisfied
- [ ] Homework and exams are subsets of the reading bank
- [ ] Exams meet the recommended mix and ⭐⭐⭐ cap
- [ ] Calculation solutions show units and sanity checks
- [ ] Solutions explain the physical meaning, not just numbers
