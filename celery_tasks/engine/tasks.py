# 导入main中的app
import random
import time

from celery_tasks.main import app
from celery_tasks.common.logger import MyLogger

log = MyLogger()


# 模拟任务执行耗费时间，从[base_time-fluctuation,base_time+fluctuation]随机选择时间。
def generate_random_time(base_time, fluctuation):
    # 在浮动范围[-fluctuation,+fluctuation]内生成随机数
    random_offset = random.uniform(-fluctuation, fluctuation)
    # 计算最终休眠时间
    sleep_time = base_time + random_offset
    # 确保休眠时间不为负数
    sleep_time = max(0, sleep_time)
    return sleep_time


# 成功的回调
def on_success_callback(self, retval, task_id, args, kwargs):
    log.success(f'任务执行成功,正确返回')
    print(f"Task succeeded with result: {retval}")


# 失败的回调
def on_failure_callback(self, exc, task_id, args, kwargs, einfo):
    log.error("任务执行失败")
    log.exception(exc)
    print("Task failed with exception: {}".format(exc))


# 定义异步任务
@app.task(bind=True, on_success=on_success_callback, on_failure=on_failure_callback)
def my_task(self, param):
    try:
        log.info("Task start with param: {}".format(param))
        log.info("mock 模拟逻辑执行...")
        # 执行任务的逻辑
        # print("mock 模拟逻辑执行...")
        random_sleep_time = generate_random_time(3, 1)
        # print(f'随机休眠{random_sleep_time}秒')
        log.info(f'随机休眠{random_sleep_time}秒')
        time.sleep(random_sleep_time)
        # 如果任务成功完成，则调用 on_success 回调函数
        return "Task completed successfully with param: {}".format(param)
    except Exception as exc:
        # 如果任务执行失败，则调用 on_failure 回调函数
        # countdown: 设置任务重新执行前的延迟时间（秒）。
        # max_retries: 设置任务的最大重试次数，达到最大次数后任务将不再重新执行。
        # retry_backoff: 一个可选的参数，用于在每次重试之间增加延迟的系数，可以是整数或浮点数。例如，设置为 2 可以使每次重试的等待时间翻倍。
        raise self.retry(exc=exc, countdown=10, max_retries=3, retry_backoff=2)  # 可选的重试机制
