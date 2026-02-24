# Session Prompt: Convert Lecture Reading → Quarto RevealJS Slides

**Paste this at the start of a new Claude Code session.**

---

## Task

Convert the lecture reading `modules/module-NN/readings/lecture-NN-<topic>-reading.qmd` into a Quarto RevealJS slide deck at `modules/module-NN/slides/lecture-NN-<topic>.qmd`.

## Ground Rules (Non-Negotiable)

### Content Quality
- **Slides are study material, not decoration.** Students study from these. Every slide must contain enough information that a student reviewing it later can reconstruct the idea — no vague one-liners or mysterious bullet fragments.
- **One idea per slide.** If a slide answers two questions, split it.
- **Show equations with scaffolding.** Every equation slide needs: the equation, what the symbols mean, what it predicts, and at least one scaling/limiting case. Use the equation system (`{{< include ... >}}` + `{{< eqrefcard ... >}}`).
- **No fabricated numbers.** All values come from the reading. If a number isn't in the reading, use order-of-magnitude or mark VERIFY.
- **CGS units always.** Solar units for stellar quantities. Never SI (meters, kg, Joules).

### Overflow Prevention (CRITICAL)
- **Word budget: ≤ 35 words of prose per slide** (equations, figure captions, and speaker notes don't count toward this).
- **Never put a wall of text on a slide.** If you need more context, put it in speaker notes (`::: {.notes}`).
- **Test mental rendering:** Before writing a slide, ask yourself: "Will this overflow on a 16:9 projector?" If the answer is "maybe," split or trim.
- **Use `.smaller` in YAML frontmatter** (all existing decks use `smaller: true`).
- **Long equations:** If an equation is wider than ~60 characters, break it across lines with `\begin{aligned}`.
- **Tables:** Keep to 3–4 columns max. Use `.text-sm` class if needed.
- **Lists:** Max 5–6 items. If longer, use `.incremental` and split across slides.
- **Two-column layouts** (`:::: {.columns}`) are your friend for image+text slides — use `width="55%"` / `width="45%"` splits.

### Quiz Extension (Exact Syntax)
The quiz extension uses a specific format. Get it exactly right:

```markdown
## Quiz Title {background-color="#1a1a2e"}

::: {.quiz}
Clear, specific question stem — not vague.

- [ ] Wrong answer A (with plausible reasoning in parentheses)
- [x] Correct answer (with brief explanation)
- [ ] Wrong answer B (targeting a specific misconception)
- [ ] Wrong answer C (another common error)
:::

::: {.notes}
Timing: ~1 min. Give 20–30 seconds to think. Then discuss.
Common misconception: [what students get wrong and why].
:::
```

**Quiz rules:**
- Use `- [x]` for the correct answer, `- [ ]` for wrong answers
- Always 4 options
- Each wrong answer should target a **specific misconception** (not random nonsense)
- Include brief parenthetical reasoning with each option so students learn from wrong answers too
- The question stem must be **specific and testable** — not "Which of these is important?"
- Place quizzes after every major concept (roughly every 10–15 slides)
- Quiz slides get `{background-color="#1a1a2e"}` for visual distinction

### Progressive Disclosure
- **Fragments:** Use `:::{.fragment}` or `. . .` (pause) to reveal content step-by-step
- **Incremental lists:** Wrap with `::: {.incremental}` for bullet-by-bullet reveal
- **Equations:** Show the equation first, then reveal the interpretation/scaling on click
- **Worked examples:** Setup → pause → solve → pause → interpret (never show all at once)
- **Pattern:** Setup → Predict → Reveal is the default for quantitative ideas

### Speaker Notes (Every Slide)
Every slide must have `::: {.notes}` containing:
- **Timing estimate** (e.g., "2–3 min")
- **What to say** — the narrative connecting to the next slide
- **What to emphasize** — point to specific parts of figures/equations
- **Misconceptions** to address (if relevant)
- **Teaching moves** — "think-pair-share", "ask for predictions", etc.

## Required Structure

### YAML Frontmatter (Copy Exactly)
```yaml
---
title: "Lecture N: Title"
subtitle: "Subtitle"
author: "Dr. Anna Rosen"
date: "YYYY-MM-DD"
description: "One-line description for listings."
draft: true

format:
  revealjs:
    theme: [default, ../../../assets/theme/slides/theme.scss]
    smaller: true
    slide-number: true
    transition: fade
    transition-speed: fast
    background-transition: fade
    center: false
    footer: "ASTR 201 • Module N, Lecture N"
    chalkboard: true
    code-line-numbers: true
    fig-align: center
    html-math-method: mathjax
    pointer:
      color: "#dc2626"
      pointerSize: 18
    spotlight:
      size: 80
      fadeInAndOut: 150
      toggleSpotlightOnMouseDown: true
      initialPresentationMode: false
    quiz:
      shuffleOptions: true
      defaultCorrect: "✓ Correct!"
      defaultIncorrect: "✗ Not quite—let's discuss."

revealjs-plugins:
  - pointer
  - spotlight
  - attribution
  - quiz

filters:
  - roughnotation

execute:
  echo: false
  warning: false
  message: false
---
```

### Deck Skeleton (Mandatory Sections)

1. **Learning Objectives** — `.incremental` list, 4–6 objectives
2. **Hook slide** — Background image or provocative question that creates curiosity
3. **O→M→I Framework slide** — Mermaid diagram + table showing Observable/Model/Inference for this lecture
4. **Content sections** — One `## {.center}` section divider per major part of the reading, then content slides
5. **Quiz slides** — At least one per major concept section (minimum 3 per deck)
6. **Worked example** — At least one step-by-step calculation with progressive reveal
7. **Summary / Key Takeaways** — `.incremental` list
8. **Looking Ahead** — Preview of next lecture + reading assignment

### Slide Type Patterns

**Equation slide:**
```markdown
## Equation Title

{{< include ../../../_includes/equations/name.qmd >}}

. . .

{{< eqrefcard name >}}

::: {.notes}
Timing. Unpack each symbol. Point to the scaling. Ask: "what happens if we double X?"
:::
```

**Figure slide:**
```markdown
## Slide Title

{{< img figure-id width="90%" >}}

::: {.notes}
What to point to. What pattern to notice. What question to ask students.
:::
```

**Two-column (image + text):**
```markdown
## Slide Title

:::: {.columns}
::: {.column width="55%"}
{{< img figure-id width="100%" >}}
:::

::: {.column width="45%"}
Key points about the figure:

::: {.incremental}
- Point 1
- Point 2
- Point 3
:::
:::
::::
```

**Section divider:**
```markdown
## {.center}

::: {.r-fit-text}
Section Title
:::

*One-line tagline*
```

**Prediction prompt:**
```markdown
## Predict First {background-color="#1a1a2e"}

:::: {.columns}
::: {.column width="60%"}
**Setup:** [Scenario description]

**Question:** [Specific, testable prediction]
:::

::: {.column width="40%"}
*Take 30 seconds. Commit to an answer before we continue.*
:::
::::
```

## Shortcode Reference

| Shortcode | Use in slides | Purpose |
|-----------|--------------|---------|
| `{{< img id >}}` | Yes | Image without caption (for slides) |
| `{{< img id width="X%" >}}` | Yes | Image with size control |
| `{{< fig id >}}` | **No** (readings only) | Image with caption |
| `{{< media id >}}` | Yes | Video/embed with credit (registered in `assets/media.yml`) |
| `{{< include path >}}` | Yes | Include equation LaTeX from `_includes/equations/` |
| `{{< eqrefcard id >}}` | Yes | Equation meaning card |
| `{{< eqshow id >}}` | Yes | Title + equation + meaning in one call |

## Layout Classes Available

| Class | Effect |
|-------|--------|
| `.layout-2col` | Equal 2-column grid |
| `.layout-2col-40-60` | 40/60 weighted columns |
| `.layout-2col-60-40` | 60/40 weighted columns |
| `.layout-grid-2` | 2-item grid |
| `.layout-grid-3` | 3-item grid |
| `.layout-hero` | Image + caption below |
| `.layout-triad` | Three-column with borders |
| `.text-sm` | Smaller text |
| `.text-lg` | Larger text |
| `.text-center` | Center-aligned |
| `.text-muted` | De-emphasized color |
| `.mt-2` | Margin-top spacing |
| `.r-fit-text` | Auto-scale to fill |

## RoughNotation (Animated Highlights)

```markdown
[**key term**]{.rn rn-type="underline" rn-color="#ff6b6b"}
[**important**]{.rn rn-type="box" rn-color="#4ecdc4"}
```

Types: `underline`, `box`, `circle`, `highlight`, `strike-through`, `bracket`

## Process

1. **Read the full reading first** — understand the narrative arc, key equations, figures, and "Check Yourself" questions
2. **Identify the 4–6 major concept chunks** — these become your section dividers
3. **Map reading content to slide types** — equations get equation slides, figures get figure slides, "Check Yourself" questions become quizzes, worked examples become step-by-step reveals
4. **Write slides section by section** — don't skip ahead
5. **Write speaker notes for every slide** — these carry the lecture narrative
6. **Add quizzes after each major section** — adapt "Check Yourself" and "Think First" prompts from the reading
7. **Verify:** `quarto render` must succeed with no errors

## What NOT to Do

- ❌ Vague slides ("Stars are interesting" — says nothing a student can study from)
- ❌ Walls of text (if you're pasting a paragraph, it belongs in speaker notes)
- ❌ Equations without interpretation (showing $L \propto M^{3.5}$ without saying what it means)
- ❌ Quizzes with joke wrong answers (every option must target a real misconception)
- ❌ Missing speaker notes (every slide needs them — timing + narrative + teaching moves)
- ❌ Skipping the reading's key content (slides must cover all major ideas from the reading)
- ❌ Using `{{< fig >}}` in slides (use `{{< img >}}` instead — no captions in slides)
- ❌ Forgetting `smaller: true` in YAML (causes overflow on most content-heavy slides)
- ❌ Quiz syntax errors (`[x]` without the space → won't render; must be `- [x]`)

## Files to Read Before Starting

1. The reading you're converting (the source material)
2. `assets/templates/slides-template.qmd` (canonical template — copy YAML from here)
3. `docs/contracts/quarto-reveal-lecture-slides-playbook.md` (the playbook)
4. `data/equations.yml` + `data/eqcards.yml` (equation registry — know which equations exist)
5. `assets/figures.yml` (figure registry — know which figures are available)
6. One existing slide deck for voice/style calibration (e.g., `modules/module-02/slides/lecture-01-distance-and-parallax.qmd`)
