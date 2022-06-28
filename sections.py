import dash_bootstrap_components as dbc
import dash_latex as dl
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
                "This dashboard allows you to interactively explore concepts related "
                "to the quantum Fourier transform in the context of Shor's algorithm."
            ),
            style=paragraph_style,
        ),
    ],
    style=vertical_margin,
)

period = html.Div(
    [
        html.H2(children="The period-finding problem"),
        html.Div(
            children=[
                "The key to factorizing a large ",
                html.Span(
                    "semiprime",
                    id="semiprime",
                    style=dict(
                        textDecoration="underline", color="teal", cursor="pointer"
                    ),
                ),
                dl.DashLatex(
                    children=(
                        " $N$ is finding the period of the modulo function $a^n \mod{N}$, where $1 < a < N$ "
                        "is selected randomly and $n \in \mathbb{N}$. (In case $a$ happens to be a factor of $N$, "
                        "which is highly unlikely, the entire factoring problem is solved immediately.) The sought "
                        "period $0 < r < N$ is the smallest number such that $a^r \mod{N} = 1$. On a classical computer, "
                        "finding $r$ requires checking all possible solutions, which scales "
                    )
                ),
                html.Span(
                    "exponentially",
                    id="exponentially",
                    style=dict(
                        textDecoration="underline", color="teal", cursor="pointer"
                    ),
                ),
                dl.DashLatex(children=(" with the number of (binary) digits in $N$.")),
            ],
            style=paragraph_style,
        ),
        html.Div(
            children=[
                dl.DashLatex(
                    children=(
                        "Shor's algorithm leverages the fact that a quantum computer can calculate the value of the "
                        "function $a^n \mod{N}$ (referred to from here on as the remainder) for all $n = 1, ..., N-1$ "
                        "(in other words, all the possible periods) in parallel. Don't be mistaken, though: when the result "
                        "is measured, the system randomly collapses into one of those values with uniform probability, which "
                        "is not useful at all. But here's the trick. With the help of the QFT, it is possible to get the wave "
                        "function of the yet unobserved quantum system to interfere with itself in a way that amplifies the "
                        "relevant, and supresses the irrelevant components. How exactly this is done is elaborated in another "
                        "section."
                    )
                )
            ],
            style=dict(**paragraph_style, marginTop=20, marginBottom=20),
        ),
        html.Div(
            children=[
                dl.DashLatex(
                    children=(
                        "Below you can see a visual representation of the aforementioned perodic function with adjustable "
                        f"$a$ and $N$ parameters, represented by a hypothetical ${N_QUBITS}$-bit quantum system. "
                        f"This system can encode the integers in binary notation up to $2^{N_QUBITS} = {N_STATES}$, "
                        "so we'll only look at $N$-s in this range. By howering over each circle in the figure, you can see each "
                    )
                ),
                html.Span(
                    "basis state",
                    id="basis_state",
                    style=dict(
                        textDecoration="underline", color="teal", cursor="pointer"
                    ),
                ),
                dl.DashLatex(
                    children=(
                        ", expressed in both decimal and binary notation, as well as the associated remainder for clarity."
                    )
                ),
            ],
            style=dict(**paragraph_style, marginTop=20, marginBottom=20),
        ),
        html.Div(
            children=[
                dl.DashLatex(
                    children=(
                        "Next, a remainder - let this be denoted by $k$ - is randomly measured, leading the quantum "
                        "system to collapse into the superposition of basis states consistent with $k$, that is, "
                        "all $1 < n < N$, for which $a^n \mod{N} = k$. You can simulate this measurement for yourself "
                        "by pressing the button below."
                    )
                )
            ],
            style=dict(**paragraph_style, marginTop=20, marginBottom=20),
        ),
        dbc.Tooltip(
            "A semiprime is the product of two primes.",
            target="semiprime",
        ),
        dbc.Tooltip(
            "Exponential scaling in this case means that if N increases by one digit (expressed in binary notation), "
            "finding the period requires twice as much computing time, and becomes practically impossible for "
            "large numbers (in the order of hundreds of digits).",
            target="exponentially",
            style=dict(textAlign="center"),
        ),
        dbc.Tooltip(
            "A basis state is a sequence of 1-s and 0-s that represent an integer in binary notation. "
            "This is what the quantum system collapses into, when measured.",
            target="basis_state",
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
        html.Button(
            id="measure_remainder_button",
            children="make measurement",
            style=dict(marginTop=20),
        ),
        html.P(
            id="measure_remainder_result",
            style=dict(**paragraph_style, marginTop=20),
        ),
        html.P(
            id="measure_remainder_msg",
            style=dict(**paragraph_style, marginTop=20),
        ),
        html.Div(id="modulo_figure"),
    ],
    style=vertical_margin,
)
