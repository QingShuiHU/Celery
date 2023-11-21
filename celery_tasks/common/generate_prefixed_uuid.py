import datetime
import threading
import uuid


def generate_prefixed_uuid(prefix):
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4()).replace('-', '')  # 生成UUID并去除连接符'-'
    prefixed_uuid = f"{prefix}_{current_time}_{unique_id}"
    return prefixed_uuid


def check_duplicates(thread_num, prefix):
    generated_uuids = set()
    lock = threading.Lock()  # 创建一个锁用于线程安全操作集合

    def generate_and_check():

        # 在 Python 中，nonlocal 关键字用于在函数或作用域内标识一个变量不是局部变量，也不是全局变量，而是外围作用域（非全局作用域）中的变量。
        # 当一个嵌套函数（函数内部包含另一个函数）试图修改或引用外部函数的变量时，可以使用 nonlocal 关键字。
        nonlocal generated_uuids
        new_uuid = generate_prefixed_uuid(prefix)
        with lock:
            generated_uuids.add(new_uuid)

    threads = []
    for _ in range(thread_num):
        thread = threading.Thread(target=generate_and_check)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Generated UUIDs:")
    for uuid_generated in generated_uuids:
        print(uuid_generated)


if __name__ == '__main__':
    prefix = "example"
    threadNum = 10000
    # 并发threadNum个线程，每个线程调用generate_prefixed_uuid函数生成一个带前缀的UUID，检查是否有重复的UUID
    # 重复的UUID会被打印出来
    check_duplicates(threadNum, prefix)
