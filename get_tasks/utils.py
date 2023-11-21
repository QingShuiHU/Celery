# utils.py

import pika


def create_connection():
    """
    创建RabbitMQ连接的函数
    """
    # 用户名和密码连接RabbitMQ
    # credentials = pika.PlainCredentials('your_username', 'your_password')
    connection_params = pika.ConnectionParameters(
        host='localhost',
        port=5672,  # 默认RabbitMQ端口
        # credentials=credentials  # 添加用户名和密码
    )
    connection = pika.BlockingConnection(connection_params)
    return connection
