import threading


def singleton(cls):
    '''
    单例模式，双检查锁
    :param cls:
    :return:
    '''
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
