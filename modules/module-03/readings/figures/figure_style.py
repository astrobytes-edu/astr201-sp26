from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[4]
MODULE03_OUTPUT_DIR = PROJECT_ROOT / "assets" / "images" / "module-03"


def apply_textbook_style() -> None:
    """Apply clean, print-friendly defaults for ASTR 201 line-art figures."""
    mpl.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 1.0,
            "axes.labelsize": 12,
            "axes.titlesize": 14,
            "axes.titleweight": "semibold",
            "xtick.labelsize": 10.5,
            "ytick.labelsize": 10.5,
            "legend.frameon": False,
            "legend.fontsize": 10.5,
            "font.size": 11,
            "mathtext.fontset": "stix",
            "font.family": "STIXGeneral",
            "lines.linewidth": 2.2,
            "lines.markersize": 6,
            "grid.alpha": 0.18,
            "grid.linewidth": 0.8,
            "axes.grid": False,
        }
    )


def save_dual(fig: plt.Figure, stem: str | Path) -> None:
    """Save both SVG and PNG versions of a figure into the module-03 image directory."""
    stem_path = Path(stem)
    if not stem_path.is_absolute():
        stem_path = MODULE03_OUTPUT_DIR / stem_path

    stem_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem_path.with_suffix(".svg"))
    fig.savefig(stem_path.with_suffix(".png"), dpi=300)
