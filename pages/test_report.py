import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from shared import shared_info
from report_parser import parse_report

dash.register_page(__name__)

page_info = shared_info(__file__)

progress = dbc.Progress(
    value=page_info["progress"],
    striped=True,
    animated=True,
    label=f"{page_info['progress']}%",
)

report = parse_report()


def generate_report_view(report):
    if report is None:
        return html.P("No report found.")

    status = "PASS" if report["exitcode"] == 0 else "FAIL"

    # tests = []
    # for test in report["tests"]:
    #     tests.append(html.H4(f"Test: {test['nodeid']}"))
    #     tests.append(html.P(f"Status: {test['outcome']}"))
    # Build table
    table = []
    head = html.Thead(html.Tr([html.Th("Test"), html.Th("Status")]))
    for test in report["tests"]:
        style = {"color": "green"} if test["outcome"] == "passed" else {"color": "red"}
        table.append(
            html.Tr([html.Td(test["nodeid"]), html.Td(test["outcome"], style=style)])
        )
    table = [head, html.Tbody(table)]

    table_style = {
        "border": "1px solid black",
        "border-collapse": "collapse",
        "width": "100%",
    }

    return html.Div(
        [
            html.H3(f"Report: {status}"),
            dbc.Table(table, bordered=True),
        ]
    )


layout = html.Div(
    [
        progress,
        html.H1("Test Report", style={"textAlign": "center"}),
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
                    [generate_report_view(report)],
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
