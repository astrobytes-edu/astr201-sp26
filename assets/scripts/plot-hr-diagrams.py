#!/usr/bin/env python
"""
Generate the HR diagram figures for ASTR 201 Module 2, Lecture 5.

Produces two figures:
1. Observer's HR diagram: M_V vs B-V (color-magnitude diagram)
2. Theorist's HR diagram: log(L/L_sun) vs log(T_eff) with lines of constant R

Uses representative stellar data (physically correct positions) rather than
a real catalog, for pedagogical clarity.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Output paths
outpath_observer = "../images/module-02/week-06/hr-diagram-observer.png"
outpath_theorist = "../images/module-02/week-06/hr-diagram-theorist.png"

# =============================================================================
# Shared data: representative stellar populations
# =============================================================================

# Main sequence: (T_eff [K], log(L/L_sun), M_V, B-V, spectral_type)
main_sequence = [
    (42000, 5.7, -5.7, -0.33, "O5"),
    (30000, 4.5, -4.0, -0.30, "B0"),
    (20000, 3.2, -1.5, -0.24, "B5"),
    (11000, 1.9, 0.6, -0.02, "A0"),
    (8200, 1.2, 1.9, 0.15, "A5"),
    (7200, 0.8, 2.7, 0.30, "F0"),
    (6400, 0.5, 3.5, 0.44, "F5"),
    (5800, 0.0, 4.8, 0.65, "G2"),
    (5300, -0.4, 5.9, 0.81, "K0"),
    (4400, -0.8, 7.4, 1.15, "K5"),
    (3850, -1.1, 8.8, 1.40, "M0"),
    (3200, -2.0, 11.8, 1.60, "M3"),
    (3000, -3.0, 12.3, 1.65, "M5"),
]

# Add scatter around main sequence for realism (50 stars per spectral type region)
np.random.seed(42)
ms_scatter_T = []
ms_scatter_logL = []
ms_scatter_MV = []
ms_scatter_BV = []
ms_scatter_colors = []

for i in range(len(main_sequence) - 1):
    T1, logL1, MV1, BV1, _ = main_sequence[i]
    T2, logL2, MV2, BV2, _ = main_sequence[i + 1]
    n = 40
    for _ in range(n):
        frac = np.random.uniform(0, 1)
        T = T1 * (T2 / T1) ** frac + np.random.normal(0, 0.02 * T1)
        logL = logL1 + frac * (logL2 - logL1) + np.random.normal(0, 0.15)
        MV = MV1 + frac * (MV2 - MV1) + np.random.normal(0, 0.3)
        BV = BV1 + frac * (BV2 - BV1) + np.random.normal(0, 0.03)
        ms_scatter_T.append(max(T, 2500))
        ms_scatter_logL.append(logL)
        ms_scatter_MV.append(MV)
        ms_scatter_BV.append(BV)

# Giants / Red giants
giants_data = [
    (5000, 1.7, 0.9, 0.80),    # G-type giant
    (4800, 2.0, 0.5, 0.90),
    (4500, 2.2, 0.0, 1.00),    # K-type giant
    (4200, 2.4, -0.3, 1.10),
    (4000, 2.6, -0.7, 1.20),
    (3800, 2.8, -1.0, 1.35),   # M-type giant
    (4700, 1.5, 1.2, 0.85),
    (4300, 2.1, 0.2, 1.05),
    (3900, 2.5, -0.5, 1.30),
    (5200, 1.5, 1.0, 0.75),
    (4600, 2.3, -0.1, 0.95),
]

# Add scatter to giants
giant_T = []
giant_logL = []
giant_MV = []
giant_BV = []
for T, logL, MV, BV in giants_data:
    for _ in range(8):
        giant_T.append(T + np.random.normal(0, 200))
        giant_logL.append(logL + np.random.normal(0, 0.2))
        giant_MV.append(MV + np.random.normal(0, 0.3))
        giant_BV.append(BV + np.random.normal(0, 0.05))

# Supergiants
supergiants_data = [
    (3500, 4.5, -6.0, 1.60),   # M supergiant (Betelgeuse-like)
    (3800, 4.2, -5.5, 1.50),
    (4200, 4.0, -5.0, 1.20),
    (6000, 4.3, -6.5, 0.60),   # F supergiant
    (8000, 4.8, -7.0, 0.10),   # A/B supergiant
    (12000, 5.0, -7.5, -0.10),
    (25000, 5.5, -7.0, -0.25), # O/B supergiant
]

# White dwarfs
wd_data = [
    (30000, -2.0, 10.0, -0.30),
    (25000, -2.3, 10.5, -0.25),
    (20000, -2.5, 11.0, -0.15),
    (15000, -2.8, 11.5, 0.00),
    (12000, -3.0, 12.0, 0.10),
    (10000, -3.2, 12.5, 0.20),
    (8000, -3.5, 13.0, 0.35),
    (6000, -4.0, 14.0, 0.55),
]

# Add scatter to white dwarfs
wd_T = []
wd_logL = []
wd_MV = []
wd_BV = []
for T, logL, MV, BV in wd_data:
    for _ in range(5):
        wd_T.append(T + np.random.normal(0, 500))
        wd_logL.append(logL + np.random.normal(0, 0.15))
        wd_MV.append(MV + np.random.normal(0, 0.2))
        wd_BV.append(BV + np.random.normal(0, 0.03))

# =============================================================================
# Color function: map temperature to approximate star color
# =============================================================================
def temp_to_color(T):
    """Map effective temperature to an approximate visual color."""
    if T > 25000:
        return "#7B9BFF"   # blue
    elif T > 10000:
        return "#A8C4FF"   # light blue
    elif T > 7500:
        return "#FFFFFF"   # white
    elif T > 6000:
        return "#FFF8E0"   # pale yellow
    elif T > 5200:
        return "#FFE44D"   # yellow
    elif T > 4000:
        return "#FFA500"   # orange
    else:
        return "#FF5533"   # red


# =============================================================================
# Figure 1: Observer's HR Diagram (M_V vs B-V)
# =============================================================================
fig1, ax1 = plt.subplots(figsize=(9, 7))

# Main sequence scatter
ms_colors_obs = [temp_to_color(T) for T in ms_scatter_T]
ax1.scatter(ms_scatter_BV, ms_scatter_MV, c=ms_colors_obs, s=8, alpha=0.6,
            edgecolors='#666666', linewidth=0.2, zorder=3)

# Giants
g_colors = [temp_to_color(T) for T in giant_T]
ax1.scatter(giant_BV, giant_MV, c=g_colors, s=20, alpha=0.7,
            edgecolors='#666666', linewidth=0.3, zorder=3)

# Supergiants
for T, logL, MV, BV in supergiants_data:
    ax1.scatter(BV, MV, c=temp_to_color(T), s=80, alpha=0.8,
                edgecolors='#333333', linewidth=0.8, zorder=4)

# White dwarfs
wd_colors = [temp_to_color(T) for T in wd_T]
ax1.scatter(wd_BV, wd_MV, c=wd_colors, s=12, alpha=0.7,
            edgecolors='#666666', linewidth=0.3, zorder=3)

# Sun
ax1.scatter([0.65], [4.83], c='#FFD700', s=200, edgecolors='black',
            linewidth=1.5, zorder=10, marker='o')
ax1.annotate('Sun', xy=(0.65, 4.83), xytext=(0.85, 3.5),
             fontsize=11, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=1.2))

# Region labels
ax1.text(-0.15, -5.5, 'Supergiants', fontsize=11, fontweight='bold',
         color='#444444', ha='center')
ax1.text(1.2, -0.5, 'Giants', fontsize=11, fontweight='bold',
         color='#444444', ha='center')
ax1.text(0.5, 9.0, 'Main\nSequence', fontsize=11, fontweight='bold',
         color='#444444', ha='center', linespacing=1.3)
ax1.text(-0.1, 12.5, 'White\nDwarfs', fontsize=10, fontweight='bold',
         color='#444444', ha='center', linespacing=1.3)

# Spectral type labels at top
sp_labels = [("O", -0.33), ("B", -0.20), ("A", 0.0), ("F", 0.30),
             ("G", 0.60), ("K", 1.0), ("M", 1.5)]
for label, bv in sp_labels:
    ax1.text(bv, -7.8, label, fontsize=10, ha='center', color='#555555',
             fontweight='bold')

# Formatting
ax1.set_xlabel(r'Color Index $(B - V)$', fontsize=13)
ax1.set_ylabel(r'Absolute Magnitude $M_V$', fontsize=13)
ax1.set_title("The Observer's HR Diagram", fontsize=14, pad=12)
ax1.set_xlim(-0.45, 1.8)
ax1.set_ylim(16, -8)  # Inverted: brighter at top
ax1.grid(True, alpha=0.15, linewidth=0.5)

# Secondary x-axis label
ax1.text(0.5, -0.08, r'$\longleftarrow$ Hotter                  Cooler $\longrightarrow$',
         transform=ax1.transAxes, fontsize=10, ha='center', color='#888888')

fig1.tight_layout()
fig1.savefig(outpath_observer, dpi=200, bbox_inches='tight', facecolor='white')
print(f"Saved: {outpath_observer}")
plt.close(fig1)


# =============================================================================
# Figure 2: Theorist's HR Diagram with Lines of Constant R
# =============================================================================
fig2, ax2 = plt.subplots(figsize=(9, 7))

# Lines of constant radius (Stefan-Boltzmann: L = 4pi R^2 sigma T^4)
# In solar units: L/L_sun = (R/R_sun)^2 (T/T_sun)^4
# log(L) = 2*log(R/R_sun) + 4*log(T/T_sun) + log(L_sun) ... in log form:
# log(L/L_sun) = 2*log(R/R_sun) + 4*log(T/5800)
T_sun = 5800  # K

log_T_grid = np.linspace(3.4, 4.75, 300)  # log10(T)
T_grid = 10**log_T_grid

radii = [0.01, 0.1, 1.0, 10, 100, 1000]  # R/R_sun
radius_labels = [r'$0.01\,R_\odot$', r'$0.1\,R_\odot$', r'$1\,R_\odot$',
                 r'$10\,R_\odot$', r'$100\,R_\odot$', r'$1000\,R_\odot$']

for R, label in zip(radii, radius_labels):
    logL = 2 * np.log10(R) + 4 * np.log10(T_grid / T_sun)
    ax2.plot(log_T_grid, logL, '--', color='#999999', linewidth=0.8,
             alpha=0.7, zorder=1)
    # Place label at the right end (low T side)
    idx = -1  # rightmost point
    if logL[idx] > -4.5 and logL[idx] < 6.5:
        ax2.text(log_T_grid[idx] + 0.02, logL[idx], label,
                 fontsize=8, color='#777777', va='center')
    elif logL[0] > -4.5 and logL[0] < 6.5:
        # Place at left end
        ax2.text(log_T_grid[0] - 0.02, logL[0], label,
                 fontsize=8, color='#777777', va='center', ha='right')

# Main sequence scatter
ms_logT = [np.log10(T) for T in ms_scatter_T]
ms_colors_th = [temp_to_color(T) for T in ms_scatter_T]
ax2.scatter(ms_logT, ms_scatter_logL, c=ms_colors_th, s=8, alpha=0.6,
            edgecolors='#666666', linewidth=0.2, zorder=3)

# Giants
g_logT = [np.log10(T) for T in giant_T]
g_colors_th = [temp_to_color(T) for T in giant_T]
ax2.scatter(g_logT, giant_logL, c=g_colors_th, s=20, alpha=0.7,
            edgecolors='#666666', linewidth=0.3, zorder=3)

# Supergiants
for T, logL, MV, BV in supergiants_data:
    ax2.scatter(np.log10(T), logL, c=temp_to_color(T), s=80, alpha=0.8,
                edgecolors='#333333', linewidth=0.8, zorder=4)

# White dwarfs
wd_logT = [np.log10(T) for T in wd_T]
wd_colors_th = [temp_to_color(T) for T in wd_T]
ax2.scatter(wd_logT, wd_logL, c=wd_colors_th, s=12, alpha=0.7,
            edgecolors='#666666', linewidth=0.3, zorder=3)

# Sun
ax2.scatter([np.log10(5800)], [0.0], c='#FFD700', s=200, edgecolors='black',
            linewidth=1.5, zorder=10, marker='o')
ax2.annotate('Sun', xy=(np.log10(5800), 0.0), xytext=(3.6, 0.8),
             fontsize=11, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=1.2))

# Region labels
ax2.text(4.5, 5.5, 'Supergiants', fontsize=11, fontweight='bold',
         color='#444444', ha='center')
ax2.text(3.65, 2.8, 'Giants', fontsize=11, fontweight='bold',
         color='#444444', ha='center')
ax2.text(3.9, -1.0, 'Main\nSequence', fontsize=11, fontweight='bold',
         color='#444444', ha='center', linespacing=1.3)
ax2.text(4.35, -3.0, 'White\nDwarfs', fontsize=10, fontweight='bold',
         color='#444444', ha='center', linespacing=1.3)

# Formatting
ax2.set_xlabel(r'$\log_{10}(T_{\rm eff}\ /\ {\rm K})$', fontsize=13)
ax2.set_ylabel(r'$\log_{10}(L\ /\ L_\odot)$', fontsize=13)
ax2.set_title("The Theorist's HR Diagram", fontsize=14, pad=12)
ax2.set_xlim(4.75, 3.4)  # Reversed: hot on left
ax2.set_ylim(-4.5, 6.5)
ax2.grid(True, alpha=0.15, linewidth=0.5)

# Temperature labels at top
temp_labels = [(4.7, "50,000 K"), (4.5, "30,000 K"), (4.0, "10,000 K"),
               (3.76, "5,800 K"), (3.6, "4,000 K")]
for logT, label in temp_labels:
    ax2.text(logT, 6.8, label, fontsize=8, ha='center', color='#888888')

# Secondary axis note
ax2.text(0.5, -0.08,
         r'$\longleftarrow$ Hotter                  Cooler $\longrightarrow$',
         transform=ax2.transAxes, fontsize=10, ha='center', color='#888888')

fig2.tight_layout()
fig2.savefig(outpath_theorist, dpi=200, bbox_inches='tight', facecolor='white')
print(f"Saved: {outpath_theorist}")
plt.close(fig2)
