from celery import Celery, current_task
import time
import pytest
import subprocess
import os

app = Celery("tasks", broker="amqp://localhost", backend="db+sqlite:///db.sqlite3")


@app.task
def add(x, y):
    time.sleep(2.0)
    return x + y


@app.task(bind=True)
def long_running_task(self, total_steps):
    state = []

    # Set initial state for the task
    self.update_state(
        state="PROGRESS", meta={"current": 0, "total": total_steps, "data": state}
    )

    # Wait for webui to connect to the task
    time.sleep(2)

    # Start background subprocess
    current_dif_of_this_file = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_dif_of_this_file)
    print(f"Here: {os.getcwd()}")
    os.chdir("pyadi-iio")
    cmd = [
        "../venv/bin/python",
        "-m",
        "pytest",
        "-vs",
        "test/test_pluto_p.py",
        "--uri",
        "ip:pluto.local",
        "--hw",
        "pluto",
        "--json-report",
        "-k",
        "test_pluto_attr",
    ]
    print(cmd)
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    print("Process started")
    # time.sleep(4)
    # # Get the current output from the subprocess
    # print("Output: ")
    # while True:
    #     output = process.stdout.readline()
    #     if output == "" and process.poll() is not None:
    #         break
    #     if output:
    #         print("GOT:")
    #         print(output.strip())
    #         break
    # print("Output end")
    # errors = process.stderr.read()
    # if errors:
    #     print("Errors:", errors)
    #     errors = str(errors).split("\n")
    #     state.append(errors)
    #     self.update_state(state="FAILURE", meta={"current": 0, "total": total_steps, "data": state})
    #     return {"status": "FAILURE", "errors": errors, "data": state}

    timeout_seconds = 10

    while process.poll() is None:
        now = time.time()
        output = process.stdout.readline()
        if output:
            print("GOT:")
            print(output.strip())
            state.append(output.strip())
            self.update_state(
                state="PROGRESS",
                meta={"current": 0, "total": total_steps, "data": state},
            )
        else:
            duration = time.time() - now
            if duration > timeout_seconds:
                print("Timeout")
                process.kill()
                break
    print("Process ended")

    error_code = process.returncode
    print(f"Error code: {error_code}")
    if error_code != 0:
        output = process.stdout.readlines()
        error = process.stderr.readlines()
        state.append(f"Error code: {error_code}")
        state.append("Output:")
        state.extend(output)
        state.append("Errors:")
        state.extend(error)
        self.update_state(
            state="FAILURE", meta={"current": 0, "total": total_steps, "data": state}
        )
        return {"status": "FAILURE", "errors": state, "data": state}
    else:
        state.append("Task completed!")
        self.update_state(
            state="SUCCESS", meta={"current": 0, "total": total_steps, "data": state}
        )
        return {"status": "SUCCESS", "data": state}

    for i in range(total_steps):
        # Simulate work by sleeping
        time.sleep(1)

        # Get the output from the subprocess
        for line in process.stdout:
            print(line)
            state.append(line)

        # Update the task state with progress information
        # state.append("Step " + str(i))
        self.update_state(
            state="PROGRESS", meta={"current": i, "total": total_steps, "data": state}
        )

    return {
        "current": total_steps,
        "total": total_steps,
        "status": "Task completed!",
        "data": state,
    }
