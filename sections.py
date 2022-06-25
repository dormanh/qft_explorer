import dash_bootstrap_components as dbc
import numpy as np

from dash import dcc, html

from constants import (
    paragraph_style,
    subtitle_style,
    vertical_margin,
    INITIAL_N,
    N_STATES,
    N_QUBITS,
    VALID_NS,
)


intro = html.Div(
    [
        html.H2(children="Introduction"),
        html.H5(
            id="intro_text_1",
            children=(
                "This dashboard allows you to explore concepts related to Shor's algorithm "
                "and the quantum Fourier transform in an interactive fashion."
            ),
            style=paragraph_style,
        ),
    ],
    style=vertical_margin,
)

period = html.Div(
    [
        html.H2(children="The period-finding problem"),
        html.P(
            children=[
                "Factorizing a large ",
                html.Span(
                    "semiprime",
                    id="semiprime",
                    style=dict(
                        textDecoration="underline", color="purple", cursor="pointer"
                    ),
                ),
                " $N$ is equivalent to finding the period of the modulo function $a^n mod N$, "
                "where $1 < a < N$ is randomly selected and $n = 1, ...  N$. The sought period "
                "$0 < r < N$ is the lowest number such that $a^r mod N = 1$. Below you can see a visual "
                "representation of this perodic function with adjustable $a$ and $N$ parameters. "
                f"As our {N_QUBITS}-bit system can only represent natural numbers smaller than {N_STATES}, "
                "we'll look at semiprimes in this range for the illustration of the problem.",
            ],
            style=paragraph_style,
        ),
        dbc.Tooltip(
            "A semiprime is the product of two primes.",
            target="semiprime",
        ),
        html.H4("select N", style=subtitle_style),
        dcc.Slider(
            id="N_selector",
            min=0,
            max=len(VALID_NS) - 1,
            step=1,
            value=np.where(np.array(VALID_NS) == INITIAL_N)[0][0],
            marks={i: str(n) for i, n in enumerate(VALID_NS)},
        ),
        html.H4("select the a parameter", style=subtitle_style),
        dcc.Slider(id="a_selector", min=0, step=1),
        html.H4("select a basis state", style=subtitle_style),
        dcc.Slider(
            id="basis_state_slider",
            min=0,
            max=N_STATES - 1,
            step=1,
            value=0,
            marks={n: str(n) if (n % 5 == 0) else "" for n in range(N_STATES)},
        ),
        html.Button(
            id="measure_remainder_button",
            children="make measurement",
            style=dict(marginTop=20),
        ),
        html.P(
            id="period_text_2",
            style=dict(**paragraph_style, marginTop=20),
        ),
        html.Div(id="modulo_figure"),
    ],
    style=vertical_margin,
)
