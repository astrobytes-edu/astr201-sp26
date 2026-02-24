#!/usr/bin/env python
"""
Generate the mass-luminosity relation plot for ASTR 201 Module 2, Lecture 4.

Plots log(L/L_sun) vs log(M/M_sun) for main-sequence stars with:
- Representative data points (from well-measured eclipsing binaries)
- Power-law fit L ~ M^3.5 overlay
- Sun marked explicitly
- Color-coded by approximate spectral type
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Output path
outpath = "../images/module-02/week-06/mass-luminosity-relation.png"

# --- Physically correct data: representative main-sequence binary measurements ---
# Sources: Torres et al. (2010) review, supplemented with well-known systems
# Format: (M/M_sun, L/L_sun, spectral_type_label)
ms_data = [
    # Low-mass M dwarfs
    (0.08, 0.0004, "M"),
    (0.10, 0.001, "M"),
    (0.15, 0.003, "M"),
    (0.20, 0.008, "M"),
    (0.30, 0.02, "M"),
    (0.40, 0.05, "M"),
    (0.50, 0.09, "M"),
    # K dwarfs
    (0.60, 0.16, "K"),
    (0.70, 0.28, "K"),
    (0.80, 0.45, "K"),
    # G dwarfs
    (0.90, 0.65, "G"),
    (1.00, 1.00, "G"),  # Sun
    (1.10, 1.5, "G"),
    # F dwarfs
    (1.30, 3.0, "F"),
    (1.50, 5.5, "F"),
    (1.70, 9.0, "F"),
    # A stars
    (2.0, 16, "A"),
    (2.5, 40, "A"),
    (3.0, 80, "A"),
    # B stars
    (5.0, 600, "B"),
    (7.0, 3000, "B"),
    (10.0, 8000, "B"),
    (15.0, 30000, "B"),
    # O stars
    (25.0, 120000, "O"),
    (40.0, 500000, "O"),
    (60.0, 1200000, "O"),
]

masses = np.array([d[0] for d in ms_data])
lums = np.array([d[1] for d in ms_data])
sptypes = [d[2] for d in ms_data]

# Color map by spectral type
sptype_colors = {
    "O": "#6B8BFF",   # blue
    "B": "#8CB4FF",   # light blue
    "A": "#FFFFFF",    # white
    "F": "#FFF4D6",   # pale yellow
    "G": "#FFD700",   # yellow
    "K": "#FF8C00",   # orange
    "M": "#FF4500",   # red-orange
}
colors = [sptype_colors[sp] for sp in sptypes]

# Power-law fit line: L = M^3.5
m_fit = np.logspace(np.log10(0.07), np.log10(80), 200)
l_fit = m_fit**3.5

# --- Plot ---
fig, ax = plt.subplots(1, 1, figsize=(8, 6))

# Fit line
ax.plot(m_fit, l_fit, 'k--', linewidth=1.5, alpha=0.6,
        label=r'$L \propto M^{3.5}$')

# Data points with edge colors
for i, (m, l, sp) in enumerate(ms_data):
    ax.scatter(m, l, c=colors[i], s=60, edgecolors='#333333',
               linewidth=0.7, zorder=5)

# Mark the Sun
ax.scatter([1.0], [1.0], c='#FFD700', s=200, edgecolors='black',
           linewidth=1.5, zorder=10, marker='o')
ax.annotate(r'Sun ($1\,M_\odot,\ 1\,L_\odot$)',
            xy=(1.0, 1.0), xytext=(2.5, 0.3),
            fontsize=10, ha='left',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))

# Spectral type legend markers (manual)
for sp, color in [("O", "#6B8BFF"), ("B", "#8CB4FF"), ("A", "#FFFFFF"),
                   ("F", "#FFF4D6"), ("G", "#FFD700"), ("K", "#FF8C00"),
                   ("M", "#FF4500")]:
    ax.scatter([], [], c=color, s=50, edgecolors='#333333',
               linewidth=0.7, label=sp)

# Annotations for physical implications
ax.annotate(r'$2\,M_\odot \to 11\,L_\odot$',
            xy=(2.0, 16), xytext=(0.3, 50),
            fontsize=9, color='#555555',
            arrowprops=dict(arrowstyle='->', color='#888888', lw=0.8))

ax.annotate(r'$10\,M_\odot \to 3{,}000\,L_\odot$',
            xy=(10, 8000), xytext=(15, 300),
            fontsize=9, color='#555555',
            arrowprops=dict(arrowstyle='->', color='#888888', lw=0.8))

# Formatting
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'Mass ($M / M_\odot$)', fontsize=13)
ax.set_ylabel(r'Luminosity ($L / L_\odot$)', fontsize=13)
ax.set_title('The Mass-Luminosity Relation (Main Sequence)', fontsize=14, pad=12)
ax.set_xlim(0.06, 100)
ax.set_ylim(1e-4, 3e6)
ax.legend(loc='upper left', fontsize=9, framealpha=0.9, ncol=2)
ax.grid(True, which='both', alpha=0.2, linewidth=0.5)

# Add secondary note
ax.text(0.97, 0.03,
        r'Slope $\approx 3.5$ (empirical fit)',
        transform=ax.transAxes, fontsize=9, ha='right', va='bottom',
        color='#666666', style='italic')

fig.tight_layout()
fig.savefig(outpath, dpi=200, bbox_inches='tight', facecolor='white')
print(f"Saved: {outpath}")
plt.close()
