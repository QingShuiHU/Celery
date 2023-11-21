# celery相关配置

# redis格式:'redis://:{PASSWORD}@localhost:6379/0'
# broker(消息中间件来接收和发送任务消息)
broker_url = 'redis://@localhost:6379/0'
# backend(存储worker执行的结果)
result_backend = 'redis://@localhost:6379/1'

# 设置时间参照，不设置默认使用的UTC时间
timezone = 'Asia/Shanghai'
# 序列化配置
# 指定任务的序列化
task_serializer = 'json'
# 指定执行结果的序列化
result_serializer = 'json'
accept_content = ['json']
# broker_connection_retry_on_startup = True

# 并发设置
worker_concurrency = 20  # 并发工作进程数

# 超时设置
task_time_limit = 300  # 任务超时时间，单位为秒
