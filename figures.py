import numpy as np

from plotly import graph_objects as go
from typing import Optional

from computations import compute_consistent_exponents, compute_remainders


def modulo_figure(N: int, a: int, measurement: Optional[int] = None) -> go.Figure:
    """Constructs a figure to represents the modulo function,
    the period of which has to be found in order to factor N."""
    ns = np.arange(1, N)
    remainders = compute_remainders(N, a)

    point_traces = [
        go.Scatter(
            x=[n],
            y=[r],
            mode="markers",
            marker=dict(
                color="white",
                size=10,
                line=dict(color="teal", width=2),
            ),
            name=str(n),
            hoverinfo="text",
            hovertext=f"{n=} <br>qubit state={n:06b} <br>remainder={r}",
        )
        for n, r in zip(ns, remainders)
    ]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=ns,
                y=remainders,
                mode="lines",
                line=dict(color="teal"),
                hoverinfo="skip",
            ),
            *point_traces,
        ],
        layout=dict(
            xaxis=dict(
                title="n",
                range=(-1, N + 1),
                dtick=1,
                ticklabelstep=5,
                linecolor="black",
                gridcolor="lightgrey",
            ),
            yaxis=dict(
                title="remainder",
                range=(min(remainders) - 1, max(remainders) + 1),
                dtick=1,
                ticklabelstep=5,
                linecolor="black",
                gridcolor="lightgrey",
            ),
            showlegend=False,
            plot_bgcolor="white",
        ),
    )
    if measurement:
        xs = compute_consistent_exponents(N, a, measurement)
        ys = np.ones_like(xs) * measurement
        return fig.add_traces(
            [
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="markers",
                    marker=dict(color="black", size=12),
                    hoverinfo="skip",
                ),
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="markers+lines",
                    marker=dict(color="orangered", size=8),
                    line_color="black",
                    hoverinfo="skip",
                ),
            ]
        )
    return fig
