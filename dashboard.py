import dash
import numpy as np

from dash import dcc, html
from dash import callback_context as context
from dash.dependencies import Input, Output

from computations import compute_consistent_exponents


from constants import (
    VALID_NS,
    font_style,
    horizontal_margin,
    main_title,
    vertical_margin,
)
from computations import compute_remainders, compute_valid_as
from figures import modulo_figure
from sections import intro, period

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css",
    ],
    external_scripts=[
        "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js",
    ],
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    children=[html.H1(children=main_title), intro, period],
    style=dict(**vertical_margin, **horizontal_margin, **font_style),
)


@app.callback(
    Output("a_selector", "max"),
    Output("a_selector", "marks"),
    Output("a_selector", "value"),
    [Input("N_selector", "value")],
)
def update_a_selector(N_idx: int) -> tuple[list[int], int]:
    """Updates the selector for the `a` parameter."""
    valid_as = compute_valid_as(VALID_NS[N_idx])
    return (
        len(valid_as) - 1,
        {i: str(a) for i, a in enumerate(valid_as)},
        valid_as[0],
    )


@app.callback(
    Output("modulo_figure", "children"),
    Output("measure_remainder_msg", "children"),
    Output("measure_remainder_button", "n_clicks"),
    [
        Input("N_selector", "value"),
        Input("a_selector", "value"),
        Input("measure_remainder_button", "n_clicks"),
    ],
)
def update_modulo_figure(N_idx: int, a: int, n_clicks: int) -> tuple[dcc.Graph, str]:
    """Updates the modulo figure, if a parameter changes, a
    different basis state is selected or a measurement is made."""
    if context.triggered[0]["prop_id"].split(".")[0] != "measure_remainder_button":
        n_clicks = 0
    N = VALID_NS[N_idx]
    remainders = compute_remainders(N, a)
    measurement = np.random.choice(remainders) if n_clicks else None
    fig = dcc.Graph(figure=modulo_figure(N, a, measurement=measurement))
    text = (
        (
            f"Out of the possible {len(set(remainders))} remainders, you measured {measurement}, "
            f"causing the system to collapse into a superposition of the following basis states: "
            f"{', '.join(map(str, compute_consistent_exponents(N, a, measurement)))}."
        )
        if n_clicks
        else ""
    )
    return fig, text, n_clicks


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
