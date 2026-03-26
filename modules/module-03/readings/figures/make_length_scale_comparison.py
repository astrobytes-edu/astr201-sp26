from __future__ import annotations

import matplotlib.pyplot as plt

from figure_style import apply_textbook_style, save_dual


def main() -> None:
    """Build a log-scale ruler comparing the de Broglie wavelength with nuclear size."""
    apply_textbook_style()

    fig, ax = plt.subplots(figsize=(11.2, 3.8), layout="constrained")

    scales_cm = {
        r"nuclear scale" "\n" r"$\sim 10^{-13}\,\mathrm{cm}$": 1e-13,
        r"solar-core proton" "\n" r"$\lambda_{\mathrm{dB}} \sim 6.5 \times 10^{-11}\,\mathrm{cm}$": 6.5e-11,
        r"atomic scale" "\n" r"$\sim 10^{-8}\,\mathrm{cm}$": 1e-8,
    }

    ax.set_xscale("log")
    ax.set_xlim(5e-14, 5e-8)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Length scale (cm)")

    for i, (label, x_val) in enumerate(scales_cm.items()):
        y_val = 0.72 - i * 0.25
        ax.scatter([x_val], [y_val], s=80, zorder=3)
        ax.vlines(x_val, y_val - 0.08, y_val + 0.08, linewidth=1.5)
        ax.annotate(
            label,
            xy=(x_val, y_val),
            xytext=(12, 0),
            textcoords="offset points",
            va="center",
            fontsize=11,
        )

    ax.annotate(
        "Hundreds of times larger",
        xy=(6.5e-11, 0.47),
        xytext=(6e-12, 0.92),
        arrowprops=dict(arrowstyle="->", lw=1.5),
        fontsize=11,
    )

    ax.set_title(
        "The proton's de Broglie wavelength is much larger than the nuclear scale",
        fontsize=15,
        fontweight="semibold",
    )
    save_dual(fig, "debroglie-vs-nuclear-scale")


if __name__ == "__main__":
    main()

