#!/usr/bin/env python3

"""Generate publication-style figures for the mass-limits reading."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, LogFormatterMathtext


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "assets" / "images" / "module-03"


def configure_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "font.family": "STIXGeneral",
            "mathtext.fontset": "stix",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 13,
            "xtick.labelsize": 10.5,
            "ytick.labelsize": 10.5,
            "legend.fontsize": 10.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 1.0,
        }
    )


def add_log_grid(ax: plt.Axes) -> None:
    ax.grid(which="major", color="#d6d6d6", linewidth=0.8)
    ax.grid(which="minor", color="#efefef", linewidth=0.45)
    ax.xaxis.set_major_locator(LogLocator(base=10))
    ax.yaxis.set_major_locator(LogLocator(base=10))
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_formatter(LogFormatterMathtext())


def generate_eddington_crossover() -> None:
    """Plot main-sequence luminosity, Eddington limit, and their ratio."""
    configure_style()

    mass = np.logspace(-0.1, 2.35, 500)
    lum_ms = mass**3.5
    lum_edd = 3.8e4 * mass
    ratio = lum_ms / lum_edd
    crossover_mass = (3.8e4) ** 0.4

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(13.2, 5.8)
    )
    fig.subplots_adjust(top=0.84, bottom=0.14, left=0.08, right=0.98, wspace=0.13)

    ms_color = "#1f77b4"
    edd_color = "#c43c39"
    ratio_color = "#5a3e9d"
    guide_color = "#444444"

    ax1.loglog(mass, lum_ms, color=ms_color, linewidth=2.8, label=r"Naive $L \propto M^{3.5}$")
    ax1.loglog(mass, lum_edd, color=edd_color, linewidth=2.8, label=r"$L_{\mathrm{Edd}} \propto M$")
    ax1.axvline(crossover_mass, color=guide_color, linestyle="--", linewidth=1.6)
    ax1.annotate(
        r"Naive crossover" "\n" r"$M \sim 10^2\,M_\odot$",
        xy=(crossover_mass, 3.8e4 * crossover_mass),
        xytext=(18, 1.6e5),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": guide_color, "linewidth": 1.2},
        fontsize=10.5,
        ha="left",
        va="bottom",
    )
    ax1.fill_between(
        mass,
        lum_ms,
        lum_edd,
        where=lum_ms >= lum_edd,
        color="#f6d7d5",
        alpha=0.5,
        interpolate=True,
    )
    ax1.text(
        46,
        2.2e7,
        "Radiation increasingly\nconstrains structure",
        color="#7d2320",
        fontsize=10.5,
        ha="left",
        va="top",
    )
    ax1.set_title("(a) Luminosity Curves", loc="left", pad=10)
    ax1.set_xlabel(r"Mass $(M/M_\odot)$")
    ax1.set_ylabel(r"Luminosity $(L/L_\odot)$")
    add_log_grid(ax1)
    ax1.legend(
        frameon=False,
        loc="lower right",
        handlelength=2.0,
        labelspacing=0.35,
        borderpad=0.2,
    )
    ax1.set_xlim(0.8, 220)
    ax1.set_ylim(1e0, 2e8)

    ax2.loglog(mass, ratio, color=ratio_color, linewidth=2.8)
    ax2.axhline(1.0, color=edd_color, linestyle="--", linewidth=1.8)
    ax2.axvline(crossover_mass, color=guide_color, linestyle="--", linewidth=1.6)
    ax2.fill_between(
        mass,
        ratio,
        1.0,
        where=ratio >= 1.0,
        color="#efe6fb",
        alpha=0.65,
        interpolate=True,
    )
    ax2.annotate(
        r"$L/L_{\mathrm{Edd}} = 1$",
        xy=(1.1, 1.0),
        xytext=(1.9, 1.55),
        arrowprops={"arrowstyle": "-", "color": edd_color, "linewidth": 1.0},
        color=edd_color,
        fontsize=10.5,
    )
    ax2.annotate(
        r"$L/L_{\mathrm{Edd}} \propto M^{2.5}$" "\n" r"(if the $M^{3.5}$ trend held)",
        xy=(14, ratio[np.searchsorted(mass, 14)]),
        xytext=(2.0, 3.0e-3),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": ratio_color, "linewidth": 1.2},
        fontsize=10.5,
        color=ratio_color,
        ha="left",
    )
    ax2.text(
        26,
        8.5,
        "Naive extrapolation enters\nEddington territory",
        color="#4a2f7e",
        fontsize=10.5,
        ha="left",
        va="bottom",
    )
    ax2.set_title("(b) Eddington Ratio", loc="left", pad=10)
    ax2.set_xlabel(r"Mass $(M/M_\odot)$")
    ax2.set_ylabel(r"$L/L_{\mathrm{Edd}}$")
    add_log_grid(ax2)
    ax2.set_xlim(0.8, 220)
    ax2.set_ylim(1e-5, 4e1)

    fig.suptitle(
        "Main-Sequence Luminosity vs. the Eddington Limit",
        fontsize=17,
        y=0.985,
    )

    png_path = OUTDIR / "eddington-vs-main-sequence-luminosity.png"
    svg_path = OUTDIR / "eddington-vs-main-sequence-luminosity.svg"
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(svg_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    generate_eddington_crossover()


if __name__ == "__main__":
    main()
