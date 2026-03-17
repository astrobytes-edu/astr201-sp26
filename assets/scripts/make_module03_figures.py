#!/usr/bin/env python3
"""
Generate pedagogical figures for ASTR 201 Module 3: Stellar Structure & Evolution.

The Lecture 1-3 figures are optimized for dual use in white lecture slides and
Quarto readings. The later-module figures retain the darker infographic style
already used elsewhere in Module 3. All physics is in CGS/solar units unless
the plotted axis explicitly uses a derived convenience unit such as MeV or fm.

Usage:
    uv run python assets/scripts/make_module03_figures.py

Output directory: assets/images/module-03/
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as pe
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# Global style: dark theme matching NASA infographics
# ─────────────────────────────────────────────────────────────
DARK_BG = "#0d1117"
PANEL_BG = "#161b22"
TEXT_COLOR = "#e6edf3"
MUTED_TEXT = "#8b949e"
ACCENT_BLUE = "#58a6ff"
ACCENT_CYAN = "#56d4dd"
ACCENT_ORANGE = "#f0883e"
ACCENT_RED = "#f85149"
ACCENT_GREEN = "#3fb950"
ACCENT_PURPLE = "#bc8cff"
ACCENT_YELLOW = "#e3b341"
ACCENT_PINK = "#f778ba"
GRID_COLOR = "#21262d"

SLIDE_BG = "#ffffff"
SLIDE_TEXT = "#22324d"
SLIDE_MUTED = "#66758b"
SLIDE_GRID = "#d7e0ea"
SLIDE_PANEL = "#f4f7fb"
SLIDE_TEAL = "#2f7f78"
SLIDE_ORANGE = "#c47b33"
SLIDE_ROSE = "#b55d70"
SLIDE_GOLD = "#b2871b"

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "images" / "module-03"

# ─────────────────────────────────────────────────────────────
# Physical constants (CGS unless otherwise noted)
# ─────────────────────────────────────────────────────────────
G_CGS = 6.674e-8
K_B_CGS = 1.380649e-16
M_P_CGS = 1.6726219e-24
H_CGS = 6.62607015e-27
C_CGS = 2.99792458e10
M_SUN_CGS = 1.98847e33
R_SUN_CGS = 6.957e10
L_SUN_CGS = 3.828e33
YEAR_S = 3.15576e7
KEV_TO_ERG = 1.602176634e-9
MEV_TO_ERG = 1.602176634e-6
E2_MEV_FM = 1.4399764
T_CORE_SUN = 1.5e7
MU_SOLAR_IONIZED = 0.6


def apply_dark_style(fig, ax):
    """Apply consistent dark styling to a figure and axes."""
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(PANEL_BG)
    ax.tick_params(colors=TEXT_COLOR, which="both")
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)


def apply_slide_style(fig, ax):
    """Apply white-slide styling for deck-ready figures."""
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.tick_params(colors=SLIDE_TEXT, which="both", labelsize=11)
    ax.xaxis.label.set_color(SLIDE_TEXT)
    ax.yaxis.label.set_color(SLIDE_TEXT)
    ax.title.set_color(SLIDE_TEXT)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(SLIDE_GRID)
        ax.spines[side].set_linewidth(1.0)
    ax.grid(True, color=SLIDE_GRID, linewidth=0.8, alpha=0.9)


def finalize_slide_axes(ax, grid=True):
    """Apply the standard slide-axis treatment to an existing axes."""
    ax.set_facecolor(SLIDE_BG)
    ax.tick_params(colors=SLIDE_TEXT, which="both", labelsize=11)
    ax.xaxis.label.set_color(SLIDE_TEXT)
    ax.yaxis.label.set_color(SLIDE_TEXT)
    ax.title.set_color(SLIDE_TEXT)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(SLIDE_GRID)
        ax.spines[side].set_linewidth(1.0)
    ax.grid(grid, color=SLIDE_GRID, linewidth=0.8, alpha=0.9)


def save_slide_figure(fig, filename):
    """Save a white-background figure into the module-03 image directory."""
    fig.savefig(OUTPUT_DIR / filename, facecolor=SLIDE_BG, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {filename}")


def solar_main_sequence_luminosity(mass_solar):
    """
    Approximate main-sequence luminosity in solar units.

    Uses common piecewise pedagogical fits:
    - very low mass: L = 0.23 M^2.3
    - Sun-like:      L = M^4
    - massive:       L ∝ M^3.5
    - very massive:  luminosity growth flattens relative to the naive law
    """
    mass = np.asarray(mass_solar, dtype=float)
    luminosity = np.empty_like(mass)

    low = mass < 0.43
    mid = (mass >= 0.43) & (mass < 2.0)
    high = (mass >= 2.0) & (mass < 20.0)
    very_high = mass >= 20.0

    luminosity[low] = 0.23 * mass[low] ** 2.3
    luminosity[mid] = mass[mid] ** 4.0
    luminosity[high] = 1.5 * mass[high] ** 3.5
    luminosity[very_high] = 1.5 * 20.0 ** 3.5 * (mass[very_high] / 20.0) ** 1.8
    return luminosity


def solar_main_sequence_radius(mass_solar):
    """Approximate main-sequence radius in solar units."""
    mass = np.asarray(mass_solar, dtype=float)
    radius = np.empty_like(mass)

    low = mass < 1.5
    high = ~low

    radius[low] = mass[low] ** 0.8
    continuity = 1.5 ** (0.8 - 0.57)
    radius[high] = continuity * mass[high] ** 0.57
    return radius


def accessible_fuel_fraction(mass_solar):
    """
    Crude accessible-hydrogen fraction for main-sequence lifetime estimates.

    This is pedagogical, not a stellar-evolution code:
    - very low mass fully convective stars can access a large fraction
    - Sun-like stars access only the core
    - massive stars burn a smaller fraction before leaving the MS
    """
    mass = np.asarray(mass_solar, dtype=float)
    fraction = np.empty_like(mass)
    fraction[mass < 0.35] = 0.70
    fraction[(mass >= 0.35) & (mass < 1.5)] = 0.12
    fraction[mass >= 1.5] = 0.08
    return fraction


def solar_normalized_timescales(mass_solar):
    """Return main-sequence timescales in years for a mass grid."""
    mass = np.asarray(mass_solar, dtype=float)
    radius = solar_main_sequence_radius(mass)
    luminosity = solar_main_sequence_luminosity(mass)
    fuel_fraction = accessible_fuel_fraction(mass)
    fuel_fraction_sun = accessible_fuel_fraction(np.array([1.0]))[0]

    tau_dyn_sun = 50.0 / (60.0 * 24.0 * 365.25)
    tau_kh_sun = 3.0e7
    tau_nuc_sun = 1.0e10

    tau_dyn = tau_dyn_sun * np.sqrt(radius**3 / mass)
    tau_kh = tau_kh_sun * mass**2 / (radius * luminosity)
    tau_nuc = tau_nuc_sun * (fuel_fraction / fuel_fraction_sun) * mass / luminosity
    tau_nuc_naive = tau_nuc_sun * mass ** (-2.5)

    return {
        "radius": radius,
        "luminosity": luminosity,
        "fuel_fraction": fuel_fraction,
        "tau_dyn": tau_dyn,
        "tau_kh": tau_kh,
        "tau_nuc": tau_nuc,
        "tau_nuc_naive": tau_nuc_naive,
    }


def approximate_turnoff_mass(target_age_yr, masses=None):
    """Invert the pedagogical lifetime curve to estimate the turnoff mass."""
    if masses is None:
        masses = np.logspace(np.log10(0.12), np.log10(20.0), 2000)
    lifetimes = solar_normalized_timescales(masses)["tau_nuc"]
    return masses[np.argmin(np.abs(np.log10(lifetimes) - np.log10(target_age_yr)))]


# ═════════════════════════════════════════════════════════════
# Figure 1: Binding Energy per Nucleon
# Used in: R3 (Nuclear Fusion), R9 (High-Mass Evolution)
# ═════════════════════════════════════════════════════════════
def make_binding_energy_curve():
    """Dual-use binding-energy curve with clear mass-energy interpretation."""
    isotopes = [
        (1, 0.0, r"$^1$H", SLIDE_MUTED),
        (2, 1.112, r"$^2$H", SLIDE_MUTED),
        (3, 2.827, r"$^3$He", SLIDE_MUTED),
        (4, 7.074, r"$^4$He", SLIDE_TEAL),
        (12, 7.680, r"$^{12}$C", SLIDE_ORANGE),
        (16, 7.976, r"$^{16}$O", SLIDE_ORANGE),
        (28, 8.448, r"$^{28}$Si", SLIDE_ORANGE),
        (56, 8.790, r"$^{56}$Fe", SLIDE_ROSE),
        (62, 8.794, r"$^{62}$Ni", SLIDE_MUTED),
        (197, 7.916, r"$^{197}$Au", SLIDE_GOLD),
        (235, 7.591, r"$^{235}$U", ACCENT_PURPLE),
    ]

    a_vals = np.array([row[0] for row in isotopes])
    be_vals = np.array([row[1] for row in isotopes])
    a_smooth = np.linspace(1, 240, 700)
    be_smooth = np.interp(a_smooth, a_vals, be_vals)

    fig, ax = plt.subplots(figsize=(12.6, 7.1), dpi=220)
    apply_slide_style(fig, ax)

    iron_mask = a_smooth <= 56
    ax.plot(a_smooth[iron_mask], be_smooth[iron_mask], color=SLIDE_TEAL, linewidth=3.2)
    ax.plot(a_smooth[~iron_mask], be_smooth[~iron_mask], color=ACCENT_PURPLE, linewidth=3.2)

    ax.axvspan(1, 56, color=SLIDE_TEAL, alpha=0.06, zorder=0)
    ax.axvspan(56, 240, color=ACCENT_PURPLE, alpha=0.05, zorder=0)

    for a_num, binding, label, color in isotopes:
        ax.plot(a_num, binding, "o", color=color, markersize=8.5,
                markeredgecolor=SLIDE_BG, markeredgewidth=1.5, zorder=5)

    label_offsets = {
        1: (6, -12), 4: (6, 6), 12: (6, 6), 16: (6, -10),
        28: (6, -12), 56: (6, 8), 197: (6, 6), 235: (-18, -14),
    }
    for a_num, binding, label, color in isotopes:
        if a_num in label_offsets:
            dx, dy = label_offsets[a_num]
            ax.annotate(label, (a_num, binding), xytext=(dx, dy),
                        textcoords="offset points", fontsize=11,
                        color=color, fontweight="bold")

    ax.annotate("Fusion of light nuclei\nmoves up this side",
                xy=(14, 7.55), xytext=(38, 5.7),
                fontsize=11, color=SLIDE_TEAL, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SLIDE_TEAL, lw=1.6))
    ax.annotate("Beyond iron, fusion moves\ndown the curve and costs energy",
                xy=(135, 8.35), xytext=(160, 6.4),
                fontsize=11, color=ACCENT_PURPLE, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ACCENT_PURPLE, lw=1.6),
                ha="center")
    ax.annotate("Iron peak:\nmost tightly bound",
                xy=(56, 8.79), xytext=(86, 9.08),
                fontsize=11.5, color=SLIDE_ROSE, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SLIDE_ROSE, lw=1.6),
                ha="center")

    ax.text(0.02, 0.96,
            "Higher binding energy per nucleon means lower total mass-energy.",
            transform=ax.transAxes, fontsize=11, color=SLIDE_TEXT,
            ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.35", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    ax.set_xlabel("Mass Number, $A$", fontsize=14)
    ax.set_ylabel("Binding Energy per Nucleon (MeV)", fontsize=14)
    ax.set_xlim(0, 240)
    ax.set_ylim(0, 9.4)
    ax.set_title("Binding Energy per Nucleon and Why Fusion Releases Energy",
                 fontsize=18.5, fontweight="bold", pad=14)

    fig.tight_layout()
    save_slide_figure(fig, "binding-energy-curve.png")


# ═════════════════════════════════════════════════════════════
# Figure 2: Photon Random Walk
# Used in: R4 (Radiation Transport)
# ═════════════════════════════════════════════════════════════
def make_random_walk():
    """
    Simulated photon random walk inside the Sun.

    Shows how a photon scatters ~10^24 times, taking ~170,000 years
    to traverse what light could cross in 2.3 seconds.
    """
    rng = np.random.default_rng(42)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7), dpi=200,
                             gridspec_kw={"width_ratios": [1.2, 1]})

    # ── Left panel: random walk visualization ──
    ax = axes[0]
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)

    n_steps = 2000
    angles = rng.uniform(0, 2 * np.pi, n_steps)
    step_length = 1.0  # normalized mean free path
    x = np.cumsum(step_length * np.cos(angles))
    y = np.cumsum(step_length * np.sin(angles))
    x = np.insert(x, 0, 0)
    y = np.insert(y, 0, 0)

    # Color gradient along the walk (time evolution)
    cmap = LinearSegmentedColormap.from_list(
        "photon", [ACCENT_CYAN, ACCENT_BLUE, ACCENT_PURPLE, ACCENT_PINK]
    )
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(0, n_steps)
    lc = LineCollection(segments, cmap=cmap, norm=norm, alpha=0.6, linewidths=0.8)
    lc.set_array(np.arange(n_steps))
    ax.add_collection(lc)

    # Start and end points
    ax.plot(0, 0, "o", color=ACCENT_YELLOW, markersize=12, zorder=10,
            markeredgecolor="white", markeredgewidth=1.5)
    ax.plot(x[-1], y[-1], "*", color=ACCENT_RED, markersize=15, zorder=10,
            markeredgecolor="white", markeredgewidth=1)

    # Net displacement arrow
    ax.annotate(
        "", xy=(x[-1], y[-1]), xytext=(0, 0),
        arrowprops=dict(arrowstyle="-|>", color=ACCENT_ORANGE, lw=2.5),
        zorder=9,
    )

    # Labels
    net_dist = np.sqrt(x[-1]**2 + y[-1]**2)
    ax.text(0, -5, "Born here", fontsize=11, color=ACCENT_YELLOW,
            ha="center", fontweight="bold")
    ax.text(x[-1], y[-1] + 4, f"After {n_steps} steps", fontsize=10,
            color=ACCENT_RED, ha="center", fontweight="bold")

    ax.text(
        x[-1]/2 - 8, y[-1]/2 + 3,
        f"Net distance ≈ √N × ℓ\n= √{n_steps} × ℓ ≈ {net_dist:.0f} ℓ",
        fontsize=10, color=ACCENT_ORANGE, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=DARK_BG, edgecolor=ACCENT_ORANGE, alpha=0.8),
    )

    pad = 10
    lim = max(abs(x).max(), abs(y).max()) + pad
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$ (mean free paths)", fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel("$y$ (mean free paths)", fontsize=12, color=TEXT_COLOR)
    ax.set_title(f"Random Walk: {n_steps} Scatterings", fontsize=15,
                 fontweight="bold", color=TEXT_COLOR, pad=10)
    ax.tick_params(colors=MUTED_TEXT)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ── Right panel: the numbers ──
    ax2 = axes[1]
    ax2.set_facecolor(DARK_BG)
    ax2.axis("off")

    info_text = [
        ("The Photon's Journey", 20, "bold", TEXT_COLOR, 0.95),
        ("Inside the Sun", 14, "normal", MUTED_TEXT, 0.90),
        ("", 10, "normal", TEXT_COLOR, 0.84),
        ("Mean free path:", 13, "bold", ACCENT_CYAN, 0.80),
        ("ℓ ≈ 1 cm", 16, "normal", TEXT_COLOR, 0.75),
        ("(in the solar core)", 10, "normal", MUTED_TEXT, 0.71),
        ("", 10, "normal", TEXT_COLOR, 0.65),
        ("Number of scatterings:", 13, "bold", ACCENT_BLUE, 0.61),
        ("N = (R/ℓ)² ≈ 10²⁴", 16, "normal", TEXT_COLOR, 0.56),
        ("", 10, "normal", TEXT_COLOR, 0.50),
        ("Diffusion time:", 13, "bold", ACCENT_PURPLE, 0.46),
        ("t = Nℓ/c ≈ 170,000 yr", 16, "normal", TEXT_COLOR, 0.41),
        ("", 10, "normal", TEXT_COLOR, 0.35),
        ("Straight-line time:", 13, "bold", ACCENT_ORANGE, 0.31),
        ("t = R/c ≈ 2.3 seconds", 16, "normal", TEXT_COLOR, 0.26),
        ("", 10, "normal", TEXT_COLOR, 0.20),
        ("Ratio:", 13, "bold", ACCENT_PINK, 0.16),
        ("170,000 yr / 2.3 s ≈ 2 × 10¹²", 14, "normal", TEXT_COLOR, 0.11),
        ("The Sun is opaque.", 12, "normal", ACCENT_RED, 0.04),
    ]

    for text, size, weight, color, ypos in info_text:
        style = "italic" if text == "The Sun is opaque." else "normal"
        ax2.text(0.05, ypos, text, fontsize=size, fontweight=weight,
                 fontstyle=style, color=color, transform=ax2.transAxes, va="top")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "random-walk.png",
                facecolor=DARK_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ random-walk.png")


# ═════════════════════════════════════════════════════════════
# Figure 3: Timescale Hierarchy
# Used in: R1 (Ages & Lifetimes)
# ═════════════════════════════════════════════════════════════
def make_timescale_hierarchy():
    """Compare the Sun's three clocks and emphasize their physical meaning."""
    fig, ax = plt.subplots(figsize=(13.2, 6.6), dpi=220)
    apply_slide_style(fig, ax)

    timescales = [
        {
            "symbol": r"$\tau_{\rm dyn}$",
            "value_s": 50.0 * 60.0,
            "label": "~50 min",
            "desc": "Dynamical response",
            "reservoir": "set by mean density",
            "color": SLIDE_TEAL,
        },
        {
            "symbol": r"$\tau_{\rm KH}$",
            "value_s": 3.0e7 * YEAR_S,
            "label": "~30 Myr",
            "desc": "Kelvin-Helmholtz cooling",
            "reservoir": r"gravitational/thermal reservoir $\,/\,L$",
            "color": SLIDE_ORANGE,
        },
        {
            "symbol": r"$\tau_{\rm nuc}$",
            "value_s": 1.0e10 * YEAR_S,
            "label": "~10 Gyr",
            "desc": "Hydrogen-burning lifetime",
            "reservoir": r"fusion energy reservoir $\,/\,L$",
            "color": SLIDE_ROSE,
        },
    ]

    references = [
        (3600.0, "1 hour", SLIDE_MUTED),
        (YEAR_S, "1 year", SLIDE_MUTED),
        (1.0e6 * YEAR_S, "1 Myr", SLIDE_MUTED),
        (1.0e9 * YEAR_S, "1 Gyr", SLIDE_MUTED),
        (13.8e9 * YEAR_S, "Age of universe", SLIDE_GOLD),
    ]
    y_positions = [2, 1, 0]

    for y_val, data in zip(y_positions, timescales):
        log_time = np.log10(data["value_s"])
        ax.hlines(y_val, 0.0, log_time, color=data["color"], linewidth=10, alpha=0.18)
        ax.hlines(y_val, 0.0, log_time, color=data["color"], linewidth=3.2)
        ax.plot(log_time, y_val, "o", color=data["color"], markersize=11,
                markeredgecolor=SLIDE_BG, markeredgewidth=1.8, zorder=5)

        ax.text(-0.7, y_val, data["symbol"], fontsize=18, color=data["color"],
                fontweight="bold", ha="right", va="center")
        ax.text(-3.6, y_val + 0.18, data["desc"], fontsize=12, color=SLIDE_TEXT,
                ha="left", va="center", fontweight="bold")
        ax.text(-3.6, y_val - 0.16, data["reservoir"], fontsize=10.2,
                color=SLIDE_MUTED, ha="left", va="center")
        ax.text(log_time + 0.35, y_val + 0.03, data["label"], fontsize=15,
                color=data["color"], fontweight="bold", va="center",
                path_effects=[pe.withStroke(linewidth=3, foreground=SLIDE_BG)])

    for ref_time, label, color in references:
        log_time = np.log10(ref_time)
        ax.axvline(log_time, color=color, linewidth=0.95, alpha=0.7, linestyle=(0, (2, 3)))
        ax.text(log_time, 2.7, label, fontsize=8.8, color=color, ha="center", va="bottom")

    arrows = [
        (np.log10(50.0 * 60.0), np.log10(3.0e7 * YEAR_S), 1.45, r"$\times 3\times10^{11}$"),
        (np.log10(3.0e7 * YEAR_S), np.log10(1.0e10 * YEAR_S), 0.45, r"$\times 300$"),
    ]
    for x1, x2, y_val, label in arrows:
        ax.annotate("", xy=(x2, y_val), xytext=(x1, y_val),
                    arrowprops=dict(arrowstyle="<->", color=SLIDE_GOLD, lw=1.5))
        ax.text((x1 + x2) / 2.0, y_val + 0.12, label, fontsize=11, color=SLIDE_GOLD,
                ha="center", fontweight="bold")

    ax.text(0.5, 1.035,
            r"$\tau_{\rm dyn} \ll \tau_{\rm KH} \ll \tau_{\rm nuc}$"
            " because stars restore force balance much faster than they leak or burn energy.",
            transform=ax.transAxes, fontsize=10.8, color=SLIDE_MUTED,
            ha="center", va="bottom")

    ax.set_xlim(-4.2, 18.8)
    ax.set_ylim(-0.5, 3.0)
    ax.set_xlabel(r"$\log_{10}(\mathrm{time/s})$", fontsize=14)
    ax.set_yticks([])
    ax.set_title("Three Stellar Clocks for the Sun", fontsize=19, fontweight="bold", pad=15)

    fig.tight_layout()
    save_slide_figure(fig, "timescale-hierarchy.png")


# ═════════════════════════════════════════════════════════════
# Figure 4: Stellar Timescales vs Mass
# Used in: L1/R1 (Ages & Lifetimes)
# ═════════════════════════════════════════════════════════════
def make_timescales_vs_mass():
    """Plot the three stellar clocks with honest low- and high-mass caveats."""
    masses = np.logspace(np.log10(0.1), np.log10(30.0), 600)
    model = solar_normalized_timescales(masses)

    fig, ax = plt.subplots(figsize=(12.5, 7.2), dpi=220)
    apply_slide_style(fig, ax)
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.plot(masses, model["tau_dyn"], color=SLIDE_TEAL, linewidth=3.0, label=r"$\tau_{\rm dyn}$")
    ax.plot(masses, model["tau_kh"], color=SLIDE_ORANGE, linewidth=3.0, label=r"$\tau_{\rm KH}$")
    ax.plot(masses, model["tau_nuc"], color=SLIDE_ROSE, linewidth=3.0, label=r"$\tau_{\rm nuc}$")

    ax.axvspan(0.1, 0.35, color=SLIDE_TEAL, alpha=0.06, zorder=0)
    ax.axvspan(15.0, 30.0, color=SLIDE_GOLD, alpha=0.06, zorder=0)
    ax.text(0.14, 3.0e11, "low-mass caveat:\nfull convection\nextends lifetimes",
            fontsize=9.8, color=SLIDE_TEAL, ha="left", va="top")
    ax.text(16.3, 3.0e11, "high-mass caveat:\n$L(M)$ flattens,\nso lifetimes are longer\nthan naive extrapolation",
            fontsize=9.6, color=SLIDE_GOLD, ha="left", va="top")

    ax.axhline(13.8e9, color=SLIDE_GOLD, linestyle=(0, (4, 3)), linewidth=1.6, alpha=0.9)
    ax.text(30.0, 13.8e9 * 1.06, "age of universe", color=SLIDE_GOLD,
            fontsize=10.4, fontweight="bold", ha="right", va="bottom")

    for color, y_val in [(SLIDE_TEAL, model["tau_dyn"][np.argmin(np.abs(masses - 1.0))]),
                         (SLIDE_ORANGE, model["tau_kh"][np.argmin(np.abs(masses - 1.0))]),
                         (SLIDE_ROSE, model["tau_nuc"][np.argmin(np.abs(masses - 1.0))])]:
        ax.plot(1.0, y_val, "o", color=color, markersize=8.5,
                markeredgecolor=SLIDE_BG, markeredgewidth=1.4, zorder=5)
    ax.text(1.08, 1.8e10, "Sun", color=SLIDE_TEXT, fontsize=11, fontweight="bold")

    ax.text(0.13, 2.2e-4, r"$\tau_{\rm dyn}$", color=SLIDE_TEAL, fontsize=12, fontweight="bold")
    ax.text(0.13, 2.5e7, r"$\tau_{\rm KH}$", color=SLIDE_ORANGE, fontsize=12, fontweight="bold")
    ax.text(4.2, 3.0e8, r"$\tau_{\rm nuc}$", color=SLIDE_ROSE, fontsize=12, fontweight="bold")

    ax.text(0.98, 0.04,
            "Order-of-magnitude main-sequence model: piecewise $L(M)$, approximate $R(M)$,\n"
            "and a larger accessible-fuel fraction for fully convective low-mass stars.",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=9.4, color=SLIDE_MUTED)

    ax.set_xlabel(r"Stellar Mass ($M/M_\odot$)", fontsize=14)
    ax.set_ylabel("Timescale (yr)", fontsize=14)
    ax.set_xlim(0.1, 30.0)
    ax.set_ylim(1.0e-6, 5.0e11)
    ax.set_title("How the Three Stellar Clocks Change with Mass",
                 fontsize=19, fontweight="bold", pad=12)
    ax.legend(loc="lower left", frameon=False, fontsize=10.5)

    fig.tight_layout()
    save_slide_figure(fig, "timescales-vs-mass.png")


# ═════════════════════════════════════════════════════════════
# Figure 5: Onion-Shell Burning Structure
# Used in: R9 (High-Mass Evolution & Supernovae)
# ═════════════════════════════════════════════════════════════
def make_onion_shell():
    """
    Concentric shells of a massive star just before core collapse.

    Each shell burns a different fuel at a different temperature,
    with timescales that accelerate from millions of years to a single day.
    """
    fig, ax = plt.subplots(figsize=(10, 10), dpi=200, subplot_kw={"aspect": "equal"})
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.axis("off")

    shells = [
        {"fuel": "H → He", "T": "20 MK", "time": "~7 Myr",
         "r": 1.0, "color": "#3b82f6", "alpha": 0.25},
        {"fuel": "He → C, O", "T": "200 MK", "time": "~700,000 yr",
         "r": 0.82, "color": "#06b6d4", "alpha": 0.30},
        {"fuel": "C → Ne, Na, Mg", "T": "800 MK", "time": "~600 yr",
         "r": 0.65, "color": "#22c55e", "alpha": 0.30},
        {"fuel": "Ne → O, Mg", "T": "1.5 GK", "time": "~1 yr",
         "r": 0.50, "color": "#eab308", "alpha": 0.35},
        {"fuel": "O → Si, S", "T": "2 GK", "time": "~6 months",
         "r": 0.38, "color": "#f97316", "alpha": 0.40},
        {"fuel": "Si → Fe", "T": "3.5 GK", "time": "~1 day",
         "r": 0.26, "color": "#ef4444", "alpha": 0.45},
        {"fuel": "Fe core", "T": "~8 GK", "time": "INERT",
         "r": 0.14, "color": "#9f1239", "alpha": 0.8},
    ]

    # Draw shells from outside in
    for shell in shells:
        circle = plt.Circle((0, 0), shell["r"], facecolor=shell["color"],
                            alpha=shell["alpha"], edgecolor=shell["color"],
                            linewidth=1.5, zorder=2)
        ax.add_patch(circle)

    # Iron core glow effect
    for r_frac in np.linspace(0.14, 0.02, 8):
        glow = plt.Circle((0, 0), r_frac, facecolor=ACCENT_RED,
                          alpha=0.08, edgecolor="none", zorder=3)
        ax.add_patch(glow)

    # Labels: fuel on left, timescale on right
    label_angles_left = [150, 140, 130, 120, 110, 100]
    label_angles_right = [30, 40, 50, 60, 70, 80]

    for i, shell in enumerate(shells[:-1]):  # skip Fe core (labeled separately)
        # Midpoint radius between this shell and next
        r_mid = (shell["r"] + shells[i + 1]["r"]) / 2

        # Fuel label on left
        angle_l = np.radians(label_angles_left[i])
        x_l = r_mid * np.cos(angle_l)
        y_l = r_mid * np.sin(angle_l)

        # Arrow to outside
        x_out = (shell["r"] + 0.12) * np.cos(angle_l)
        y_out = (shell["r"] + 0.12) * np.sin(angle_l)

        ax.annotate(
            f"{shell['fuel']}\n{shell['T']}",
            xy=(x_l, y_l), xytext=(x_out, y_out),
            fontsize=9, color=shell["color"], fontweight="bold",
            ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color=shell["color"],
                            lw=1, alpha=0.5),
        )

        # Timescale label on right
        angle_r = np.radians(label_angles_right[i])
        x_r = (shell["r"] + 0.15) * np.cos(angle_r)
        y_r = (shell["r"] + 0.15) * np.sin(angle_r)
        ax.text(x_r, y_r, shell["time"], fontsize=9,
                color=shell["color"], ha="center", va="center",
                alpha=0.8, fontstyle="italic")

    # Fe core label
    ax.text(0, 0, "Fe\ncore", fontsize=14, color="white",
            ha="center", va="center", fontweight="bold", zorder=5)
    ax.text(0, -0.20, "INERT\n(nuclear ash)", fontsize=8, color=ACCENT_RED,
            ha="center", va="center", zorder=5, alpha=0.8)

    # Title and subtitle
    ax.text(0, 1.15, "Onion-Shell Structure", fontsize=20,
            color=TEXT_COLOR, ha="center", va="center", fontweight="bold")
    ax.text(0, 1.07, "A 25 M☉ star, moments before core collapse",
            fontsize=12, color=MUTED_TEXT, ha="center", va="center")

    # Time acceleration note
    ax.text(
        0, -1.12,
        "Each layer burns faster than the last:\n"
        "H burning lasts millions of years  →  Si burning lasts one day",
        fontsize=10, color=ACCENT_ORANGE, ha="center", va="center",
        fontstyle="italic",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=DARK_BG,
                  edgecolor=ACCENT_ORANGE, alpha=0.5),
    )

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "onion-shell-burning.png",
                facecolor=DARK_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ onion-shell-burning.png")


# ═════════════════════════════════════════════════════════════
# Figure 5: White Dwarf Mass-Radius Relation
# Used in: R8 (Degeneracy & Chandrasekhar Limit)
# ═════════════════════════════════════════════════════════════
def make_wd_mass_radius():
    """
    White dwarf mass-radius relation R ∝ M^{-1/3},
    showing the approach to the Chandrasekhar limit.

    Uses the full relativistic Chandrasekhar equation
    (simplified form) showing the radius going to zero at M_Ch.
    """
    fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
    apply_dark_style(fig, ax)

    M_ch = 1.44  # Chandrasekhar mass in solar masses

    # Non-relativistic regime: R ∝ M^{-1/3}
    # Normalized so R(0.6 M_sun) ≈ 1 R_earth ≈ 0.009 R_sun
    R_earth = 0.00916  # R_earth / R_sun
    M_ref = 0.6
    R_0 = R_earth / M_ref**(-1/3)

    M_nr = np.linspace(0.15, 1.2, 200)
    R_nr = R_0 * M_nr**(-1/3)

    # Relativistic correction: R → 0 as M → M_Ch
    # Use approximate formula: R ∝ M^{-1/3} * (1 - (M/M_Ch)^{4/3})^{1/2}
    M_full = np.linspace(0.15, 1.43, 500)
    R_full = R_0 * M_full**(-1/3) * np.sqrt(np.maximum(0, 1 - (M_full / M_ch)**(4/3)))

    # Plot both
    ax.plot(M_nr, R_nr / R_earth, "--", color=ACCENT_CYAN, linewidth=1.5,
            alpha=0.4, label=r"Non-relativistic: $R \propto M^{-1/3}$")
    ax.plot(M_full, R_full / R_earth, "-", color=ACCENT_CYAN, linewidth=3,
            label="Full relativistic", zorder=4)

    # Chandrasekhar limit vertical line
    ax.axvline(M_ch, color=ACCENT_RED, linewidth=2, linestyle="--",
               alpha=0.7, zorder=3)
    ax.text(M_ch + 0.02, 1.8, f"$M_{{\\rm Ch}} = {M_ch}\\,M_\\odot$",
            fontsize=14, color=ACCENT_RED, fontweight="bold", rotation=0)
    ax.text(M_ch + 0.02, 1.6, "Chandrasekhar\nlimit", fontsize=10,
            color=ACCENT_RED, alpha=0.8)

    # Key white dwarfs
    known_wds = [
        (0.50, "Sirius B\n(0.50 M☉)", ACCENT_YELLOW),
        (1.02, "Sirius B*\n(1.02 M☉)", ACCENT_YELLOW),
        (0.60, "Typical WD\n(0.60 M☉)", ACCENT_GREEN),
    ]
    # Actually, Sirius B is 1.02 M_sun. Let me use correct values.
    known_wds = [
        (1.02, "Sirius B", ACCENT_YELLOW),
        (0.60, "Typical WD", ACCENT_GREEN),
    ]
    for M_wd, label, color in known_wds:
        R_wd = R_0 * M_wd**(-1/3) * np.sqrt(max(0, 1 - (M_wd / M_ch)**(4/3)))
        ax.plot(M_wd, R_wd / R_earth, "o", color=color, markersize=10,
                markeredgecolor="white", markeredgewidth=1.5, zorder=6)
        offset = (10, 10) if M_wd < 0.8 else (10, 10)
        ax.annotate(
            label, (M_wd, R_wd / R_earth), xytext=offset,
            textcoords="offset points", fontsize=10, color=color,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=color, lw=1),
        )

    # Annotations
    ax.annotate(
        "More mass → smaller WD!\n(counter-intuitive)",
        xy=(0.9, 0.75), xytext=(0.25, 0.5),
        fontsize=11, color=ACCENT_ORANGE, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=ACCENT_ORANGE, lw=1.5),
        bbox=dict(boxstyle="round,pad=0.3", facecolor=DARK_BG,
                  edgecolor=ACCENT_ORANGE, alpha=0.8),
    )

    # Earth reference
    ax.axhline(1.0, color=ACCENT_GREEN, linewidth=0.8, alpha=0.3, linestyle=":")
    ax.text(0.17, 1.03, "$R_\\oplus$", fontsize=10, color=ACCENT_GREEN, alpha=0.5)

    # "Gravity wins" region
    ax.fill_betweenx([0, 2.2], M_ch, 1.6, color=ACCENT_RED,
                     alpha=0.05, zorder=1)
    ax.text(1.50, 0.3, "GRAVITY\nWINS", fontsize=14, color=ACCENT_RED,
            ha="center", fontweight="bold", alpha=0.4)

    ax.set_xlabel(r"White Dwarf Mass ($M / M_\odot$)", fontsize=14)
    ax.set_ylabel(r"White Dwarf Radius ($R / R_\oplus$)", fontsize=14)
    ax.set_title("White Dwarf Mass-Radius Relation", fontsize=18,
                 fontweight="bold", pad=15)
    ax.set_xlim(0.1, 1.6)
    ax.set_ylim(0, 2.2)
    ax.legend(fontsize=11, loc="upper right",
              facecolor=PANEL_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "wd-mass-radius.png",
                facecolor=DARK_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ wd-mass-radius.png")


# ═════════════════════════════════════════════════════════════
# Figure 6: Compact Object Scale Comparison
# Used in: R10 (Neutron Stars & Black Holes)
# ═════════════════════════════════════════════════════════════
def make_compact_object_scale():
    """
    Size comparison of Earth, white dwarf, neutron star,
    and stellar-mass black hole (Schwarzschild radius).

    Radii in km:
      Earth:  6,371 km
      WD:     ~6,000 km (typical 0.6 M_sun)
      NS:     ~10 km
      BH (3 M_sun): R_s = 8.9 km
    """
    fig, ax = plt.subplots(figsize=(14, 7), dpi=200)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.axis("off")

    objects = [
        {
            "name": "Earth",
            "radius_km": 6371,
            "color": ACCENT_BLUE,
            "x": 0.13,
            "notes": "R = 6,371 km\nρ ~ 5.5 g/cm³",
        },
        {
            "name": "White Dwarf",
            "radius_km": 6000,
            "color": ACCENT_CYAN,
            "x": 0.38,
            "notes": "R ~ 6,000 km\nM ~ 0.6 M☉\nρ ~ 10⁶ g/cm³",
        },
        {
            "name": "Neutron Star",
            "radius_km": 10,
            "color": ACCENT_ORANGE,
            "x": 0.63,
            "notes": "R ~ 10 km\nM ~ 1.4 M☉\nρ ~ 10¹⁴ g/cm³",
        },
        {
            "name": "Black Hole\n(3 M☉)",
            "radius_km": 8.9,
            "color": ACCENT_RED,
            "x": 0.85,
            "notes": "Rₛ = 8.9 km\nM = 3 M☉\nρ → ∞ (singularity)",
        },
    ]

    # Max visual radius for the figure (data coords)
    max_visual_r = 0.12
    max_real_r = max(o["radius_km"] for o in objects)
    y_center = 0.45

    for obj in objects:
        x = obj["x"]
        r_real = obj["radius_km"]

        # Use log-ish scaling so tiny objects are still visible
        # but proportions are conveyed
        if r_real > 100:
            r_visual = max_visual_r * (r_real / max_real_r)
        else:
            # NS and BH are ~10 km; show them small but visible
            r_visual = 0.008

        # Draw the object
        if obj["name"].startswith("Black"):
            # Black hole: dark circle with bright ring
            bh = plt.Circle((x, y_center), r_visual, facecolor="black",
                            edgecolor=ACCENT_RED, linewidth=2, zorder=5)
            ax.add_patch(bh)
            # Accretion ring glow
            for dr in [0.003, 0.006, 0.009]:
                glow = plt.Circle((x, y_center), r_visual + dr,
                                  facecolor="none", edgecolor=ACCENT_ORANGE,
                                  linewidth=1, alpha=0.3 - dr * 20, zorder=4)
                ax.add_patch(glow)
        elif obj["name"] == "Neutron Star":
            # Neutron star: small bright orange dot
            ns = plt.Circle((x, y_center), r_visual, facecolor=ACCENT_ORANGE,
                            edgecolor="white", linewidth=1.5, zorder=5)
            ax.add_patch(ns)
            # Glow effect
            for dr in [0.005, 0.010, 0.015]:
                glow = plt.Circle((x, y_center), r_visual + dr,
                                  facecolor=ACCENT_ORANGE,
                                  alpha=0.1, edgecolor="none", zorder=3)
                ax.add_patch(glow)
        else:
            circle = plt.Circle((x, y_center), r_visual,
                                facecolor=obj["color"], alpha=0.4,
                                edgecolor=obj["color"], linewidth=2, zorder=5)
            ax.add_patch(circle)

        # Name
        ax.text(x, y_center + max_visual_r + 0.06, obj["name"],
                fontsize=14, color=obj["color"], ha="center", va="bottom",
                fontweight="bold")

        # Notes below
        ax.text(x, y_center - max_visual_r - 0.06, obj["notes"],
                fontsize=10, color=obj["color"], ha="center", va="top",
                alpha=0.8)

    # Title
    ax.text(0.5, 0.97, "Compact Objects: A Scale Comparison",
            fontsize=20, color=TEXT_COLOR, ha="center", va="top",
            fontweight="bold", transform=ax.transAxes)

    # Scale note
    ax.text(
        0.5, 0.03,
        "A white dwarf packs a star's mass into an Earth-sized sphere.  "
        "A neutron star packs it into a city.  "
        "A black hole has no surface at all.",
        fontsize=11, color=MUTED_TEXT, ha="center", va="bottom",
        fontstyle="italic", transform=ax.transAxes,
    )

    # "Not to scale" with arrow between WD and NS
    ax.annotate(
        "×600 smaller!", xy=(0.52, y_center), xytext=(0.52, y_center + 0.04),
        fontsize=10, color=ACCENT_YELLOW, ha="center", fontweight="bold",
    )
    ax.annotate(
        "", xy=(0.63, y_center), xytext=(0.46, y_center),
        arrowprops=dict(arrowstyle="<->", color=ACCENT_YELLOW, lw=1.5, alpha=0.6),
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    fig.savefig(OUTPUT_DIR / "compact-object-scale.png",
                facecolor=DARK_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ compact-object-scale.png")


# ═════════════════════════════════════════════════════════════
# Figure 7: Stellar Structure Zones
# Used in: R5 (Stellar Structure & Scalings)
# ═════════════════════════════════════════════════════════════
def make_stellar_structure_zones():
    """
    Cross-section comparison: low-mass star (convective envelope,
    radiative core) vs. high-mass star (radiative envelope,
    convective core). The structural reversal is a key insight.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), dpi=200,
                             subplot_kw={"aspect": "equal"})
    fig.patch.set_facecolor(DARK_BG)

    def draw_star(ax, title, subtitle, inner_r, inner_color, inner_label,
                  outer_color, outer_label, inner_pattern, outer_pattern):
        ax.set_facecolor(DARK_BG)
        ax.axis("off")

        # Outer envelope
        outer = plt.Circle((0, 0), 1.0, facecolor=outer_color, alpha=0.25,
                           edgecolor=outer_color, linewidth=2)
        ax.add_patch(outer)

        # Inner core
        core = plt.Circle((0, 0), inner_r, facecolor=inner_color, alpha=0.4,
                          edgecolor=inner_color, linewidth=2)
        ax.add_patch(core)

        # Pattern indicators
        if inner_pattern == "radiative":
            # Wavy arrows for radiative transport
            for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
                r1 = inner_r * 0.3
                r2 = inner_r * 0.8
                x1, y1 = r1 * np.cos(angle), r1 * np.sin(angle)
                x2, y2 = r2 * np.cos(angle), r2 * np.sin(angle)
                ax.annotate(
                    "", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="white",
                                    lw=0.8, alpha=0.3),
                )
                # Wiggly line (tilde)
                ax.text((x1+x2)/2, (y1+y2)/2, "~", fontsize=6,
                        color="white", alpha=0.3, ha="center", va="center",
                        rotation=np.degrees(angle))
        else:
            # Circular arrows for convection
            for angle in [0.3, 1.3, 2.3, 3.3, 4.3, 5.3]:
                r = inner_r * 0.6
                x_c = r * np.cos(angle)
                y_c = r * np.sin(angle)
                arc = mpatches.Arc((x_c, y_c), inner_r * 0.3, inner_r * 0.3,
                                   angle=np.degrees(angle), theta1=0, theta2=270,
                                   color="white", alpha=0.3, linewidth=0.8)
                ax.add_patch(arc)

        if outer_pattern == "radiative":
            for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
                r1 = inner_r + (1 - inner_r) * 0.2
                r2 = inner_r + (1 - inner_r) * 0.8
                x1, y1 = r1 * np.cos(angle), r1 * np.sin(angle)
                x2, y2 = r2 * np.cos(angle), r2 * np.sin(angle)
                ax.annotate(
                    "", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="white",
                                    lw=0.8, alpha=0.2),
                )
        else:
            for angle in np.linspace(0, 2*np.pi, 10, endpoint=False):
                r = inner_r + (1 - inner_r) * 0.5
                x_c = r * np.cos(angle)
                y_c = r * np.sin(angle)
                circ_r = (1 - inner_r) * 0.15
                arc = mpatches.Arc((x_c, y_c), circ_r, circ_r,
                                   angle=np.degrees(angle), theta1=0, theta2=270,
                                   color="white", alpha=0.2, linewidth=0.8)
                ax.add_patch(arc)

        # Labels
        ax.text(0, 0, inner_label, fontsize=11, color="white",
                ha="center", va="center", fontweight="bold")
        mid_r = (inner_r + 1) / 2
        ax.text(mid_r * 0.7, -mid_r * 0.7, outer_label, fontsize=10,
                color="white", ha="center", va="center", fontweight="bold",
                alpha=0.8)

        ax.text(0, 1.2, title, fontsize=16, color=TEXT_COLOR,
                ha="center", va="center", fontweight="bold")
        ax.text(0, 1.08, subtitle, fontsize=11, color=MUTED_TEXT,
                ha="center", va="center")

        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)

    # Low-mass star: radiative core + convective envelope
    draw_star(
        axes[0],
        "Low-Mass Star", "(M ≲ 1.5 M☉, e.g., the Sun)",
        inner_r=0.35,
        inner_color=ACCENT_YELLOW,
        inner_label="Radiative\ncore",
        outer_color=ACCENT_ORANGE,
        outer_label="Convective\nenvelope",
        inner_pattern="radiative",
        outer_pattern="convective",
    )

    # High-mass star: convective core + radiative envelope
    draw_star(
        axes[1],
        "High-Mass Star", "(M ≳ 1.5 M☉, e.g., 10 M☉)",
        inner_r=0.45,
        inner_color=ACCENT_CYAN,
        inner_label="Convective\ncore",
        outer_color=ACCENT_BLUE,
        outer_label="Radiative\nenvelope",
        inner_pattern="convective",
        outer_pattern="radiative",
    )

    # Connecting text
    fig.text(
        0.5, 0.02,
        "The transport mechanism reverses between low-mass and high-mass stars:\n"
        "low-mass stars have radiative cores and convective envelopes; "
        "high-mass stars have the opposite.",
        fontsize=11, color=ACCENT_ORANGE, ha="center", va="bottom",
        fontstyle="italic",
    )

    fig.suptitle("Internal Structure of Main-Sequence Stars",
                 fontsize=20, color=TEXT_COLOR, fontweight="bold", y=0.98)

    fig.tight_layout(rect=[0, 0.06, 1, 0.94])
    fig.savefig(OUTPUT_DIR / "stellar-structure-zones.png",
                facecolor=DARK_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ stellar-structure-zones.png")


# ═════════════════════════════════════════════════════════════
# Figure 8: Mass Limits Spectrum
# Used in: R6 (Mass Limits)
# ═════════════════════════════════════════════════════════════
def make_mass_limits():
    """
    Stellar mass spectrum from brown dwarfs to the most massive stars.
    Shows the quantum floor (0.08 M_sun) and radiation ceiling (~150 M_sun).
    """
    fig, ax = plt.subplots(figsize=(14, 5), dpi=200)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)

    # Mass range (log scale)
    log_m = np.linspace(-1.5, 2.5, 1000)

    # IMF: approximate Salpeter-like shape for visual
    # dN/dM ∝ M^{-2.35}
    imf = 10**((-2.35) * log_m)
    imf = imf / imf.max() * 0.8

    # Plot IMF as filled area
    ax.fill_between(log_m, 0, imf, alpha=0.15, color=ACCENT_BLUE)
    ax.plot(log_m, imf, color=ACCENT_BLUE, linewidth=1.5, alpha=0.5)

    # Key boundaries
    boundaries = [
        (-1.1, "H-burning\nminimum\n0.08 M☉", ACCENT_CYAN,
         "QM floor:\nDegeneracy halts\ncontraction before\nfusion ignites"),
        (0, "1 M☉\n(Sun)", ACCENT_YELLOW, None),
        (2.18, "Eddington\nlimit\n~150 M☉", ACCENT_RED,
         "Radiation ceiling:\nL_rad > L_Edd\ntears star apart"),
    ]

    for log_m_val, label, color, note in boundaries:
        ax.axvline(log_m_val, color=color, linewidth=2 if note else 1.5,
                   linestyle="--" if note else ":", alpha=0.7, zorder=3)
        y_top = 0.9 if note else 0.85
        ax.text(log_m_val, y_top, label, fontsize=11, color=color,
                ha="center", va="top", fontweight="bold")
        if note:
            side = -0.35 if log_m_val < 0 else 0.15
            ax.text(log_m_val + side, 0.55, note, fontsize=9, color=color,
                    ha="center" if log_m_val < 0 else "left", va="top",
                    alpha=0.7,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=DARK_BG,
                              edgecolor=color, alpha=0.5))

    # Regions
    regions = [
        (-1.5, -1.1, "Brown\nDwarfs", ACCENT_PURPLE, 0.05),
        (-1.1, 2.18, "Hydrogen-Burning Stars", ACCENT_BLUE, 0.03),
    ]
    for x1, x2, label, color, alpha in regions:
        ax.axvspan(x1, x2, alpha=alpha, color=color, zorder=1)
        ax.text((x1 + x2) / 2, 0.02, label, fontsize=10, color=color,
                ha="center", va="bottom", alpha=0.6)

    # Specific objects
    objects = [
        (-1.3, "Jupiter\n(0.001 M☉)", MUTED_TEXT),
        (-0.6, "M dwarf\n(0.25 M☉)", ACCENT_RED),
        (0.3, "Sirius\n(2 M☉)", ACCENT_CYAN),
        (1.3, "Spica\n(20 M☉)", ACCENT_BLUE),
    ]
    for log_m_val, label, color in objects:
        imf_val = 10**((-2.35) * log_m_val) / (10**((-2.35) * (-1.5))) * 0.8
        ax.plot(log_m_val, imf_val, "o", color=color, markersize=8,
                markeredgecolor="white", markeredgewidth=1, zorder=5)
        ax.text(log_m_val, imf_val + 0.03, label, fontsize=8, color=color,
                ha="center", va="bottom")

    ax.set_xlabel(r"$\log_{10}(M / M_\odot)$", fontsize=14, color=TEXT_COLOR)
    ax.set_ylabel("Relative Number\n(IMF shape)", fontsize=12, color=TEXT_COLOR)
    ax.set_title("The Stellar Mass Spectrum", fontsize=18,
                 color=TEXT_COLOR, fontweight="bold", pad=15)
    ax.set_xlim(-1.5, 2.5)
    ax.set_ylim(0, 1.0)
    ax.tick_params(colors=MUTED_TEXT)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "mass-limits-spectrum.png",
                facecolor=DARK_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ mass-limits-spectrum.png")


# ═════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating Module 3 figures → {OUTPUT_DIR}/\n")

    make_binding_energy_curve()
    make_random_walk()
    make_timescale_hierarchy()
    make_timescales_vs_mass()
    make_onion_shell()
    make_wd_mass_radius()
    make_compact_object_scale()
    make_stellar_structure_zones()
    make_mass_limits()

    print(f"\n✓ All figures saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
