# ASTR 201 Course Pedagogy Tools (Readings + Slides) — Spec + UX Contract

**Status:** Draft  
**Owner:** Anna (instructor)  
**Last updated:** 2026-02-10  

## 0) Problem Statement

ASTR 201 materials already include strong explanations, worked examples, and static “Quick Check” callouts. The next quality jump is to make active learning feel *structural* (not occasional): students should repeatedly (1) commit to predictions, (2) reason from assumptions, and (3) build multi-step inference chains that feel like doing astronomy.

This spec defines three reusable course-wide tools you can drop into *any* reading or slide deck:

1. **Mystery Star Dossiers** (case-based storyline)
2. **Predict -> Commit -> Reveal (PCR)** with confidence
3. **Assumption Cards** (model validity + failure modes)
4. **A/B Contrast Anchors** (discrimination practice)

These are content patterns (no new code required).

## 1) Prime Directive / Non-Negotiables

1. **Correctness first.** The tool must reduce misconception risk, not amplify it.
2. **Low authoring friction.** If it is annoying to write, it will not scale across the course.
3. **Retrieval practice is real.** Prompts must require a committed answer (not “read and nod”).
4. **Short + frequent beats.** Prefer many 30–90 second engagements over rare 10-minute ones.
5. **Accessible structure.** Clear headings, descriptive callout titles, no color-only meaning.
6. **Student-safe.** Any “answers” are either hidden/collapsed in readings or placed in instructor-only notes.

## 2) Scope

### In scope (v1)

- Standard templates for readings (`.qmd`) and slides (RevealJS)
- A consistency contract (naming, placement cadence, and minimal required fields)
- Instructor facilitation notes (optional)

### Out of scope (v1)

- Building new interactive widgets or extensions
- Grading or analytics
- Formal question banks

## 3) Shared Vocabulary (Course-Wide)

Across all three tools, maintain the same epistemic framing:

- **Observable:** a measured quantity (with units and measurement method)
- **Model:** assumptions that connect observables to a claim
- **Inference:** the derived quantity (and its uncertainty/limits)

If a tool instance does not explicitly name at least one of these, it is probably decorative.

## 4) Tool D: A/B Contrast Anchors

### 4.1 Purpose

Many ASTR 201 misconceptions come from *category confusion* (students collapsing two distinct quantities into one “brightness” idea, or treating a modeling assumption like a measured fact). A/B contrasts force discrimination: students must say what differs, what stays the same, and which measurement would break a degeneracy.

### 4.2 Cognitive Goal

- Improves conceptual precision (difference-making)
- Builds transfer: students reuse the same contrast in new contexts
- Reduces “plug-and-chug” by requiring qualitative reasoning first

### 4.3 Contract (Required Fields)

Each contrast anchor must include:

- **A vs B names:** the two things being contrasted
- **One invariant:** what stays the same between A and B (explicit)
- **One difference:** what changes between A and B (explicit)
- **One diagnostic:** what you would measure/observe to tell them apart (explicit)
- **One common wrong move:** a short misconception line (optional but recommended)

### 4.4 Recommended Cadence

- 2–4 contrasts per reading, placed:
  - immediately after defining a quantity
  - immediately before a worked example that uses it

Keep a “course canon” list and reuse the same contrasts repeatedly:

- flux vs luminosity
- received flux vs surface flux vs surface brightness (intensity)
- degrees vs radians vs arcseconds
- parallax angle $p$ vs full shift $2p$
- color vs temperature (and the role of reddening)
- blackbody idealization vs real stellar spectra (lines + continuum)

### 4.5 Reading Template (Quarto)

```markdown
::: {.callout-tip title="A/B Contrast Anchor: Flux vs. Luminosity"}
**A:** Flux $F$ (what we measure at Earth)  
**B:** Luminosity $L$ (what the star emits)

**Invariant:** The star’s intrinsic power output does not depend on where the observer stands (that’s $L$).  
**Difference:** Flux decreases with distance: $F \\propto 1/d^2$.

**Diagnostic:** If you only measure brightness (flux), you cannot infer $L$ without distance; measure parallax to get $d$.

**Common wrong move:** “A star looks dim, so it has low luminosity.”
:::
```

### 4.6 Slide Template (RevealJS)

- Put the A/B contrast on a single slide with a one-line “diagnostic measurement” prompt.
- For live engagement: have students vote on which measurement breaks the degeneracy, then reveal.

## 4) Tool A: Mystery Star Dossiers

### 4.1 Purpose

Make readings feel like *solving an astronomy problem* instead of consuming a chapter. Students track a small set of stars across multiple sections/lectures and repeatedly update what they know and what they can infer.

### 4.2 Cognitive Goal

- Reduces cognitive load by reusing familiar “characters”
- Builds transfer: students see the same inference chain in multiple contexts
- Encourages model-based thinking (what information breaks degeneracies)

### 4.3 Contract (Required Fields)

Each dossier instance must specify:

- **Star label:** `Star A`, `Star B`, etc. (or a named star if appropriate)
- **What we observed:** one or more observables (with units)
- **What we can infer now:** one inference (with equation reference)
- **What we cannot infer yet:** one explicit limitation (degeneracy / missing observable)
- **Next measurement:** what would break the degeneracy

### 4.4 Recommended Cadence

- 1–2 dossier stars per module (max 3)
- Dossier appears:
  - at the start (hook + baseline observables)
  - after each major equation/tool is introduced (update)
  - at the end (summary “final dossier”)

### 4.5 Reading Template (Quarto)

```markdown
::: {.callout-important title="Mystery Star Dossier: Star A"}
**What we observed (today):**
- Parallax: $p = 0.050''$
- Flux at Earth: $F = 2.0\\times10^{-11}\\ \\text{erg cm}^{-2}\\ \\text{s}^{-1}$

**What we can infer now:**
- Distance: $d(\\text{pc}) = 1/p('') = 20\\ \\text{pc}$
- Luminosity (preview): $L = 4\\pi d^2 F$ (needs $d$ in cm)

**What we cannot infer yet (be explicit):**
- Radius: we still need temperature (color) to use Stefan-Boltzmann.

**Next measurement to request:**
- Color index / spectrum peak to infer $T$ (Wien) and then $R$.
:::
```

Notes:

- Keep the dossier short enough to be re-read quickly.
- Use consistent units (course convention: CGS unless explicitly stated).

### 4.6 Slide Template (RevealJS)

- Put the dossier on a single slide that you revisit (“checkpoint slide”).
- Keep “answers” for computed values in speaker notes or a fragment reveal.

## 5) Tool B: Predict -> Commit -> Reveal (PCR) With Confidence

### 5.1 Purpose

Turn passive reading into active model testing by requiring a prediction *before* an explanation or derivation.

### 5.2 Cognitive Goal

- Generates desirable difficulty (retrieval)
- Surfaces misconceptions early
- Creates an affective “game loop” (commit, then find out)

### 5.3 Contract (Required Fields)

Each PCR beat must include:

- **Predict:** the prompt (1–2 sentences, specific)
- **Commit:** a forced choice or a numeric/scaling answer
- **Confidence:** low/medium/high (self-calibration)
- **Reveal:** the correct answer + one-sentence “why”

### 5.4 Recommended Cadence

- 2–5 PCR beats per lecture reading (depending on length)
- Place PCR beats immediately before:
  - a key derivation step
  - a common misconception trap
  - an “error propagation / scaling” moment

### 5.5 Reading Template (Quarto, no new extension)

```markdown
::: {.callout-tip title="Predict -> Commit -> Reveal"}
**Predict:** If distance doubles, what happens to received flux?

**Commit:** Choose one:
- (A) flux doubles
- (B) flux halves
- (C) flux becomes 1/4
- (D) flux stays the same

**Confidence:** low / medium / high

::: {.callout-note collapse="true" title="Reveal"}
**Answer:** (C). Inverse-square spreading gives $F \\propto 1/d^2$, so $F(2d) = F(d)/4$.
:::
:::
```

Authoring guidance:

- Keep the reveal short: one equation and one sentence.
- Write wrong choices to match real misconceptions (distance vs luminosity; linear vs square).

### 5.6 Slide Template (RevealJS)

- Use the existing quiz extension in slides when appropriate.
- If you use `.quiz`, the “confidence” step can be a quick show of hands or a 5-second pause.

## 6) Tool C: Assumption Cards (Model Validity + Failure Modes)

### 6.1 Purpose

Students should leave each lecture knowing not only *how* to compute, but *when the computation is valid* and how to detect violations observationally.

### 6.2 Cognitive Goal

- Builds scientific reasoning habits (“what would break this?”)
- Reduces brittle plug-and-chug behavior
- Prepares students for real astronomy where models are approximate

### 6.3 Contract (Required Fields)

Each assumption card must include:

- **Model statement:** the equation/relationship
- **Assumptions:** 2–4 bullets
- **Failure modes:** 1–3 bullets (realistic)
- **Diagnostic:** what you would measure/observe to detect the failure

### 6.4 Recommended Cadence

- One assumption card per “core equation”:
  - small-angle approximation
  - parallax distance
  - inverse-square law
  - Wien’s law (applied to stars)
  - Stefan-Boltzmann (effective temperature)

### 6.5 Reading Template (Quarto)

```markdown
::: {.callout-important title="Assumption Card: Inverse-Square Law"}
**Model:** $F = \\dfrac{L}{4\\pi d^2}$

**Assumptions (what must be true):**
- Emission is isotropic (no strong beaming).
- Absorption/scattering between star and us is negligible or corrected (extinction).
- We are measuring bolometric flux (or we apply a bolometric correction).

**Failure modes (what breaks it):**
- Dust reddening/extinction reduces observed flux and biases inferred $L$ low.
- Strong anisotropy (jets, pulsars) makes flux direction-dependent.

**How to diagnose:**
- Compare colors to expected intrinsic colors (reddening signatures).
- Measure multi-band photometry / spectra to estimate extinction and bolometric correction.
:::
```

Slide guidance:

- Put assumption cards right after the derivation, not at the end.
- Use a consistent visual treatment so students recognize “this is about validity.”

## 7) Consistency Rules (So It Scales)

1. Use the same titles across the course:
   - `Mystery Star Dossier: Star A`
   - `Predict -> Commit -> Reveal`
   - `Assumption Card: <model name>`
2. Keep each tool instance under ~12 lines in the source file.
3. Maintain unit explicitness (especially where students commonly confuse degrees/radians, pc/cm, flux/luminosity).
4. Every “Reveal” should contain at least one of:
   - a unit check
   - a scaling check
   - a misconception fix sentence

## 8) Suggested Rollout Plan

1. Pick one module as the “style anchor” (Module 2 is a good candidate).
2. Add:
   - 1 dossier star used in two consecutive readings
   - 3 PCR beats per reading
   - assumption cards for the two core equations in that reading
3. After teaching, do a quick audit:
   - Which prompts generated discussion?
   - Which misconceptions persisted?
   - Which tool instances were too long?
