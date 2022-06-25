import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from constants import (
    N_STATES,
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
    Output("period_text_2", "children"),
    [Input("N_selector", "value"), Input("a_selector", "value")],
)
def update_period_finding_text(N_idx: int, a: int) -> str:
    return (
        f"The system is set to an equal superposition of n being in each of the {(N:=VALID_NS[N_idx])}, "
        f"and the associated remainder in each of the {len(set(compute_remainders(N, a, N_STATES)))} "
        f"possible basis states. Next, one of the possible remainders is measured, and the system collapses "
        "to a superposition of the basis states that are consistent with this measurement."
    )


@app.callback(
    Output("modulo_figure", "children"),
    [
        Input("N_selector", "value"),
        Input("a_selector", "value"),
        Input("basis_state_slider", "value"),
        Input("measure_remainder_button", "n_clicks"),
    ],
)
def update_modulo_figure(
    N_idx: int, a: int, basis_state: int, n_clicks: int
) -> dcc.Graph:
    """Updates the modulo figure, if a parameter changes, a
    different basis state is selected or a measurement is made."""
    return dcc.Graph(
        figure=modulo_figure(VALID_NS[N_idx], a, N_STATES, basis_state, bool(n_clicks))
    )


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
