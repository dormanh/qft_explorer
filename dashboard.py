import dash
import numpy as np

from dash import dcc, html
from dash.dependencies import Input, Output
from math import ceil
from typing import Callable

from figures import modulo_figure
from narrative import narrative_dict

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

N = 35
a = 4
n_qbits = 2 ** ceil(np.log2(N))
basis_states = np.arange(n_qbits)
remainders = np.array([a ** int(x) % N for x in basis_states])

main_title = "Explore the quantum Fourier transform!"
margin_style = dict(marginTop=100, marginBottom=100, marginLeft=200, marginRight=200)
font_style = dict(fontSize=16, fontFamily="courier")
paragraph_style = dict(
    textAlign="justify",
    fontSize=14,
    fontWeight="normal",
)

sections = dict(
    intro=[],
    period_finding_problem=[
        dcc.Slider(id="basis_state_slider", min=0, max=N, step=1, value=0),
        html.Button(
            "make measurement",
            id="measure_remainder_button",
            style=dict(marginTop=20),
        ),
        html.Div(id="modulo_figure"),
    ],
)

app.layout = html.Div(
    children=[
        html.H1(children=main_title),
        *[
            html.Div(
                id=k,
                children=[
                    html.H2(children=d["title"]),
                    html.H5(
                        id=f"{k}_text",
                        children=d["text"](n_qbits, remainders)
                        if isinstance(d["text"], Callable)
                        else d["text"],
                        style=paragraph_style,
                    ),
                    html.Div(
                        children=sections[k],
                        style=dict(marginTop=20),
                    ),
                ],
            )
            for k, d in narrative_dict.items()
        ],
    ],
    style=dict(**margin_style, **font_style),
)


@app.callback(
    Output("modulo_figure", "children"),
    [
        Input("basis_state_slider", "value"),
        Input("measure_remainder_button", "n_clicks"),
    ],
)
def update_modulo_figure(basis_state: int, n_clicks: int) -> dcc.Graph:
    """Updates the modulo figure, if a new basis state is selected or a measurement is made."""
    return dcc.Graph(figure=modulo_figure(N, a, basis_state, bool(n_clicks)))


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
