narrative_dict = dict(
    intro=dict(
        title="Introduction",
        text=(
            "This dashboard allows you to explore concepts related to Shor's algorithm "
            "and the quantum Fourier transform in an interactive fashion."
        ),
    ),
    period_finding_problem=dict(
        title="The period-finding problem",
        text=lambda n_qbits, remainders: (
            f"The system is set to an equal superposition of n being in each of the {n_qbits}, "
            f"and the associated remainder in each of the {len(set(remainders))} possible basis states. "
            f"Next, one of the possible remainders is measured, and the system collapses to a superposition "
            "of the basis states that are consistent with this measurement."
        ),
    ),
)
