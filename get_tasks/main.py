# main.py

import threading
import producer
import consume

# 创建一个线程来执行生产者
producer_thread = threading.Thread(target=producer.produce_message)

# 创建多个线程来执行消费者
num_consumers = 10  # 假设有10个消费者
consumer_threads = []

for i in range(num_consumers):
    thread = threading.Thread(target=consume.consume_message)
    consumer_threads.append(thread)

# 启动生产者和消费者线程
producer_thread.start()

for thread in consumer_threads:
    thread.start()

# 等待所有线程结束
producer_thread.join()

for thread in consumer_threads:
    thread.join()
