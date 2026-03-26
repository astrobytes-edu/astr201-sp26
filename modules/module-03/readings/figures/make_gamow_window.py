from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from figure_style import apply_textbook_style, save_dual


def main() -> None:
    """Build a cleaned-up schematic Gamow-window figure for the reading."""
    apply_textbook_style()

    fig, ax = plt.subplots(figsize=(10.8, 5.2), layout="constrained")

    energy = np.linspace(0.15, 30.0, 1600)  # keV, pedagogical schematic axis
    kbt = 1.29  # keV
    e_g = 120.0  # schematic Gamow scale for visual pedagogy only

    thermal = np.exp(-energy / kbt)
    tunneling = np.exp(-np.sqrt(e_g / energy))
    product = thermal * tunneling

    thermal /= thermal.max()
    tunneling /= tunneling.max()
    product /= product.max()

    ax.plot(energy, thermal, label=r"Thermal rarity $\propto e^{-E/k_B T}$")
    ax.plot(energy, tunneling, label="Tunneling transmission (schematic)")
    ax.plot(energy, product, linewidth=2.8, label="Combined fusion weighting")

    i_peak = int(np.argmax(product))
    e_peak = float(energy[i_peak])
    y_peak = float(product[i_peak])

    halfmax = 0.55 * y_peak
    mask = product >= halfmax
    ax.fill_between(energy[mask], 0, product[mask], alpha=0.18)

    ax.axvline(kbt, linestyle="--", linewidth=1.5)
    ax.axvline(e_peak, linestyle=":", linewidth=1.5)

    ax.annotate(
        r"$k_B T$",
        xy=(kbt, 0.78),
        xytext=(kbt + 1.6, 0.90),
        arrowprops=dict(arrowstyle="->", lw=1.4),
        fontsize=10.5,
    )
    ax.annotate(
        "Gamow-window peak",
        xy=(e_peak, y_peak),
        xytext=(e_peak + 3.2, 0.83),
        arrowprops=dict(arrowstyle="->", lw=1.4),
        fontsize=10.5,
    )
    ax.text(
        0.10,
        0.94,
        r"Low $E$: common but tunnel poorly",
        transform=ax.transAxes,
        fontsize=10.5,
        va="top",
    )
    ax.text(
        0.62,
        0.94,
        r"High $E$: tunnel better but are rare",
        transform=ax.transAxes,
        fontsize=10.5,
        va="top",
    )

    ax.set_xlabel("Collision energy (keV)")
    ax.set_ylabel("Relative weighting")
    ax.set_yticks([])
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 1.12)
    ax.set_title(
        "Most fusion comes from a narrow overlap region",
        fontsize=15,
        fontweight="semibold",
    )
    ax.legend(loc="upper right")

    save_dual(fig, "gamow-window-upgraded")


if __name__ == "__main__":
    main()

