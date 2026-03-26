from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from figure_style import apply_textbook_style, save_dual


def barrier_potential(x: np.ndarray) -> np.ndarray:
    """Return a smooth schematic barrier used for the pedagogical comparison figure."""
    return 1.9 * np.exp(-0.5 * (x / 1.15) ** 2)


def main() -> None:
    """Build a two-panel comparison of classical reflection and quantum tunneling."""
    apply_textbook_style()

    fig, axs = plt.subplots(
        1, 2, figsize=(12.5, 4.8), layout="constrained", sharey=True
    )

    x = np.linspace(-5.0, 5.0, 1200)
    v_barrier = barrier_potential(x)
    energy = 0.58
    x_turn = abs(x[np.argmin(np.abs(v_barrier - energy))])

    ax = axs[0]
    ax.plot(x, v_barrier, color="C0")
    ax.axhline(energy, linestyle="--", linewidth=1.5, color="C1")
    ax.axvline(-x_turn, linestyle=":", linewidth=1.2, color="0.45")
    ax.axvline(x_turn, linestyle=":", linewidth=1.2, color="0.45")

    ax.annotate(
        "",
        xy=(-x_turn - 0.15, energy),
        xytext=(-4.5, energy),
        arrowprops=dict(arrowstyle="->", lw=2.2),
    )
    ax.annotate(
        "",
        xy=(-4.5, energy - 0.06),
        xytext=(-x_turn - 0.15, energy - 0.06),
        arrowprops=dict(arrowstyle="->", lw=2.2),
    )

    ax.text(-4.55, energy + 0.12, "incoming", fontsize=10.5)
    ax.text(-4.55, energy - 0.28, "reflected", fontsize=10.5)
    ax.text(-x_turn + 0.1, 0.05, "turning\npoint", fontsize=10.5)
    ax.text(2.15, 1.98, r"$V(x)$", fontsize=11)
    ax.text(2.0, energy + 0.08, r"$E$", fontsize=11)

    ax.set_title("Classical picture")
    ax.set_xlabel("Position")
    ax.set_ylabel("Potential / amplitude (schematic)")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.9, 2.2)
    ax.set_yticks([])
    ax.set_xticks([])

    ax = axs[1]
    ax.plot(x, v_barrier, color="C0")
    ax.axhline(energy, linestyle="--", linewidth=1.5, color="C1")
    ax.axvline(-x_turn, linestyle=":", linewidth=1.2, color="0.45")
    ax.axvline(x_turn, linestyle=":", linewidth=1.2, color="0.45")

    psi = np.zeros_like(x)
    left = x < -x_turn
    middle = (x >= -x_turn) & (x <= x_turn)
    right = x > x_turn

    psi[left] = 0.28 * np.sin(4.8 * (x[left] + x_turn)) - 0.45
    kappa = 1.35
    psi[middle] = 0.28 * np.exp(-kappa * (x[middle] + x_turn)) - 0.45
    amp_right = 0.28 * np.exp(-kappa * (2.0 * x_turn))
    psi[right] = amp_right * np.cos(4.8 * (x[right] - x_turn)) - 0.45

    ax.plot(x, psi, color="C2", zorder=3)
    ax.text(2.15, 1.98, r"$V(x)$", fontsize=11)
    ax.text(2.0, energy + 0.08, r"$E$", fontsize=11)

    ax.annotate(
        "oscillatory\nbefore barrier",
        xy=(-3.0, -0.42),
        xytext=(-4.3, -0.08),
        arrowprops=dict(arrowstyle="->", lw=1.5),
        fontsize=10.5,
    )
    ax.annotate(
        "exponential decay\ninside barrier",
        xy=(0.0, -0.28),
        xytext=(-0.4, 0.55),
        arrowprops=dict(arrowstyle="->", lw=1.5),
        fontsize=10.5,
        ha="center",
    )
    ax.annotate(
        "nonzero amplitude\nbeyond barrier",
        xy=(3.15, -0.44),
        xytext=(2.25, 0.4),
        arrowprops=dict(arrowstyle="->", lw=1.5),
        fontsize=10.5,
    )

    ax.set_title("Quantum picture")
    ax.set_xlabel("Position")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.9, 2.2)
    ax.set_yticks([])
    ax.set_xticks([])

    fig.suptitle(
        "Barrier crossing: classical turning point vs quantum tunneling",
        fontsize=15,
        fontweight="semibold",
    )
    save_dual(fig, "classical-vs-quantum-barrier")


if __name__ == "__main__":
    main()

