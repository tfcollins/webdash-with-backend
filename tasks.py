from celery import Celery, current_task
import time

app = Celery("tasks", broker="amqp://localhost", backend="db+sqlite:///db.sqlite3")


@app.task
def add(x, y):
    time.sleep(2.0)
    return x + y


@app.task(bind=True)
def long_running_task(self, total_steps):
    state = []
    for i in range(total_steps):
        # Simulate work by sleeping
        time.sleep(1)

        # Update the task state with progress information
        state.append("Step " + str(i))
        self.update_state(state="PROGRESS", meta={"current": i, "total": total_steps, "data": state})

    return {"current": total_steps, "total": total_steps, "status": "Task completed!", "data": state}
