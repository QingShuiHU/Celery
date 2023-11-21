# producer.py
"""
模拟向rabbitmq任务队列中放入任务，此部分已经由甲方实现，功能测试的模拟，最终需要移除
"""
import json
import random
import string

import utils


def generate_random_md5():
    # 生成一个随机的模拟 MD5，假设长度为32
    md5_length = 32
    chars = string.hexdigits.lower()  # 使用16进制字符（0-9，a-f）
    return ''.join(random.choice(chars) for _ in range(md5_length))


def generate_random_file_path():
    # 生成一个随机的模拟文件路径，假设文件路径长度随机8~20个字符
    path_length = random.randint(8, 20)
    chars = string.ascii_letters + string.digits + '/_'  # 使用字母、数字和一些特殊字符
    return ''.join(random.choice(chars) for _ in range(path_length))


def produce_message():
    """
    生产者生产消息的函数（模拟向rabbitmq中发送任务）
    """
    connection = utils.create_connection()
    channel = connection.channel()

    # 创建一个队列
    channel.queue_declare(queue='fake_engine')

    # 生产消息(发送任务，模拟任务积压)
    for i in range(1000):
        #  测试任务数据，模拟
        mock_task_data = {"taskID": f"Task {i}", "md5": generate_random_md5(), "filePath": generate_random_file_path()}
        # 将模拟任务数据转换为字符串
        json_message = json.dumps(mock_task_data)
        # 将字符串使用UTF-8编码为字节串 (rabbitmq中生产者和消费者应该统一编码，防止乱码)
        json_message_bytes = json_message.encode('utf-8')
        channel.basic_publish(exchange='', routing_key='fake_engine', body=json_message_bytes)
        print(f"Produced: {json_message}")

    # 关闭连接
    connection.close()


if __name__ == "__main__":
    produce_message()
