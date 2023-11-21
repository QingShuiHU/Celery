# 从rabbitmq中获取任务，分发到celery 【rabbitmq的消费者，celery的生产者】
import json
import time

import utils
from concurrent.futures import ThreadPoolExecutor
from celery_tasks.engine.tasks import my_task
from celery_tasks.common.logger import MyLogger

log = MyLogger()


def process_task(task):
    """
    处理任务的函数
    """
    log.info(f"从rabbitmq中接收到任务,转发给celery,Processing 任务数据: {task}")
    # print(f"从rabbitmq中接收到任务,转发给celery,Processing 任务数据: {task}")
    # todo 返回 类型,可以获取任务id,任务状态,还可以调整为同步执行等信息
    task_info = my_task.delay(task)
    log.info(task_info)
    # print(task_info)
    log.info("rabbitmq处理完成(消费者) 转发celery(生产者)异步任务，记录日志")
    # print("rabbitmq处理完成(消费者) 转发celery(生产者)异步任务，记录日志")


def consume_message():
    """
    rabbitmq消费者,消费rabbitmq任务消息的函数（任务分发到celery）
    """
    connection = utils.create_connection()
    channel = connection.channel()

    # 创建一个队列
    channel.queue_declare(queue='fake_engine')

    def callback(ch, method, properties, body):
        """
        处理从队列中接收到的消息
        """
        json_message_bytes = body.decode('utf-8')
        # 解码消息并还原为 JSON 对象
        task_data = json.loads(json_message_bytes)
        log.info(f'接收到任务，任务数据:{task_data}')
        # print(f'接收到任务，任务数据:{task_data}')
        # 提取 MD5 和文件路径
        md5 = task_data.get('md5')
        file_path = task_data.get('filePath')
        log.info(f'从任务中获取到md5:{md5} file_path:{file_path}')
        # print(f'从任务中获取到md5:{md5} file_path:{file_path}')
        process_task(task_data)
        # # 在线程池中异步执行任务
        # with ThreadPoolExecutor() as executor:
        #     executor.submit(process_task, task_data)

    # 消费消息
    channel.basic_consume(queue='fake_engine', on_message_callback=callback, auto_ack=True)

    print('Waiting for tasks. To exit press CTRL+C')
    # 开始消费消息
    channel.start_consuming()


if __name__ == "__main__":
    consume_message()

