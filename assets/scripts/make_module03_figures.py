#!/usr/bin/env python3
"""
Generate pedagogical figures for ASTR 201 Module 3: Stellar Structure & Evolution.

The figures are optimized for dual use in white lecture slides and Quarto
readings. All physics is in CGS/solar units unless the plotted axis explicitly
uses a derived convenience unit such as MeV or fm.

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
# Global figure palette
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

SLIDE_TICK_SIZE = 13
SLIDE_LABEL_SIZE = 15
SLIDE_TITLE_SIZE = 19
SLIDE_BODY_SIZE = 12.5
SLIDE_SMALL_SIZE = 11.5
SLIDE_LEGEND_SIZE = 12.5
SLIDE_EXPORT_DPI = 240

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
    ax.tick_params(colors=SLIDE_TEXT, which="both", labelsize=SLIDE_TICK_SIZE)
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
    ax.tick_params(colors=SLIDE_TEXT, which="both", labelsize=SLIDE_TICK_SIZE)
    ax.xaxis.label.set_color(SLIDE_TEXT)
    ax.yaxis.label.set_color(SLIDE_TEXT)
    ax.title.set_color(SLIDE_TEXT)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(SLIDE_GRID)
        ax.spines[side].set_linewidth(1.0)
    if grid:
        ax.grid(True, color=SLIDE_GRID, linewidth=0.8, alpha=0.9)
    else:
        ax.grid(False)


def save_slide_figure(fig, filename):
    """Save a white-background figure into the module-03 image directory."""
    fig.savefig(
        OUTPUT_DIR / filename,
        facecolor=SLIDE_BG,
        bbox_inches="tight",
        dpi=SLIDE_EXPORT_DPI,
        pad_inches=0.08,
    )
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

    fig, axes = plt.subplots(1, 2, figsize=(14, 7), dpi=220,
                             gridspec_kw={"width_ratios": [1.2, 1]})

    # ── Left panel: random walk visualization ──
    ax = axes[0]
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)

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
    ax.plot(0, 0, "o", color=SLIDE_GOLD, markersize=12, zorder=10,
            markeredgecolor=SLIDE_BG, markeredgewidth=1.5)
    ax.plot(x[-1], y[-1], "*", color=SLIDE_ROSE, markersize=15, zorder=10,
            markeredgecolor=SLIDE_BG, markeredgewidth=1)

    # Net displacement arrow
    ax.annotate(
        "", xy=(x[-1], y[-1]), xytext=(0, 0),
        arrowprops=dict(arrowstyle="-|>", color=SLIDE_ORANGE, lw=2.5),
        zorder=9,
    )

    # Labels
    net_dist = np.sqrt(x[-1]**2 + y[-1]**2)
    ax.text(0, -5, "Born here", fontsize=11, color=SLIDE_GOLD,
            ha="center", fontweight="bold")
    ax.text(x[-1], y[-1] + 4, f"After {n_steps} steps", fontsize=10,
            color=SLIDE_ROSE, ha="center", fontweight="bold")

    ax.text(
        x[-1]/2 - 8, y[-1]/2 + 3,
        f"Net distance ≈ √N × ℓ\n= √{n_steps} × ℓ ≈ {net_dist:.0f} ℓ",
        fontsize=10, color=SLIDE_ORANGE, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=SLIDE_PANEL, edgecolor=SLIDE_ORANGE),
    )

    pad = 10
    lim = max(abs(x).max(), abs(y).max()) + pad
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$ (mean free paths)", fontsize=12, color=SLIDE_TEXT)
    ax.set_ylabel("$y$ (mean free paths)", fontsize=12, color=SLIDE_TEXT)
    ax.set_title(f"Random Walk: {n_steps} Scatterings", fontsize=15,
                 fontweight="bold", color=SLIDE_TEXT, pad=10)
    ax.tick_params(colors=SLIDE_MUTED)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(SLIDE_GRID)
    ax.grid(True, color=SLIDE_GRID, linewidth=0.8, alpha=0.8)

    # ── Right panel: the numbers ──
    ax2 = axes[1]
    ax2.set_facecolor(SLIDE_BG)
    ax2.axis("off")

    r_sun_cm = 7.0e10
    mean_free_path_cm = 1.96e-2
    c_cm_s = 3.0e10
    n_scatterings = (r_sun_cm / mean_free_path_cm) ** 2
    diffusion_time_yr = (r_sun_cm ** 2) / (mean_free_path_cm * c_cm_s * YEAR_S)
    straight_line_time_s = r_sun_cm / c_cm_s
    opacity_penalty = diffusion_time_yr * YEAR_S / straight_line_time_s

    info_text = [
        ("The Photon's Journey", 20, "bold", SLIDE_TEXT, 0.95),
        ("Toy walk left; Sun right", 14, "normal", SLIDE_MUTED, 0.90),
        ("", 10, "normal", SLIDE_TEXT, 0.84),
        ("Mean free path:", 13, "bold", SLIDE_TEAL, 0.80),
        (f"ℓ ≈ {mean_free_path_cm:.2f} cm", 16, "normal", SLIDE_TEXT, 0.75),
        ("(one-zone solar-core estimate)", 10, "normal", SLIDE_MUTED, 0.71),
        ("", 10, "normal", SLIDE_TEXT, 0.65),
        ("Number of scatterings:", 13, "bold", "#4c74a7", 0.61),
        (f"N = (R/ℓ)^2 ≈ {n_scatterings / 1e25:.1f} × 10^25", 16, "normal", SLIDE_TEXT, 0.56),
        ("", 10, "normal", SLIDE_TEXT, 0.50),
        ("Diffusion time:", 13, "bold", "#8f63a3", 0.46),
        (f"t ≈ {diffusion_time_yr / 1e5:.1f} × 10^5 yr", 16, "normal", SLIDE_TEXT, 0.41),
        ("", 10, "normal", SLIDE_TEXT, 0.35),
        ("Straight-line time:", 13, "bold", SLIDE_ORANGE, 0.31),
        (f"t = R/c ≈ {straight_line_time_s:.1f} s", 16, "normal", SLIDE_TEXT, 0.26),
        ("", 10, "normal", SLIDE_TEXT, 0.20),
        ("Opacity penalty:", 13, "bold", SLIDE_ROSE, 0.16),
        (f"t_diff / (R/c) ≈ {opacity_penalty / 1e12:.1f} × 10^12", 14, "normal", SLIDE_TEXT, 0.11),
        ("Energy diffuses; not one immortal photon.", 11, "normal", SLIDE_ROSE, 0.04),
    ]

    for text, size, weight, color, ypos in info_text:
        style = "italic" if text.startswith("The Sun is transparent") else "normal"
        ax2.text(0.05, ypos, text, fontsize=size, fontweight=weight,
                 fontstyle=style, color=color, transform=ax2.transAxes, va="top")

    ax2.text(0.05, 0.88,
             "Toy Monte Carlo + one-zone solar scaling",
             transform=ax2.transAxes, fontsize=10.5, color=SLIDE_MUTED,
             bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    fig.tight_layout()
    save_slide_figure(fig, "random-walk.png")


# ═════════════════════════════════════════════════════════════
# Figure 3: Optical Depth / Mean Free Path Cartoon
# Used in: R4 (Radiation Transport)
# ═════════════════════════════════════════════════════════════
def make_optical_depth_slab():
    """Compare optically thin and optically thick slabs as counts of mean free paths."""
    fig, axes = plt.subplots(1, 2, figsize=(13.4, 5.9), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)

    specs = [
        {
            "title": r"Optically Thin: $\tau < 1$",
            "slab_width": 4.0,
            "ell_draw": 8.5,
            "tau_label": r"$\tau \sim R/\ell \approx 0.5$",
            "color": SLIDE_TEAL,
            "note": "A photon usually crosses\nwithout interacting.",
        },
        {
            "title": r"Optically Thick: $\tau \gg 1$",
            "slab_width": 9.6,
            "ell_draw": 1.2,
            "tau_label": r"$\tau \sim R/\ell \approx 8$",
            "color": SLIDE_ROSE,
            "note": "Many short steps fit across\none slab thickness.",
        },
    ]

    for ax, spec in zip(axes, specs):
        ax.set_facecolor(SLIDE_BG)
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 6.6)
        ax.axis("off")

        x0 = 2.0
        y0 = 2.3
        slab_height = 1.6

        slab = mpatches.FancyBboxPatch(
            (x0, y0),
            spec["slab_width"],
            slab_height,
            boxstyle="round,pad=0.02,rounding_size=0.18",
            facecolor="#eef4fb",
            edgecolor=SLIDE_GRID,
            linewidth=1.8,
        )
        ax.add_patch(slab)

        ax.text(
            x0 + spec["slab_width"] / 2,
            y0 + 0.34 * slab_height,
            "stellar material",
            ha="center",
            va="center",
            fontsize=12,
            color=SLIDE_MUTED,
            fontweight="bold",
        )

        ax.text(
            x0 + spec["slab_width"] / 2,
            5.85,
            spec["title"],
            ha="center",
            va="center",
            fontsize=17,
            color=SLIDE_TEXT,
            fontweight="bold",
        )

        ax.annotate(
            "",
            xy=(x0 + spec["slab_width"], 1.55),
            xytext=(x0, 1.55),
            arrowprops=dict(arrowstyle="<->", lw=2.2, color=SLIDE_ORANGE),
        )
        ax.text(
            x0 + spec["slab_width"] / 2,
            1.05,
            r"$R$",
            ha="center",
            va="center",
            fontsize=15,
            color=SLIDE_ORANGE,
            fontweight="bold",
        )

        ell_x0 = x0 - 0.35 if spec["slab_width"] < spec["ell_draw"] else x0
        ell_x1 = ell_x0 + spec["ell_draw"]
        ax.annotate(
            "",
            xy=(ell_x1, 4.65),
            xytext=(ell_x0, 4.65),
            arrowprops=dict(arrowstyle="<->", lw=2.2, color=ACCENT_BLUE),
        )
        ax.text(
            0.5 * (ell_x0 + ell_x1),
            5.05,
            r"$\ell$",
            ha="center",
            va="center",
            fontsize=15,
            color=ACCENT_BLUE,
            fontweight="bold",
        )

        if spec["slab_width"] < spec["ell_draw"]:
            photon_y = y0 + 0.62 * slab_height
            ax.annotate(
                "",
                xy=(x0 + spec["slab_width"] + 0.9, photon_y),
                xytext=(x0 - 1.0, photon_y),
                arrowprops=dict(arrowstyle="-|>", lw=2.8, color=spec["color"]),
            )
        else:
            interaction_x = np.arange(x0 + spec["ell_draw"], x0 + spec["slab_width"], spec["ell_draw"])
            start_x = x0 - 0.7
            y_mid = y0 + 0.62 * slab_height

            for hit_x in interaction_x:
                ax.annotate(
                    "",
                    xy=(hit_x, y_mid),
                    xytext=(start_x, y_mid),
                    arrowprops=dict(arrowstyle="-|>", lw=2.4, color=spec["color"]),
                )
                ax.plot(
                    hit_x,
                    y_mid,
                    "o",
                    color=spec["color"],
                    markersize=7.5,
                    markeredgecolor=SLIDE_BG,
                    markeredgewidth=1.0,
                    zorder=4,
                )
                start_x = hit_x

            ax.annotate(
                "",
                xy=(x0 + spec["slab_width"] + 0.8, y_mid),
                xytext=(start_x, y_mid),
                arrowprops=dict(arrowstyle="-|>", lw=2.4, color=spec["color"]),
            )

        ax.text(
            x0 + spec["slab_width"] / 2,
            0.35,
            spec["tau_label"],
            ha="center",
            va="center",
            fontsize=13,
            color=spec["color"],
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=spec["color"]),
        )
        ax.text(
            x0 + spec["slab_width"] / 2,
            5.35,
            spec["note"],
            ha="center",
            va="center",
            fontsize=11.5,
            color=SLIDE_MUTED,
        )

    fig.suptitle(
        "Optical Depth Counts How Many Mean Free Paths Fit Across the Star",
        fontsize=18.5,
        fontweight="bold",
        color=SLIDE_TEXT,
        y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    save_slide_figure(fig, "optical-depth-slab.png")


# ═════════════════════════════════════════════════════════════
# Figure 4: Random-Walk Displacement Scaling
# Used in: R4 (Radiation Transport)
# ═════════════════════════════════════════════════════════════
def make_random_walk_scaling():
    """Show why random-walk displacement grows only as the square root of step count."""
    fig, ax = plt.subplots(figsize=(11.8, 6.8), dpi=220)
    apply_slide_style(fig, ax)

    n_steps = np.logspace(0, 6, 500)
    total_path = n_steps
    net_displacement = np.sqrt(n_steps)

    ax.loglog(
        n_steps,
        total_path,
        color=SLIDE_ORANGE,
        linewidth=3.0,
        label=r"Total path length $\sim N\ell$",
    )
    ax.loglog(
        n_steps,
        net_displacement,
        color=SLIDE_TEAL,
        linewidth=3.4,
        label=r"Net displacement $\sim \sqrt{N}\,\ell$",
    )
    ax.fill_between(
        n_steps,
        net_displacement,
        total_path,
        color=SLIDE_ORANGE,
        alpha=0.10,
    )

    highlight_steps = np.array([10, 100, 10_000, 1_000_000])
    ax.scatter(highlight_steps, np.sqrt(highlight_steps), color=SLIDE_TEAL, s=40, zorder=4)
    ax.scatter(highlight_steps, highlight_steps, color=SLIDE_ORANGE, s=40, zorder=4)

    ax.annotate(
        r"At $N=10^6$ steps:" "\n" r"path length $\sim 10^6\ell$" "\n" r"displacement $\sim 10^3\ell$",
        xy=(1.0e6, 1.0e3),
        xytext=(1.2e4, 2.2e4),
        fontsize=11.5,
        color=SLIDE_TEXT,
        bbox=dict(boxstyle="round,pad=0.35", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
        arrowprops=dict(arrowstyle="-|>", color=SLIDE_TEAL, lw=2.0),
    )
    ax.text(
        0.03,
        0.85,
        "The vertical gap grows quickly:\nrandom walks waste distance on repeated redirection.",
        transform=ax.transAxes,
        fontsize=11.5,
        color=SLIDE_MUTED,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round,pad=0.32", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
    )

    guide_x = np.array([20, 200])
    ax.loglog(guide_x, 6e4 * (guide_x / guide_x[0]), "--", color=SLIDE_ORANGE, linewidth=1.7, alpha=0.85)
    ax.loglog(guide_x, 300 * (guide_x / guide_x[0]) ** 0.5, "--", color=SLIDE_TEAL, linewidth=1.7, alpha=0.85)
    ax.text(95, 1.8e5, "slope 1", color=SLIDE_ORANGE, fontsize=11.5, rotation=27)
    ax.text(110, 550, "slope 1/2", color=SLIDE_TEAL, fontsize=11.5, rotation=13)

    ax.set_xlabel(r"Number of steps, $N$", fontsize=14)
    ax.set_ylabel(r"Distance scale (in units of $\ell$)", fontsize=14)
    ax.set_title("Random Walks Grow Only as the Square Root of Step Count",
                 fontsize=18.5, fontweight="bold", pad=14)
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.0, 1.01),
        ncol=2,
        frameon=False,
        fontsize=12.0,
        columnspacing=1.2,
        handlelength=1.7,
    )
    fig.tight_layout()
    save_slide_figure(fig, "random-walk-scaling.png")


# ═════════════════════════════════════════════════════════════
# Figure 5: Radiative Flux Throttled by Opacity
# Used in: R4 (Radiation Transport)
# ═════════════════════════════════════════════════════════════
def make_radiative_flux_opacity():
    """Show that larger opacity throttles radiative energy flow for the same gradient."""
    fig, axes = plt.subplots(
        1, 2, figsize=(13.6, 6.1), dpi=220, gridspec_kw={"width_ratios": [1.0, 1.05]}
    )
    fig.patch.set_facecolor(SLIDE_BG)

    ax1, ax2 = axes
    apply_slide_style(fig, ax1)
    apply_slide_style(fig, ax2)

    radius = np.linspace(0, 1.0, 300)
    u_norm = 1.0 - 0.82 * radius ** 1.25
    ax1.plot(radius, u_norm, color=SLIDE_ORANGE, linewidth=3.0)
    ax1.fill_between(radius, u_norm, 0, color=SLIDE_ORANGE, alpha=0.10)
    ax1.set_xlim(0, 1.0)
    ax1.set_ylim(0, 1.08)
    ax1.set_xlabel(r"Radius, $r/R$", fontsize=14)
    ax1.set_ylabel(r"Normalized radiation energy density", fontsize=13.5)
    ax1.set_title(r"A gradient in $u_{\rm rad}=aT^4$ drives outward flow",
                  fontsize=17.5, fontweight="bold", pad=12)

    ax1.text(0.07, 0.96, "hot interior", color=SLIDE_ORANGE, fontsize=11.5, fontweight="bold")
    ax1.text(0.75, 0.18, "cooler exterior", color=SLIDE_MUTED, fontsize=11.5, fontweight="bold")

    x_ref = 0.48
    y_ref = np.interp(x_ref, radius, u_norm)
    ax1.annotate(
        "",
        xy=(x_ref + 0.21, y_ref - 0.12),
        xytext=(x_ref - 0.02, y_ref - 0.12),
        arrowprops=dict(arrowstyle="-|>", lw=3.0, color=SLIDE_TEAL),
    )
    ax1.annotate(
        "low $\\kappa$:\nlarger $F_{\\rm rad}$",
        xy=(x_ref + 0.21, y_ref - 0.12),
        xytext=(0.63, 0.80),
        textcoords="axes fraction",
        fontsize=11.2,
        color=SLIDE_TEAL,
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.30", facecolor=SLIDE_PANEL, edgecolor=SLIDE_TEAL),
    )
    ax1.annotate(
        "",
        xy=(x_ref + 0.11, y_ref - 0.28),
        xytext=(x_ref - 0.02, y_ref - 0.28),
        arrowprops=dict(arrowstyle="-|>", lw=3.0, color=SLIDE_ROSE),
    )
    ax1.annotate(
        "high $\\kappa$:\nsmaller $F_{\\rm rad}$",
        xy=(x_ref + 0.11, y_ref - 0.28),
        xytext=(0.63, 0.54),
        textcoords="axes fraction",
        fontsize=11.2,
        color=SLIDE_ROSE,
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.30", facecolor=SLIDE_PANEL, edgecolor=SLIDE_ROSE),
    )
    ax1.text(
        0.05,
        0.13,
        r"Same $d(aT^4)/dr$ and same $\rho$",
        transform=ax1.transAxes,
        fontsize=11.0,
        color=SLIDE_MUTED,
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
    )

    kappa_rel = np.logspace(-1, 1.3, 300)
    flux_rel = 1.0 / kappa_rel
    ax2.loglog(kappa_rel, flux_rel, color=SLIDE_ROSE, linewidth=3.2)
    ax2.scatter([1.0, 10.0], [1.0, 0.1], color=[SLIDE_TEAL, SLIDE_ROSE], s=55, zorder=4)
    ax2.axvline(1.0, color=SLIDE_GRID, linestyle="--", linewidth=1.2)
    ax2.axvline(10.0, color=SLIDE_GRID, linestyle="--", linewidth=1.2)
    ax2.axhline(1.0, color=SLIDE_GRID, linestyle="--", linewidth=1.2)
    ax2.axhline(0.1, color=SLIDE_GRID, linestyle="--", linewidth=1.2)

    ax2.annotate(
        r"$10\times$ opacity" "\n" r"$\Rightarrow 10\times$ smaller flux",
        xy=(10.0, 0.1),
        xytext=(2.6, 0.42),
        fontsize=11.3,
        color=SLIDE_TEXT,
        bbox=dict(boxstyle="round,pad=0.34", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
        arrowprops=dict(arrowstyle="-|>", color=SLIDE_ROSE, lw=2.0),
    )
    ax2.text(
        0.04,
        0.93,
        r"Fixed gradient: $F_{\rm rad} \propto 1/\kappa$",
        transform=ax2.transAxes,
        fontsize=11.3,
        color=SLIDE_MUTED,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round,pad=0.30", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
    )

    ax2.set_xlabel(r"Opacity relative to baseline, $\kappa/\kappa_0$", fontsize=13.5)
    ax2.set_ylabel(r"Relative radiative flux, $F_{\rm rad}/F_0$", fontsize=13.5)
    ax2.set_title("Higher Opacity Throttles Radiative Energy Flow",
                  fontsize=17.5, fontweight="bold", pad=12)

    fig.tight_layout()
    save_slide_figure(fig, "radiative-flux-opacity.png")


# ═════════════════════════════════════════════════════════════
# Figure 6: Radiation vs Convection Transport
# Used in: R4 (Radiation Transport)
# ═════════════════════════════════════════════════════════════
def make_radiation_vs_convection_transport():
    """Contrast radiative diffusion with convection using the same stellar slice."""
    fig, axes = plt.subplots(1, 2, figsize=(13.8, 7.2), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)

    slice_cmap = LinearSegmentedColormap.from_list(
        "stellar_slice", ["#ffd99a", "#f7f2e8", "#e6edf9"]
    )
    warm_arrow = "#d46a2f"
    cool_arrow = ACCENT_BLUE
    connector = "#8da0b4"

    def draw_slice(ax, panel_title):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_facecolor(SLIDE_BG)

        x0, y0, width, height = 0.18, 0.12, 0.64, 0.74
        gradient = np.linspace(0, 1, 500).reshape(-1, 1)
        ax.imshow(
            gradient,
            extent=(x0, x0 + width, y0, y0 + height),
            origin="lower",
            cmap=slice_cmap,
            aspect="auto",
            alpha=0.95,
            zorder=0,
        )
        border = mpatches.FancyBboxPatch(
            (x0, y0),
            width,
            height,
            boxstyle="round,pad=0.015,rounding_size=0.035",
            facecolor="none",
            edgecolor=SLIDE_GRID,
            linewidth=1.7,
            zorder=2,
        )
        ax.add_patch(border)

        ax.text(
            0.50,
            0.965,
            panel_title,
            ha="center",
            va="top",
            fontsize=16,
            color=SLIDE_TEXT,
            fontweight="bold",
        )

        ax.annotate(
            "",
            xy=(0.08, y0 + height),
            xytext=(0.08, y0),
            arrowprops=dict(arrowstyle="-|>", lw=1.8, color=SLIDE_MUTED),
        )
        ax.text(0.08, y0 - 0.05, "center", ha="center", va="top",
                fontsize=10.8, color=SLIDE_MUTED, fontweight="bold")
        ax.text(0.08, y0 + height + 0.03, "surface", ha="center", va="bottom",
                fontsize=10.8, color=SLIDE_MUTED, fontweight="bold")

        return x0, y0, width, height

    # ── Left panel: radiation diffusion ──────────────────────
    ax = axes[0]
    x0, y0, width, height = draw_slice(ax, "RADIATION\n(DIFFUSION)")
    rng = np.random.default_rng(7)

    for x_start in (0.31, 0.50, 0.67):
        x = x_start
        y = y0 + 0.05
        points = [(x, y)]
        for _ in range(15):
            dx = rng.normal(0.0, 0.055)
            dy = abs(rng.normal(0.055, 0.028))
            if rng.random() < 0.30:
                dy *= -0.35
            x = np.clip(x + dx, x0 + 0.035, x0 + width - 0.035)
            y = np.clip(y + dy, y0 + 0.035, y0 + height - 0.035)
            points.append((x, y))
            if y >= y0 + height - 0.05:
                break

        for p0, p1 in zip(points[:-1], points[1:]):
            ax.annotate(
                "",
                xy=p1,
                xytext=p0,
                arrowprops=dict(
                    arrowstyle="-|>",
                    lw=2.0,
                    color=SLIDE_ORANGE,
                    alpha=0.95,
                    shrinkA=0,
                    shrinkB=0,
                    mutation_scale=8,
                ),
            )

    ax.text(
        0.50,
        0.79,
        "random walk",
        ha="center",
        va="center",
        fontsize=12.2,
        color=SLIDE_TEXT,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
    )
    ax.annotate(
        "many small steps",
        xy=(0.47, 0.41),
        xytext=(0.08, 0.38),
        fontsize=11.0,
        color=SLIDE_TEXT,
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
        arrowprops=dict(arrowstyle="-|>", color=SLIDE_ORANGE, lw=1.8),
    )
    ax.annotate(
        "inefficient transport",
        xy=(0.61, 0.70),
        xytext=(0.82, 0.56),
        fontsize=11.0,
        color=SLIDE_TEXT,
        ha="right",
        va="center",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
        arrowprops=dict(arrowstyle="-|>", color=SLIDE_ORANGE, lw=1.8),
    )
    ax.annotate(
        "",
        xy=(0.33, 0.20),
        xytext=(0.43, 0.20),
        arrowprops=dict(arrowstyle="<->", color=SLIDE_ORANGE, lw=1.8),
    )
    ax.text(0.38, 0.16, r"$\ell$", ha="center", va="center",
            fontsize=12.5, color=SLIDE_ORANGE, fontweight="bold")
    ax.annotate(
        "high opacity ->\nshort mean free path",
        xy=(0.38, 0.20),
        xytext=(0.08, 0.12),
        fontsize=10.8,
        color=SLIDE_TEXT,
        ha="left",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
        arrowprops=dict(arrowstyle="-|>", color=SLIDE_ORANGE, lw=1.6),
    )

    # ── Right panel: convection ──────────────────────────────
    ax = axes[1]
    x0, y0, width, height = draw_slice(ax, "CONVECTION\n(BULK MOTION)")

    def draw_cell(xc):
        yc = 0.49
        half_w = 0.12
        half_h = 0.23
        x_left = xc - 0.70 * half_w
        x_right = xc + 0.70 * half_w
        y_bottom = yc - half_h
        y_top = yc + half_h

        ax.annotate(
            "",
            xy=(x_left, y_top),
            xytext=(x_left, y_bottom),
            arrowprops=dict(arrowstyle="-|>", lw=3.0, color=warm_arrow),
        )
        ax.annotate(
            "",
            xy=(x_right, y_bottom),
            xytext=(x_right, y_top),
            arrowprops=dict(arrowstyle="-|>", lw=3.0, color=cool_arrow),
        )
        top_arc = mpatches.FancyArrowPatch(
            (x_left, y_top),
            (x_right, y_top),
            connectionstyle="arc3,rad=0.55",
            arrowstyle="-|>",
            mutation_scale=10,
            lw=2.0,
            color=connector,
            alpha=0.95,
        )
        bottom_arc = mpatches.FancyArrowPatch(
            (x_right, y_bottom),
            (x_left, y_bottom),
            connectionstyle="arc3,rad=-0.55",
            arrowstyle="-|>",
            mutation_scale=10,
            lw=2.0,
            color=connector,
            alpha=0.95,
        )
        ax.add_patch(top_arc)
        ax.add_patch(bottom_arc)

    draw_cell(0.39)
    draw_cell(0.61)

    ax.annotate(
        "hot rises\n(low density)",
        xy=(0.31, 0.68),
        xytext=(0.14, 0.78),
        fontsize=11.0,
        color=SLIDE_TEXT,
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=warm_arrow),
        arrowprops=dict(arrowstyle="-|>", color=warm_arrow, lw=1.8),
    )
    ax.annotate(
        "cool sinks\n(high density)",
        xy=(0.69, 0.33),
        xytext=(0.86, 0.24),
        fontsize=11.0,
        color=SLIDE_TEXT,
        ha="right",
        va="center",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=cool_arrow),
        arrowprops=dict(arrowstyle="-|>", color=cool_arrow, lw=1.8),
    )
    ax.text(
        0.50,
        0.16,
        "bulk motion\ntransports energy",
        ha="center",
        va="center",
        fontsize=12.0,
        color=SLIDE_TEXT,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.30", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
    )

    fig.suptitle(
        "Energy Transport in Stars: Radiation vs Convection",
        fontsize=19.0,
        fontweight="bold",
        color=SLIDE_TEXT,
        y=0.965,
    )
    fig.text(
        0.50,
        0.055,
        "Radiation: many small steps $\\rightarrow$ slow diffusion\n"
        "Convection: large-scale motion $\\rightarrow$ efficient transport",
        ha="center",
        va="center",
        fontsize=12.4,
        color=SLIDE_TEXT,
        fontweight="bold",
    )
    fig.subplots_adjust(left=0.04, right=0.98, top=0.90, bottom=0.12, wspace=0.08)
    save_slide_figure(fig, "radiation-vs-convection-transport.png")


# ═════════════════════════════════════════════════════════════
# Figure 7: Eddington Force Balance
# Used in: R4 (Radiation Transport)
# ═════════════════════════════════════════════════════════════
def make_eddington_force_balance():
    """Schematic of gravity and radiation balancing on a gas parcel."""
    fig, ax = plt.subplots(figsize=(12.8, 6.5), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 7.0)
    ax.axis("off")

    star_center = (2.8, 3.5)
    for radius, color, alpha in [
        (1.55, "#ffd8a8", 0.22),
        (1.32, "#f9c97b", 0.34),
        (1.08, "#f5b451", 0.72),
        (0.82, "#f29f38", 0.95),
    ]:
        ax.add_patch(mpatches.Circle(star_center, radius, facecolor=color, edgecolor="none", alpha=alpha))

    ax.text(
        star_center[0],
        star_center[1],
        "star",
        ha="center",
        va="center",
        fontsize=16,
        color=SLIDE_TEXT,
        fontweight="bold",
        path_effects=[pe.withStroke(linewidth=3, foreground=SLIDE_BG, alpha=0.7)],
    )

    parcel_x = 8.35
    parcel_y = 3.5
    parcel = mpatches.FancyBboxPatch(
        (parcel_x - 0.55, parcel_y - 0.45),
        1.1,
        0.9,
        boxstyle="round,pad=0.05,rounding_size=0.12",
        facecolor="#eef4fb",
        edgecolor=SLIDE_GRID,
        linewidth=1.8,
    )
    ax.add_patch(parcel)
    ax.text(parcel_x, parcel_y, "gas\nparcel", ha="center", va="center",
            fontsize=12.5, color=SLIDE_TEXT, fontweight="bold")

    ax.plot(
        [star_center[0] + 1.55, parcel_x - 0.55],
        [star_center[1], parcel_y],
        color=SLIDE_MUTED,
        linestyle=(0, (4, 4)),
        linewidth=1.6,
    )
    ax.text(5.55, 3.78, r"$r$", fontsize=15, color=SLIDE_MUTED, fontweight="bold")

    for y_offset in (-0.45, 0.0, 0.45):
        ax.annotate(
            "",
            xy=(parcel_x - 0.6, parcel_y + y_offset),
            xytext=(star_center[0] + 1.7, parcel_y + y_offset),
            arrowprops=dict(arrowstyle="-|>", lw=2.0, color=SLIDE_ROSE, alpha=0.55),
        )
    ax.text(
        5.65,
        4.55,
        r"radiation flux $F = L/(4\pi r^2)$",
        ha="center",
        va="center",
        fontsize=11.5,
        color=SLIDE_ROSE,
        bbox=dict(boxstyle="round,pad=0.26", facecolor=SLIDE_PANEL, edgecolor=SLIDE_ROSE),
    )

    ax.annotate(
        "",
        xy=(parcel_x - 1.55, parcel_y),
        xytext=(parcel_x - 0.58, parcel_y),
        arrowprops=dict(arrowstyle="-|>", lw=3.1, color=ACCENT_BLUE),
    )
    ax.text(
        parcel_x - 2.55,
        parcel_y + 0.48,
        r"gravity" "\n" r"$g = GM/r^2$",
        ha="center",
        va="center",
        fontsize=12,
        color=ACCENT_BLUE,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=ACCENT_BLUE),
    )

    ax.annotate(
        "",
        xy=(parcel_x + 1.45, parcel_y),
        xytext=(parcel_x + 0.58, parcel_y),
        arrowprops=dict(arrowstyle="-|>", lw=3.1, color=SLIDE_ROSE),
    )
    ax.text(
        parcel_x + 2.55,
        parcel_y + 0.48,
        r"radiation" "\n" r"$g_{\rm rad} = \kappa F/c$",
        ha="center",
        va="center",
        fontsize=12,
        color=SLIDE_ROSE,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_ROSE),
    )

    ax.text(
        8.1,
        5.95,
        "At the Eddington limit:",
        fontsize=15,
        color=SLIDE_TEXT,
        fontweight="bold",
        ha="center",
    )
    ax.text(
        8.1,
        5.05,
        r"$g_{\rm rad}=g$" "\n"
        r"$\kappa L/(4\pi r^2 c)=GM/r^2$" "\n"
        r"$L = L_{\rm Edd}$",
        fontsize=13,
        color=SLIDE_TEXT,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.34", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
    )

    ax.text(
        0.98,
        0.10,
        "Below $L_{\\rm Edd}$ gravity wins; near $L_{\\rm Edd}$ radiation can lift the gas.",
        transform=ax.transAxes,
        ha="right",
        va="center",
        fontsize=11.3,
        color=SLIDE_MUTED,
    )
    ax.set_title("The Eddington Limit Is a Force-Balance Ceiling",
                 fontsize=18.5, color=SLIDE_TEXT, fontweight="bold", pad=12)

    fig.tight_layout()
    save_slide_figure(fig, "eddington-force-balance.png")


# ═════════════════════════════════════════════════════════════
# Figure 7: Timescale Hierarchy
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
    ax.text(15.8, 4.0e10, "high-mass caveat:\n$L(M)$ flattens,\nso lifetimes stay longer\nthan naive extrapolation",
            fontsize=9.2, color=SLIDE_GOLD, ha="left", va="top")

    ax.axhline(13.8e9, color=SLIDE_GOLD, linestyle=(0, (4, 3)), linewidth=1.6, alpha=0.9)
    ax.text(6.0, 13.8e9 * 1.10, "age of universe", color=SLIDE_GOLD,
            fontsize=10.2, fontweight="bold", ha="left", va="bottom")

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
# Lecture 1-3 figure suite additions
# ═════════════════════════════════════════════════════════════
def make_main_sequence_lifetime_vs_mass():
    """Compare naive and more realistic main-sequence lifetime trends."""
    masses = np.logspace(np.log10(0.08), np.log10(30.0), 600)
    model = solar_normalized_timescales(masses)

    fig, ax = plt.subplots(figsize=(12.0, 7.0), dpi=220)
    apply_slide_style(fig, ax)
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.plot(masses, model["tau_nuc"], color=SLIDE_ROSE, linewidth=3.2,
            label="piecewise lifetime model")
    ax.plot(masses, model["tau_nuc_naive"], color=SLIDE_TEAL, linewidth=2.0,
            linestyle="--", label=r"naive $M^{-2.5}$ guide")

    ax.axhline(13.8e9, color=SLIDE_GOLD, linestyle=(0, (4, 3)), linewidth=1.5)
    ax.text(0.083, 1.55e10, "age of universe", color=SLIDE_GOLD,
            fontsize=10.2, fontweight="bold", va="bottom")

    ax.axvspan(0.08, 0.35, color=SLIDE_TEAL, alpha=0.07)
    ax.axvspan(15.0, 30.0, color=SLIDE_GOLD, alpha=0.07)
    ax.text(0.1, 1.0e12, "fully convective\nlow-mass stars:\nmore fuel is accessible",
            color=SLIDE_TEAL, fontsize=10, ha="left", va="top")
    ax.text(16.2, 1.0e8, "very massive stars:\n$L(M)$ flattens, so the\nnaive law becomes too short",
            color=SLIDE_GOLD, fontsize=9.8, ha="left", va="bottom")

    ax.plot(1.0, 1.0e10, "o", color=SLIDE_ROSE, markersize=8.5,
            markeredgecolor=SLIDE_BG, markeredgewidth=1.4)
    ax.text(1.08, 1.3e10, "Sun", color=SLIDE_TEXT, fontsize=11, fontweight="bold")

    ax.set_xlabel(r"Stellar Mass ($M/M_\odot$)", fontsize=14)
    ax.set_ylabel("Main-Sequence Lifetime (yr)", fontsize=14)
    ax.set_xlim(0.08, 30.0)
    ax.set_ylim(1.0e6, 2.0e13)
    ax.set_title("Main-Sequence Lifetime vs Stellar Mass", fontsize=18.5,
                 fontweight="bold", pad=12)
    ax.legend(loc="lower left", frameon=False, fontsize=10.5)

    fig.tight_layout()
    save_slide_figure(fig, "main-sequence-lifetime-vs-mass.png")


def make_cluster_turnoff_clock():
    """Schematic HR-style panels showing the turnoff as an age clock."""
    ages = [5.0e7, 7.0e8, 6.0e9]
    labels = ["50 Myr cluster", "700 Myr cluster", "6 Gyr cluster"]
    colors = [SLIDE_TEAL, SLIDE_ORANGE, SLIDE_ROSE]
    masses = np.logspace(np.log10(0.6), np.log10(15.0), 250)
    lifetimes = solar_normalized_timescales(masses)["tau_nuc"]
    temperatures = 5800.0 * masses**0.5
    luminosities = solar_main_sequence_luminosity(masses)

    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.9), dpi=220, sharey=True)
    fig.patch.set_facecolor(SLIDE_BG)

    for ax, age, label, color in zip(axes, ages, labels, colors):
        finalize_slide_axes(ax, grid=False)
        ax.set_xscale("log")
        ax.set_xlim(3.2e4, 3.0e3)
        ax.set_ylim(-1.0, 4.8)

        alive = lifetimes >= age
        ax.plot(temperatures[alive], np.log10(luminosities[alive]),
                color=color, linewidth=3.0)
        ax.plot(temperatures[alive][::10], np.log10(luminosities[alive][::10]),
                "o", color=color, markersize=3.5, alpha=0.8)

        m_to = approximate_turnoff_mass(age, masses)
        t_to = 5800.0 * m_to**0.5
        l_to = solar_main_sequence_luminosity(np.array([m_to]))[0]
        giant_t = np.array([t_to, 0.82 * t_to, 0.67 * t_to, 0.55 * t_to])
        giant_l = np.array([l_to, 1.7 * l_to, 3.0 * l_to, 5.0 * l_to])
        ax.plot(giant_t, np.log10(giant_l), color=SLIDE_ORANGE, linewidth=2.3,
                linestyle="--")
        ax.plot(t_to, np.log10(l_to), "o", color=SLIDE_GOLD, markersize=7.5,
                markeredgecolor=SLIDE_BG, markeredgewidth=1.3, zorder=5)

        ax.annotate(fr"turnoff $\approx {m_to:.1f}\,M_\odot$",
                    xy=(t_to, np.log10(l_to)),
                    xytext=(0.68 * t_to, np.log10(l_to) + 0.8),
                    fontsize=9.5, color=SLIDE_GOLD, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=SLIDE_GOLD, lw=1.4))
        ax.set_title(label, fontsize=12.5, color=SLIDE_TEXT, fontweight="bold")

    axes[0].set_ylabel(r"$\log_{10}(L/L_\odot)$", fontsize=13)
    for ax in axes:
        ax.set_xlabel("Temperature (K)", fontsize=12)
    fig.suptitle("The Main-Sequence Turnoff Is a Cluster Age Clock",
                 fontsize=18, color=SLIDE_TEXT, fontweight="bold", y=1.02)
    fig.tight_layout()
    save_slide_figure(fig, "cluster-turnoff-clock.png")


def make_fuel_vs_burn_rate():
    """Show why burn rate outpaces the fuel supply as mass increases."""
    masses = np.logspace(np.log10(0.1), np.log10(30.0), 400)
    model = solar_normalized_timescales(masses)
    fuel = (model["fuel_fraction"] / accessible_fuel_fraction(np.array([1.0]))[0]) * masses
    burn_rate = model["luminosity"]

    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=220)
    apply_slide_style(fig, ax)
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.plot(masses, fuel, color=SLIDE_TEAL, linewidth=3.0, label="accessible fuel reservoir")
    ax.plot(masses, burn_rate, color=SLIDE_ORANGE, linewidth=3.0, label="luminosity / burn rate")
    ax.fill_between(masses, fuel, burn_rate, where=burn_rate >= fuel,
                    color=SLIDE_ORANGE, alpha=0.08)

    reps = np.array([0.2, 1.0, 10.0])
    rep_model = solar_normalized_timescales(reps)
    rep_fuel = (rep_model["fuel_fraction"] / accessible_fuel_fraction(np.array([1.0]))[0]) * reps
    rep_burn = rep_model["luminosity"]
    for mass, fval, bval in zip(reps, rep_fuel, rep_burn):
        ax.plot(mass, fval, "o", color=SLIDE_TEAL, markersize=7.5, markeredgecolor=SLIDE_BG, markeredgewidth=1.2)
        ax.plot(mass, bval, "o", color=SLIDE_ORANGE, markersize=7.5, markeredgecolor=SLIDE_BG, markeredgewidth=1.2)
        ax.text(mass, max(fval, bval) * 1.4, fr"${mass:g}\,M_\odot$", fontsize=10,
                color=SLIDE_TEXT, ha="center", fontweight="bold")

    ax.text(0.12, 2.0e-1, "fuel grows roughly with mass", fontsize=10.5, color=SLIDE_TEAL)
    ax.text(2.8, 1.5e3, "burn rate rises much faster", fontsize=10.5, color=SLIDE_ORANGE)

    ax.set_xlabel(r"Stellar Mass ($M/M_\odot$)", fontsize=14)
    ax.set_ylabel("Relative Scale (solar-normalized)", fontsize=14)
    ax.set_xlim(0.1, 30.0)
    ax.set_ylim(1.0e-2, 2.0e5)
    ax.set_title("Why Massive Stars Die Young: Burn Rate Beats Fuel Supply",
                 fontsize=18, fontweight="bold", pad=12)
    ax.legend(loc="upper left", frameon=False, fontsize=10.5)

    fig.tight_layout()
    save_slide_figure(fig, "fuel-vs-burn-rate.png")


def make_pressure_vs_pressure_gradient():
    """Two-panel misconception killer: pressure alone versus pressure gradient."""
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.2), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)

    titles = ["Uniform Pressure: No Support", "Pressure Gradient: Outward Support"]
    top_labels = [r"$P_{\rm top}=P_{\rm bottom}$", r"$P_{\rm bottom}>P_{\rm top}$"]
    arrow_sizes = [(0.18, 0.18), (0.12, 0.28)]

    for ax, title, top_label, (top_w, bottom_w) in zip(axes, titles, top_labels, arrow_sizes):
        ax.set_facecolor(SLIDE_BG)
        ax.axis("off")
        shell = mpatches.FancyBboxPatch((0.36, 0.35), 0.28, 0.28,
                                        boxstyle="round,pad=0.02,rounding_size=0.02",
                                        facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID, linewidth=1.5)
        ax.add_patch(shell)
        ax.text(0.50, 0.49, "gas shell", ha="center", va="center",
                fontsize=15, color=SLIDE_TEXT, fontweight="bold")

        ax.annotate("", xy=(0.50, 0.35), xytext=(0.50, 0.35 - bottom_w),
                    arrowprops=dict(arrowstyle="-|>", lw=7, color=SLIDE_TEAL))
        ax.annotate("", xy=(0.50, 0.63), xytext=(0.50, 0.63 + top_w),
                    arrowprops=dict(arrowstyle="-|>", lw=7, color=SLIDE_ORANGE))
        ax.annotate("", xy=(0.72, 0.18), xytext=(0.72, 0.37),
                    arrowprops=dict(arrowstyle="-|>", lw=5, color=SLIDE_ROSE))
        ax.text(0.74, 0.18, "gravity", fontsize=12.5, color=SLIDE_ROSE,
                va="center", fontweight="bold")
        ax.text(0.50, 0.93, title, ha="center", va="center",
                fontsize=17, color=SLIDE_TEXT, fontweight="bold")
        ax.text(0.50, 0.82, top_label, ha="center", va="center",
                fontsize=13, color=SLIDE_TEXT)

    axes[0].text(0.50, 0.16, r"net pressure force $=0$", ha="center", va="center",
                 fontsize=13.5, color=SLIDE_TEXT, fontweight="bold")
    axes[1].text(0.50, 0.16, r"net pressure force $>0$", ha="center", va="center",
                 fontsize=13.5, color=SLIDE_TEAL, fontweight="bold")

    fig.suptitle("A Star Is Supported by a Pressure Gradient, Not by Pressure Alone",
                 fontsize=21, color=SLIDE_TEXT, fontweight="bold", y=1.02)
    fig.tight_layout()
    save_slide_figure(fig, "pressure-vs-pressure-gradient.png")


def make_hydrostatic_reasoning_ladder():
    """Preview the logic chain from gravity to a fusion-scale core temperature."""
    fig, ax = plt.subplots(figsize=(14.2, 4.8), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.axis("off")

    steps = [
        ("Gravity", r"$g(r)=\dfrac{GM(r)}{r^2}$", "sets the inward pull", SLIDE_GOLD),
        ("Force Balance", r"$\dfrac{dP}{dr}=-\rho g$", "hydrostatic equilibrium", SLIDE_ROSE),
        ("Pressure Scale", r"$P_c \sim \dfrac{GM^2}{R^4}$", "required central pressure", SLIDE_ORANGE),
        ("Gas Pressure", r"$P \approx P_{\rm gas}$" "\n" r"$\sim \rho \dfrac{k_B T}{\mu m_p}$", "microphysics of support", SLIDE_TEAL),
        ("Temperature Scale", r"$T_c \sim \dfrac{\mu G M m_p}{k_B R}$", "gravity sets the core temperature", ACCENT_BLUE),
    ]

    box_w = 0.16
    box_h = 0.46
    y0 = 0.26
    xs = np.linspace(0.11, 0.89, len(steps))

    for idx, (title, equation, subtitle, color) in enumerate(steps):
        x0 = xs[idx] - box_w / 2.0
        patch = mpatches.FancyBboxPatch(
            (x0, y0),
            box_w,
            box_h,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=SLIDE_PANEL,
            edgecolor=color,
            linewidth=2.2,
        )
        ax.add_patch(patch)
        ax.text(xs[idx], y0 + box_h - 0.09, title, ha="center", va="center",
                fontsize=14.5, color=SLIDE_TEXT, fontweight="bold")
        ax.text(xs[idx], y0 + 0.21, equation, ha="center", va="center",
                fontsize=13.5, color=color, fontweight="bold")
        ax.text(xs[idx], y0 + 0.07, subtitle, ha="center", va="center",
                fontsize=12, color=SLIDE_MUTED)

        if idx < len(steps) - 1:
            ax.annotate(
                "",
                xy=(xs[idx + 1] - box_w / 2.0 - 0.018, y0 + box_h / 2.0),
                xytext=(xs[idx] + box_w / 2.0 + 0.018, y0 + box_h / 2.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=SLIDE_GRID),
            )

    ax.text(0.50, 0.92, "The Logic of Hydrostatic Equilibrium",
            ha="center", va="center", fontsize=20.5, color=SLIDE_TEXT, fontweight="bold")
    ax.text(
        0.50,
        0.10,
        "Guiding question: what holds a star up, and how hot must the core be for that support to exist?",
        ha="center",
        va="center",
        fontsize=12.5,
        color=SLIDE_TEXT,
        bbox=dict(boxstyle="round,pad=0.34", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
    )

    fig.tight_layout()
    save_slide_figure(fig, "hydrostatic-reasoning-ladder.png")


def make_hydrostatic_equilibrium():
    """Cross-section view of local shell-by-shell force balance in a star."""
    fig, ax = plt.subplots(figsize=(8.8, 8.2), dpi=220, subplot_kw={"aspect": "equal"})
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.axis("off")

    for radius, color, alpha in [(1.0, SLIDE_GOLD, 0.16), (0.72, SLIDE_ORANGE, 0.14), (0.44, SLIDE_TEAL, 0.18)]:
        ax.add_patch(plt.Circle((0, 0), radius, facecolor=color, edgecolor=color, alpha=alpha, linewidth=2))

    ax.add_patch(plt.Circle((0, 0), 0.60, fill=False, edgecolor=SLIDE_TEXT, linewidth=2.0, linestyle="--"))
    ax.text(0.55, 0.66, r"thin shell at $r$", fontsize=13.5, color=SLIDE_TEXT, fontweight="bold")

    for angle in np.linspace(0, 2 * np.pi, 10, endpoint=False):
        x1, y1 = 0.62 * np.cos(angle), 0.62 * np.sin(angle)
        x2, y2 = 0.86 * np.cos(angle), 0.86 * np.sin(angle)
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=SLIDE_ROSE, lw=1.8, alpha=0.85))
    for angle in np.linspace(0, 2 * np.pi, 10, endpoint=False):
        x1, y1 = 0.30 * np.cos(angle), 0.30 * np.sin(angle)
        x2, y2 = 0.54 * np.cos(angle), 0.54 * np.sin(angle)
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=SLIDE_TEAL, lw=1.8, alpha=0.85))

    ax.text(0, 0, "core", ha="center", va="center", fontsize=14.5, color=SLIDE_TEXT, fontweight="bold")
    ax.text(-1.05, -0.95, "gravity pulls every shell inward", fontsize=12.5, color=SLIDE_ROSE, fontweight="bold")
    ax.text(-1.05, -1.10, "the pressure gradient pushes outward", fontsize=12.5, color=SLIDE_TEAL, fontweight="bold")
    ax.text(0.0, 1.16, "Hydrostatic equilibrium is local: each shell supports the weight above it.",
            ha="center", va="bottom", fontsize=13, color=SLIDE_TEXT,
            bbox=dict(boxstyle="round,pad=0.35", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.30)
    fig.tight_layout()
    save_slide_figure(fig, "hydrostatic-equilibrium.png")


def make_hydrostatic_shell_force_balance():
    """Annotated shell-force diagram mirroring the derivation in the reading."""
    fig, ax = plt.subplots(figsize=(12.5, 5.3), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.axis("off")

    shell = mpatches.FancyBboxPatch((0.34, 0.32), 0.32, 0.30,
                                    boxstyle="round,pad=0.03,rounding_size=0.03",
                                    facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID, linewidth=1.5)
    ax.add_patch(shell)
    ax.text(0.50, 0.47, r"shell: $\rho(r),\,A,\,dr$", ha="center", va="center",
            fontsize=15.5, color=SLIDE_TEXT, fontweight="bold")

    ax.annotate("", xy=(0.28, 0.47), xytext=(0.08, 0.47),
                arrowprops=dict(arrowstyle="-|>", lw=7, color=SLIDE_TEAL))
    ax.text(0.06, 0.56, r"$F_{\rm in}=P(r)A$", fontsize=13.5, color=SLIDE_TEAL, fontweight="bold")

    ax.annotate("", xy=(0.72, 0.47), xytext=(0.92, 0.47),
                arrowprops=dict(arrowstyle="-|>", lw=5, color=SLIDE_ORANGE))
    ax.text(0.74, 0.56, r"$F_{\rm out}=P(r+dr)A$", fontsize=13.5, color=SLIDE_ORANGE, fontweight="bold")

    ax.annotate("", xy=(0.50, 0.14), xytext=(0.50, 0.30),
                arrowprops=dict(arrowstyle="-|>", lw=6, color=SLIDE_ROSE))
    ax.text(0.52, 0.13, r"$F_g=-g(r)\rho A\,dr$", fontsize=13.5, color=SLIDE_ROSE, fontweight="bold")

    ax.text(0.50, 0.82, r"$F_P = P(r)A - P(r+dr)A \approx -A\frac{dP}{dr}dr$",
            ha="center", fontsize=15.5, color=SLIDE_TEXT, fontweight="bold")
    ax.text(0.50, 0.74, r"because $dP/dr<0$, the pressure-gradient force points outward",
            ha="center", fontsize=13, color=SLIDE_TEXT)
    ax.text(0.50, 0.04, r"Hydrostatic equilibrium: $F_P + F_g = 0$",
            ha="center", fontsize=15.5, color=SLIDE_TEXT, fontweight="bold")

    fig.tight_layout()
    save_slide_figure(fig, "hydrostatic-shell-force-balance.png")


def make_toy_star_radial_profiles():
    """Uniform-density toy-star profiles for M(r), g(r), and P(r)."""
    r = np.linspace(0.0, 1.0, 500)
    mass_profile = r**3
    gravity_profile = r
    pressure_profile = 1.0 - r**2

    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.6), dpi=220, sharex=True)
    fig.patch.set_facecolor(SLIDE_BG)
    series = [
        (mass_profile, SLIDE_TEAL, r"$M(r)/M = (r/R)^3$", "enclosed mass"),
        (gravity_profile, SLIDE_ORANGE, r"$g(r)/g(R) = r/R$", "gravity rises outward inside"),
        (pressure_profile, SLIDE_ROSE, r"$P(r)/P_c = 1-(r/R)^2$", "pressure peaks at the center"),
    ]

    for ax, (yvals, color, equation, subtitle) in zip(axes, series):
        finalize_slide_axes(ax, grid=True)
        ax.plot(r, yvals, color=color, linewidth=3.0)
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.05)
        ax.set_xlabel(r"$r/R$", fontsize=13.5)
        ax.text(0.05, 0.93, equation, transform=ax.transAxes,
                fontsize=12.5, color=color, fontweight="bold")
        ax.text(0.05, 0.83, subtitle, transform=ax.transAxes,
                fontsize=11.5, color=SLIDE_MUTED)
    axes[0].set_ylabel("Normalized value", fontsize=14)
    fig.suptitle("Toy Model: Uniform-Density Star Interior Profiles",
                 fontsize=20, color=SLIDE_TEXT, fontweight="bold", y=1.03)
    fig.text(0.5, -0.02, "This is a toy model, not a real solar model. The point is the trend: support is most demanding in the center.",
             ha="center", fontsize=12, color=SLIDE_MUTED)

    fig.tight_layout()
    save_slide_figure(fig, "toy-star-radial-profiles.png")


def make_pressure_gradient_scale_estimate():
    """Show why dP/dr ~ P_c / R is a reasonable order-of-magnitude estimate."""
    r = np.linspace(0.0, 1.0, 500)
    pressure = np.clip((1.0 - r**1.7) ** 1.25, 0.0, None)

    fig, ax = plt.subplots(figsize=(10.4, 6.6), dpi=220)
    apply_slide_style(fig, ax)
    ax.plot(r, pressure, color=SLIDE_TEAL, linewidth=3.2, label="toy smooth pressure profile")
    ax.fill_between(r, 0.0, pressure, color=SLIDE_TEAL, alpha=0.10)
    ax.plot([0.0, 1.0], [1.0, 0.0], linestyle="--", color=SLIDE_ORANGE, linewidth=2.0,
            label=r"scale estimate: $\Delta P/\Delta r \sim P_c/R$")

    ax.scatter([0.0, 1.0], [1.0, 0.0], color=[SLIDE_ROSE, SLIDE_ORANGE], s=55, zorder=5)
    ax.text(0.02, 1.03, r"$P_c$", color=SLIDE_ROSE, fontsize=13, fontweight="bold")
    ax.text(0.80, 0.06, r"$P(R)\approx 0$", color=SLIDE_ORANGE, fontsize=13, fontweight="bold")

    ax.annotate(
        "",
        xy=(0.06, 0.98),
        xytext=(0.06, 0.02),
        arrowprops=dict(arrowstyle="<->", lw=1.8, color=SLIDE_ROSE),
    )
    ax.text(0.09, 0.52, r"$\Delta P \sim P_c$", color=SLIDE_ROSE,
            fontsize=13, fontweight="bold", va="center")

    ax.annotate(
        "",
        xy=(1.0, -0.10),
        xytext=(0.0, -0.10),
        arrowprops=dict(arrowstyle="<->", lw=1.8, color=SLIDE_ORANGE),
        annotation_clip=False,
    )
    ax.text(0.50, -0.16, r"$\Delta r \sim R$", color=SLIDE_ORANGE,
            fontsize=13, fontweight="bold", ha="center")

    ax.text(0.55, 0.73, "Assume the profile varies smoothly\nacross the star, not in a sharp jump.",
            fontsize=12.5, color=SLIDE_TEXT,
            bbox=dict(boxstyle="round,pad=0.30", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))
    ax.text(0.55, 0.45, r"Then $\dfrac{dP}{dr}$ has the same scale as"
            "\n" r"$\dfrac{\Delta P}{\Delta r} \sim \dfrac{P_c}{R}$",
            fontsize=13, color=SLIDE_TEXT,
            bbox=dict(boxstyle="round,pad=0.30", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-0.20, 1.08)
    ax.set_xlabel(r"Fractional Radius ($r/R$)", fontsize=14.5)
    ax.set_ylabel(r"Normalized Pressure ($P/P_c$)", fontsize=14.5)
    ax.set_title("Why the Pressure-Gradient Scale Is $dP/dr \sim P_c/R$",
                 fontsize=19.5, fontweight="bold", pad=10)
    ax.legend(loc="upper right", frameon=False, fontsize=12)

    fig.tight_layout()
    save_slide_figure(fig, "pressure-gradient-scale-estimate.png")


def make_central_pressure_scaling_grid():
    """Heatmap showing how central pressure depends on mass and radius."""
    masses = np.linspace(0.3, 10.0, 200)
    radii = np.linspace(0.2, 4.0, 200)
    m_grid, r_grid = np.meshgrid(masses, radii)
    pressure = 1.1e16 * (m_grid**2) / (r_grid**4)

    fig, ax = plt.subplots(figsize=(8.8, 6.8), dpi=220)
    apply_slide_style(fig, ax)
    image = ax.pcolormesh(masses, radii, np.log10(pressure), cmap="YlOrRd", shading="auto")
    contours = ax.contour(masses, radii, np.log10(pressure),
                          levels=np.arange(14, 19), colors=SLIDE_TEXT, alpha=0.35, linewidths=0.8)
    ax.clabel(contours, fmt=lambda v: fr"$10^{{{int(v)}}}$", fontsize=10)
    ax.plot(1.0, 1.0, "o", color=SLIDE_TEXT, markersize=7, markeredgecolor=SLIDE_BG, markeredgewidth=1.2)
    ax.text(1.1, 1.06, "Sun", color=SLIDE_TEXT, fontsize=12, fontweight="bold")
    ax.set_xlabel(r"Mass ($M/M_\odot$)", fontsize=14.5)
    ax.set_ylabel(r"Radius ($R/R_\odot$)", fontsize=14.5)
    ax.set_title(r"Order-of-Magnitude Central Pressure from $P_c \sim GM^2/R^4$",
                 fontsize=18.5, fontweight="bold", pad=10)
    cbar = fig.colorbar(image, ax=ax, pad=0.02)
    cbar.set_label(r"$\log_{10}(P_c/\mathrm{dyn\,cm^{-2}})$", color=SLIDE_TEXT, fontsize=13)
    cbar.ax.tick_params(colors=SLIDE_TEXT, labelsize=12)
    cbar.outline.set_edgecolor(SLIDE_GRID)

    fig.tight_layout()
    save_slide_figure(fig, "central-pressure-scaling-grid.png")


def make_radiation_pressure_mass_scaling():
    """Show the relative rise of radiation support with stellar mass."""
    masses = np.logspace(np.log10(0.5), np.log10(60.0), 400)
    relative_ratio = masses**2

    fig, ax = plt.subplots(figsize=(10.8, 6.8), dpi=220)
    apply_slide_style(fig, ax)
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.plot(masses, relative_ratio, color=SLIDE_ROSE, linewidth=3.0)
    ax.fill_between(masses, 1.0, relative_ratio, where=relative_ratio >= 1.0,
                    color=SLIDE_ROSE, alpha=0.10)

    sample_masses = np.array([1.0, 10.0, 30.0])
    sample_ratios = sample_masses**2
    ax.scatter(sample_masses, sample_ratios, s=55, color=[SLIDE_TEAL, SLIDE_ORANGE, SLIDE_ROSE], zorder=5)
    ax.text(1.08, 1.12, "Sun", color=SLIDE_TEXT, fontsize=12, fontweight="bold")
    ax.text(10.7, 115, r"$10\,M_\odot$", color=SLIDE_TEXT, fontsize=12, fontweight="bold")
    ax.text(31.5, 980, r"$30\,M_\odot$", color=SLIDE_TEXT, fontsize=12, fontweight="bold")

    ax.text(
        0.04,
        0.94,
        r"Hydrostatic scaling gives $\dfrac{P_{\rm rad}}{P_{\rm gas}} \propto \dfrac{T^3}{\rho} \propto M^2$"
        "\n"
        r"Vertical axis is normalized so the Sun sits at $1$.",
        transform=ax.transAxes,
        fontsize=12.5,
        color=SLIDE_TEXT,
        va="top",
        bbox=dict(boxstyle="round,pad=0.34", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID),
    )

    ax.set_xlabel(r"Mass ($M/M_\odot$)", fontsize=15)
    ax.set_ylabel(r"Relative $P_{\rm rad}/P_{\rm gas}$" "\n" r"(normalized to Sun)", fontsize=15)
    ax.set_xlim(0.5, 60.0)
    ax.set_ylim(0.2, 5.0e3)
    ax.set_title("Radiation Pressure Gains Ground Rapidly in Massive Stars",
                 fontsize=19.5, fontweight="bold", pad=12)

    fig.tight_layout()
    save_slide_figure(fig, "radiation-pressure-mass-scaling.png")


def make_virial_energy_partition():
    """Correct virial-energy bookkeeping plus the contraction-heating chain."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(13.0, 5.8), dpi=220,
                                            gridspec_kw={"width_ratios": [1.0, 1.1]})
    fig.patch.set_facecolor(SLIDE_BG)

    finalize_slide_axes(ax_left, grid=False)
    energies = np.array([-2.0, 1.0, -1.0])
    labels = [r"$U_{\rm grav}$", r"$K_{\rm th}$", r"$E_{\rm tot}$"]
    colors = [SLIDE_ROSE, SLIDE_TEAL, SLIDE_GOLD]
    ax_left.axhline(0.0, color=SLIDE_GRID, linewidth=1.2)
    ax_left.bar(labels, energies, color=colors, width=0.58)
    ax_left.set_ylim(-2.4, 1.4)
    ax_left.set_ylabel("Relative energy units", fontsize=13.5)
    ax_left.set_title("Virial Energy Ledger", fontsize=17.5, fontweight="bold")
    ax_left.text(0.02, 0.95, r"$2K_{\rm th} + U_{\rm grav} = 0$",
                 transform=ax_left.transAxes, fontsize=13, color=SLIDE_TEXT,
                 fontweight="bold", va="top")
    ax_left.text(0.02, 0.84, r"$K_{\rm th}=-\frac{1}{2}U_{\rm grav}$",
                 transform=ax_left.transAxes, fontsize=12, color=SLIDE_TEXT, va="top")
    ax_left.text(0.02, 0.74, r"$E_{\rm tot}=K_{\rm th}+U_{\rm grav}=\frac{1}{2}U_{\rm grav}<0$",
                 transform=ax_left.transAxes, fontsize=12, color=SLIDE_TEXT, va="top")

    ax_right.set_facecolor(SLIDE_BG)
    ax_right.axis("off")
    chain = [
        ("star radiates\nenergy", SLIDE_ORANGE),
        ("total energy becomes\nmore negative", SLIDE_GOLD),
        ("star contracts", SLIDE_ROSE),
        ("$U_{\\rm grav}$ drops\nfurther", SLIDE_ROSE),
        ("$K_{\\rm th}$ rises", SLIDE_TEAL),
        ("core gets hotter", SLIDE_TEAL),
    ]
    xs = np.linspace(0.08, 0.92, len(chain))
    for idx, ((text, color), xpos) in enumerate(zip(chain, xs)):
        ax_right.text(xpos, 0.55, text, ha="center", va="center",
                      fontsize=12.5, color=SLIDE_TEXT,
                      bbox=dict(boxstyle="round,pad=0.35", facecolor=SLIDE_PANEL, edgecolor=color, linewidth=1.6))
        if idx < len(chain) - 1:
            ax_right.annotate("", xy=(xs[idx + 1] - 0.055, 0.55), xytext=(xpos + 0.055, 0.55),
                              arrowprops=dict(arrowstyle="-|>", color=color, lw=1.7))
    ax_right.set_title("Why Losing Energy Can Make a Star Hotter",
                       fontsize=17.5, color=SLIDE_TEXT, fontweight="bold", pad=12)

    fig.tight_layout()
    save_slide_figure(fig, "virial-energy-partition.png")


def make_core_temperature_scaling():
    """Show that hydrostatic core temperature rises only weakly across the MS."""
    masses = np.logspace(np.log10(0.1), np.log10(20.0), 400)
    radius = masses**0.8
    temperature = 15.0 * masses / radius
    fixed_radius = 15.0 * masses

    fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=220)
    apply_slide_style(fig, ax)
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.plot(masses, temperature, color=SLIDE_TEAL, linewidth=3.0,
            label=r"hydrostatic scaling: $T_c \propto M/R$ with $R \propto M^{0.8}$")
    ax.plot(masses, fixed_radius, color=SLIDE_MUTED, linewidth=1.8, linestyle="--",
            label=r"if radius were fixed: $T_c \propto M$")
    ax.plot(1.0, 15.0, "o", color=SLIDE_TEAL, markersize=8, markeredgecolor=SLIDE_BG, markeredgewidth=1.3)
    ax.text(1.08, 16.3, "Sun", color=SLIDE_TEXT, fontsize=12, fontweight="bold")
    ax.text(0.13, 45, "gravity sets the\nfusion-scale temperature", color=SLIDE_TEAL,
            fontsize=12, fontweight="bold")

    ax.set_xlabel(r"Mass ($M/M_\odot$)", fontsize=15)
    ax.set_ylabel(r"Core Temperature Scale (MK)", fontsize=15)
    ax.set_xlim(0.1, 20.0)
    ax.set_ylim(5.0, 4.0e2)
    ax.set_title("Hydrostatic Equilibrium Predicts Only a Modest Rise in Core Temperature",
                 fontsize=19.5, fontweight="bold", pad=12)
    ax.legend(loc="upper left", frameon=False, fontsize=12)

    fig.tight_layout()
    save_slide_figure(fig, "core-temperature-scaling.png")


def make_fusion_force_scale_map():
    """Scale map showing which force matters where in the fusion story."""
    fig, ax = plt.subplots(figsize=(12.4, 5.8), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.set_xscale("log")
    ax.set_xlim(1e-16, 2e11)
    ax.set_ylim(-0.6, 4.4)

    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(SLIDE_GRID)
    ax.spines["bottom"].set_linewidth(1.1)
    ax.tick_params(axis="x", colors=SLIDE_TEXT, labelsize=12.5)
    ax.tick_params(axis="y", length=0, colors=SLIDE_TEXT, labelsize=12.5, pad=14)
    ax.grid(True, axis="x", color=SLIDE_GRID, linewidth=0.8, alpha=0.9)

    rows = [
        ("weak interaction", 3.3, 5e-17, 2e-16, SLIDE_GOLD,
         "proton-to-neutron conversion\nin Step 1"),
        ("strong interaction", 2.3, 4e-14, 4e-13, SLIDE_TEAL,
         "binds nucleons once they\nreach nuclear distance"),
        ("electromagnetism", 1.3, 1e-13, 5e-7, SLIDE_ROSE,
         "charged nuclei repel during approach"),
        ("gravity", 0.3, 5e8, 7e10, "#4d7cab",
         "compresses the whole star\nand sets the core conditions"),
    ]

    ax.set_yticks([3.3, 2.3, 1.3, 0.3])
    ax.set_yticklabels([row[0] for row in rows], fontweight="bold")
    for tick, (_, _, _, _, color, _) in zip(ax.get_yticklabels(), rows):
        tick.set_color(color)

    for label, y, x1, x2, color, note in rows:
        ax.plot([x1, x2], [y, y], color=color, linewidth=9, solid_capstyle="round")
        ax.text(x2 * 1.08, y, note, ha="left", va="center",
                fontsize=10.4, color=SLIDE_TEXT)

    scale_markers = [
        (1e-16, "weak"),
        (1e-13, "1 fm\nnuclear"),
        (1e-8, "atom"),
        (7e10, "Sun radius"),
    ]
    for x, label in scale_markers:
        ax.axvline(x, color=SLIDE_GRID, linewidth=1.0, linestyle=(0, (3, 3)))
        ax.text(x, -0.16, label, ha="center", va="top",
                fontsize=10.3, color=SLIDE_MUTED)

    ax.text(0.98, 0.94,
            "This is a dominance map for the fusion story,\nnot a literal plot of force magnitude.",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=10.2, color=SLIDE_MUTED,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    ax.set_xlabel("Characteristic Length Scale (cm)", fontsize=14, color=SLIDE_TEXT, labelpad=8)
    ax.set_title("Which Force Matters Where in Stellar Fusion?",
                 fontsize=18.5, color=SLIDE_TEXT, fontweight="bold", pad=12)

    fig.tight_layout()
    save_slide_figure(fig, "fusion-force-scale-map.png")


def make_maxwell_boltzmann_speeds_solar_core():
    """Physically computed proton speed distribution in the solar core."""
    v = np.linspace(0.0, 2.4e8, 800)
    prefactor = 4.0 * np.pi * (M_P_CGS / (2.0 * np.pi * K_B_CGS * T_CORE_SUN)) ** 1.5
    pdf = prefactor * v**2 * np.exp(-M_P_CGS * v**2 / (2.0 * K_B_CGS * T_CORE_SUN))
    pdf /= pdf.max()

    v_mp = np.sqrt(2.0 * K_B_CGS * T_CORE_SUN / M_P_CGS)
    v_mean = np.sqrt(8.0 * K_B_CGS * T_CORE_SUN / (np.pi * M_P_CGS))
    v_rms = np.sqrt(3.0 * K_B_CGS * T_CORE_SUN / M_P_CGS)

    fig, ax = plt.subplots(figsize=(11.8, 6.8), dpi=220)
    apply_slide_style(fig, ax)
    ax.plot(v / 1.0e7, pdf, color=SLIDE_TEAL, linewidth=3.0)
    ax.fill_between(v / 1.0e7, 0.0, pdf, color=SLIDE_TEAL, alpha=0.12)

    for value, label, color in [(v_mp, "most probable", SLIDE_ORANGE),
                                (v_mean, "mean", SLIDE_GOLD),
                                (v_rms, "rms", SLIDE_ROSE)]:
        ax.axvline(value / 1.0e7, color=color, linewidth=1.6, linestyle=(0, (4, 3)))
        ax.text(value / 1.0e7 + 0.08, 0.92, label, color=color, fontsize=12,
                fontweight="bold", rotation=90, va="top")

    ax.text(0.66, 0.95,
            fr"$T = {T_CORE_SUN:.1e}\,$K" "\n"
            fr"$v_{{\rm mp}} \approx {v_mp/1.0e7:.1f}\times10^7$ cm s$^{{-1}}$",
            transform=ax.transAxes, fontsize=12.5, color=SLIDE_TEXT,
            va="top", bbox=dict(boxstyle="round,pad=0.35", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    ax.set_xlabel(r"Proton Speed ($10^7\,\mathrm{cm\,s^{-1}}$)", fontsize=15)
    ax.set_ylabel("Normalized Probability Density", fontsize=15)
    ax.set_xlim(0.0, 24.0)
    ax.set_ylim(0.0, 1.08)
    ax.set_title("Maxwell-Boltzmann Proton Speeds in the Solar Core",
                 fontsize=19.5, fontweight="bold", pad=12)

    fig.tight_layout()
    save_slide_figure(fig, "maxwell-boltzmann-speeds-solar-core.png")


def make_fusion_energy_scale_ladder():
    """Log-scale comparison of the key proton-fusion energy scales."""
    kT_kev = (K_B_CGS * T_CORE_SUN) / KEV_TO_ERG
    mean_kev = 1.5 * kT_kev
    barrier_kev = 1400.0
    energy_kev = np.linspace(0.2, 45.0, 900)
    gamow_kev = 493.0
    product = np.exp(-energy_kev / kT_kev) * np.exp(-np.sqrt(gamow_kev / energy_kev))
    peak_kev = energy_kev[np.argmax(product)]

    fig, ax = plt.subplots(figsize=(11.8, 3.8), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.set_xscale("log")
    ax.set_xlim(0.7, 4000.0)
    ax.set_ylim(-0.8, 0.95)

    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(SLIDE_GRID)
    ax.spines["bottom"].set_linewidth(1.1)
    ax.tick_params(axis="x", colors=SLIDE_TEXT, labelsize=12.5)
    ax.tick_params(axis="y", length=0)
    ax.grid(True, axis="x", color=SLIDE_GRID, linewidth=0.8, alpha=0.9)

    ax.hlines(0.0, 1.0, barrier_kev, color=SLIDE_MUTED, linewidth=3.0, alpha=0.35)
    ax.annotate("", xy=(barrier_kev, 0.0), xytext=(1.0, 0.0),
                arrowprops=dict(arrowstyle="<->", lw=1.5, color=SLIDE_MUTED))
    ax.text(np.sqrt(barrier_kev), 0.16, r"factor $\sim 10^3$",
            ha="center", va="bottom", fontsize=10.8, color=SLIDE_MUTED, fontweight="bold")

    markers = [
        (kT_kev, SLIDE_TEAL, r"$k_B T \approx 1.3\,\mathrm{keV}$", -0.35),
        (mean_kev, SLIDE_GOLD, r"$\langle E \rangle \approx 1.9\,\mathrm{keV}$", 0.33),
        (peak_kev, SLIDE_ORANGE, fr"Gamow window few-keV peak" "\n" fr"$\approx {peak_kev:.1f}\,\mathrm{{keV}}$", -0.35),
        (barrier_kev, SLIDE_ROSE, r"Coulomb barrier" "\n" r"$\approx 1.4\,\mathrm{MeV}$", 0.33),
    ]
    for x, color, label, y in markers:
        ax.plot(x, 0.0, marker="o", markersize=10, color=color, markeredgecolor=SLIDE_BG, markeredgewidth=1.2, zorder=5)
        ax.vlines(x, 0.0, y * 0.75, color=color, linewidth=1.8, linestyle=(0, (3, 2)))
        ax.text(x, y, label, ha="center", va="center", fontsize=10.6, color=color,
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    ax.text(0.98, 0.90, "Solar-core fusion is a few-keV problem confronting a MeV barrier.",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=10.4, color=SLIDE_TEXT)

    ax.set_xlabel("Energy (keV)", fontsize=14, color=SLIDE_TEXT, labelpad=8)
    ax.set_yticks([])
    ax.set_title("The Key Energy Scales for Proton-Proton Fusion",
                 fontsize=18, color=SLIDE_TEXT, fontweight="bold", pad=12)

    fig.tight_layout()
    save_slide_figure(fig, "fusion-energy-scale-ladder.png")


def make_maxwell_boltzmann_energies_barrier_tail():
    """Energy distribution with the Coulomb barrier far out in the tail."""
    energy_kev = np.linspace(0.01, 1500.0, 2200)
    energy_erg = energy_kev * KEV_TO_ERG
    kT = K_B_CGS * T_CORE_SUN
    pdf = (2.0 / np.sqrt(np.pi)) * np.sqrt(energy_erg) * np.exp(-energy_erg / kT) / (kT ** 1.5)
    pdf /= pdf.max()
    barrier_kev = 1400.0
    thermal_kev = kT / KEV_TO_ERG
    thermal32_kev = 1.5 * thermal_kev

    fig, ax = plt.subplots(figsize=(11.8, 6.8), dpi=220)
    apply_slide_style(fig, ax)
    ax.semilogy(energy_kev, pdf, color=SLIDE_ORANGE, linewidth=3.0)
    ax.axvline(thermal_kev, color=SLIDE_TEAL, linewidth=1.8, linestyle=(0, (4, 3)))
    ax.axvline(thermal32_kev, color=SLIDE_GOLD, linewidth=1.6, linestyle=(0, (2, 2)))
    ax.axvline(barrier_kev, color=SLIDE_ROSE, linewidth=2.0)
    ax.axvspan(barrier_kev, 1500.0, color=SLIDE_ROSE, alpha=0.10)

    ax.text(65, 2.5e-1, r"$k_B T \approx 1.3$ keV" "\n"
            r"$\frac{3}{2}k_B T \approx 2$ keV",
            color=SLIDE_TEXT, fontsize=10.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))
    ax.text(barrier_kev - 18, 2e-10, "Coulomb barrier\n~1.4 MeV", color=SLIDE_ROSE,
            fontsize=10.5, fontweight="bold", ha="right", va="bottom")
    ax.text(760, 5e-12, "Classically accessible particles\nlive in an effectively empty tail.",
            color=SLIDE_TEXT, fontsize=10.5, ha="center",
            bbox=dict(boxstyle="round,pad=0.35", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    ax.set_xlabel("Proton Kinetic Energy (keV)", fontsize=14)
    ax.set_ylabel("Normalized Probability Density", fontsize=14)
    ax.set_xlim(0.0, 1500.0)
    ax.set_ylim(1.0e-14, 2.0)
    ax.set_title("The Coulomb Barrier Sits Far Out in the Maxwell-Boltzmann Tail",
                 fontsize=18, fontweight="bold", pad=12)

    fig.tight_layout()
    save_slide_figure(fig, "maxwell-boltzmann-energies-barrier-tail.png")


def make_coulomb_barrier_and_tunneling():
    """Potential-energy schematic with honest scale separation and tunneling region."""
    r_fm = np.logspace(np.log10(0.4), np.log10(1000.0), 1200)
    coulomb = E2_MEV_FM / r_fm
    nuclear_well = -32.0 * np.exp(-((r_fm - 0.65) / 0.22) ** 2)
    total = coulomb + nuclear_well
    thermal_mev = 0.002
    turning_point = E2_MEV_FM / thermal_mev

    fig, ax = plt.subplots(figsize=(11.8, 6.9), dpi=220)
    apply_slide_style(fig, ax)
    ax.set_xscale("log")
    ax.plot(r_fm, coulomb, color=SLIDE_ROSE, linewidth=2.4, label="Coulomb repulsion")
    ax.plot(r_fm, total, color=SLIDE_TEAL, linewidth=3.0, label="schematic total potential")
    ax.axhline(thermal_mev, color=SLIDE_GOLD, linewidth=1.8, linestyle=(0, (4, 3)))
    ax.axvspan(1.0, turning_point, color=SLIDE_ORANGE, alpha=0.08)
    ax.axvline(1.0, color=SLIDE_TEXT, linewidth=1.0, linestyle=":")

    ax2 = ax.twinx()
    ax2.set_ylim(-1.1, 1.1)
    ax2.set_yticks([])
    for side in ("top", "right", "left", "bottom"):
        ax2.spines[side].set_visible(False)
    ax2.tick_params(left=False, right=False, labelleft=False, labelright=False, bottom=False, labelbottom=False)

    allowed = r_fm >= turning_point
    forbidden = (r_fm < turning_point) & (r_fm >= 1.0)
    inside = r_fm < 1.0
    psi_allowed = 0.55 * np.sin(10.0 * np.log(r_fm[allowed] / turning_point) + 0.4)
    psi_forbidden = 0.55 * (r_fm[forbidden] / turning_point) ** 1.05
    psi_inside = 0.10 * np.sin(12.0 * (r_fm[inside] - 0.45)) - 0.08

    ax2.plot(r_fm[allowed], psi_allowed, color=ACCENT_BLUE, linewidth=2.0, alpha=0.95)
    ax2.plot(r_fm[forbidden], psi_forbidden, color=ACCENT_BLUE, linewidth=2.4, alpha=0.95)
    ax2.plot(r_fm[inside], psi_inside, color=ACCENT_BLUE, linewidth=2.0, alpha=0.95)

    ax.text(1.08, 1.55, "nuclear scale\n~1 fm", color=SLIDE_TEXT, fontsize=10.5, fontweight="bold")
    ax.text(turning_point * 0.88, 0.012, "classical turning point\nfor a few-keV proton",
            color=SLIDE_GOLD, fontsize=10.3, fontweight="bold", ha="right")
    ax.text(18.0, 0.22, "classically forbidden region:\nquantum tunneling is required",
            color=SLIDE_ORANGE, fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))
    ax.text(210.0, 1.45,
            "schematic wavefunction amplitude\noscillatory outside, decaying inside barrier",
            color=ACCENT_BLUE, fontsize=10.3, fontweight="bold", ha="right",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    ax.set_xlabel("Separation (fm)", fontsize=14)
    ax.set_ylabel("Potential Energy (MeV)", fontsize=14)
    ax.set_xlim(0.4, 1000.0)
    ax.set_ylim(-1.2, 2.2)
    ax.set_title("Coulomb Barrier and Quantum Tunneling for Proton-Proton Fusion",
                 fontsize=17.5, fontweight="bold", pad=12)
    ax.legend(loc="upper right", frameon=False, fontsize=10.2)

    fig.tight_layout()
    save_slide_figure(fig, "coulomb-barrier-and-tunneling.png")


def make_gamow_window_cartoon():
    """Pedagogical Gamow-window style plot from Maxwell and tunneling factors."""
    energy_kev = np.linspace(0.2, 45.0, 900)
    kT_kev = (K_B_CGS * T_CORE_SUN) / KEV_TO_ERG
    gamow_kev = 493.0

    maxwell = np.exp(-energy_kev / kT_kev)
    tunneling = np.exp(-np.sqrt(gamow_kev / energy_kev))
    product = maxwell * tunneling
    maxwell /= maxwell.max()
    tunneling /= tunneling.max()
    product /= product.max()
    peak_energy = energy_kev[np.argmax(product)]

    fig, ax = plt.subplots(figsize=(11.4, 6.6), dpi=220)
    apply_slide_style(fig, ax)
    ax.plot(energy_kev, maxwell, color=SLIDE_ORANGE, linewidth=2.4, label="Maxwell factor")
    ax.plot(energy_kev, tunneling, color=SLIDE_TEAL, linewidth=2.4, label="tunneling factor")
    ax.plot(energy_kev, product, color=SLIDE_ROSE, linewidth=3.2, label="combined weighting")
    ax.axvline(peak_energy, color=SLIDE_GOLD, linewidth=1.7, linestyle=(0, (4, 3)))
    ax.text(peak_energy + 0.7, 0.92, fr"Gamow-like peak\n$\approx {peak_energy:.1f}$ keV",
            color=SLIDE_GOLD, fontsize=10.5, fontweight="bold")
    ax.text(0.98, 0.95, "schematic weighting,\nnot a full cross section",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=10, color=SLIDE_MUTED)

    ax.set_xlabel("Collision Energy (keV)", fontsize=14)
    ax.set_ylabel("Relative Weight", fontsize=14)
    ax.set_xlim(0.0, 45.0)
    ax.set_ylim(0.0, 1.08)
    ax.set_title("Why Fusion Comes from a Narrow Energy Window",
                 fontsize=18, fontweight="bold", pad=12)
    ax.legend(loc="upper right", frameon=False, fontsize=10.2)

    fig.tight_layout()
    save_slide_figure(fig, "gamow-window-cartoon.png")


def make_pp_chain():
    """Reaction-flow diagram with force labels and the weak bottleneck."""
    fig, ax = plt.subplots(figsize=(13.6, 5.8), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.axis("off")

    boxes = [
        (0.09, 0.55, r"$p+p$", "charged protons approach"),
        (0.34, 0.55, r"$d + e^+ + \nu_e$", "Step 1: weak bottleneck"),
        (0.59, 0.55, r"$^3{\rm He} + \gamma$", "Step 2: strong binding"),
        (0.84, 0.55, r"$^4{\rm He} + 2p$", "Step 3: helium made"),
    ]
    for x0, y0, title, subtitle in boxes:
        ax.text(x0, y0, title, ha="center", va="center",
                fontsize=15, color=SLIDE_TEXT, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.42", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID, linewidth=1.4))
        ax.text(x0, y0 - 0.12, subtitle, ha="center", va="top", fontsize=10, color=SLIDE_MUTED)

    arrows = [
        (0.16, 0.52, 0.27, 0.52, "EM tunneling + weak conversion", SLIDE_ORANGE),
        (0.41, 0.52, 0.52, 0.52, "EM encounter + strong binding", SLIDE_TEAL),
        (0.66, 0.52, 0.77, 0.52, "EM encounter + strong binding", SLIDE_TEAL),
    ]
    for x1, y1, x2, y2, text, color in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", lw=2.0, color=color))
        ax.text((x1 + x2) / 2.0, y1 + 0.07, text, ha="center", va="bottom",
                fontsize=10, color=color, fontweight="bold")

    ax.text(0.34, 0.79, "This first step is slow enough\nto keep the Sun alive for billions of years.",
            ha="center", va="center", fontsize=11.2, color=SLIDE_ROSE, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", facecolor=SLIDE_PANEL, edgecolor=SLIDE_ROSE, linewidth=1.5))
    ax.text(0.50, 0.15,
            r"net: $4p \rightarrow {}^4{\rm He} + 2e^+ + 2\nu_e + \gamma + \mathrm{energy}$",
            ha="center", va="center", fontsize=14, color=SLIDE_TEXT, fontweight="bold")
    ax.text(0.50, 0.94, "The Proton-Proton Chain Uses All Four Forces",
            ha="center", va="center", fontsize=18, color=SLIDE_TEXT, fontweight="bold")

    fig.tight_layout()
    save_slide_figure(fig, "pp-chain.png")


def make_fusion_energy_budget():
    """Compact energy bookkeeping for one net pp-chain reaction."""
    fig, ax = plt.subplots(figsize=(11.6, 4.8), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
    ax.axis("off")

    total = 26.7
    retained = 26.2
    neutrino = 0.5

    ax.text(0.05, 0.85, r"Mass deficit: $\Delta m = 0.02872\,\mathrm{amu}$",
            fontsize=13, color=SLIDE_TEXT, fontweight="bold")
    ax.text(0.05, 0.73, r"$E = \Delta m c^2 \approx 26.7\,\mathrm{MeV}$",
            fontsize=16, color=SLIDE_ROSE, fontweight="bold")

    x0, y0, width, height = 0.08, 0.38, 0.78, 0.16
    ax.add_patch(mpatches.Rectangle((x0, y0), width, height, facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID, linewidth=1.2))
    retained_width = width * retained / total
    neutrino_width = width * neutrino / total
    ax.add_patch(mpatches.Rectangle((x0, y0), retained_width, height, facecolor=SLIDE_TEAL, edgecolor="none"))
    ax.add_patch(mpatches.Rectangle((x0 + retained_width, y0), neutrino_width, height, facecolor=SLIDE_GOLD, edgecolor="none"))

    ax.text(x0 + retained_width / 2, y0 + height / 2, r"$26.2\,\mathrm{MeV}$ stays in the star",
            ha="center", va="center", fontsize=12, color="white", fontweight="bold")
    ax.text(x0 + retained_width + neutrino_width / 2, y0 + height / 2,
            r"$0.5\,\mathrm{MeV}$", ha="center", va="center",
            fontsize=11, color=SLIDE_TEXT, fontweight="bold")
    ax.annotate("neutrinos escape", xy=(x0 + retained_width + neutrino_width / 2, y0 + height),
                xytext=(0.83, 0.69), textcoords="axes fraction",
                fontsize=11, color=SLIDE_GOLD, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SLIDE_GOLD, lw=1.4))
    ax.text(0.08, 0.16,
            "Almost all of the released energy thermalizes inside the star.\n"
            "That is why the Sun's luminosity tracks fusion while neutrinos reveal the core directly.",
            fontsize=11.2, color=SLIDE_TEXT)

    fig.tight_layout()
    save_slide_figure(fig, "fusion-energy-budget.png")


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
    fig, ax = plt.subplots(figsize=(10, 10), dpi=220, subplot_kw={"aspect": "equal"})
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
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
         "r": 0.14, "color": "#8f2b45", "alpha": 0.85},
    ]

    # Draw shells from outside in
    for shell in shells:
        circle = plt.Circle((0, 0), shell["r"], facecolor=shell["color"],
                            alpha=shell["alpha"], edgecolor=shell["color"],
                            linewidth=1.5, zorder=2)
        ax.add_patch(circle)

    # Iron core glow effect
    for r_frac in np.linspace(0.14, 0.02, 8):
        glow = plt.Circle((0, 0), r_frac, facecolor=SLIDE_ROSE,
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
    ax.text(0, 0, "Fe\ncore", fontsize=14, color=SLIDE_BG,
            ha="center", va="center", fontweight="bold", zorder=5)
    ax.text(0, -0.20, "INERT\n(nuclear ash)", fontsize=8, color=SLIDE_ROSE,
            ha="center", va="center", zorder=5, alpha=0.8)

    # Title and subtitle
    ax.text(0, 1.15, "Onion-Shell Structure", fontsize=20,
            color=SLIDE_TEXT, ha="center", va="center", fontweight="bold")
    ax.text(0, 1.07, "A 25 M☉ star, moments before core collapse",
            fontsize=12, color=SLIDE_MUTED, ha="center", va="center")

    # Time acceleration note
    ax.text(
        0, -1.12,
        "Each layer burns faster than the last:\n"
        "H burning lasts millions of years  →  Si burning lasts one day",
        fontsize=10, color=SLIDE_ORANGE, ha="center", va="center",
        fontstyle="italic",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=SLIDE_PANEL,
                  edgecolor=SLIDE_ORANGE),
    )

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)

    fig.tight_layout()
    save_slide_figure(fig, "onion-shell-burning.png")


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
    fig, ax = plt.subplots(figsize=(10.6, 7.0), dpi=220)
    apply_slide_style(fig, ax)

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
    ax.plot(M_nr, R_nr / R_earth, "--", color=SLIDE_ORANGE, linewidth=1.6,
            alpha=0.4, label=r"Non-relativistic: $R \propto M^{-1/3}$")
    ax.plot(M_full, R_full / R_earth, "-", color=SLIDE_TEAL, linewidth=3,
            label="Full relativistic", zorder=4)

    # Chandrasekhar limit vertical line
    ax.axvline(M_ch, color=SLIDE_ROSE, linewidth=2, linestyle="--",
               alpha=0.7, zorder=3)
    ax.text(M_ch + 0.02, 1.8, f"$M_{{\\rm Ch}} = {M_ch}\\,M_\\odot$",
            fontsize=14, color=SLIDE_ROSE, fontweight="bold", rotation=0)
    ax.text(M_ch + 0.02, 1.6, "Chandrasekhar\nlimit", fontsize=10,
            color=SLIDE_ROSE, alpha=0.8)

    # Key white dwarfs
    known_wds = [
        (0.50, "Sirius B\n(0.50 M☉)", ACCENT_YELLOW),
        (1.02, "Sirius B*\n(1.02 M☉)", ACCENT_YELLOW),
        (0.60, "Typical WD\n(0.60 M☉)", ACCENT_GREEN),
    ]
    # Actually, Sirius B is 1.02 M_sun. Let me use correct values.
    known_wds = [
        (1.02, "Sirius B", SLIDE_GOLD),
        (0.60, "Typical WD", SLIDE_TEAL),
    ]
    for M_wd, label, color in known_wds:
        R_wd = R_0 * M_wd**(-1/3) * np.sqrt(max(0, 1 - (M_wd / M_ch)**(4/3)))
        ax.plot(M_wd, R_wd / R_earth, "o", color=color, markersize=10,
                markeredgecolor=SLIDE_BG, markeredgewidth=1.5, zorder=6)
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
        fontsize=11, color=SLIDE_ORANGE, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=SLIDE_ORANGE, lw=1.5),
        bbox=dict(boxstyle="round,pad=0.3", facecolor=SLIDE_PANEL,
                  edgecolor=SLIDE_ORANGE),
    )

    # Earth reference
    ax.axhline(1.0, color=SLIDE_GOLD, linewidth=0.8, alpha=0.45, linestyle=":")
    ax.text(0.17, 1.03, "$R_\\oplus$", fontsize=10, color=SLIDE_GOLD, alpha=0.8)

    # "Gravity wins" region
    ax.fill_betweenx([0, 2.2], M_ch, 1.6, color=SLIDE_ROSE,
                     alpha=0.05, zorder=1)
    ax.text(1.50, 0.3, "GRAVITY\nWINS", fontsize=14, color=SLIDE_ROSE,
            ha="center", fontweight="bold", alpha=0.4)

    ax.set_xlabel(r"White Dwarf Mass ($M / M_\odot$)", fontsize=14)
    ax.set_ylabel(r"White Dwarf Radius ($R / R_\oplus$)", fontsize=14)
    ax.set_title("White Dwarf Mass-Radius Relation", fontsize=18,
                 fontweight="bold", pad=15)
    ax.set_xlim(0.1, 1.6)
    ax.set_ylim(0, 2.2)
    ax.text(0.03, 0.95, "toy equation with relativistic cutoff",
            transform=ax.transAxes, fontsize=10.2, color=SLIDE_MUTED,
            bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))
    ax.legend(fontsize=11, loc="upper right", frameon=False)

    fig.tight_layout()
    save_slide_figure(fig, "wd-mass-radius.png")


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
    fig, ax = plt.subplots(figsize=(14, 7), dpi=220)
    fig.patch.set_facecolor(SLIDE_BG)
    ax.set_facecolor(SLIDE_BG)
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
                            edgecolor=SLIDE_ROSE, linewidth=2, zorder=5)
            ax.add_patch(bh)
            # Accretion ring glow
            for dr in [0.003, 0.006, 0.009]:
                glow = plt.Circle((x, y_center), r_visual + dr,
                                  facecolor="none", edgecolor=SLIDE_ORANGE,
                                  linewidth=1, alpha=0.3 - dr * 20, zorder=4)
                ax.add_patch(glow)
        elif obj["name"] == "Neutron Star":
            # Neutron star: small bright orange dot
            ns = plt.Circle((x, y_center), r_visual, facecolor=SLIDE_ORANGE,
                            edgecolor=SLIDE_BG, linewidth=1.5, zorder=5)
            ax.add_patch(ns)
            # Glow effect
            for dr in [0.005, 0.010, 0.015]:
                glow = plt.Circle((x, y_center), r_visual + dr,
                                  facecolor=SLIDE_ORANGE,
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
            fontsize=20, color=SLIDE_TEXT, ha="center", va="top",
            fontweight="bold", transform=ax.transAxes)

    # Scale note
    ax.text(
        0.5, 0.03,
        "A white dwarf packs a star's mass into an Earth-sized sphere.  "
        "A neutron star packs it into a city.  "
        "A black hole has no surface at all.",
        fontsize=11, color=SLIDE_MUTED, ha="center", va="bottom",
        fontstyle="italic", transform=ax.transAxes,
    )

    # "Not to scale" with arrow between WD and NS
    ax.annotate(
        "×600 smaller!", xy=(0.52, y_center), xytext=(0.52, y_center + 0.04),
        fontsize=10, color=SLIDE_GOLD, ha="center", fontweight="bold",
    )
    ax.annotate(
        "", xy=(0.63, y_center), xytext=(0.46, y_center),
        arrowprops=dict(arrowstyle="<->", color=SLIDE_GOLD, lw=1.5, alpha=0.6),
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    save_slide_figure(fig, "compact-object-scale.png")


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
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), dpi=220,
                             subplot_kw={"aspect": "equal"})
    fig.patch.set_facecolor(SLIDE_BG)

    def draw_star(ax, title, subtitle, inner_r, inner_color, inner_label,
                  outer_color, outer_label, inner_pattern, outer_pattern):
        ax.set_facecolor(SLIDE_BG)
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
                    arrowprops=dict(arrowstyle="->", color=SLIDE_TEXT,
                                    lw=0.8, alpha=0.25),
                )
                # Wiggly line (tilde)
                ax.text((x1+x2)/2, (y1+y2)/2, "~", fontsize=6,
                        color=SLIDE_TEXT, alpha=0.25, ha="center", va="center",
                        rotation=np.degrees(angle))
        else:
            # Circular arrows for convection
            for angle in [0.3, 1.3, 2.3, 3.3, 4.3, 5.3]:
                r = inner_r * 0.6
                x_c = r * np.cos(angle)
                y_c = r * np.sin(angle)
                arc = mpatches.Arc((x_c, y_c), inner_r * 0.3, inner_r * 0.3,
                                   angle=np.degrees(angle), theta1=0, theta2=270,
                                   color=SLIDE_TEXT, alpha=0.25, linewidth=0.8)
                ax.add_patch(arc)

        if outer_pattern == "radiative":
            for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
                r1 = inner_r + (1 - inner_r) * 0.2
                r2 = inner_r + (1 - inner_r) * 0.8
                x1, y1 = r1 * np.cos(angle), r1 * np.sin(angle)
                x2, y2 = r2 * np.cos(angle), r2 * np.sin(angle)
                ax.annotate(
                    "", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=SLIDE_TEXT,
                                    lw=0.8, alpha=0.18),
                )
        else:
            for angle in np.linspace(0, 2*np.pi, 10, endpoint=False):
                r = inner_r + (1 - inner_r) * 0.5
                x_c = r * np.cos(angle)
                y_c = r * np.sin(angle)
                circ_r = (1 - inner_r) * 0.15
                arc = mpatches.Arc((x_c, y_c), circ_r, circ_r,
                                   angle=np.degrees(angle), theta1=0, theta2=270,
                                   color=SLIDE_TEXT, alpha=0.18, linewidth=0.8)
                ax.add_patch(arc)

        # Labels
        ax.text(0, 0, inner_label, fontsize=11, color=SLIDE_TEXT,
                ha="center", va="center", fontweight="bold")
        mid_r = (inner_r + 1) / 2
        ax.text(mid_r * 0.7, -mid_r * 0.7, outer_label, fontsize=10,
                color=SLIDE_TEXT, ha="center", va="center", fontweight="bold",
                alpha=0.85)

        ax.text(0, 1.2, title, fontsize=16, color=SLIDE_TEXT,
                ha="center", va="center", fontweight="bold")
        ax.text(0, 1.08, subtitle, fontsize=11, color=SLIDE_MUTED,
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
        fontsize=11, color=SLIDE_ORANGE, ha="center", va="bottom",
        fontstyle="italic",
    )

    fig.suptitle("Internal Structure of Main-Sequence Stars",
                 fontsize=20, color=SLIDE_TEXT, fontweight="bold", y=0.98)

    fig.tight_layout(rect=[0, 0.06, 1, 0.94])
    save_slide_figure(fig, "stellar-structure-zones.png")


# ═════════════════════════════════════════════════════════════
# Figure 8: Mass Limits Spectrum
# Used in: R6 (Mass Limits)
# ═════════════════════════════════════════════════════════════
def make_mass_limits():
    """
    Stellar mass spectrum from brown dwarfs to the most massive stars.
    Shows the quantum floor (0.08 M_sun) and radiation ceiling (~150 M_sun).
    """
    fig, ax = plt.subplots(figsize=(14, 5), dpi=220)
    apply_slide_style(fig, ax)

    # Mass range in physical units; both axes will be logarithmic.
    mass = np.logspace(-2.0, 2.5, 1400)

    # Kroupa-style broken-power-law IMF:
    # dN/dM ∝ M^{-alpha}
    # alpha = 0.3   for M < 0.08 Msun   (brown dwarfs)
    # alpha = 1.3   for 0.08 <= M < 0.5 Msun
    # alpha = 2.3   for M >= 0.5 Msun   (Salpeter-like high-mass slope)
    alpha = np.piecewise(
        mass,
        [mass < 0.08, (mass >= 0.08) & (mass < 0.5), mass >= 0.5],
        [0.3, 1.3, 2.3],
    )
    imf = np.empty_like(mass)

    low = mass < 0.08
    mid = (mass >= 0.08) & (mass < 0.5)
    high = mass >= 0.5

    imf[low] = mass[low] ** (-0.3)
    c_mid = 0.08 ** (1.3 - 0.3)
    imf[mid] = c_mid * mass[mid] ** (-1.3)
    c_high = c_mid * 0.5 ** (2.3 - 1.3)
    imf[high] = c_high * mass[high] ** (-2.3)

    # Normalize at 1 solar mass so the stellar regime is easier to read and
    # the high-mass tail remains visibly nonzero on the plot.
    imf_ref = c_high
    imf /= imf_ref

    # For a log-mass x-axis, the more visually meaningful quantity is the
    # abundance per logarithmic interval: dN/dlogM = M * dN/dM.
    spectrum = mass * imf
    y_floor = 1e-3

    ax.fill_between(mass, y_floor, spectrum, alpha=0.14, color="#5b84b8")
    ax.plot(mass, spectrum, color="#4d7cab", linewidth=2.2, alpha=0.95, zorder=3)

    # Key boundaries
    boundaries = [
        (0.08, "H-burning\nminimum\n0.08 M☉", SLIDE_TEAL,
         "QM floor:\nDegeneracy halts\ncontraction before\nfusion ignites"),
        (1.0, "1 M☉\n(Sun)", SLIDE_GOLD, None),
        (150.0, "Eddington\nlimit\n~150 M☉", SLIDE_ROSE,
         "Radiation ceiling:\nL_rad > L_Edd\ntears star apart"),
    ]

    for mass_val, label, color, note in boundaries:
        ax.axvline(mass_val, color=color, linewidth=2 if note else 1.5,
                   linestyle="--" if note else ":", alpha=0.7, zorder=3)
        if mass_val == 0.08:
            y_top = 1.6
            x_pos = mass_val * 1.24
        elif mass_val == 1.0:
            y_top = 1.35
            x_pos = mass_val
        else:
            y_top = 1.8
            x_pos = mass_val
        ax.text(x_pos, y_top, label, fontsize=11, color=color,
                ha="center", va="top", fontweight="bold")
        if note:
            x_note = mass_val * (0.42 if mass_val < 1 else 1.45)
            note_y = 2.3e-1 if mass_val < 1 else 1.7e-1
            ax.text(x_note, note_y, note, fontsize=9, color=color,
                    ha="center" if mass_val < 1 else "left", va="top",
                    alpha=0.85,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=SLIDE_PANEL,
                              edgecolor=color))

    # Regions
    regions = [
        (0.001, 0.08, "Brown\nDwarfs", "#9a76b9", 0.08),
        (0.08, 150.0, "Hydrogen-Burning Stars", "#4d7cab", 0.04),
    ]
    for m1, m2, label, color, alpha in regions:
        ax.axvspan(m1, m2, alpha=alpha, color=color, zorder=1)
        region_y = 1.2e-3 if m2 <= 0.08 else 1.5e-3
        ax.text(np.sqrt(m1 * m2), region_y, label, fontsize=10, color=color,
                ha="center", va="bottom", alpha=0.6)

    # Specific objects
    objects = [
        (0.25, "M dwarf\n(0.25 M☉)", SLIDE_ROSE),
        (2.0, "Sirius\n(2 M☉)", SLIDE_TEAL),
        (20.0, "Spica\n(20 M☉)", "#4d7cab"),
    ]
    for mass_val, label, color in objects:
        if mass_val < 0.08:
            imf_val = mass_val ** (-0.3)
        elif mass_val < 0.5:
            imf_val = c_mid * mass_val ** (-1.3)
        else:
            imf_val = c_high * mass_val ** (-2.3)
        imf_val /= imf.max()
        plot_y = max(mass_val * imf_val, y_floor * 1.8)
        ax.plot(mass_val, plot_y, "o", color=color, markersize=8,
                markeredgecolor=SLIDE_BG, markeredgewidth=1, zorder=5)
        if "M dwarf" in label:
            ax.text(mass_val, plot_y / 1.28, label, fontsize=8, color=color,
                    ha="center", va="top")
        elif "Sirius" in label:
            ax.text(mass_val, plot_y * 1.45, label, fontsize=8, color=color,
                    ha="center", va="bottom")
        else:
            ax.text(mass_val, plot_y * 1.35, label, fontsize=8, color=color,
                    ha="center", va="bottom")

    # Mark the Kroupa break between low- and high-mass stellar slopes.
    ax.axvline(0.5, color="#7a86a3", linewidth=1.3,
               linestyle=":", alpha=0.7, zorder=2)
    ax.text(0.5, 1.85, "Kroupa break\n0.5 M☉", fontsize=9,
            color="#7a86a3", ha="center", va="bottom")

    ax.set_xlabel(r"Mass $(M/M_\odot)$", fontsize=14, color=SLIDE_TEXT)
    ax.set_ylabel(r"Relative abundance per log interval $\left[M\,\xi(M)\right]$", fontsize=12, color=SLIDE_TEXT)
    ax.set_title("The Stellar Mass Spectrum", fontsize=18,
                 color=SLIDE_TEXT, fontweight="bold", pad=15)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.01, 300.0)
    ax.set_ylim(y_floor, 4.0)
    ax.grid(True, which="major", color=SLIDE_GRID, linewidth=0.8, alpha=0.9)
    ax.grid(True, which="minor", color=SLIDE_GRID, linewidth=0.45, alpha=0.45)
    ax.text(0.98, 0.95, "Kroupa IMF + physical boundaries",
            transform=ax.transAxes, ha="right", va="top",
            fontsize=10.2, color=SLIDE_MUTED,
            bbox=dict(boxstyle="round,pad=0.28", facecolor=SLIDE_PANEL, edgecolor=SLIDE_GRID))

    fig.tight_layout()
    save_slide_figure(fig, "mass-limits-spectrum.png")


# ═════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating Module 3 figures → {OUTPUT_DIR}/\n")

    make_binding_energy_curve()
    make_random_walk()
    make_optical_depth_slab()
    make_random_walk_scaling()
    make_radiative_flux_opacity()
    make_radiation_vs_convection_transport()
    make_eddington_force_balance()
    make_timescale_hierarchy()
    make_timescales_vs_mass()
    make_main_sequence_lifetime_vs_mass()
    make_cluster_turnoff_clock()
    make_fuel_vs_burn_rate()
    make_pressure_vs_pressure_gradient()
    make_hydrostatic_reasoning_ladder()
    make_hydrostatic_equilibrium()
    make_hydrostatic_shell_force_balance()
    make_toy_star_radial_profiles()
    make_pressure_gradient_scale_estimate()
    make_central_pressure_scaling_grid()
    make_radiation_pressure_mass_scaling()
    make_virial_energy_partition()
    make_core_temperature_scaling()
    make_fusion_force_scale_map()
    make_maxwell_boltzmann_speeds_solar_core()
    make_fusion_energy_scale_ladder()
    make_maxwell_boltzmann_energies_barrier_tail()
    make_coulomb_barrier_and_tunneling()
    make_gamow_window_cartoon()
    make_pp_chain()
    make_fusion_energy_budget()
    make_onion_shell()
    make_wd_mass_radius()
    make_compact_object_scale()
    make_stellar_structure_zones()
    make_mass_limits()

    print(f"\n✓ All figures saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
