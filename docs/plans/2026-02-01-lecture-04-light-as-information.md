# Lecture 4: Light as Information — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create slides and reading companion for Week 3's "Light as Information" lecture covering EM spectrum, blackbody radiation, and Wien's law.

**Architecture:** Two Quarto files following existing templates. Slides use RevealJS with pointer/spotlight/quiz extensions. Reading is a comprehensive companion with worked examples, "Check Yourself" questions, and collapsible solutions. Both use the figure registry (`assets/figures.yml`) for images.

**Tech Stack:** Quarto, RevealJS, MathJax, YAML figure registry, `{{< fig >}}` shortcode

---

## Pre-Implementation: Figure Registry Updates

### Task 0: Register Required Figures ✅ COMPLETED

**Status:** 17 figures registered in `assets/figures.yml` under "Lecture 04: Light as Information"

**Available figures (use these shortcode IDs):**

| Shortcode ID | Description | Use In |
|--------------|-------------|--------|
| `em-wave-diagram` | EM wave with E and B fields | Reading: What is light |
| `mechanical-vs-em-wave` | Mechanical vs EM wave comparison | Reading: Wave basics |
| `em-spectrum-bands` | Full EM spectrum with wavelength scale | Slides + Reading |
| `em-spectrum-astro-objects` | EM spectrum with astronomical sources | Optional spoiler |
| `wavelength-energy-relation` | λ vs energy visual | Slides: photon energy |
| `prism-dispersion` | Prism separating light | Reading: dispersion |
| `blackbody-stellar-spectra` | Planck curves for 3 star temps | **Main blackbody figure** |
| `continuous-vs-line-spectrum` | Sun vs fluorescent bulb | Reading: spectrum types |
| `three-types-of-spectra` | Continuous/absorption/emission | Preview for spectroscopy |
| `light-matter-behaviors` | 5 behaviors of light | Reading: blackbody definition |
| `absorption-emission-elements` | Element spectral fingerprints | Preview for spectroscopy |
| `hydrogen-absorption` | H absorption with energy levels | Preview for spectroscopy |
| `hydrogen-emission` | H emission with energy levels | Preview for spectroscopy |
| `altair-spectrum-annotated` | Real stellar spectrum | Reading: synthesis |
| `doppler-shift-exoplanet` | Doppler shift diagram | Preview for Week 6 |
| `betelgeuse-size` | Betelgeuse with solar system overlay | Wien's law examples |
| `earth-reflectance-spectra` | Surface material spectra | Optional: biosignatures preview |

**Still needed (placeholders):**

| Need | Description | Source suggestion |
|------|-------------|-------------------|
| `cmb-spectrum-planck` | CMB blackbody fit from Planck satellite | ESA/Planck public data |
| UV catastrophe diagram | Rayleigh-Jeans vs Planck comparison | Create or find open-source |

**Note:** The `blackbody-stellar-spectra` figure (from JWST education) shows 3000 K, 5000 K, and 8000 K stars with Wien's law clearly illustrated—this is the primary blackbody figure for both slides and reading.

---

## Task 1: Create Lecture 4 Slides

**Files:**
- Create: `modules/module-01/slides/lecture-04-light-as-information.qmd`
- Reference: `assets/templates/slides-template.qmd`

**Step 1: Create slides file from template**

```bash
cp assets/templates/slides-template.qmd modules/module-01/slides/lecture-04-light-as-information.qmd
```

**Step 2: Replace YAML frontmatter**

Replace the entire YAML block with:

```yaml
---
title: "Lecture 4:<br> Light as Information"
subtitle: "How Photons Encode the Universe"
author: "Dr. Anna Rosen"
date: "2026-02-03"
description: "Everything we know about the cosmos comes from light. By understanding how light behaves—how it's emitted and what wavelengths dominate—we can infer temperature without ever touching a star."
draft: false
format:
  revealjs:
    theme: [default, ../../../assets/theme/slides/theme.scss]
    title-slide-attributes:
      data-background-image: "/assets/images/common/cosmic-cliffs-jwst.png"
      data-background-opacity: "0.20"
    smaller: true
    slide-number: true
    transition: fade
    transition-speed: fast
    background-transition: fade
    center: false
    footer: "ASTR 201 • Dr. Anna Rosen • Lecture 4"
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

**Step 3: Write Learning Objectives slide**

```markdown
## Learning Objectives

By the end of this lecture, you will be able to:

::: {.incremental .text-md}
- Describe the electromagnetic spectrum and relate wavelength, frequency, and photon energy
- Explain what a blackbody is and interpret the Planck spectrum qualitatively
- Identify limiting cases of the Planck function (Rayleigh-Jeans, Wien tail)
- Use Wien's law to estimate temperature from peak wavelength
:::

::: {.notes}
Read these aloud. Emphasize: by end of today, you can look at star color → estimate temperature.
Timing: ~2 min.
:::
```

**Step 4: Write Opening Hook**

```markdown
---

## {background-image="/assets/images/common/noirlab-nightsky-mosaic.jpg" background-opacity="0.2"}

::: {.r-fit-text}
Why are some stars red and some blue?
:::

::: {.notes}
Hook: Let this sit for 5 seconds. The answer involves quantum mechanics, temperature, and the birth of modern physics.
:::

---

## The Spoiler

By the end of today, you'll be able to:

. . .

Look at a star's **color** → estimate its **surface temperature** to within a few hundred Kelvin.

. . .

By the end of this course, you'll derive its mass, radius, age, and eventual fate.

. . .

**All from light.**

::: {.notes}
Set up the payoff. Color encodes temperature. This is the first inference tool in our toolkit.
:::
```

**Step 5: Write Part 1 — EM Spectrum (~6 slides)**

```markdown
---

## {.center}

::: {.r-fit-text}
Part 1: The Electromagnetic Spectrum
:::

*Light as a Messenger*

---

## What Is Light?

Light is an **electromagnetic wave** — oscillating electric and magnetic fields traveling through space.

. . .

Three ways to characterize it:

::: {.incremental}
- **Wavelength** ($\lambda$): distance between wave crests (meters, nm, Å)
- **Frequency** ($\nu$): oscillations per second (Hz)
- **Speed** ($c$): $c = \lambda \nu = 3 \times 10^8$ m/s in vacuum
:::

::: {.notes}
~3 min. Emphasize: wavelength and frequency are inversely related. If you know one + c, you know the other.
:::

---

## The Electromagnetic Spectrum

{{< fig em-spectrum-bands >}}

::: {.fragment}
Different wavelengths = different physics revealed.
:::

::: {.notes}
Point out: radio sees cold gas, X-rays see million-degree plasma. The universe looks different depending on which "eyes" you use.
:::

---

## Spoiler: Multi-Wavelength Astronomy

{{< fig jwst-vs-hst-ngc1566 >}}

. . .

Same galaxy. Different wavelengths. Different story.

::: {.notes}
Callback to Lecture 1. We'll understand WHY each wavelength shows different structure.
:::

---

## Photon Energy

Light also behaves as particles — **photons**.

Each photon carries energy:

$$E = h\nu = \frac{hc}{\lambda}$$

::: {.fragment}
where $h = 6.63 \times 10^{-34}$ J·s is **Planck's constant**.
:::

. . .

::: {.fragment .highlight-red}
**Key insight:** Short wavelength = high energy. This is why gamma rays are dangerous and radio waves aren't.
:::

::: {.notes}
~3 min. This equation will matter when we discuss why atoms absorb specific colors — that's spectroscopy in a few weeks.
:::

---

## Concept Check

::: {.quiz}
A photon with wavelength 500 nm has ______ energy than a photon with wavelength 1000 nm.

- [x] More (2× more)
- [ ] Less (half as much)
- [ ] The same
- [ ] Cannot determine
:::

::: {.notes}
E ∝ 1/λ. Half the wavelength = double the energy.
:::
```

**Step 6: Write Part 2 — Blackbody Radiation (~8 slides)**

```markdown
---

## {.center}

::: {.r-fit-text}
Part 2: Blackbody Radiation
:::

*Thermal Emission and the Birth of Quantum Mechanics*

---

## What Is a Blackbody?

A **blackbody** is an idealized object that:

::: {.incremental}
- Absorbs all light that hits it (no reflection)
- Re-emits radiation based *only* on its temperature
- Emits at all wavelengths, but not equally
:::

. . .

::: {.fragment .highlight-red}
**Why it matters:** Stars are approximately blackbodies. Understanding ideal blackbodies lets us estimate real stellar temperatures.
:::

::: {.notes}
~3 min. "Blackbody" means perfect absorber, not that it looks black — hot blackbodies glow!
:::

---

## The Planck Spectrum — Qualitative

{{< fig blackbody-stellar-spectra >}}

::: {.fragment}
Notice two things:
:::

::: {.incremental}
- The **peak shifts left** (bluer) as temperature increases
- The **whole curve rises** (more total energy) as temperature increases
:::

::: {.notes}
~3 min. This is the qualitative picture. We'll make it quantitative with Wien's law.
:::

---

## The Ultraviolet Catastrophe

Before quantum mechanics, classical physics predicted:

. . .

<!-- TODO: Need UV catastrophe figure showing Rayleigh-Jeans vs Planck -->

. . .

**Rayleigh-Jeans law:** Intensity $\propto T/\lambda^4$ at all wavelengths.

::: {.fragment .highlight-red}
**Problem:** This predicts infinite energy at short wavelengths. Ovens don't emit infinite UV!
:::

::: {.notes}
~3 min. This was a crisis. Classical physics was fundamentally wrong about thermal radiation.
:::

---

## Planck's Solution (1900)

Max Planck proposed: energy comes in discrete packets (**quanta**).

$$E = h\nu$$

. . .

This suppresses high-frequency emission — you can't emit a fraction of a photon.

. . .

::: {.fragment .highlight-red}
**"An act of desperation."** — Planck

This was the birth of quantum mechanics.
:::

::: {.notes}
~2 min. Planck didn't fully believe his own solution. It took Einstein (1905) to take quanta seriously.
:::

---

## The Planck Function — Meeting a Real Equation

$$B_\lambda(T) = \frac{2hc^2}{\lambda^5} \frac{1}{e^{hc/\lambda k_B T} - 1}$$

. . .

**Don't panic.** Let's unpack it:

::: {.incremental}
- $B_\lambda$ = intensity at wavelength $\lambda$
- The $\lambda^5$ in denominator: shorter wavelengths *could* dominate...
- But the exponential **suppresses** short wavelengths when $hc/\lambda \gg k_B T$
:::

::: {.notes}
~5 min. Go slow. The goal is comfort, not mastery. They'll see equations like this throughout their career.
:::

---

## Limiting Cases — The Key to Not Being Intimidated

| Regime | Condition | Behavior | Name |
|--------|-----------|----------|------|
| Long $\lambda$ | $hc/\lambda \ll k_B T$ | $B_\lambda \propto T/\lambda^4$ | Rayleigh-Jeans |
| Short $\lambda$ | $hc/\lambda \gg k_B T$ | $B_\lambda \to 0$ (exponential cutoff) | Wien tail |

. . .

::: {.fragment .highlight-red}
**The skill:** Complex equations reduce to simple behavior at extremes. Learn the limits.
:::

::: {.notes}
~3 min. This is the takeaway for the Planck function. Know the limiting cases.
:::

---

## Pause & Predict

**Question:** Why doesn't the Rayleigh-Jeans law (classical physics) apply at short wavelengths?

. . .

**Answer:** At short wavelengths, $hc/\lambda > k_B T$, meaning the photon energy exceeds the thermal energy available. You can't emit a photon you can't afford.

::: {.notes}
Test understanding of the QM argument.
:::
```

**Step 7: Write Part 3 — Wien's Law (~6 slides)**

```markdown
---

## {.center}

::: {.r-fit-text}
Part 3: Wien's Law
:::

*Color Tells Temperature*

---

## Wien's Displacement Law

The Planck function peaks at a wavelength that depends only on temperature:

$$\lambda_{\text{peak}} = \frac{b}{T} = \frac{2.898 \times 10^{-3}\ \text{m·K}}{T}$$

. . .

Or equivalently:

$$\lambda_{\text{peak}} \cdot T = 2.898 \times 10^{-3}\ \text{m·K}$$

. . .

::: {.fragment .highlight-red}
**Physical meaning:** Hotter → bluer. Cooler → redder. This is *why* color encodes temperature.
:::

::: {.notes}
~3 min. This is the key inference tool. Memorize the constant (or know where to find it).
:::

---

## Optional Deep Dive: Where Does Wien's Law Come From?

Wien's law comes from finding where $dB_\lambda/d\lambda = 0$.

. . .

This requires calculus (product rule + chain rule on the Planck function).

. . .

The result: $hc/\lambda_{\text{peak}} \approx 4.97\, k_B T$

. . .

::: {.fragment}
**Preview:** This is why calculus matters — it lets you extract key physics from complex equations.
:::

::: {.notes}
~2 min. Optional depth for the curious. Most students can skip to the result.
:::

---

## Worked Example: The Sun

The Sun's spectrum peaks at $\lambda_{\text{peak}} \approx 500$ nm (green-yellow light).

. . .

Solve for temperature:

$$T = \frac{b}{\lambda_{\text{peak}}} = \frac{2.898 \times 10^{-3}\ \text{m·K}}{500 \times 10^{-9}\ \text{m}}$$

. . .

$$T = 5800\ \text{K}$$

. . .

::: {.fragment .highlight-red}
We just measured the Sun's surface temperature using only the color of sunlight!
:::

::: {.notes}
~3 min. Walk through the calculation. Emphasize: this is inference from observation.
:::

---

## Hot vs Cool Stars

{{< fig betelgeuse-size >}}

| Star | Color | $\lambda_{\text{peak}}$ | Temperature |
|------|-------|-------------------------|-------------|
| Betelgeuse | Red | ~830 nm | ~3500 K |
| Sun | Yellow | ~500 nm | ~5800 K |
| Rigel | Blue-white | ~240 nm | ~12000 K |

::: {.notes}
~3 min. The range of stellar temperatures spans a factor of ~30.
:::

---

## Concept Check

::: {.quiz}
Rigel's peak wavelength is in the UV (~240 nm). Why does it look blue-white to our eyes, not invisible?

- [ ] Our eyes are sensitive to UV
- [x] The Planck curve is broad — Rigel emits plenty of visible light, just more blue than red
- [ ] Rigel is not actually a blackbody
- [ ] Atmospheric scattering shifts UV to visible
:::

::: {.notes}
Common misconception: peak = only emission. The Planck curve is broad!
:::

---

## Spoiler: The Cosmic Microwave Background

{{< fig cmb-map >}}

. . .

Peak wavelength: $\lambda_{\text{peak}} \approx 1.1$ mm (microwaves)

. . .

$$T = \frac{b}{\lambda_{\text{peak}}} = \frac{2.898 \times 10^{-3}}{1.1 \times 10^{-3}} = 2.7\ \text{K}$$

. . .

::: {.fragment .highlight-red}
This is the afterglow of the Big Bang — the oldest light in the universe. We'll return to this in cosmology (Module 4).
:::

::: {.notes}
~3 min. Cosmology spoiler. Plant the seed for Module 4.
:::
```

**Step 8: Write Synthesis and Closing (~4 slides)**

```markdown
---

## {.center}

::: {.r-fit-text}
Part 4: Synthesis
:::

*Observable → Model → Inference*

---

## The Inference Chain

| We Measure | We Use | We Infer |
|------------|--------|----------|
| Color / peak wavelength | Wien's law | Surface temperature |
| Spectrum shape | Planck function | Confirmation of thermal emission |

. . .

**Coming in Module 2:**

| We Measure | We Use | We Infer |
|------------|--------|----------|
| Apparent brightness (flux) | Inverse square law | Luminosity (if we know distance) |
| Temperature + Luminosity | Stefan-Boltzmann | Radius |

::: {.notes}
~3 min. Preview the tools we'll build. Each week adds more inference capability.
:::

---

## Summary: Key Takeaways

::: {.incremental}
1. **Light is a messenger** — wavelength, frequency, and photon energy encode physical information
2. **Blackbodies emit thermal radiation** — the Planck spectrum depends only on temperature
3. **Wien's law: $\lambda_{\text{peak}} = b/T$** — color directly encodes temperature
4. **Limiting cases tame complex equations** — Rayleigh-Jeans at long λ, Wien tail at short λ
:::

---

## The Takeaway {.center}

If you forget everything else from today, remember this:

::: {.fragment .fade-up}
::: {.r-fit-text}
**Color tells temperature.**
:::
:::

::: {.fragment .mt-2}
Wien's law lets you convert what you see into what you know.
:::

::: {.notes}
This is the core message. Make it memorable.
:::

---

## Looking Ahead

**Next time (Week 4):** Distance — how do we measure how far away stars are?

- Parallax, angular size, solid angle
- Inverse square law: flux ↔ luminosity ↔ distance
- Magnitudes and the distance modulus

**Before then:**

- Read: FoA Ch 2 (pp. 11–16) on distance measurement
- Review: Wien's law worked examples in the reading

::: {.notes}
Connect to Week 4. The inverse square law completes the inference toolkit foundation.
:::
```

**Step 9: Verify slides render**

```bash
quarto preview modules/module-01/slides/lecture-04-light-as-information.qmd
```

Expected: Slides render without errors, navigation works, math displays correctly.

**Step 10: Commit slides**

```bash
git add modules/module-01/slides/lecture-04-light-as-information.qmd
git commit -m "feat(module-01): add Lecture 4 slides - Light as Information

- EM spectrum overview with photon energy (E = hν)
- Blackbody radiation and Planck function with limiting cases
- Wien's law with worked examples (Sun, stars, CMB)
- Spoilers connecting to Module 2 (flux) and Module 4 (cosmology)"
```

---

## Task 2: Create Lecture 4 Reading Companion

**Files:**
- Create: `modules/module-01/readings/lecture-04-light-as-information.qmd`
- Reference: `assets/templates/reading-template.qmd`

**Step 1: Create reading file from template**

```bash
cp assets/templates/reading-template.qmd modules/module-01/readings/lecture-04-light-as-information.qmd
```

**Step 2: Replace YAML frontmatter**

```yaml
---
title: "Light as Information"
subtitle: "How Photons Encode the Universe"
author: "Dr. Anna Rosen"
date: "2026-02-03"
description: "Everything we know about the cosmos comes from light. By understanding how light behaves—how it's emitted and what wavelengths dominate—we can infer temperature without ever touching a star."
draft: false
categories: [light, blackbody, thermal-radiation]
course: ASTR 201
module: "1 - Foundations"

learning-objectives:
  - Describe the electromagnetic spectrum and relate wavelength, frequency, and photon energy
  - Explain what a blackbody is and interpret the Planck spectrum qualitatively
  - Identify limiting cases of the Planck function (Rayleigh-Jeans, Wien tail)
  - Use Wien's law to estimate temperature from peak wavelength

concept-throughline:
  - Light is a messenger that carries encoded physics
  - Blackbody radiation connects temperature to observable color
  - Limiting cases make complex equations tractable
  - This is the foundation for all light-based astronomical inference

math-level: symbolic_with_interpretation
mode: Draft
prerequisites: Basic algebra, scientific notation, familiarity with wavelength/frequency from physics
---
```

**Step 3: Write Opening Section**

```markdown
::: {.callout-important}
## The Big Idea

**Light is a messenger that carries encoded physics.** By understanding how objects emit and absorb light, we can infer their properties — starting with temperature — without ever visiting them.
:::

## Why Light Matters

Look up on a clear night. Every point of light you see is a message from across space and time. But what does that message contain?

In Lecture 1, we learned that astronomers can directly measure only four things: **brightness, position, wavelength, and timing**. Everything else — temperature, mass, radius, age, composition — must be *inferred*. Today we begin building the inference toolkit, starting with the question: **what can we learn from a star's color?**

The answer turns out to involve one of the most important developments in physics: the birth of quantum mechanics. Max Planck's attempt to explain how hot objects glow led to a revolution that reshaped our understanding of the universe. And the equation he derived — the Planck function — remains the foundation of stellar astrophysics.

### What You'll Learn

By the end of this reading, you'll be able to look at a star and estimate its surface temperature from its color. You'll understand why hot stars are blue and cool stars are red. And you'll have your first encounter with a professional-grade physics equation — the Planck function — along with strategies for making such equations less intimidating.

---
```

**Step 4: Write Part 1 — The Electromagnetic Spectrum**

```markdown
## Part 1: The Electromagnetic Spectrum

### Light as a Wave

Light is an electromagnetic wave — oscillating electric and magnetic fields that propagate through space at a constant speed. Three quantities characterize any wave:

**Wavelength ($\lambda$):** The distance between successive wave crests, typically measured in meters, nanometers (nm = $10^{-9}$ m), or Ångströms (Å = $10^{-10}$ m).

**Frequency ($\nu$):** The number of oscillations per second, measured in Hertz (Hz = s$^{-1}$).

**Speed ($c$):** In vacuum, all electromagnetic waves travel at $c = 3 \times 10^8$ m/s — the speed of light.

These three quantities are related by:

$$c = \lambda \nu$$

This means if you know any two, you can calculate the third. Since $c$ is constant, wavelength and frequency are inversely related: long wavelength means low frequency, short wavelength means high frequency.

### The Spectrum: Radio to Gamma

The electromagnetic spectrum spans an enormous range of wavelengths, from radio waves kilometers long to gamma rays smaller than atomic nuclei. We divide this spectrum into named bands:

| Band | Wavelength Range | What It Reveals |
|------|------------------|-----------------|
| Radio | > 1 mm | Cold gas, magnetic fields, pulsars |
| Microwave | 1 mm – 1 mm | CMB, molecular clouds |
| Infrared | 700 nm – 1 mm | Warm dust, cool stars, exoplanets |
| Visible | 400 – 700 nm | Stellar surfaces, nebulae |
| Ultraviolet | 10 – 400 nm | Hot stars, active galactic nuclei |
| X-ray | 0.01 – 10 nm | Million-degree plasma, black hole accretion |
| Gamma | < 0.01 nm | Extreme events: supernovae, GRBs |

**Key insight:** Different wavelengths reveal different physics. A galaxy looks completely different in radio vs. X-rays because you're seeing different physical components — cold gas vs. hot plasma. This is why astronomers build telescopes for every part of the spectrum.

{{< fig em-spectrum-bands >}}

### Light as Particles: Photon Energy

Light also behaves as particles called **photons**. Each photon carries a discrete amount of energy given by:

$$E = h\nu = \frac{hc}{\lambda}$$

where $h = 6.63 \times 10^{-34}$ J·s is **Planck's constant**.

This equation encodes a crucial fact: **short wavelength = high energy**. Gamma-ray photons carry billions of times more energy than radio photons. This is why gamma rays can damage DNA while radio waves pass harmlessly through your body.

::: {.callout-note}
## Unit Check

Let's verify that $E = hc/\lambda$ gives energy units:

$$[E] = \frac{[\text{J·s}][\text{m/s}]}{[\text{m}]} = \frac{\text{J·m}}{\text{m}} = \text{J}\ \checkmark$$

Units work out. This is always worth checking.
:::

::: {.callout-tip}
## Check Yourself

A photon has wavelength 200 nm. Another has wavelength 800 nm. How do their energies compare?

::: {.callout-note collapse="true"}
## Solution

Since $E \propto 1/\lambda$, the 200 nm photon has 4× more energy than the 800 nm photon.

$$\frac{E_{200}}{E_{800}} = \frac{\lambda_{800}}{\lambda_{200}} = \frac{800}{200} = 4$$

The shorter-wavelength photon is more energetic.
:::
:::

---
```

**Step 5: Write Part 2 — Blackbody Radiation**

```markdown
## Part 2: Blackbody Radiation

### What Is a Blackbody?

A **blackbody** is an idealized object that absorbs all electromagnetic radiation that falls on it — no reflection, no transmission. When heated, a blackbody re-emits radiation with a spectrum that depends *only* on its temperature.

This might seem abstract, but blackbodies are everywhere in astronomy:

- **Stars** are approximate blackbodies (their spectra deviate due to absorption lines, but the overall shape follows the blackbody curve)
- **Planets** emit thermal radiation approximately as blackbodies
- **The Cosmic Microwave Background** is the most perfect blackbody ever measured

Understanding blackbody radiation is therefore fundamental to stellar astrophysics.

### The Planck Spectrum: Qualitative Picture

When you heat an object, it glows. The color of that glow depends on temperature:

- A stovetop burner glows dull red (~700 K)
- An incandescent bulb filament glows yellow-white (~2700 K)
- The Sun's surface glows yellow (~5800 K)
- A welding arc glows blue-white (~6000+ K)

{{< fig blackbody-stellar-spectra >}}

The figure shows blackbody spectra at three different temperatures. Notice two patterns:

1. **The peak shifts to shorter wavelengths as temperature increases.** Hot objects peak in the blue/UV; cool objects peak in the red/infrared.

2. **The total energy emitted increases dramatically with temperature.** The area under the curve (total power radiated) grows as $T^4$ — we'll quantify this with the Stefan-Boltzmann law in Module 2.

### The Ultraviolet Catastrophe

Before 1900, physicists tried to derive the blackbody spectrum using classical physics. The result was the **Rayleigh-Jeans law**:

$$B_\lambda \propto \frac{T}{\lambda^4}$$

This works well at long wavelengths. But notice the problem: as $\lambda \to 0$, the intensity goes to infinity! Classical physics predicted that any warm object should emit infinite energy in the ultraviolet and beyond.

<!-- TODO: Need UV catastrophe figure showing Rayleigh-Jeans vs Planck -->

This was called the **ultraviolet catastrophe** — a fundamental failure of classical physics. Ovens don't emit infinite UV radiation. Something was deeply wrong.

### Planck's Quantum Solution

In 1900, Max Planck found the solution — though he called it "an act of desperation." He proposed that energy is emitted in discrete packets called **quanta**, with energy $E = h\nu$.

This changes everything at short wavelengths. To emit a high-frequency photon, an oscillator needs energy $h\nu$. If the thermal energy available ($\sim k_B T$) is less than $h\nu$, emission is suppressed. You can't emit a fraction of a photon.

This quantum suppression cuts off the ultraviolet catastrophe and produces the correct blackbody spectrum.

### The Planck Function

The complete blackbody spectrum is given by the **Planck function**:

$$B_\lambda(T) = \frac{2hc^2}{\lambda^5} \frac{1}{e^{hc/\lambda k_B T} - 1}$$

This looks intimidating. Let's break it down:

- $B_\lambda(T)$ = spectral radiance (intensity per unit wavelength) at wavelength $\lambda$ and temperature $T$
- The $\lambda^{-5}$ factor would make short wavelengths dominate...
- But the exponential term $e^{hc/\lambda k_B T}$ in the denominator suppresses short wavelengths
- The competition between these terms creates the peak

**You don't need to memorize this equation.** But you should recognize it and understand its structure. Equations like this will appear throughout your astronomy career.

### Limiting Cases: Taming the Planck Function

The key to not being intimidated by complex equations is understanding their **limiting cases** — what happens when one term dominates.

**Case 1: Long wavelengths (Rayleigh-Jeans limit)**

When $\lambda$ is large, $hc/\lambda k_B T \ll 1$. The exponential can be approximated as $e^x \approx 1 + x$ for small $x$:

$$e^{hc/\lambda k_B T} - 1 \approx \frac{hc}{\lambda k_B T}$$

Substituting into the Planck function:

$$B_\lambda \approx \frac{2hc^2}{\lambda^5} \cdot \frac{\lambda k_B T}{hc} = \frac{2ck_B T}{\lambda^4}$$

This is the Rayleigh-Jeans law — classical physics works at long wavelengths because quantum effects are negligible.

**Case 2: Short wavelengths (Wien limit)**

When $\lambda$ is small, $hc/\lambda k_B T \gg 1$. The exponential dominates, and the "-1" in the denominator becomes negligible:

$$B_\lambda \approx \frac{2hc^2}{\lambda^5} e^{-hc/\lambda k_B T}$$

The exponential cuts off emission at short wavelengths — this is the quantum suppression that prevents the ultraviolet catastrophe.

::: {.callout-tip}
## The Pattern

Complex equations often have simple limiting behavior. When you encounter a scary equation:

1. Identify the variables that can be "large" or "small"
2. Take limits to see what terms dominate
3. The limiting behavior is usually much simpler

This is a professional skill. Practice it.
:::

::: {.callout-tip}
## Check Yourself

In the Rayleigh-Jeans limit, does intensity increase or decrease with temperature? With wavelength?

::: {.callout-note collapse="true"}
## Solution

From $B_\lambda \propto T/\lambda^4$:

- **Temperature:** Intensity increases linearly with $T$. Hotter = brighter.
- **Wavelength:** Intensity decreases as $\lambda^{-4}$. Shorter wavelengths are brighter (in this limit).

But remember: this limit only applies at long wavelengths. At short wavelengths, the Wien limit takes over and intensity drops exponentially.
:::
:::

---
```

**Step 6: Write Part 3 — Wien's Law**

```markdown
## Part 3: Wien's Displacement Law

### The Peak Wavelength

The Planck function has a peak — a wavelength where emission is maximum. This peak wavelength depends only on temperature:

$$\lambda_{\text{peak}} = \frac{b}{T}$$

where $b = 2.898 \times 10^{-3}$ m·K is **Wien's displacement constant**.

This can be rewritten as:

$$\lambda_{\text{peak}} \cdot T = 2.898 \times 10^{-3}\ \text{m·K}$$

**Physical interpretation:** Hotter objects peak at shorter (bluer) wavelengths. Cooler objects peak at longer (redder) wavelengths. This is why hot stars are blue and cool stars are red.

{{< fig wavelength-energy-relation >}}

### Where Does Wien's Law Come From?

Wien's law comes from finding the maximum of the Planck function — setting $dB_\lambda/d\lambda = 0$ and solving for $\lambda$.

This requires calculus (product rule and chain rule applied to the Planck function). The calculation is involved, but the result is elegant:

$$\frac{hc}{\lambda_{\text{peak}} k_B T} \approx 4.965$$

Rearranging gives Wien's law. The constant $b = hc/(4.965 \, k_B)$.

**Why this matters:** Wien's law isn't arbitrary — it follows directly from the physics of the Planck function. Calculus lets us extract simple, powerful results from complex equations.

### Worked Example: The Sun

**Problem:** The Sun's spectrum peaks at approximately 500 nm. What is the Sun's surface temperature?

**Solution:**

Using Wien's law:

$$T = \frac{b}{\lambda_{\text{peak}}} = \frac{2.898 \times 10^{-3}\ \text{m·K}}{500 \times 10^{-9}\ \text{m}}$$

$$T = \frac{2.898 \times 10^{-3}}{5 \times 10^{-7}} = 5796\ \text{K} \approx 5800\ \text{K}$$

**Interpretation:** The Sun's surface temperature is about 5800 K. We determined this using only the color of sunlight — no thermometer required.

::: {.callout-note}
## Unit Check

$$[T] = \frac{[\text{m·K}]}{[\text{m}]} = \text{K}\ \checkmark$$
:::

### Worked Example: Comparing Stars

**Problem:** Betelgeuse (a red supergiant) has a peak wavelength around 830 nm. Rigel (a blue supergiant) peaks around 240 nm. Calculate their surface temperatures.

**Solution:**

For Betelgeuse:
$$T_{\text{Betelgeuse}} = \frac{2.898 \times 10^{-3}}{830 \times 10^{-9}} = 3490\ \text{K} \approx 3500\ \text{K}$$

For Rigel:
$$T_{\text{Rigel}} = \frac{2.898 \times 10^{-3}}{240 \times 10^{-9}} = 12075\ \text{K} \approx 12000\ \text{K}$$

{{< fig betelgeuse-size >}}

**Interpretation:** Rigel is about 3.5× hotter than Betelgeuse. The color difference — blue vs. red — directly reflects this temperature difference. When you look at Orion, you're literally seeing temperature encoded as color.

### A Common Misconception

**Question:** Rigel's peak wavelength (240 nm) is in the ultraviolet. Why does Rigel appear blue-white to our eyes, not invisible?

**Answer:** The Planck curve is *broad*. Rigel emits strongly across a wide range of wavelengths, including the entire visible spectrum. But it emits *more* blue light than red light (because the visible band is on the blue side of the peak). Our eyes perceive this as blue-white.

Remember: peak wavelength ≠ only wavelength. Blackbodies emit at all wavelengths; the peak just tells you where emission is strongest.

### Worked Example: The Cosmic Microwave Background

**Problem:** The Cosmic Microwave Background (CMB) — the afterglow of the Big Bang — peaks at a wavelength of about 1.1 mm. What is the temperature of the CMB?

**Solution:**

$$T_{\text{CMB}} = \frac{2.898 \times 10^{-3}\ \text{m·K}}{1.1 \times 10^{-3}\ \text{m}} = 2.63\ \text{K} \approx 2.7\ \text{K}$$

{{< fig cmb-map >}}

**Interpretation:** The CMB has a temperature of about 2.7 K — just 2.7 degrees above absolute zero. This is the temperature of the universe itself, left over from the hot early cosmos that has been cooling for 13.8 billion years.

The CMB is the most perfect blackbody ever measured. Deviations from a perfect Planck curve are less than 1 part in 100,000 — a stunning confirmation of Big Bang cosmology.

::: {.callout-tip}
## Check Yourself

An object has a peak wavelength of 1 μm (1000 nm). What is its temperature? Is this object hotter or cooler than the Sun?

::: {.callout-note collapse="true"}
## Solution

$$T = \frac{2.898 \times 10^{-3}}{1 \times 10^{-6}} = 2898\ \text{K} \approx 2900\ \text{K}$$

This is about half the Sun's temperature (5800 K), so the object is cooler. An object at 2900 K would glow deep red — think of a hot coal or a very cool star like Proxima Centauri.
:::
:::

---
```

**Step 7: Write Summary Section**

```markdown
## Summary: Light as Information

We've built the first tool in our astronomical inference toolkit: **using color to measure temperature**.

1. **The electromagnetic spectrum** spans from radio to gamma rays, with each wavelength revealing different physics. Photon energy $E = hc/\lambda$ means short wavelengths carry more energy.

2. **Blackbodies** are idealized thermal emitters. Stars approximate blackbodies, making blackbody physics directly applicable to stellar astrophysics.

3. **The Planck function** describes the blackbody spectrum. Complex as it looks, its limiting cases are simple: Rayleigh-Jeans at long wavelengths, exponential cutoff at short wavelengths.

4. **Wien's law** ($\lambda_{\text{peak}} = b/T$) lets us convert color to temperature. Hot stars are blue; cool stars are red. This works from 3000 K (red dwarfs) to 40000 K (O-type stars) to 2.7 K (the cosmic microwave background).

### Reference Table: Key Equations

| Quantity | Equation | What It Tells You |
|----------|----------|-------------------|
| Wave relation | $c = \lambda \nu$ | Wavelength and frequency are inversely related |
| Photon energy | $E = h\nu = hc/\lambda$ | Short wavelength = high energy |
| Wien's law | $\lambda_{\text{peak}} = b/T$ | Peak wavelength encodes temperature |
| Wien's constant | $b = 2.898 \times 10^{-3}$ m·K | Memorize this (or know where to find it) |

### Reference Table: Temperature and Color

| Object | Temperature | Peak Wavelength | Spectral Band |
|--------|-------------|-----------------|---------------|
| CMB | 2.7 K | 1.1 mm | Microwave |
| Cool dust | 30 K | 100 μm | Far-IR |
| Brown dwarf | 1000 K | 2.9 μm | Near-IR |
| M dwarf (Proxima Cen) | 3000 K | 970 nm | Near-IR |
| K dwarf | 4500 K | 640 nm | Visible (orange) |
| Sun (G dwarf) | 5800 K | 500 nm | Visible (green-yellow) |
| A star (Sirius) | 10000 K | 290 nm | Near-UV |
| O star | 40000 K | 72 nm | Far-UV |

::: {.callout-tip}
## Looking Ahead

We can now infer temperature from color. But that's only part of the picture. In **Week 4**, we'll learn to measure **distance** — and then combine distance with brightness to infer **luminosity** (intrinsic power output).

In **Week 5**, we'll return to blackbody physics to derive the **Stefan-Boltzmann law**: $L = 4\pi R^2 \sigma T^4$. Combined with Wien's law, this lets us calculate stellar radii from temperature and luminosity.

Each week, the inference chain grows longer. By the end of Module 2, you'll be able to characterize a star — temperature, luminosity, radius, and eventually mass — all from the light it sends us.
:::
```

**Step 8: Verify reading renders**

```bash
quarto preview modules/module-01/readings/lecture-04-light-as-information.qmd
```

Expected: Reading renders without errors, math displays correctly, collapsible solutions work.

**Step 9: Commit reading**

```bash
git add modules/module-01/readings/lecture-04-light-as-information.qmd
git commit -m "feat(module-01): add Lecture 4 reading - Light as Information

- EM spectrum with photon energy and multi-wavelength astronomy
- Blackbody radiation: qualitative Planck spectrum, UV catastrophe, QM motivation
- Planck function with limiting cases (Rayleigh-Jeans, Wien tail)
- Wien's law with worked examples (Sun, Betelgeuse/Rigel, CMB)
- Check Yourself questions with solutions
- Reference tables for equations and stellar temperatures"
```

---

## Task 3: Update Module 1 Index

**Files:**
- Modify: `modules/module-01/index.qmd`

**Step 1: Read current index**

Read the file to find where to add Lecture 4 links.

**Step 2: Add Lecture 4 to the lecture listings**

Add after Lecture 3 entries:

```markdown
### Lecture 4: Light as Information (Week 3)

- [Slides: Light as Information](slides/lecture-04-light-as-information.qmd)
- [Reading: Light as Information](readings/lecture-04-light-as-information.qmd)
```

**Step 3: Verify module index renders**

```bash
quarto preview modules/module-01/index.qmd
```

**Step 4: Commit module index update**

```bash
git add modules/module-01/index.qmd
git commit -m "docs(module-01): add Lecture 4 links to module index"
```

---

## Task 4: Final Verification

**Step 1: Full site render**

```bash
quarto render
```

Expected: No errors or warnings related to Lecture 4 files.

**Step 2: Check for broken links**

```bash
grep -r "lecture-04" _site/
```

Expected: Links to slides and reading appear and resolve correctly.

**Step 3: Visual verification**

Open `_site/modules/module-01/index.html` in browser and verify:
- [ ] Lecture 4 links appear
- [ ] Slides load and navigate correctly
- [ ] Reading loads with math rendering
- [ ] Collapsible solutions work

---

## Summary

| Task | Files | Status |
|------|-------|--------|
| 0 | `assets/figures.yml` | Register 5 new figures |
| 1 | `modules/module-01/slides/lecture-04-light-as-information.qmd` | Create ~30 slides |
| 2 | `modules/module-01/readings/lecture-04-light-as-information.qmd` | Create ~1200 line reading |
| 3 | `modules/module-01/index.qmd` | Add Lecture 4 links |
| 4 | Full site | Verify render and links |

Total commits: 4
