# ASTR 201 Quick Check (HTML Readings) — Spec + UX Contract

**Status:** Draft  
**Owner:** Anna (instructor)  
**Last updated:** 2026-02-10  

## 0) Task Classification (per `docs/llm-lab-protocol.md`)

Dominant: **Architectural exploration** + **Pedagogy/UX contract** + **Documentation**.

## 1) Problem Statement

ASTR 201 readings (Quarto HTML pages) currently use static callouts like “Quick Check Yourself” with collapsible answers. This supports retrieval practice, but it does not provide the same interactive affordances as the existing RevealJS quiz plugin used in slides.

We want a reading-first interaction pattern that:

- encourages students to commit to an answer (retrieval practice)
- gives immediate feedback
- optionally reveals an explanation (and keeps it hidden by default)
- stays lightweight, accessible, and non-graded

Important constraint: the existing slide quiz uses `::: {.quiz}` and must remain available for RevealJS decks. The new reading tool must not collide with that.

## 2) Prime Directive / Non‑Negotiables

1. **Non-graded:** No grade export, no backend, no analytics required.
2. **No “answer leak” in the default reading view:** Correct choices must not visibly render as checked/marked before the student clicks “Check”.
3. **Accessible by default:** Keyboard navigable, screen-reader sensible, no color-only feedback.
4. **Format-gated:** Applies to HTML readings/pages, not RevealJS slides.
5. **Authoring is simple:** Works with Quarto Markdown; no hand-written HTML required.
6. **Graceful degradation:** If JS fails/disabled, students still have a usable experience (even if less interactive).

## 3) Scope

### In scope (v1)

- Single-choice and multi-select “quick check” questions in HTML pages
- Optional “Explanation” block embedded inside the question container
- Shuffle options (optional, default off)
- Retry/reset (optional, default on)
- Minimal styling consistent with the course site

### Out of scope (v1)

- Grading, scoring persistence, instructor dashboards
- Question banks, randomization from pools
- Math input, free-response autograding
- Preventing students from inspecting HTML/JS to discover answers (not a goal)

## 4) Naming + Authoring Contract

### 4.1 Name (avoid `.quiz` collision)

Use a new container class: `.quick-check`.

Rationale: `.quiz` is already reserved for RevealJS decks and is implemented as a `revealjs-plugins` extension.

### 4.2 Minimal authoring syntax (recommended)

```markdown
::: {.quick-check}
**Quick Check:** A star has parallax $p = 0.2''$. What is its distance?

- [5 pc]{.correct}
- [0.2 pc]
- [2 pc]
- [20 pc]

::: {.explanation}
Use $d(\text{pc}) = 1/p('')$, so $d = 1/0.2 = 5$ pc.
:::
:::
```

Rules:

- Exactly one option should have `{.correct}` for single-choice questions.
- Multiple `{.correct}` options are allowed for multi-select questions (see §4.4).
- The `.explanation` block is optional.

### 4.3 Alternate authoring syntax (supported for convenience)

Support task-list markers inside `.quick-check`:

```markdown
::: {.quick-check}
**Quick Check:** Which statements are true?

- [x] A 2× increase in distance makes flux 4× smaller.
- [x] Flux scales as $d^{-2}$ for isotropic emission.
- [ ] Flux is intrinsic to the star.

::: {.explanation}
Inverse-square spreading gives $F \propto 1/d^2$.
:::
:::
```

Contract:

- `[x]` indicates correct and must not render as a visible checked box in the HTML output.
- `[ ]` indicates incorrect and must not render as a visible unchecked box in the HTML output.

### 4.4 Multi-select vs single-choice

Two supported ways to declare multi-select:

1. Add a class:
   - `::: {.quick-check .multiple}`
2. Or add an attribute:
   - `::: {.quick-check kind="multiple"}`

Default is single-choice.

## 5) UX Contract (Student Experience)

### 5.1 Rendered widget (v1)

Each quick check renders as:

- a question stem
- a list of options as radio buttons (single) or checkboxes (multiple)
- actions:
  - `Check`
  - `Reset` (optional)
- feedback region:
  - short “Correct” / “Try again” message
  - optional explanation (collapsed by default; revealed after checking)

### 5.2 Feedback rules

- Before checking: no option is marked correct/incorrect.
- After checking:
  - correct options are visibly indicated (icon + text, not only color)
  - incorrect selected options are indicated
  - if an explanation is present, it becomes available (default: auto-expand after check)

### 5.3 Retry rules (default)

Default: allow retry.

- If the student is incorrect, keep their selections and allow another attempt.
- Provide a `Reset` control to clear selections.

Optional config (v2 or via config): “lock after check”.

### 5.4 Shuffling rules

Optional shuffle:

- If enabled, shuffle options on page load.
- Reset should not reshuffle (keeps the same order for local coherence).

## 6) Accessibility Contract

1. Use native form controls (`<input type="radio">`, `<input type="checkbox">`) for options.
2. Group options in a `<fieldset>` with a `<legend>` (the question stem).
3. Feedback is announced to screen readers via an `aria-live="polite"` region.
4. Focus management:
   - After “Check”, focus moves to feedback region (or remains on the button; TBD).
   - After “Reset”, focus moves back to the first option.
5. No color-only cues:
   - Use icons (e.g., checkmark / x) plus text labels like “Correct answer” / “Incorrect”.
6. Reduced motion:
   - Respect `prefers-reduced-motion`; no animated shakes/flashes.

## 7) Degradation (No JS / JS Failure)

Goal: remain usable for retrieval practice without leaking the answer by default.

Recommended fallback behavior:

- Render a static question and options, but no “correct” highlighting.
- Render the explanation as a collapsed `<details>` block titled “Explanation” (only if an explanation exists).

If the author used `[x]` syntax, the filter must still remove visible checked boxes even in no-JS mode.

## 8) Architecture Proposal (Implementation, not in this doc’s scope)

### Approach (recommended): Pandoc Lua filter + bundled JS/CSS

- A Pandoc Lua filter transforms `Div` blocks with class `quick-check` into a stable HTML structure.
- The filter injects a Quarto HTML dependency for JS/CSS, following the established pattern used by `_extensions/EmilHvitfeldt/roughnotation/rough.lua`.

### Format gating

The filter must run only for HTML outputs and must not affect RevealJS:

- Run for: `html`, `html:js` (Quarto site pages, readings)
- Do not run for: `revealjs`

### Data model / “answer secrecy”

Store correctness in non-visible metadata (e.g., `data-correct="true"` on option wrappers).

This prevents accidental “answer leak” in the rendered view. It does not attempt to prevent deliberate inspection.

## 9) Stable DOM Contract (for JS/CSS)

Suggested DOM (illustrative):

```html
<div class="quick-check" data-qc-kind="single">
  <form class="qc-form">
    <fieldset>
      <legend class="qc-stem">...</legend>
      <div class="qc-options">
        <label class="qc-option" data-correct="true">
          <input type="radio" name="qc-123" />
          <span class="qc-option-text">5 pc</span>
        </label>
      </div>
    </fieldset>
    <div class="qc-actions">
      <button type="button" class="qc-check">Check</button>
      <button type="button" class="qc-reset">Reset</button>
    </div>
    <div class="qc-feedback" aria-live="polite"></div>
    <div class="qc-explanation" hidden>...</div>
  </form>
</div>
```

JS should rely only on these class hooks, not on brittle Pandoc-generated markup.

## 10) Configuration Surface (YAML)

Proposed Quarto config:

```yaml
quick-check:
  shuffleOptions: false
  allowRetry: true
  lockAfterCheck: false
  revealExplanationOnCheck: true
  showReset: true
```

Per-question overrides can be via attributes:

- `shuffle="true"`
- `allow-retry="false"`
- `lock-after-check="true"`

## 11) Testing Plan (HTML-only)

1. Create a tiny fixture page with:
   - single-choice question
   - multi-select question
   - explanation block
   - math in stem and options
2. Render with `quarto render`.
3. Manual checks:
   - keyboard-only path works
   - screen reader announces feedback (spot-check)
   - correct answers are not visually pre-marked
   - JS-disabled fallback does not show checked boxes for `[x]`

## 12) Pedagogical Guidance (How to Use Well)

This tool is for retrieval practice, not trick questions.

- Put quick checks immediately after the concept they test.
- Keep stems short and specific.
- Wrong options should reflect common misconceptions (one per question is usually enough).
- Explanations should be:
  - brief (2–5 sentences)
  - causal (“why this is right / why the tempting wrong choice fails”)
  - unit- and scaling-aware (especially in ASTR 201)

## 13) Future Extensions (v2+ ideas)

- Per-option explanations (attach to each option, shown after check)
- “Confidence” selector (low/medium/high) before checking
- Spaced repetition hints (link back to the section that answers it)
- Lightweight progress indicator (localStorage only; no grades)

