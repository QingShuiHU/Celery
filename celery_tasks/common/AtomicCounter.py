import threading

from singleton import singleton


@singleton
class AtomicCounter:
    def __init__(self, initial_value=0):
        self.value = initial_value
        self.lock = threading.Lock()

    def increment_and_get(self):
        with self.lock:
            self.value += 1
            return self.value

    def get_value(self):
        with self.lock:
            return self.value
