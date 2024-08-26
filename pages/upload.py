import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from shared import shared_info

dash.register_page(__name__)

page_info = shared_info(__file__)

progress = dbc.Progress(
    value=page_info["progress"],
    striped=True,
    animated=True,
    label=f"{page_info['progress']}%",
)

layout = html.Div(
    [
        progress,
        html.H1("Upload Report", style={"textAlign": "center"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Checklist(
                            label_checked_style={"opacity": 1},
                            input_checked_style={"opacity": 1},
                            options=page_info["options"],
                            value=page_info["value"],
                            id="checklist-input",
                        ),
                    ],
                    width=2,
                    style={"border-right": "3px solid black"},
                ),
                dbc.Col(
                    width=6,
                ),
            ]
        ),
        html.Br(),
        dbc.Button("Back", href=page_info["prev"]),
        dbc.Button("Next", href=page_info["next"]),
    ]
)


# @callback(Output("analytics-output", "children"), Input("analytics-input", "value"))
# def update_city_selected(input_value):
#     return f"You selected: {input_value}"
