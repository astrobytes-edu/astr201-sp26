from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from figure_style import apply_textbook_style, save_dual


def add_box(ax: plt.Axes, xy: tuple[float, float], wh: tuple[float, float], text: str) -> None:
    """Add a rounded logic box to the causal flow figure."""
    x_pos, y_pos = xy
    width, height = wh
    patch = FancyBboxPatch(
        (x_pos, y_pos),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.4,
        facecolor="white",
    )
    ax.add_patch(patch)
    ax.text(x_pos + width / 2, y_pos + height / 2, text, ha="center", va="center", fontsize=11)


def main() -> None:
    """Build a horizontal causal map for the Part 3 quantum argument."""
    apply_textbook_style()

    fig, ax = plt.subplots(figsize=(12.2, 3.8), layout="constrained")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.axis("off")

    boxes = [
        (0.25, 1.2, "Gravity compresses core"),
        (2.55, 1.2, "Coulomb barrier\nblocks classical fusion"),
        (4.85, 1.2, "de Broglie wavelength:\nproton behaves as a wave"),
        (7.15, 1.2, "Uncertainty:\nno exact classical trajectory"),
        (9.45, 1.2, "Tunneling allows\nrare close approach"),
    ]

    width, height = 1.85, 0.72
    right_edges: list[tuple[float, float]] = []
    for x_pos, y_pos, text in boxes:
        add_box(ax, (x_pos, y_pos), (width, height), text)
        right_edges.append((x_pos + width, y_pos + height / 2))

    for i in range(len(right_edges) - 1):
        x0, y0 = right_edges[i]
        x1 = boxes[i + 1][0]
        y1 = boxes[i + 1][1] + height / 2
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", lw=1.8))

    ax.text(10.0, 0.42, "Then the weak interaction\nsets the actual rate.", fontsize=11.5)
    ax.annotate(
        "",
        xy=(10.2, 1.2),
        xytext=(10.55, 0.78),
        arrowprops=dict(arrowstyle="->", lw=1.6),
    )

    ax.set_title(
        "Causal map: why the Sun needs quantum mechanics to shine",
        fontsize=15,
        fontweight="semibold",
    )
    save_dual(fig, "fusion-logic-flow")


if __name__ == "__main__":
    main()

