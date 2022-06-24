import dash
import numpy as np

from dash import dcc, html
from dash.dependencies import Input, Output

from computations import compute_remainders, compute_valid_as, compute_valid_Ns, exp2int
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


N_QUBITS = 6
N_STATES = exp2int(N_QUBITS)
VALID_NS = compute_valid_Ns(N_STATES)
INITIAL_N = 35

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
        dcc.Slider(
            id="N_selector",
            min=0,
            max=len(VALID_NS),
            step=1,
            value=np.where(np.array(VALID_NS) == INITIAL_N)[0][0],
            marks={i: str(n) for i, n in enumerate(VALID_NS)},
        ),
        dcc.Slider(id="a_selector", min=0, step=1),
        dcc.Slider(
            id="basis_state_slider",
            min=0,
            max=N_QUBITS,
            value=0,
            marks={
                i: str(int(n))
                for i, n in enumerate(np.logspace(0, N_QUBITS, N_QUBITS + 1, base=2))
            },
        ),
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
                        children=d["text"] if isinstance(d["text"], str) else None,
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
    Output("a_selector", "max"),
    Output("a_selector", "marks"),
    Output("a_selector", "value"),
    [Input("N_selector", "value")],
)
def update_a_selector(N_idx: int) -> tuple[list[int], int]:
    """Updates the selector for the `a` parameter."""
    valid_as = compute_valid_as(VALID_NS[N_idx])
    return (
        len(valid_as),
        {i: str(a) for i, a in enumerate(valid_as)},
        valid_as[0],
    )


@app.callback(
    Output("period_finding_problem_text", "children"),
    [Input("N_selector", "value"), Input("a_selector", "value")],
)
def update_period_finding_text(N_idx: int, a: int) -> str:
    return narrative_dict["period_finding_problem"]["text"](
        N := VALID_NS[N_idx], compute_remainders(N, a, N_STATES)
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
