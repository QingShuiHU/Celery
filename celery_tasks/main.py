# from celery import Celery
#
# app = Celery("celery sms app")
# # celery项目配置： worker代理人，指定任务存储到哪里区。
#
# # celery配置
# app.config_from_object('celery_tasks.config')
#
# # 自动加载可用的任务
# app.autodiscover_tasks([
#     'celery_tasks.sms',
# ])
#
#
# def start_celery_worker(celery_app):
#     celery_app.worker_main(argv=['worker', '--loglevel=info', "--concurrency=10"])
#
#
# if __name__ == '__main__':
#     start_celery_worker(app)

from celery import Celery

broker_url = 'redis://@127.0.0.1:6379/1',
result_backend = 'redis://@127.0.0.1:6379/2'

app = Celery('demo')
# app.conf.update(
#     broker_url='redis://@127.0.0.1:6379/1',
#     result_backend='redis://@127.0.0.1:6379/2'
# )

# 自动加载可用的任务
app.autodiscover_tasks([
    'celery_tasks.engine'
])

app.config_from_object('celery_tasks.config')


def start_celery_worker(celery_app):
    # celery_app.worker_main(argv=['worker', '--loglevel=info', "--concurrency=10"])
    celery_app.worker_main(argv=['worker', '--loglevel=info'])


if __name__ == '__main__':
    start_celery_worker(app)
