import dash
from dash import html, dcc, callback, Input, Output
import tasks
from celery.result import AsyncResult
import dash_bootstrap_components as dbc
import os

dash.register_page(__name__)

# Set environment variable CELERY_RESULT_BACKEND
os.environ["CELERY_BROKER_URL"] = "amqp://localhost"
os.environ["CELERY_RESULT_BACKEND"] = "db+sqlite:///db.sqlite3"

value = 100
progress = dbc.Progress(value=value, striped=True, animated=True, label=f"{value}%")

ra = None
log = []


def gen_log_view():
    global ra
    status = ra.status
    progress = ra.info
    l = progress['data']
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
        html.H1("Board Analog Testing"),
        html.Button("Start", id="start_button"),
        html.Div([html.Div(id="log_id_parent", children=["Nothing"])]),
        dcc.Interval(id="interval_id", interval=1 * 500, n_intervals=0, disabled=True),
        html.Br(),
        dbc.Button("Back", href="/step1"),
        dbc.Button("Next", href="/step2"),
    ]
)


@callback(
    output=[
        Output("log_id_parent", "children"),
        Output("interval_id", "disabled", allow_duplicate=True),
    ],
    inputs=Input("interval_id", "n_intervals"),
    prevent_initial_call=True,
)
def update_log(n_intervals):
    print(f"Update log: {n_intervals}")
    try:
        info, status = gen_log_view()
    except:
        info = None
        status = None

    disable = status == "SUCCESS" or status == "FAILURE"
    print(f"Disable: {disable}, status: {status}")

    return [html.Div(id="log_id", children=info), html.P(f"Task status: {status}")], disable


# Set enable flag with start button
@callback(
    output=Output("interval_id", "disabled"),
    inputs=Input("start_button", "n_clicks"),
)
def start_task(n_clicks):
    print(f"Start task: {n_clicks}")
    if n_clicks is None:
        return True
    global ra
    result = tasks.long_running_task.delay(10)
    id = result.id
    ra = AsyncResult(id)
    print(ra.status)
    return False
