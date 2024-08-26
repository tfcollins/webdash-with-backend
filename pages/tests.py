import dash
from dash import html, dcc, callback, Input, Output, State
import tasks
from celery.result import AsyncResult
import dash_bootstrap_components as dbc
import os
from shared import shared_info

dash.register_page(__name__)

# Set environment variable CELERY_RESULT_BACKEND
os.environ["CELERY_BROKER_URL"] = "amqp://localhost"
os.environ["CELERY_RESULT_BACKEND"] = "db+sqlite:///db.sqlite3"

page_info = shared_info(__file__)

progress = dbc.Progress(
    value=page_info["progress"],
    striped=True,
    animated=True,
    label=f"{page_info['progress']}%",
)

ra = None
log = []


def gen_log_view(id):
    # print(f"gen_log_view ID: {id}")
    ra = AsyncResult(id)
    # global ra
    status = ra.status
    progress = ra.info
    l = progress["data"]
    print("***" * 10)
    print(f"Status: {status}")
    print(f"Progress: {progress}")
    # Reverse l
    l = l[::-1]
    log = []
    for i in l:
        log.append(html.P(i))
        # log.append(html.Br())

    return log, status


layout = html.Div(
    [
        progress,
        html.H1("Board Analog Testing", style={"textAlign": "center"}),
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
                    [
                        html.Button("Start", id="start_button"),
                        html.Div([html.Div(id="log_id_parent", children=["Nothing"])]),
                        dcc.Interval(
                            id="interval_id",
                            interval=1 * 500,
                            n_intervals=0,
                            disabled=True,
                        ),
                        html.Br(),
                        dbc.Button("Back", href=page_info["prev"]),
                        dbc.Button("Next", href=page_info["next"]),
                    ]
                ),
            ]
        ),
        dcc.Store(id="data-store"),
    ]
)


@callback(
    output=[
        Output("log_id_parent", "children"),
        Output("interval_id", "disabled", allow_duplicate=True),
    ],
    inputs=[Input("interval_id", "n_intervals"), Input("data-store", "data")],
    prevent_initial_call=True,
)
def update_log(n_intervals, data):
    # print(f"RA: {data}")
    # print(f"Update log: {n_intervals}")
    try:
        info, status = gen_log_view(data)
    except Exception as e:
        # print(f"Error: {e}")
        info = None
        status = None

    disable = status == "SUCCESS" or status == "FAILURE"
    # print(f"Disable: {disable}, status: {status}")

    return [
        html.Div(id="log_id", children=info),
        html.P(f"Task status: {status}"),
    ], disable


# Set enable flag with start button
@callback(
    output=[Output("interval_id", "disabled"), Output("data-store", "data")],
    inputs=Input("start_button", "n_clicks"),
)
def start_task(n_clicks):
    print(f"Start task: {n_clicks}")
    if n_clicks is None:
        return True, []
    # global ra
    result = tasks.long_running_task.delay(10)
    id = result.id
    # ra = AsyncResult(id)
    # print(ra.status)
    print("### Task started")
    return False, id
