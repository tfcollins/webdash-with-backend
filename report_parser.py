import json
import os

report_file = "pyadi-iio/.report.json"


def parse_report():

    if not os.path.exists(report_file):
        return None
    with open(report_file) as f:
        data = json.load(f)

    return data
