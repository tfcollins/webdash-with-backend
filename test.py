import time
import tasks
from celery.result import AsyncResult

result = tasks.add.delay(4, 5)

for i in range(10):
    time.sleep(1)
    status = result.status
    print(f"Task status: {status}")
    if status == "SUCCESS":
        print(f"Task result: {result.result}")
        break

result = tasks.long_running_task.delay(30)
id = result.id

for i in range(10):
    time.sleep(0.3)
    result = AsyncResult(id)
    status = result.status
    print(f"Task status: {status}")
    progress = result.info
    print(f"Task progress: {progress}")
    # print(f"Task progress: {progress}")
    if status == "SUCCESS":
        print(f"Task result: {result.result}")
        break
