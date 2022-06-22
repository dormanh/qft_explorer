import dash

from dash import dcc, html
from dash.dependencies import Input, Output

from figures import modulo_figure

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
main_title = "Explore the quantum Fourier transform!"
subtitles = ["The period-finding problem"]
margin_style = dict(marginTop=100, marginBottom=100, marginLeft=200, marginRight=200)
font_style = dict(fontSize=16, fontFamily="courier")

app.layout = html.Div(
    children=[
        html.Div(html.H1(main_title)),
        html.Div(
            children=[
                html.H2(subtitles[0]),
                html.Div(
                    children=[
                        dcc.Slider(
                            id="basis_state_slider", min=0, max=N - 1, step=1, value=0
                        ),
                        html.Button(
                            "make measurement",
                            id="measure_remainder_button",
                            style=dict(marginTop=20),
                        ),
                        html.Div(id="modulo_figure"),
                    ],
                    style=dict(marginTop=20),
                ),
            ],
            style=dict(marginTop=20),
        ),
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
