import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.H1("Testing Home"),
        html.Div("Click button to start."),
        dbc.Button(
            "Start",
            href="/step1",
            # Center the button
            style={"display": "block", "margin": "auto"},
        ),
    ]
)
