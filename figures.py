import numpy as np

from ipywidgets import Button, IntSlider, Layout, VBox, interact
from math import ceil, gcd
from plotly import graph_objects as go

from computations import compute_remainders


class ModuloFigure(go.FigureWidget):
    """Intective figurewidget designed for the exploration of the period-finding problem."""

    def __init__(self, N: int, a: int) -> None:
        self._N = N
        self._a = a
        self._nqbits = 2 ** ceil(np.log2(N))
        self._x = np.arange(self._nqbits)
        self._r = np.array([a ** int(x) % N for x in self._x])
        self._p = self._x[np.where(self._r == 1)][0]
        self._runique = np.unique(self._r)
        self._button = Button(description="make measurement")
        self._slider = IntSlider(
            min=0,
            max=N,
            description="represented number",
            layout=Layout(width="800px"),
            style=dict(description_width="initial"),
        )
        point_traces = [
            go.Scatter(
                x=[x],
                y=[r],
                mode="markers",
                marker_color="teal",
                name=str(x),
            )
            for x, r in zip(self._x, self._r)
        ]
        self._base_title = (
            f"in order to factor {N=}, we first have to "
            f"find the period of the function a^n mod N "
            f"(we chose {a=} randomly)"
        )
        self._base_xtitle = f"$\large n = 1, ... {self._nqbits}$"
        self._base_ytitle = f"$\large ({a=})^n mod ({N=})$"
        super().__init__(
            data=[
                go.Scatter(
                    x=self._x,
                    y=self._r,
                    mode="lines",
                    line_color="coral",
                ),
                *point_traces,
            ],
            layout=dict(
                title=dict(
                    text=self._base_title,
                    font_size=12,
                ),
                xaxis=dict(
                    range=(-1, self._nqbits + 1),
                    title=self._base_xtitle,
                ),
                yaxis=dict(
                    range=(self._r.min() - 1, self._r.max() + 1),
                    title=self._base_ytitle,
                ),
                showlegend=False,
            ),
        )
        self._point_traces = self.data[1 : self._nqbits + 1]

    def reset(self) -> None:
        """Resets the figure to its initial state."""
        self.data = self.data[: self._nqbits + 1]
        for trace in self._point_traces:
            trace.marker.size = 5
        self.layout.title.text = self._base_title
        self.layout.xaxis.title.text = self._base_xtitle
        self.layout.yaxis.title.text = self._base_ytitle

    def intro(self) -> None:
        """Displays the figure in its initial state."""
        self.reset()
        return self

    def explore(self) -> VBox:
        """Displays the figure with a slider for highlighting individual base states."""
        self.reset()

        @interact(selected=self._slider)
        def show_with_highlight(selected: int) -> None:
            """Increases the size of the selected marker."""
            for trace in self._point_traces:
                trace.marker.size = 10 if (trace.name == str(selected)) else 5
            self.layout.title.text = (
                "the system is set to an equal superposition of "
                f"the n being in each of the {self._nqbits},<br>"
                f"and the associated remainder in each of the {len(self._runique)} "
                "possible basis states"
            )
            self.layout.xaxis.title = (
                f"qubit state: {selected:05b} (representing n={selected})"
            )
            return self

    def measure(self) -> VBox:
        """Displays the figure with a button for measuring a remainder."""
        title = f"next, one of the {len(self._runique)} possible remainders is measured"
        self.layout.title.text = title
        self._button.on_click(self.make_measurement)
        return VBox([self._button, self])

    def make_measurement(self, click: int) -> go.FigureWidget:
        """Generates and highlights a random measurement result, indicating the qubit states consistent with it."""
        if click:
            self.reset()
            self.layout.title.text = (
                f"next, one of the {len(self._runique)} possible remainders is measured"
            )
            measured = np.random.choice(self._r)
            xs = self._x[np.where(self._r == measured)]
            ys = np.ones_like(xs) * measured
            gap = ((self._r.max() - measured) or (-self._r.max())) / 10
            return self.add_traces(
                [
                    go.Scatter(
                        x=xs,
                        y=ys,
                        mode="markers",
                        marker=dict(color="black", size=10),
                    ),
                    go.Scatter(
                        x=xs,
                        y=ys,
                        mode="markers+lines",
                        marker=dict(color="white", size=5),
                        line_color="black",
                    ),
                    go.Scatter(
                        x=[xs[(i := len(xs) // 2)]],
                        y=[ys[i]] + gap,
                        mode="text",
                        text=f"measured remainder = {measured}",
                    ),
                ]
            ).update_layout(
                xaxis_title="meaning n is in the superposition of the following states: "
                f"{', '.join(xs.astype(str))}<br>and the period is {self._p} "
                "(but we can't directly measure that)",
            )


def modulo_figure(
    N: int, a: int, n_states: int, selected: int, measured: bool
) -> go.Figure:
    """Constructs a figure to represents the modulo function,
    the period of which has to be found in order to factor N."""
    basis_states = np.arange(n_states)
    remainders = compute_remainders(N, a, n_states)

    point_traces = [
        go.Scatter(
            x=[x],
            y=[r],
            mode="markers",
            marker=dict(color="teal", size=10 if x == selected else 5),
            name=str(x),
        )
        for x, r in zip(basis_states, remainders)
    ]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=basis_states,
                y=remainders,
                mode="lines",
                line_color="coral",
            ),
            *point_traces,
        ],
        layout=dict(
            xaxis=dict(
                range=(-1, n_states + 1), title=f"$\large n = 1, ... {n_states}$"
            ),
            yaxis=dict(
                range=(remainders.min() - 1, remainders.max() + 1),
                title=f"$\large ({a=})^n mod ({N=})$",
            ),
            showlegend=False,
        ),
    )
    if measured:
        measurement = np.random.choice(remainders)
        xs = basis_states[np.where(remainders == measurement)]
        ys = np.ones_like(xs) * measurement
        return fig.add_traces(
            [
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="markers",
                    marker=dict(color="black", size=10),
                ),
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="markers+lines",
                    marker=dict(color="white", size=5),
                    line_color="black",
                ),
            ]
        )
    return fig
