# ASTR 201 Activities Contract

*Types, formats, and quality standards for in-class activities and worksheets in ASTR 201.*

Version: v1.0 • Status: Active • Owner: Instructor

---

## 0) Purpose and Scope

This contract ensures consistency across all ASTR 201 activities:
- In-class worksheets
- Discussion activities (TPS)
- Data-driven exercises
- Optional demo-driven explorations

**Philosophy:** Activities must surface reasoning tools and misconceptions, not just rehearse procedures.

---

## 1) Activity Types

| Type | Description | Typical Duration | Primary Mode |
| --- | --- | --- | --- |
| **Worksheet** | Scaffolded, multi-step problem sequence | 20–45 min | Individual/Pair |
| **Discussion** | Think-Pair-Share or small-group reasoning | 10–20 min | Collaborative |
| **Data-Driven** | Interpret plots, tables, or spectra | 20–40 min | Investigation |
| **Demo-Driven (Optional)** | Interactive exploration using cosmic-playground demos | 15–30 min | Hands-on |

---

## 2) Time Budget Categories

| Category | Duration | Use Case |
| --- | --- | --- |
| **Quick** | 10–15 min | Lecture break, single concept check |
| **Standard** | 20–30 min | Lecture + activity day |
| **Full** | 40–45 min | Activity-focused day |
| **Extended** | 50–60 min | Lab or multi-part investigation |

**Rule:** Do not exceed the category by more than 10%.

---

## 3) Required Header (All Activities)

```markdown
# [Activity Title]

**Type:** Worksheet / Discussion / Data-Driven / Demo-Driven
**Duration:** [Time category] ([X] minutes)
**Learning Objective:** [One sentence]
**Materials:** [List]
**Preparation:** [What instructor should prep or announce]
```

---

## 4) Worksheet Format

1) **Warmup** (2–3 min)
   - Low-stakes recall or prediction

2) **Core Problems** (main time)
   - Scaffolded sequence (easier → harder)
   - Clear instructions and checkpoints

3) **Synthesis Question** (3–5 min)
   - Explicitly connect to measurement → model → inference

4) **Extension (Optional)**
   - Mark clearly as optional

**Scaffolding principle:** The first problem should be solvable by 90% of students.

---

## 5) Discussion (TPS) Format

| Phase | Duration | What Happens |
| --- | --- | --- |
| **Think** | 1–2 min | Individual response |
| **Pair** | 2–3 min | Compare and reconcile |
| **Share** | 3–5 min | Whole-class synthesis |

**Prompt rules:**
- Multiple defensible answers
- Targets a common misconception
- Requires reasoning, not recall

---

## 6) Data-Driven Format

1) **Context** (what the data represent)
2) **Read** (identify axes, units, trends)
3) **Model** (connect to physics relation or scaling)
4) **Infer** (extract or compare physical quantities)
5) **Sanity check** (units, limiting cases, or expected scale)

---

## 7) Demo-Driven Touchpoints (Optional)

Demos live in cosmic-playground. If used, include a short reference block:

```yaml
demo: cosmic-playground/<demo-slug>
features-used:
  - [feature 1]
  - [feature 2]
```

**Rule:** A demo must support a reasoning goal. It cannot be used as entertainment.

---

## 8) Quality Checklist

- [ ] Learning objective is explicit and measurable
- [ ] Activity targets a misconception or reasoning tool
- [ ] Students must explain, not just compute
- [ ] Units are explicit in quantitative tasks
- [ ] A synthesis question connects to the course throughline

