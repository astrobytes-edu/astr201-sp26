from __future__ import annotations

from make_classical_vs_quantum_barrier import main as barrier_main
from make_fusion_logic_flow import main as flow_main
from make_gamow_window import main as gamow_main
from make_length_scale_comparison import main as scale_main
from make_localization_wavepackets import main as wavepacket_main


def main() -> None:
    """Build the module-03 Part 3 figure suite."""
    barrier_main()
    wavepacket_main()
    scale_main()
    gamow_main()
    flow_main()


if __name__ == "__main__":
    main()
