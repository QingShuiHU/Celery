# import threading
# import pymysql
#
# from DBUtils.PooledDB import PooledDB
#
# # 创建数据库连接池
# pool = PooledDB(pymysql, 100,
#                 host='localhost',
#                 user='root',
#                 password='root',
#                 db='celery_test')
#
# # 创建互斥锁
# lock = threading.Lock()
#
#
# # 查询数据库中是否存在特定数据，并插入数据
# def check_and_insert(name, email):
#     conn = None
#     try:
#         conn = pool.connection()
#         cursor = conn.cursor()
#
#         # 加锁
#         lock.acquire()
#         cursor.execute("SELECT * FROM users WHERE name = %s OR email = %s FOR UPDATE", (name, email))
#         existing_user = cursor.fetchone()
#
#         if not existing_user:
#             cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
#             conn.commit()
#
#         cursor.close()
#     except pymysql.IntegrityError as e:
#         print(f"Transaction failed: {e}")
#         if conn:
#             conn.rollback()
#     except Exception as ex:
#         print(f"Error occurred: {ex}")
#         if conn:
#             conn.rollback()
#     finally:
#         # 释放锁
#         if lock.locked():
#             lock.release()
#         if conn:
#             conn.close()
#
#
# # 创建多个线程执行查询和插入操作
# def create_threads():
#     data_to_insert = [
#         ("Alice", "alice@example.com"),
#         ("Bob", "bob@example.com"),
#         ("Charlie", "charlie@example.com"),
#         # ("Alice", "alice@example.com")  # 尝试重复插入的数据
#     ]
#
#     threads = []
#     for data in data_to_insert:
#         name, email = data
#         thread = threading.Thread(target=check_and_insert, args=(name, email))
#         threads.append(thread)
#         thread.start()
#
#     for i in range(100):
#         name, email = ("Alice", "alice@example.com")
#         thread = threading.Thread(target=check_and_insert, args=(name, email))
#         threads.append(thread)
#         thread.start()
#
#     # 等待所有线程执行完成
#     for thread in threads:
#         thread.join()
#
#
# # 执行多线程操作
# create_threads()


import threading
import pymysql
from loguru import logger
from DBUtils.PooledDB import PooledDB

# 创建数据库连接池
pool = PooledDB(pymysql, 100,
                host='localhost',
                user='root',
                password='root',
                db='celery_test')



# 查询数据库中是否存在特定数据，并插入数据
def check_and_insert(name, email):
    conn = None
    try:
        conn = pool.connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE name = %s OR email = %s", (name, email))
        existing_user = cursor.fetchone()

        if not existing_user:
            logger.info(f"检测{name}-{email}通过，准备插入")
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()

        cursor.close()
    except pymysql.IntegrityError as e:
        print(f"Transaction failed: {e}")
        if conn:
            conn.rollback()
    except Exception as ex:
        print(f"Error occurred: {ex}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


# 创建多个线程执行查询和插入操作
def create_threads():
    data_to_insert = [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Charlie", "charlie@example.com"),
        # ("Alice", "alice@example.com")  # 尝试重复插入的数据
    ]

    threads = []
    for data in data_to_insert:
        name, email = data
        thread = threading.Thread(target=check_and_insert, args=(name, email))
        threads.append(thread)
        thread.start()

    for i in range(100):
        name, email = ("Alice", "alice@example.com")
        thread = threading.Thread(target=check_and_insert, args=(name, email))
        threads.append(thread)
        thread.start()

    # 等待所有线程执行完成
    for thread in threads:
        thread.join()


# 执行多线程操作
create_threads()
