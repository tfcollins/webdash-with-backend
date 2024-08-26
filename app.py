import time
import os
import dash
from dash import Dash, dcc, Input, Output, html, callback
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


pages = []
for page in dash.page_registry.values():
    pages.append(dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"])))

navbar = dbc.NavbarSimple(
    # children=pages,
    brand="Triton Production Test",
    brand_href="/",
    color="primary",
    dark=True,
)


app.layout = html.Div(
    [
        navbar,
        html.Br(),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
