from gevent import monkey
monkey.patch_all()

from app.app import celery
import socket

if __name__ == "__main__":
    # 获取主机名
    hostname = socket.gethostname()

    # 确保任务调度指定的队列
    celery.conf.task_default_queue = f'{hostname}_queue'

    # 定义 Celery Beat 的命令行参数
    argv = [
        'beat',
        '-l', 'INFO',
        '--scheduler', 'celery.beat:PersistentScheduler'
    ]

    # 启动 Celery Beat
    celery.start(argv)