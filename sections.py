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


def make_paragraph(contents: list) -> html.P:
    return html.P(
        children=[
            html.Span(
                c["text"],
                id="_".join(c["text"].split(" ")),
                style=dict(textDecoration="underline", color="teal", cursor="pointer"),
            )
            if c.get("span")
            else dl.DashLatex(c["text"])
            for c in contents
        ],
        style=paragraph_style,
    )


intro = html.Div(
    [
        html.H2(children="Introduction"),
        make_paragraph(
            [
                dict(
                    text=(
                        "Finding the prime factors of large numbers is considered a very hard problem in classical computing. "
                        "For perspective, factoring a $\sim 200$-digit number with a classical computer takes $\sim 10^{25}$ "
                        "elementary operations, equivalent to thousands of years in CPU time. With the help of Shor's "
                        "algorithm and a sufficiently large quantum computer, the same can be done with $\sim 10^{5}$ "
                        "operations, reducing the computing time to the fraction of a nanosecond!"
                    )
                )
            ]
        ),
        make_paragraph(
            [
                dict(
                    text=(
                        "By browsing through this dashboard, you can gain an intuitive understanding of how Shor's algorithm "
                        "works and explore one of its key components, the quantum Fourier transform."
                    )
                ),
            ]
        ),
    ],
    style=vertical_margin,
)

period = html.Div(
    [
        html.H2(children="The period-finding problem"),
        make_paragraph(
            [
                dict(text="The key to factorizing a large "),
                dict(text="semiprime", span=True),
                dict(
                    text=" $N$ is finding the ",
                ),
                dict(text="period", span=True),
                dict(
                    text=(
                        " of the function $a^n \mod{N}$, where $1 < a < N$ is a randomly selected parameter, and the domain "
                        "of the function is the natural numbers ($n \in \mathbb{N}$). (In case $a$ happens to be a factor of "
                        "$N$, which is highly unlikely, the entire factoring problem is solved immediately.) The sought period "
                        "$0 < r < N$ is the smallest number such that $a^r \mod{N} = 1$. On a classical computer, finding $r$ "
                        "requires checking all possible solutions, which scales "
                    ),
                ),
                dict(text="exponentially", span=True),
                dict(
                    text=" with the number of digits in $N$.",
                ),
            ]
        ),
        make_paragraph(
            [
                dict(
                    text=(
                        "Shor's algorithm leverages the fact that a quantum computer can calculate the value of the "
                        "function $a^n \mod{N}$ (referred to from here on as the remainder) for all $n = 1, ..., N-1$ "
                        "(in other words, all the possible periods) in parallel. Don't be mistaken, though: when the result "
                        "is measured, the system randomly collapses into one of those values with uniform probability, which "
                        "is not useful at all. But here's the trick. With the help of the QFT, it is possible to get the "
                    ),
                ),
                dict(text="wave function", span=True),
                dict(
                    text=(
                        " of the yet unobserved quantum system to interfere with itself in a way that amplifies the "
                        "relevant, and supresses the irrelevant components. How exactly this is done is elaborated in another "
                        "section."
                    ),
                ),
            ]
        ),
        make_paragraph(
            [
                dict(
                    text=(
                        "Below you can see a visual representation of the aforementioned perodic function with adjustable "
                        f"$a$ and $N$ parameters, represented by a hypothetical ${N_QUBITS}$-bit quantum system. "
                        f"This system can encode the integers in binary notation up to $2^{N_QUBITS} - 1 = {N_STATES - 1}$, "
                        "so we'll only look at semiprimes in this range. By howering over each circle in the figure, "
                        "you can see each "
                    ),
                ),
                dict(text="basis state", span=True),
                dict(
                    text=", expressed in both decimal and binary notation, as well as the associated remainder for clarity.",
                ),
            ]
        ),
        make_paragraph(
            [
                dict(
                    text=(
                        "Next, a remainder - let this be denoted by $k$ - is randomly measured, leading the quantum "
                        "system to collapse into the superposition of basis states consistent with $k$, that is, "
                        "all $1 < n < N$, for which $a^n \mod{N} = k$. You can simulate this measurement for yourself "
                        "by pressing the button below."
                    ),
                )
            ]
        ),
        dbc.Tooltip(
            "A semiprime is the product of two primes.",
            target="semiprime",
        ),
        dbc.Tooltip(
            dl.DashLatex(
                "The period $r$ of a function $f$ is a number such that the following equality holds for each $x$ "
                "in $f$'s domain: $f(x) = f(x + r)$. In other words, $f$ is invariant to translation by $r$. Not all "
                "functions have a period. Those that do are called periodic."
            ),
            target="period",
        ),
        dbc.Tooltip(
            dl.DashLatex(
                "Exponential scaling in this case means that if $N$ increases by one binary digit, finding the period "
                "requires twice as much computing time (and $10$ times as much, if $N$ increases by one decimal digit)."
            ),
            target="exponentially",
        ),
        dbc.Tooltip(
            "A basis state is a sequence of 1-s and 0-s that represent an integer in binary notation. "
            "This is what the quantum system collapses into, when measured. ",
            target="basis_state",
        ),
        dbc.Tooltip(
            "The wave function describes the evolution of a quantum system over time. It represents the probability "
            "of measuring each basis state. It also has a weird quantum-property: the so called phase that is not "
            "measurable directly, but plays a crucial role in the QFT, as we'll see later.",
            target="wave_function",
        ),
        html.P(dl.DashLatex("select $N$"), style=subtitle_style),
        dcc.Slider(
            id="N_selector",
            min=0,
            max=len(VALID_NS) - 1,
            step=1,
            value=np.where(np.array(VALID_NS) == INITIAL_N)[0][0],
            marks={i: str(n) for i, n in enumerate(VALID_NS)},
        ),
        html.P(dl.DashLatex("select the $a$ parameter"), style=subtitle_style),
        dcc.Slider(id="a_selector", min=0, step=1),
        html.Button(
            id="measure_remainder_button",
            children="make measurement",
            style=dict(marginTop=20),
        ),
        html.P(
            id="measure_remainder_result",
            style=paragraph_style,
        ),
        html.P(
            id="measure_remainder_msg",
            style=paragraph_style,
        ),
        html.Div(id="modulo_figure"),
    ],
    style=vertical_margin,
)
