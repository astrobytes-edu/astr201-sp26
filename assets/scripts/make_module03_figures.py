#!/usr/bin/env python3
"""
Generate pedagogical figures for ASTR 201 Module 3: Stellar Structure & Evolution.

Produces publication-quality, dark-themed figures matching the NASA infographic
aesthetic used elsewhere in the module. All physics is in CGS/solar units.

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


# ═════════════════════════════════════════════════════════════
# Figure 1: Binding Energy per Nucleon
# Used in: R3 (Nuclear Fusion), R9 (High-Mass Evolution)
# ═════════════════════════════════════════════════════════════
def make_binding_energy_curve():
    """
    Binding energy per nucleon vs. mass number A.

    Uses real nuclear data for key isotopes. The iron peak is the
    central story: fusion releases energy LEFT of iron, fission
    releases energy RIGHT of iron. Iron is nuclear ash.
    """
    # Real binding energy per nucleon data (MeV) for key isotopes
    # Source: Nuclear physics tables (AME2020)
    isotopes = [
        (1, 0.0, r"$^1$H", MUTED_TEXT),
        (2, 1.112, r"$^2$H", MUTED_TEXT),
        (3, 2.827, r"$^3$He", MUTED_TEXT),
        (4, 7.074, r"$^4$He", ACCENT_CYAN),
        (6, 5.333, r"$^6$Li", MUTED_TEXT),
        (7, 5.606, r"$^7$Li", MUTED_TEXT),
        (9, 6.463, r"$^9$Be", MUTED_TEXT),
        (12, 7.680, r"$^{12}$C", ACCENT_GREEN),
        (14, 7.476, r"$^{14}$N", MUTED_TEXT),
        (16, 7.976, r"$^{16}$O", ACCENT_GREEN),
        (20, 8.032, r"$^{20}$Ne", MUTED_TEXT),
        (24, 8.261, r"$^{24}$Mg", MUTED_TEXT),
        (28, 8.448, r"$^{28}$Si", ACCENT_ORANGE),
        (32, 8.493, r"$^{32}$S", MUTED_TEXT),
        (40, 8.551, r"$^{40}$Ca", MUTED_TEXT),
        (56, 8.790, r"$^{56}$Fe", ACCENT_RED),
        (58, 8.792, r"$^{58}$Ni", MUTED_TEXT),
        (62, 8.794, r"$^{62}$Ni", MUTED_TEXT),
        (80, 8.565, r"$^{80}$Se", MUTED_TEXT),
        (107, 8.554, r"$^{107}$Ag", MUTED_TEXT),
        (120, 8.505, r"$^{120}$Sn", MUTED_TEXT),
        (138, 8.376, r"$^{138}$Ba", MUTED_TEXT),
        (184, 7.999, r"$^{184}$W", MUTED_TEXT),
        (197, 7.916, r"$^{197}$Au", ACCENT_YELLOW),
        (208, 7.868, r"$^{208}$Pb", MUTED_TEXT),
        (235, 7.591, r"$^{235}$U", ACCENT_PURPLE),
        (238, 7.570, r"$^{238}$U", MUTED_TEXT),
    ]

    A_vals = np.array([iso[0] for iso in isotopes])
    BE_vals = np.array([iso[1] for iso in isotopes])

    fig, ax = plt.subplots(figsize=(12, 7), dpi=200)
    apply_dark_style(fig, ax)

    # Smooth interpolation for the curve
    from scipy.interpolate import make_interp_spline
    A_smooth = np.linspace(1, 240, 500)
    spl = make_interp_spline(A_vals, BE_vals, k=3)
    BE_smooth = spl(A_smooth)

    # Color the curve: blue (fusion releases energy) left of Fe,
    # purple (fission releases energy) right of Fe
    fe_idx = np.argmin(np.abs(A_smooth - 56))

    ax.plot(A_smooth[:fe_idx+1], BE_smooth[:fe_idx+1],
            color=ACCENT_CYAN, linewidth=2.5, zorder=3)
    ax.plot(A_smooth[fe_idx:], BE_smooth[fe_idx:],
            color=ACCENT_PURPLE, linewidth=2.5, zorder=3)

    # Plot key isotopes as points
    for A, BE, label, color in isotopes:
        marker_size = 8 if color != MUTED_TEXT else 5
        ax.plot(A, BE, "o", color=color, markersize=marker_size,
                markeredgecolor="white", markeredgewidth=0.5, zorder=5)

    # Label key isotopes with offsets to avoid overlap
    label_offsets = {
        1: (5, -12), 2: (5, -10), 4: (5, 5), 12: (-2, 7),
        16: (5, 5), 28: (-2, -14), 56: (5, 5), 62: (7, -8),
        197: (5, 5), 235: (-10, -14),
    }
    for A, BE, label, color in isotopes:
        if A in label_offsets:
            dx, dy = label_offsets[A]
            fontsize = 12 if color != MUTED_TEXT else 9
            ax.annotate(
                label, (A, BE), xytext=(dx, dy),
                textcoords="offset points", fontsize=fontsize,
                color=color, fontweight="bold" if color != MUTED_TEXT else "normal",
            )

    # Iron peak annotation
    ax.annotate(
        "Iron peak\n(most stable nucleus)",
        xy=(56, 8.79), xytext=(100, 9.2),
        fontsize=12, color=ACCENT_RED, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.5),
        ha="center",
    )

    # Fusion / fission arrows
    ax.annotate(
        "", xy=(15, 3.5), xytext=(50, 3.5),
        arrowprops=dict(arrowstyle="<-", color=ACCENT_CYAN, lw=2.5),
    )
    ax.text(32, 3.8, "FUSION releases energy",
            fontsize=11, color=ACCENT_CYAN, ha="center", fontstyle="italic")
    ax.text(32, 3.0, r"(climbing $\uparrow$ the curve)",
            fontsize=9, color=ACCENT_CYAN, ha="center", alpha=0.8)

    ax.annotate(
        "", xy=(200, 3.5), xytext=(70, 3.5),
        arrowprops=dict(arrowstyle="<-", color=ACCENT_PURPLE, lw=2.5),
    )
    ax.text(140, 3.8, "FISSION releases energy",
            fontsize=11, color=ACCENT_PURPLE, ha="center", fontstyle="italic")
    ax.text(140, 3.0, r"(descending $\downarrow$ the curve)",
            fontsize=9, color=ACCENT_PURPLE, ha="center", alpha=0.8)

    # Nucleosynthesis annotations
    ax.axvspan(1, 4.5, alpha=0.05, color=ACCENT_CYAN, zorder=1)
    ax.axvspan(4.5, 16.5, alpha=0.05, color=ACCENT_GREEN, zorder=1)
    ax.axvspan(16.5, 56, alpha=0.05, color=ACCENT_ORANGE, zorder=1)

    ax.text(2.5, 1.0, "pp-chain\n(main seq.)", fontsize=8,
            color=ACCENT_CYAN, ha="center", alpha=0.7)
    ax.text(10, 1.0, "He burning\n(red giant)", fontsize=8,
            color=ACCENT_GREEN, ha="center", alpha=0.7)
    ax.text(36, 1.0, "Successive\nburning\n(massive stars)", fontsize=8,
            color=ACCENT_ORANGE, ha="center", alpha=0.7)

    ax.set_xlabel("Mass Number, $A$", fontsize=14)
    ax.set_ylabel("Binding Energy per Nucleon (MeV)", fontsize=14)
    ax.set_title("Binding Energy per Nucleon", fontsize=18,
                 fontweight="bold", pad=15)
    ax.set_xlim(0, 250)
    ax.set_ylim(0, 9.5)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "binding-energy-curve.png",
                facecolor=DARK_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ binding-energy-curve.png")


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
    """
    Logarithmic comparison of the three fundamental stellar timescales.

    τ_dyn ~ 50 min, τ_KH ~ 30 Myr, τ_nuc ~ 10 Gyr for the Sun.
    The enormous separation is the key pedagogical point.
    """
    fig, ax = plt.subplots(figsize=(13, 6.4), dpi=220)
    apply_slide_style(fig, ax)

    # Timescales in seconds
    timescales = {
        r"$\tau_{\rm dyn}$": {
            "value_s": 3000,  # ~50 min
            "label": "~50 min",
            "desc": "Dynamical\n(free-fall)",
            "color": SLIDE_TEAL,
            "note": "pressure loss → collapse in ~50 min",
        },
        r"$\tau_{\rm KH}$": {
            "value_s": 9.5e14,  # ~30 Myr
            "label": "~30 Myr",
            "desc": "Thermal\n(Kelvin-Helmholtz)",
            "color": SLIDE_ORANGE,
            "note": "no fusion → Sun fades in ~30 Myr",
        },
        r"$\tau_{\rm nuc}$": {
            "value_s": 3.2e17,  # ~10 Gyr
            "label": "~10 Gyr",
            "desc": "Nuclear\n(main-sequence lifetime)",
            "color": SLIDE_ROSE,
            "note": "H fusion supports the Sun for ~10 Gyr",
        },
    }

    # Reference timescales for context
    references = [
        (3600, "1 hour", SLIDE_MUTED),
        (3.15e7, "1 year", SLIDE_MUTED),
        (3.15e7 * 1e6, "1 Myr", SLIDE_MUTED),
        (3.15e7 * 1e9, "1 Gyr", SLIDE_MUTED),
        (3.15e7 * 13.8e9, "Age of\nUniverse", SLIDE_GOLD),
    ]

    y_positions = [2, 1, 0]
    bar_height = 0.5

    for i, (symbol, data) in enumerate(timescales.items()):
        y = y_positions[i]
        log_val = np.log10(data["value_s"])

        ax.hlines(y, 0, log_val, color=data["color"], linewidth=8, alpha=0.16, zorder=2)
        ax.hlines(y, 0, log_val, color=data["color"], linewidth=2.8, zorder=3)

        ax.plot(log_val, y, "o", color=data["color"], markersize=10,
                markeredgecolor=SLIDE_BG, markeredgewidth=1.8, zorder=5)

        ax.text(-0.9, y, symbol, fontsize=18, color=data["color"],
                fontweight="bold", ha="right", va="center")

        ax.text(-3.0, y, data["desc"], fontsize=11, color=SLIDE_TEXT,
                ha="right", va="center", alpha=0.8)

        ax.text(log_val + 0.35, y, data["label"], fontsize=15,
                color=data["color"], fontweight="bold", va="center",
                path_effects=[pe.withStroke(linewidth=3, foreground=SLIDE_BG)])

        ax.text(log_val + 0.35, y - 0.24, data["note"], fontsize=10,
                color=SLIDE_MUTED, va="top")

    for val_s, label, color in references:
        log_val = np.log10(val_s)
        ax.axvline(log_val, color=color, linewidth=0.9, alpha=0.65, linestyle=(0, (2, 3)))
        ax.text(log_val, 2.68, label, fontsize=8.5, color=color,
                ha="center", va="bottom", alpha=0.95)

    mid_y = 1.5
    ax.annotate(
        "", xy=(np.log10(9.5e14), mid_y + 0.15),
        xytext=(np.log10(3000), mid_y + 0.15),
        arrowprops=dict(arrowstyle="<->", color=SLIDE_GOLD, lw=1.5),
    )
    ax.text(
        (np.log10(3000) + np.log10(9.5e14)) / 2, mid_y + 0.25,
        r"$\times\, 3\times 10^{11}$", fontsize=11, color=SLIDE_GOLD,
        ha="center", fontweight="bold",
    )

    mid_y2 = 0.5
    ax.annotate(
        "", xy=(np.log10(3.2e17), mid_y2 + 0.15),
        xytext=(np.log10(9.5e14), mid_y2 + 0.15),
        arrowprops=dict(arrowstyle="<->", color=SLIDE_GOLD, lw=1.5),
    )
    ax.text(
        (np.log10(9.5e14) + np.log10(3.2e17)) / 2, mid_y2 + 0.25,
        r"$\times\, 300$", fontsize=11, color=SLIDE_GOLD,
        ha="center", fontweight="bold",
    )

    ax.set_xlabel(r"$\log_{10}(\mathrm{time/s})$", fontsize=14)
    ax.set_xlim(-1.1, 18.8)
    ax.set_ylim(-0.5, 3.0)
    ax.set_yticks([])
    ax.set_title("Three Stellar Clocks for the Sun", fontsize=19,
                 fontweight="bold", pad=15)

    ax.text(
        0.5, 1.03,
        r"$\tau_{\rm dyn} \ll \tau_{\rm KH} \ll \tau_{\rm nuc}$"
        "  —  separated by many orders of magnitude",
        transform=ax.transAxes, fontsize=11, color=SLIDE_MUTED,
        ha="center", va="bottom",
    )

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "timescale-hierarchy.png",
                facecolor=SLIDE_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ timescale-hierarchy.png")


# ═════════════════════════════════════════════════════════════
# Figure 4: Stellar Timescales vs Mass
# Used in: L1/R1 (Ages & Lifetimes)
# ═════════════════════════════════════════════════════════════
def make_timescales_vs_mass():
    """
    Solar-normalized stellar timescales across the main sequence.

    Uses simple main-sequence scaling laws:
    - R ∝ M^0.8
    - L ∝ M^3.5

    This lets students see how each timescale changes with mass while
    keeping the Sun as the anchor.
    """
    masses = np.logspace(-1, 1.15, 400)  # 0.1 to ~14 M_sun

    # Main-sequence scaling relations (order-of-magnitude)
    radii = masses**0.8
    luminosities = masses**3.5

    # Solar anchors
    tau_dyn_sun_yr = 50 / (60 * 24 * 365.25)  # 50 min in years
    tau_kh_sun_yr = 3.0e7
    tau_nuc_sun_yr = 1.0e10

    # Ratio-method scalings relative to the Sun
    tau_dyn = tau_dyn_sun_yr * masses**(-0.5) * radii**1.5
    tau_kh = tau_kh_sun_yr * masses**2 * radii**(-1) * luminosities**(-1)
    tau_nuc = tau_nuc_sun_yr * masses * luminosities**(-1)

    fig, ax = plt.subplots(figsize=(12.4, 7.0), dpi=220)
    apply_slide_style(fig, ax)

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.plot(masses, tau_dyn, color=SLIDE_TEAL, linewidth=3.0)
    ax.plot(masses, tau_kh, color=SLIDE_ORANGE, linewidth=3.0)
    ax.plot(masses, tau_nuc, color=SLIDE_ROSE, linewidth=3.0)

    ax.plot(1, tau_dyn_sun_yr, "o", color=SLIDE_TEAL, markersize=8.5,
            markeredgecolor=SLIDE_BG, markeredgewidth=1.5, zorder=5)
    ax.plot(1, tau_kh_sun_yr, "o", color=SLIDE_ORANGE, markersize=8.5,
            markeredgecolor=SLIDE_BG, markeredgewidth=1.5, zorder=5)
    ax.plot(1, tau_nuc_sun_yr, "o", color=SLIDE_ROSE, markersize=8.5,
            markeredgecolor=SLIDE_BG, markeredgewidth=1.5, zorder=5)
    ax.text(1.08, 1.3e10, "Sun", color=SLIDE_TEXT, fontsize=11.5, fontweight="bold")

    age_universe = 1.38e10
    ax.axhline(age_universe, color=SLIDE_GOLD, linestyle=(0, (4, 3)), linewidth=1.6, alpha=0.85)
    ax.text(8.6, age_universe * 1.08, "Age of the universe", color=SLIDE_GOLD,
            fontsize=10.5, fontweight="bold", va="bottom")

    ax.text(0.16, 2e-4, r"$\tau_{\rm dyn} \propto M^{0.7}$",
            color=SLIDE_TEAL, fontsize=12, fontweight="bold")
    ax.text(0.16, 2.5e8, r"$\tau_{\rm KH} \propto M^{-2.3}$",
            color=SLIDE_ORANGE, fontsize=12, fontweight="bold")
    ax.text(2.4, 2.3e9, r"$\tau_{\rm nuc} \propto M^{-2.5}$",
            color=SLIDE_ROSE, fontsize=12, fontweight="bold")

    note = (
        "Order-of-magnitude main-sequence scalings\n"
        r"used here: $R \propto M^{0.8}$ and $L \propto M^{3.5}$"
    )
    ax.text(
        0.98, 0.04, note,
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=9.6, color=SLIDE_MUTED,
    )

    ax.set_xlabel(r"Stellar mass ($M/M_\odot$)", fontsize=14)
    ax.set_ylabel("Timescale (yr)", fontsize=14)
    ax.set_xlim(0.1, 14.5)
    ax.set_ylim(1e-6, 5e11)
    ax.set_title("How the Three Stellar Clocks Change with Mass",
                 fontsize=19, fontweight="bold", pad=12)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "timescales-vs-mass.png",
                facecolor=SLIDE_BG, bbox_inches="tight")
    plt.close(fig)
    print("  ✓ timescales-vs-mass.png")


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
