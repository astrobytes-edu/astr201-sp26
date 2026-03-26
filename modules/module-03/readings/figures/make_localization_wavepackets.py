from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from figure_style import apply_textbook_style, save_dual


def gaussian_packet(x: np.ndarray, sigma: float, k0: float) -> tuple[np.ndarray, np.ndarray]:
    """Return a cosine carrier inside a Gaussian envelope and the envelope itself."""
    envelope = np.exp(-0.5 * (x / sigma) ** 2)
    carrier = np.cos(k0 * x)
    return envelope * carrier, envelope


def main() -> None:
    """Build a two-case wave-packet comparison for the uncertainty discussion."""
    apply_textbook_style()

    fig, axs = plt.subplots(2, 1, figsize=(10.5, 6.6), layout="constrained", sharex=True)
    x = np.linspace(-12, 12, 2200)

    cases = [
        (1.0, 7.2, r"Tightly localized in position: small $\Delta x$, large $\Delta p$"),
        (3.6, 3.0, r"Broad in position: large $\Delta x$, small $\Delta p$"),
    ]

    for ax, (sigma, k0, title) in zip(axs, cases):
        packet, envelope = gaussian_packet(x, sigma=sigma, k0=k0)

        ax.plot(x, packet, color="C0")
        ax.plot(x, envelope, linestyle="--", linewidth=1.5, color="0.35")
        ax.plot(x, -envelope, linestyle="--", linewidth=1.5, color="0.35")
        ax.axvline(-sigma, linestyle=":", linewidth=1.2, color="0.45")
        ax.axvline(sigma, linestyle=":", linewidth=1.2, color="0.45")

        ax.text(0.02, 0.89, title, transform=ax.transAxes, fontsize=11)
        ax.text(
            0.02,
            0.73,
            rf"Approximate width $\sim 2\sigma$",
            transform=ax.transAxes,
            fontsize=10.5,
        )

        ax.set_ylabel("Amplitude")
        ax.set_yticks([])
        ax.set_ylim(-1.2, 1.2)

    axs[0].annotate(
        "many wavelengths\ncontribute",
        xy=(2.0, 0.35),
        xytext=(5.2, 0.95),
        arrowprops=dict(arrowstyle="->", lw=1.5),
        fontsize=10.5,
    )
    axs[1].annotate(
        "fewer wavelengths dominate",
        xy=(4.0, 0.45),
        xytext=(6.0, 0.95),
        arrowprops=dict(arrowstyle="->", lw=1.5),
        fontsize=10.5,
    )

    axs[1].set_xlabel("Position")
    fig.suptitle(
        "Why localization and momentum spread trade off",
        fontsize=15,
        fontweight="semibold",
    )
    save_dual(fig, "localization-wavepackets")


if __name__ == "__main__":
    main()

