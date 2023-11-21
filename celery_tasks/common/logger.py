import os
from functools import wraps
from time import perf_counter
from loguru import logger
from singleton import singleton


@singleton
class MyLogger:
    """
    日志记录器，根据时间、文件大小切割日志
    """

    def __init__(self, log_dir='D:/Users/YanDa HU/Desktop/仿冒APP/Code/taskDistribute/logs', rotation="00:00", retention='7 days', enable_level_logs=False):
        self.log_dir = log_dir
        self.rotation = rotation
        self.retention = retention
        self.enable_level_logs = enable_level_logs
        self.logger = self.configure_logger()

    def configure_logger(self):
        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)
        shared_config = {
            "level": "DEBUG",
            "enqueue": True,
            "backtrace": True,
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        }

        # 添加按照日期切割的文件 handler
        logger.add(
            sink=f"{self.log_dir}/{{time:YYYY-MM-DD}}.log",
            rotation=f"{self.rotation}",
            retention=self.retention,
            **shared_config
        )

        if self.enable_level_logs:
            # 添加按照等级切割的文件 handler 和控制台输出
            # 添加按照等级划分以及日期和大小切割的文件 handler
            for level in ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]:
                logger.add(
                    sink=self.get_log_path(f"{{time:YYYY-MM-DD}}-{level}.log"),
                    filter=self.level_filter(level),  # 使用 level_filter 方法
                    **shared_config
                )
        return logger

    def level_filter(self, level):
        """过滤日志等级"""

        def is_level(record):
            return record["level"].name == level

        return is_level

    def get_log_path(self, filename):
        return os.path.join(self.log_dir, filename)

    def __getattr__(self, level: str):
        return getattr(self.logger, level)

    def log_decorator(self):
        """
        日志装饰器，记录函数的名称、参数、返回值、运行时间和异常信息
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.logger.info('-----------函数调用-----------')
                self.logger.info(f'调用 {func.__name__} args: {args}; kwargs:{kwargs}')
                start = perf_counter()  # 开始时间
                try:
                    result = func(*args, **kwargs)
                    end = perf_counter()  # 结束时间
                    duration = end - start
                    self.logger.info(f"{func.__name__} 返回结果：{result}, 耗时：{duration:.4f}s")
                    return result
                except Exception as e:
                    self.logger.info(f"-----------调用{func.__name__}异常-----------")
                    self.logger.exception(e)
                    # raise e

            return wrapper

        return decorator


if __name__ == '__main__':
    log = MyLogger()


    # @log.catch()
    @log.log_decorator()
    def test_zero_division_error(a, b):
        # return a / b if b != 0 else float('inf')
        return a / b


    for i in range(10):
        log.error('错误信息')
        log.critical('严重错误信息')
        test_zero_division_error(1, 0)
        log.debug('调试信息')
        log.info('普通信息')
        log.success('成功信息')
        log.warning('警告信息')
