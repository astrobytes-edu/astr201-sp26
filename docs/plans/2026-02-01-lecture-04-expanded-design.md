# Lecture 4 "Light as Information" Expansion Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Expand the existing Lecture 4 reading to cover radiative processes, scattering, Bohr model, spectroscopy, and telescope basics — making Module 1 Week 3 a comprehensive "Radiation Week" foundation.

**Architecture:** Update the existing reading file by adding four new major sections after the current blackbody physics content. Each section builds toward the throughline: light carries information, and we decode it through physics.

**Tech Stack:** Quarto markdown, figure registry (`assets/figures.yml`), equation system (`data/equations.yml`, `data/eqcards.yml`), CGS units throughout.

---

## Design Decisions (from brainstorming session)

1. **One reading, one slide deck** — organized by big topics for "Radiation Week"
2. **Full Bohr model treatment** — hydrogen as the example, with quantized energy levels
3. **All radiative processes** — 5 behaviors + scattering + opacity preview
4. **Telescope basics** — collecting area (D²) and resolution (λ/D)
5. **CGS units** — mandatory for all physics (cm, g, s, erg)

---

## Current Reading Structure (before expansion)

```
Part I: The Electromagnetic Spectrum
  - What is light?
  - The EM spectrum (radio → gamma)
  - Check Yourself questions

Part II: Blackbody Radiation
  - What is a blackbody?
  - Planck function (CGS)
  - Wien's law
  - Stefan-Boltzmann law
  - Check Yourself questions

Synthesis & Next Steps
```

## Target Reading Structure (after expansion)

```
Part I: The Electromagnetic Spectrum (existing)

Part II: How Light Interacts with Matter
  - The five behaviors (absorption, emission, transmission, reflection, refraction)
  - Scattering: why the sky is blue AND sunsets are red
  - Opacity and optical depth (conceptual preview)
  - Check Yourself questions

Part III: Blackbody Radiation (existing, relocated)

Part IV: Atoms and Spectral Lines
  - The Bohr model (hydrogen example)
  - Quantized energy levels and E = hν
  - Kirchhoff's laws: three types of spectra
  - What spectral lines tell us
  - Check Yourself questions

Part V: Telescopes as Light Buckets
  - Collecting area: why bigger is better (∝ D²)
  - Angular resolution: why bigger is sharper (θ ∝ λ/D)
  - Mirrors vs lenses (brief)
  - Check Yourself questions

Synthesis & Next Steps (updated)
```

---

## Task 0: Preparation

**Files:**
- Read: `modules/module-01/readings/lecture-04-light-as-information.qmd`
- Read: `assets/figures.yml`
- Read: `data/equations.yml`

**Step 1: Verify current reading structure**

Read the existing file and confirm the structure matches what's documented above.

**Step 2: Identify insertion points**

- New Part II goes AFTER Part I (EM spectrum), BEFORE current Part II (blackbody)
- Current Part II (blackbody) becomes Part III
- New Part IV (Bohr model) goes AFTER Part III
- New Part V (telescopes) goes AFTER Part IV
- Synthesis section gets updated

**Step 3: Document existing figure IDs**

List all figure IDs currently in the reading so we don't create duplicates.

---

## Task 1: Figure Inventory (Existing Figures)

Most figures already exist in `assets/figures.yml` (lines 554-684). Use these existing IDs:

**Existing figures to use:**

| Section | Figure ID | Description |
|---------|-----------|-------------|
| Light-matter interactions | `light-matter-behaviors` | 5 behaviors (absorption, emission, transmission, reflection, refraction) |
| Bohr model | `hydrogen-absorption` | Bohr model with absorption transitions |
| Bohr model | `hydrogen-emission` | Bohr model with emission transitions |
| Three spectra types | `three-types-of-spectra` | Continuous, absorption, emission spectra |
| Absorption/emission lines | `absorption-emission-elements` | Element fingerprints (Na, N, H, O) |
| Real stellar spectrum | `altair-spectrum-annotated` | Altair showing blackbody + absorption lines |

**Figures to create (telescope section only):**

```yaml
# Add to assets/figures.yml

telescope-collecting-area:
  path: /assets/images/module-01/week-03/telescope-collecting-area.png
  alt: "Two telescopes: small diameter D collects few photons (shown as dots), large diameter 2D collects four times as many photons. Caption shows Area ∝ D²."
  caption: "**What to notice:** Collecting area scales as diameter squared. A telescope twice as wide collects four times as much light."
  module: 1

telescope-resolution:
  path: /assets/images/module-01/week-03/telescope-resolution.png
  alt: "Two images of binary star: small telescope shows blurry single blob, large telescope resolves two distinct stars. Equation θ ∝ λ/D shown."
  caption: "**What to notice:** Angular resolution improves with larger diameter. The diffraction limit θ ≈ λ/D sets the finest detail a telescope can distinguish."
  module: 1

rayleigh-scattering-sky:
  path: /assets/images/module-01/week-03/rayleigh-scattering-sky.png
  alt: "Diagram showing sunlight entering atmosphere. Blue light (short wavelength) scatters in all directions while red light (long wavelength) passes through more directly. Viewer looking up sees scattered blue; viewer at sunset sees transmitted red."
  caption: "**What to notice:** Rayleigh scattering explains both the blue sky (scattered short wavelengths) and red sunsets (transmitted long wavelengths). Same physics, different viewing geometry."
  module: 1
```

**Step 1: Add telescope and scattering figures to registry**

Add the three new figure entries above to `assets/figures.yml` under the Week 03 section.

**Step 2: Verify figure registration**

Run: `quarto render`
Expected: No errors about missing figure IDs

---

## Task 2: Register New Equations

**Files:**
- Modify: `data/equations.yml`
- Modify: `data/eqcards.yml`
- Create: `_includes/equations/bohr-energy.qmd`
- Create: `_includes/equations/photon-energy.qmd`
- Create: `_includes/equations/rayleigh-scattering.qmd`
- Create: `_includes/equations/telescope-resolution.qmd`
- Create: `_includes/equations/collecting-area.qmd`

**Step 1: Create Bohr energy level equation include**

Create file: `_includes/equations/bohr-energy.qmd`

```markdown
$$
E_n = -\frac{13.6 \text{ eV}}{n^2}
$$ {#eq-bohr-energy}
```

**Step 2: Add Bohr energy to equations.yml**

```yaml
bohr-energy:
  title: "Hydrogen Energy Levels (Bohr Model)"
  file: "_includes/equations/bohr-energy.qmd"
  anchor: "eq-bohr-energy"
  eqcard: "bohr-energy"
```

**Step 3: Add Bohr energy meaning card to eqcards.yml**

```yaml
bohr-energy:
  predicts: "The energy of an electron in hydrogen at level n"
  depends:
    - "n: principal quantum number (1, 2, 3, ...)"
  says: "Electron energies are quantized — only certain discrete values are allowed. The ground state (n=1) has E = −13.6 eV; higher levels approach zero."
  assumptions:
    - "Hydrogen atom (single electron, single proton)"
    - "Non-relativistic treatment"
    - "Ignores fine structure and spin"
  units:
    - "E_n in eV (electron volts); 1 eV = 1.6 × 10⁻¹² erg"
```

**Step 4: Create photon energy equation include**

Create file: `_includes/equations/photon-energy.qmd`

```markdown
$$
E_\gamma = h\nu = \frac{hc}{\lambda}
$$ {#eq-photon-energy}
```

**Step 5: Add photon energy to equations.yml**

```yaml
photon-energy:
  title: "Photon Energy"
  file: "_includes/equations/photon-energy.qmd"
  anchor: "eq-photon-energy"
  eqcard: "photon-energy"
```

**Step 6: Add photon energy meaning card to eqcards.yml**

```yaml
photon-energy:
  predicts: "The energy carried by a single photon"
  depends:
    - "h: Planck's constant (6.63 × 10⁻²⁷ erg s)"
    - "ν: frequency (Hz)"
    - "λ: wavelength (cm)"
    - "c: speed of light (3 × 10¹⁰ cm/s)"
  says: "A photon's energy is set by its frequency (or equivalently, wavelength). Blue photons carry more energy than red photons."
  assumptions:
    - "Single photon"
    - "Vacuum propagation (c is constant)"
  units:
    - "E in erg (CGS) or eV"
    - "ν in Hz (s⁻¹)"
    - "λ in cm"
```

**Step 7: Create Rayleigh scattering equation include**

Create file: `_includes/equations/rayleigh-scattering.qmd`

```markdown
$$
\sigma_\text{Rayleigh} \propto \lambda^{-4}
$$ {#eq-rayleigh-scattering}
```

**Step 8: Add Rayleigh scattering to equations.yml**

```yaml
rayleigh-scattering:
  title: "Rayleigh Scattering Cross Section"
  file: "_includes/equations/rayleigh-scattering.qmd"
  anchor: "eq-rayleigh-scattering"
  eqcard: "rayleigh-scattering"
```

**Step 9: Add Rayleigh scattering meaning card to eqcards.yml**

```yaml
rayleigh-scattering:
  predicts: "How strongly light scatters off particles much smaller than the wavelength"
  depends:
    - "λ: wavelength of light"
  says: "Short wavelengths scatter much more than long wavelengths. Blue light (λ ≈ 450 nm) scatters about 5× more than red light (λ ≈ 650 nm)."
  assumptions:
    - "Particle size << wavelength"
    - "Elastic scattering (no energy change)"
  units:
    - "σ in cm² (cross section)"
    - "λ in any length unit (ratio matters)"
```

**Step 10: Create telescope resolution equation include**

Create file: `_includes/equations/telescope-resolution.qmd`

```markdown
$$
\theta_\text{min} \approx \frac{\lambda}{D}
$$ {#eq-telescope-resolution}
```

**Step 11: Add telescope resolution to equations.yml**

```yaml
telescope-resolution:
  title: "Diffraction-Limited Angular Resolution"
  file: "_includes/equations/telescope-resolution.qmd"
  anchor: "eq-telescope-resolution"
  eqcard: "telescope-resolution"
```

**Step 12: Add telescope resolution meaning card to eqcards.yml**

```yaml
telescope-resolution:
  predicts: "The smallest angular separation a telescope can resolve"
  depends:
    - "λ: wavelength of observation"
    - "D: diameter of the telescope aperture"
  says: "Bigger telescopes see finer detail. Shorter wavelengths see finer detail. This is the diffraction limit — the fundamental physics limit, not engineering."
  assumptions:
    - "Diffraction-limited (no atmospheric blur)"
    - "Circular aperture"
    - "θ in radians when λ and D have same units"
  units:
    - "θ in radians"
    - "λ and D in same units (e.g., both in cm)"
```

**Step 13: Create collecting area equation include**

Create file: `_includes/equations/collecting-area.qmd`

```markdown
$$
A = \pi \left(\frac{D}{2}\right)^2 \propto D^2
$$ {#eq-collecting-area}
```

**Step 14: Add collecting area to equations.yml**

```yaml
collecting-area:
  title: "Telescope Collecting Area"
  file: "_includes/equations/collecting-area.qmd"
  anchor: "eq-collecting-area"
  eqcard: "collecting-area"
```

**Step 15: Add collecting area meaning card to eqcards.yml**

```yaml
collecting-area:
  predicts: "How much light a telescope can gather"
  depends:
    - "D: diameter of the primary mirror or lens"
  says: "Light-gathering power scales as diameter squared. A telescope twice as wide collects four times as many photons — crucial for seeing faint objects."
  assumptions:
    - "Circular aperture"
    - "No obstruction (idealized)"
  units:
    - "A in cm² (CGS)"
    - "D in cm"
```

**Step 16: Verify equation registration**

Run: `quarto render`
Expected: No errors about missing equations

---

## Task 3: Add Part II — How Light Interacts with Matter

**Files:**
- Modify: `modules/module-01/readings/lecture-04-light-as-information.qmd`

**Step 1: Locate insertion point**

Find the end of Part I (after the EM spectrum Check Yourself section). The new Part II will be inserted here.

**Step 2: Write the five behaviors section**

Insert after Part I ends:

```markdown
# Part II: How Light Interacts with Matter {#part-how-light-interacts}

When light encounters matter, it can do exactly five things: be absorbed, be emitted, pass through (transmission), bounce back (reflection), or bend (refraction). Every interaction between light and matter — from your eye reading this page to a star's spectrum — involves some combination of these five behaviors.

## The Five Behaviors of Light

### Absorption

When a photon is absorbed, its energy is transferred to the material. The photon is destroyed, and the material gains energy — often as heat, or by exciting an electron to a higher energy level.

**Key insight:** Absorption is selective. Materials absorb some wavelengths more than others. This selectivity is what makes absorption lines in stellar spectra so informative.

### Emission

Emission is absorption's partner. When an excited atom releases energy, it creates a new photon. The photon's wavelength is set by the energy difference — a direct consequence of $E = h\nu$.

**Key insight:** Hot objects emit light. The hotter they are, the more energetic (shorter wavelength) photons they produce.

### Transmission

Transmission occurs when light passes through a material without being absorbed. Glass transmits visible light but absorbs UV. The atmosphere transmits visible and radio but absorbs most UV and X-rays.

**Key insight:** A material's transmission window tells us what wavelengths can reach our detectors — and what wavelengths require space telescopes.

### Reflection

Reflection occurs when light bounces off a surface. Mirrors reflect nearly all visible light. Planets reflect some starlight — that's how we see them.

**Key insight:** The fraction of light reflected (albedo) tells us about a surface's composition and texture.

### Refraction

Refraction is the bending of light when it passes from one medium to another. This is how lenses focus light, and why stars twinkle (atmospheric refraction varies with turbulence).

**Key insight:** Refraction depends on wavelength — blue light bends more than red. This chromatic dispersion is how prisms separate white light into a spectrum.

{{< fig light-matter-behaviors >}}
```

**Step 3: Write the scattering section**

Continue in the same file:

```markdown
## Scattering: Blue Skies and Red Sunsets

Scattering is what happens when light interacts with particles and gets redirected in random directions. When the particles are much smaller than the wavelength of light — like air molecules — we get **Rayleigh scattering**.

{{< include ../../_includes/equations/rayleigh-scattering.qmd >}}

{{< eqrefcard rayleigh-scattering >}}

The $\lambda^{-4}$ dependence is dramatic. Blue light ($\lambda \approx 450$ nm) scatters about $(650/450)^4 \approx 4$ times more than red light ($\lambda \approx 650$ nm).

### Why the Sky is Blue

When sunlight enters the atmosphere, it encounters countless air molecules (N₂ and O₂). Blue light scatters much more than red light. When you look up at the sky (away from the Sun), you're seeing this scattered blue light coming from all directions.

### Why Sunsets are Red

At sunset, sunlight travels through much more atmosphere to reach your eyes. The blue light has been scattered away (mostly sideways and backward), leaving the red and orange wavelengths to continue forward. The Sun looks red because you're seeing what's left after the blue has been removed.

**Same physics, different geometry.** At noon, the Sun is overhead and light travels through relatively little atmosphere — you see scattered blue above and transmitted white from the Sun. At sunset, the long path through the atmosphere scatters away the blue, and you see the transmitted red.

{{< fig rayleigh-scattering-sky >}}

### Why Stars Twinkle

Twinkling (scintillation) is caused by turbulent refraction in the atmosphere, not scattering. Pockets of air at different temperatures act like weak, shifting lenses. This blurs and distorts starlight rapidly.

**Why don't planets twinkle?** Planets are extended objects (tiny disks, not points). The random twinkling from different parts of their disk averages out.

### Interstellar Reddening

The same physics applies to dust between stars. Interstellar dust grains preferentially scatter blue light, making distant stars appear redder than they actually are. This **interstellar reddening** must be corrected when measuring stellar colors.
```

**Step 4: Write the opacity preview section**

Continue:

```markdown
## Opacity and Optical Depth: A Preview

How easily does light pass through a material? This is quantified by **opacity** — the material's ability to block light.

**Optical depth** ($\tau$) measures how many "mean free paths" light travels through a medium:

- $\tau \ll 1$: optically thin — most photons escape without interacting
- $\tau \approx 1$: photons interact about once on average
- $\tau \gg 1$: optically thick — light is absorbed or scattered many times

We'll develop this quantitatively in Module 2 when we study stellar atmospheres. For now, the key insight is: **what we see depends on where the optical depth equals about 1**. We see into a star's photosphere but not its core because the outer layers become optically thick.

::: {.callout-note title="Preview: The τ = 1 Surface"}
When you look at the Sun, you're seeing light from where $\tau \approx 1$ — the photosphere. Light from deeper layers is absorbed and re-emitted so many times that it doesn't escape directly. This concept will be central to understanding stellar structure.
:::
```

**Step 5: Add Check Yourself questions for Part II**

Continue:

```markdown
## Check Yourself: Light-Matter Interactions

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** A red laser pointer and a blue laser pointer have the same power. Which scatters more when shining through a dusty room?

**Answer:** The blue laser scatters much more — roughly $(650/450)^4 \approx 4$ times as much. The blue beam will appear more visible from the side because more light is scattered toward your eyes.
:::

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** If the atmosphere were twice as thick, would sunsets be redder or less red?

**Answer:** Redder. More atmosphere means more scattering, which removes even more blue light. This is why sunsets through smoke or haze (which adds effective "atmosphere") are often dramatically red.
:::

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** You observe two identical stars — one nearby, one far away behind interstellar dust. Which appears redder?

**Answer:** The distant star behind the dust. Interstellar dust scatters blue light, making the transmitted light redder. This is interstellar reddening, and we must correct for it to measure true stellar colors.
:::
```

**Step 6: Verify Part II renders correctly**

Run: `quarto render modules/module-01/readings/lecture-04-light-as-information.qmd`
Expected: Clean render, no errors

**Step 7: Commit Part II**

```bash
git add modules/module-01/readings/lecture-04-light-as-information.qmd
git commit -m "feat(lecture-04): add Part II - how light interacts with matter

- Five behaviors of light (absorption, emission, transmission, reflection, refraction)
- Rayleigh scattering with λ⁻⁴ dependence
- Blue sky and red sunset explanation (same physics, different geometry)
- Star twinkling and interstellar reddening
- Opacity and optical depth preview for Module 2
- Check Yourself questions for retrieval practice

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 4: Renumber Existing Blackbody Section as Part III

**Files:**
- Modify: `modules/module-01/readings/lecture-04-light-as-information.qmd`

**Step 1: Find current Part II heading**

Locate: `# Part II: Blackbody Radiation` or similar

**Step 2: Change to Part III**

Replace: `# Part II:` with `# Part III:`

Update any internal cross-references if they exist.

**Step 3: Verify render**

Run: `quarto render modules/module-01/readings/lecture-04-light-as-information.qmd`
Expected: Clean render

**Step 4: Commit renumbering**

```bash
git add modules/module-01/readings/lecture-04-light-as-information.qmd
git commit -m "refactor(lecture-04): renumber blackbody section as Part III

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 5: Add Part IV — Atoms and Spectral Lines

**Files:**
- Modify: `modules/module-01/readings/lecture-04-light-as-information.qmd`

**Step 1: Locate insertion point**

Find the end of Part III (blackbody section). Insert Part IV after.

**Step 2: Write the Bohr model section**

```markdown
# Part IV: Atoms and Spectral Lines {#part-atoms-spectral-lines}

The Sun's spectrum isn't a smooth rainbow — it's crossed by hundreds of dark lines. These **absorption lines** are fingerprints of the elements in the Sun's atmosphere. Understanding where they come from requires us to understand how atoms interact with light.

## The Bohr Model of the Atom

In 1913, Niels Bohr proposed a model of the hydrogen atom that explained why atoms emit and absorb light at specific wavelengths. Though quantum mechanics has superseded it, the Bohr model captures the essential physics and gives correct answers for hydrogen.

**The key idea:** Electrons in atoms can only occupy discrete energy levels — not arbitrary energies, but specific quantized values.

{{< fig bohr-model-hydrogen >}}

### Energy Levels in Hydrogen

For hydrogen, the energy of level $n$ is:

{{< include ../../_includes/equations/bohr-energy.qmd >}}

{{< eqrefcard bohr-energy >}}

The ground state ($n = 1$) has $E_1 = -13.6$ eV. This is the **ionization energy** — the energy required to remove the electron entirely.

Higher levels have less negative energies:
- $n = 2$: $E_2 = -3.4$ eV
- $n = 3$: $E_3 = -1.5$ eV
- $n = \infty$: $E_\infty = 0$ (free electron)

### Photon Emission and Absorption

When an electron jumps from a higher level to a lower level, it emits a photon. The photon's energy equals the energy difference:

$$
E_\gamma = E_\text{upper} - E_\text{lower} = h\nu
$$

{{< include ../../_includes/equations/photon-energy.qmd >}}

{{< eqrefcard photon-energy >}}

**This is why spectral lines have specific wavelengths.** Each transition corresponds to a specific energy difference, which means a specific photon energy, which means a specific wavelength.

### The Hydrogen Series

Different series of lines correspond to transitions ending on different levels:

| Series | Lower level | Wavelength range | Discovery |
|--------|-------------|------------------|-----------|
| Lyman | $n = 1$ | UV (< 122 nm) | 1906 |
| Balmer | $n = 2$ | Visible (365–656 nm) | 1885 |
| Paschen | $n = 3$ | Near-IR (820–1875 nm) | 1908 |
| Brackett | $n = 4$ | IR | 1922 |

The **Balmer series** is particularly important because it falls in the visible range. The famous H-alpha line (656 nm, red) is the $n = 3 \to 2$ transition. It's what makes emission nebulae glow red.

::: {.callout-note title="Why Hydrogen?"}
Hydrogen is the simplest atom and the most abundant element in the universe. Understanding hydrogen's spectrum is the foundation for understanding all atomic spectra.
:::
```

**Step 3: Write Kirchhoff's laws section**

Continue:

```markdown
## Kirchhoff's Laws: Three Types of Spectra

In the 1860s, Gustav Kirchhoff recognized that there are exactly three types of spectra, and each arises from different physical conditions:

{{< fig three-spectra-types >}}

### 1. Continuous Spectrum

**Source:** Hot, dense matter (solid, liquid, or dense gas)

**Appearance:** Smooth rainbow of colors with no lines

**Physics:** In dense matter, atoms interact so strongly that their discrete energy levels blur together. The result is blackbody radiation — a smooth thermal spectrum.

**Example:** The interior of a star, an incandescent light bulb filament

### 2. Absorption Spectrum

**Source:** Cool gas in front of a hot continuous source

**Appearance:** Rainbow with dark lines at specific wavelengths

**Physics:** Atoms in the cooler gas absorb photons at their characteristic frequencies, removing those wavelengths from the continuous background.

**Example:** The Sun's spectrum (photosphere is hot; chromosphere absorbs)

### 3. Emission Spectrum

**Source:** Hot, thin gas with no bright background

**Appearance:** Bright lines at specific wavelengths on dark background

**Physics:** Atoms in the hot gas emit photons at their characteristic frequencies, but the gas is too thin to produce a continuous background.

**Example:** Neon signs, emission nebulae, solar prominences

### The Power of Spectroscopy

Kirchhoff's insight revolutionized astronomy. By analyzing a star's spectrum, we can determine:

- **Composition:** Which elements are present (each element has unique line patterns)
- **Temperature:** Line ratios reveal excitation conditions
- **Velocity:** Doppler shifts reveal motion toward or away from us
- **Density:** Line widths reveal pressure and density
- **Magnetic fields:** Zeeman splitting reveals field strength

**Spectroscopy transforms light into information.** This is what makes astronomy a quantitative science rather than just pretty pictures.
```

**Step 4: Add Check Yourself questions for Part IV**

Continue:

```markdown
## Check Yourself: Atoms and Spectra

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** The Lyman-alpha line is the $n = 2 \to 1$ transition in hydrogen. Calculate its wavelength.

**Answer:**
Energy difference: $E = E_2 - E_1 = (-3.4) - (-13.6) = 10.2$ eV

Convert to erg: $E = 10.2 \times 1.6 \times 10^{-12}$ erg $= 1.63 \times 10^{-11}$ erg

Wavelength: $\lambda = hc/E = (6.63 \times 10^{-27})(3 \times 10^{10})/(1.63 \times 10^{-11})$

$\lambda = 1.22 \times 10^{-5}$ cm $= 122$ nm (UV)
:::

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** You observe a nebula that glows red. What type of spectrum is this, and what transition likely produces the red color?

**Answer:** This is an **emission spectrum** from hot, thin gas. The red color is likely **H-alpha** — the Balmer series $n = 3 \to 2$ transition at 656 nm.
:::

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** A star's spectrum shows absorption lines. Where is the cool gas relative to the hot gas?

**Answer:** The cool gas must be **in front of** the hot continuous source (from our viewing direction). In a star, this means the cooler outer atmosphere (chromosphere) absorbs light from the hotter photosphere below.
:::
```

**Step 5: Verify Part IV renders correctly**

Run: `quarto render modules/module-01/readings/lecture-04-light-as-information.qmd`
Expected: Clean render, no errors

**Step 6: Commit Part IV**

```bash
git add modules/module-01/readings/lecture-04-light-as-information.qmd
git commit -m "feat(lecture-04): add Part IV - atoms and spectral lines

- Bohr model with hydrogen energy levels
- Photon energy E = hν and emission/absorption
- Hydrogen series (Lyman, Balmer, Paschen, Brackett)
- Kirchhoff's three laws with examples
- What spectroscopy reveals (composition, T, v, density, B)
- Check Yourself questions

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 6: Add Part V — Telescopes as Light Buckets

**Files:**
- Modify: `modules/module-01/readings/lecture-04-light-as-information.qmd`

**Step 1: Locate insertion point**

Find the end of Part IV. Insert Part V after.

**Step 2: Write the telescopes section**

```markdown
# Part V: Telescopes as Light Buckets {#part-telescopes}

Astronomical objects are far away and faint. Our eyes alone can detect only about 6,000 stars. Telescopes extend our reach by gathering more light and resolving finer details. At their core, telescopes are simple — but the physics behind why bigger is better is worth understanding.

## Collecting Area: Why Bigger Is Better

A telescope's most fundamental job is to collect photons. The more photons you collect, the fainter the objects you can detect and the better your signal-to-noise ratio.

{{< include ../../_includes/equations/collecting-area.qmd >}}

{{< eqrefcard collecting-area >}}

**The diameter-squared scaling is powerful.** Double the diameter, and you collect four times as many photons. The Keck telescope (10 m) collects 400 times more light than a 0.5 m amateur telescope.

{{< fig telescope-collecting-area >}}

### Why This Matters

| Telescope | Diameter | Collecting Area | Relative Power |
|-----------|----------|-----------------|----------------|
| Human eye | 0.7 cm | 0.4 cm² | 1× |
| Binoculars | 5 cm | 20 cm² | 50× |
| Amateur | 20 cm | 314 cm² | 800× |
| Keck | 10 m | 78.5 m² | 200,000× |

Faint objects require large collecting areas. This is why professional observatories have such large primary mirrors — it's about photon-counting statistics.

## Angular Resolution: Why Bigger Is Sharper

A telescope's ability to see fine detail is limited by **diffraction** — the wave nature of light causes the image of a point source to spread into a disk (the Airy disk).

The angular size of this diffraction disk is:

{{< include ../../_includes/equations/telescope-resolution.qmd >}}

{{< eqrefcard telescope-resolution >}}

**Bigger telescopes see finer detail.** A 10 m telescope has 10× better resolution than a 1 m telescope (at the same wavelength).

**Shorter wavelengths see finer detail.** The same telescope resolves finer structure in blue light than in red light, and far finer in X-rays than visible.

{{< fig telescope-resolution >}}

### The Atmosphere Limit

Ground-based optical telescopes rarely reach their diffraction limit. Atmospheric turbulence blurs images to about 1 arcsecond resolution regardless of telescope size — this is called **seeing**.

**Adaptive optics** uses deformable mirrors to correct atmospheric distortion in real time, approaching the diffraction limit from the ground.

**Space telescopes** (like Hubble and JWST) escape the atmosphere entirely and routinely achieve diffraction-limited images.

## Mirrors vs. Lenses (Brief)

Early telescopes used lenses (refractors). Modern large telescopes use mirrors (reflectors). Why?

| Aspect | Lens (Refractor) | Mirror (Reflector) |
|--------|------------------|-------------------|
| **Size limit** | ~1 m (glass sags) | 10+ m (supported from behind) |
| **Chromatic aberration** | Yes (different colors focus differently) | No |
| **Weight** | Heavy (solid glass) | Lighter (thin mirror) |
| **Cost** | Expensive to make | Cheaper per area |

All modern large telescopes are reflectors. The largest current telescope (VLT) uses 8.2 m mirrors. The upcoming ELT will use a 39 m segmented mirror.

::: {.callout-note title="Why Radio Telescopes Are Huge"}
Radio wavelengths are ~10⁶ times longer than visible light. To achieve comparable angular resolution, radio telescopes must be ~10⁶ times larger — hence dishes 100 m across, or interferometric arrays spanning continents.
:::
```

**Step 3: Add Check Yourself questions for Part V**

Continue:

```markdown
## Check Yourself: Telescopes

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** A telescope with a 4 m mirror is replaced by one with an 8 m mirror. By what factor does the collecting area increase?

**Answer:** Collecting area scales as $D^2$. The ratio is $(8/4)^2 = 4$. The new telescope collects **4 times** as many photons.
:::

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** The Hubble Space Telescope (2.4 m) observes at 500 nm. What is its angular resolution?

**Answer:** $\theta \approx \lambda/D = (500 \times 10^{-7} \text{ cm})/(240 \text{ cm}) = 2 \times 10^{-7}$ rad

Converting: $\theta = 2 \times 10^{-7} \times (206265 \text{ arcsec/rad}) \approx 0.04$ arcsec

Hubble achieves about 0.05 arcsec resolution — far better than ground-based seeing (~1 arcsec).
:::

::: {.callout-tip title="Quick Check" collapse="true"}
**Question:** Why can't we just build a 100 m optical telescope lens?

**Answer:** Lenses must be supported only at their edges. A 100 m glass lens would be impossibly heavy and would sag under its own weight, distorting the optics. Mirrors can be supported from behind and can be made thin (or segmented), making large reflectors practical while large refractors are not.
:::
```

**Step 4: Verify Part V renders correctly**

Run: `quarto render modules/module-01/readings/lecture-04-light-as-information.qmd`
Expected: Clean render, no errors

**Step 5: Commit Part V**

```bash
git add modules/module-01/readings/lecture-04-light-as-information.qmd
git commit -m "feat(lecture-04): add Part V - telescopes as light buckets

- Collecting area with D² scaling and comparison table
- Angular resolution with λ/D formula
- Atmospheric seeing and adaptive optics
- Mirrors vs lenses comparison
- Radio telescope size explanation
- Check Yourself questions

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 7: Update Synthesis and Learning Objectives

**Files:**
- Modify: `modules/module-01/readings/lecture-04-light-as-information.qmd`

**Step 1: Update learning objectives in YAML frontmatter**

Locate the `learning-objectives:` section and update to include:

```yaml
learning-objectives:
  - Identify the five ways light interacts with matter and give astronomical examples
  - Explain why the sky is blue and sunsets are red using Rayleigh scattering
  - Describe the Bohr model and calculate hydrogen transition wavelengths
  - Distinguish between continuous, absorption, and emission spectra
  - Apply Kirchhoff's laws to identify physical conditions from spectra
  - Calculate how telescope collecting area and resolution scale with diameter
  - Explain why all large modern telescopes are reflectors, not refractors
```

**Step 2: Update synthesis section**

Locate the existing synthesis section and expand:

```markdown
# Synthesis: Light as the Messenger {#synthesis}

We've covered the full journey of a photon — from its creation in matter, through its interactions as it travels, to its collection in our telescopes:

1. **The electromagnetic spectrum** spans from radio waves to gamma rays, each regime revealing different physics.

2. **Light interacts with matter** through five behaviors (absorption, emission, transmission, reflection, refraction) plus scattering. Rayleigh scattering ($\propto \lambda^{-4}$) explains everyday phenomena from blue skies to red sunsets.

3. **Blackbody radiation** connects temperature to spectrum shape. The Planck function, Wien's law, and Stefan-Boltzmann law let us extract temperature, luminosity, and radius from light alone.

4. **Atoms and spectral lines** encode composition, temperature, velocity, and more. The Bohr model explains why transitions produce specific wavelengths. Kirchhoff's laws tell us what physical conditions produce each spectrum type.

5. **Telescopes** extend our reach by collecting more photons ($\propto D^2$) and resolving finer details ($\theta \propto \lambda/D$). Modern reflectors overcome the size limits of lenses.

**The throughline:** Every piece of astronomical knowledge comes from decoding light. The physics of radiation — how it's produced, how it interacts, how we detect it — is the foundation of everything that follows.

## What's Next

In Module 2, we'll use these tools to **infer the properties of stars** — their distances, luminosities, temperatures, compositions, and masses. The light carries all this information; we just need to know how to read it.
```

**Step 3: Verify full reading renders**

Run: `quarto render modules/module-01/readings/lecture-04-light-as-information.qmd`
Expected: Clean render, all sections present

**Step 4: Commit synthesis update**

```bash
git add modules/module-01/readings/lecture-04-light-as-information.qmd
git commit -m "docs(lecture-04): update learning objectives and synthesis

- Expanded learning objectives to cover all new sections
- Updated synthesis to summarize full radiation week content
- Connected to Module 2 preview

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 8: Final Verification

**Step 1: Full site render**

Run: `quarto render`
Expected: Clean build with no errors or warnings about missing references

**Step 2: Check reading navigation**

Open: `_site/modules/module-01/readings/lecture-04-light-as-information.html`
Verify:
- Table of contents shows all five parts
- All figures render (or show as placeholders if images not yet added)
- All equations render correctly
- All Check Yourself sections are collapsible and work

**Step 3: Verify links**

Run: `grep -r "lecture-04" _site/ | head -20`
Verify: Links to lecture-04 resolve correctly

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat(lecture-04): complete radiation week expansion

Summary:
- Part II: How light interacts with matter (5 behaviors, scattering, opacity preview)
- Part III: Blackbody radiation (existing, renumbered)
- Part IV: Atoms and spectral lines (Bohr model, Kirchhoff's laws)
- Part V: Telescopes (collecting area, resolution)

Figures registered (placeholders until assets added):
- radiative-processes-five
- rayleigh-scattering-sky
- bohr-model-hydrogen
- three-spectra-types
- telescope-collecting-area
- telescope-resolution

Equations registered:
- bohr-energy
- photon-energy
- rayleigh-scattering
- telescope-resolution
- collecting-area

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Task 9: Create Placeholder Figure Assets (Optional)

If figure images don't exist yet, create placeholder files so renders don't fail:

**Step 1: Create placeholder images**

```bash
mkdir -p assets/images/module-01
touch assets/images/module-01/radiative-processes-five.png
touch assets/images/module-01/rayleigh-scattering-sky.png
touch assets/images/module-01/bohr-model-hydrogen.png
touch assets/images/module-01/three-spectra-types.png
touch assets/images/module-01/telescope-collecting-area.png
touch assets/images/module-01/telescope-resolution.png
```

**Step 2: Commit placeholders**

```bash
git add assets/images/module-01/
git commit -m "chore: add placeholder images for lecture-04 figures

Replace with actual diagrams before delivery.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Summary

This plan expands Lecture 4 from a focused blackbody reading into a comprehensive "Radiation Week" resource covering:

1. **How light interacts with matter** — absorption, emission, transmission, reflection, refraction, scattering
2. **Blackbody radiation** — existing content, renumbered
3. **Atoms and spectral lines** — Bohr model, Kirchhoff's laws, spectroscopy
4. **Telescopes** — collecting area, resolution, mirrors vs lenses

Total estimated sections: 5 parts with ~15 Check Yourself questions
Total new figures: 6
Total new equations: 5

The reading now provides a complete foundation for inferring astronomical properties from light — exactly what Module 2 requires.
