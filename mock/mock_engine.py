from celery_tasks.engine.tasks import my_task

if __name__ == '__main__':
    for i in range(100):
        value = "task" + str(i)
        # 通过flask 或者django python后端框架 把方法映射到到一个url地址上，通过url发布任务
        task = my_task.delay(value)
        print(task)
