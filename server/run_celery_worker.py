from gevent import monkey
import platform
if platform.system().lower().startswith('darwin'):
    monkey.patch_socket()
else:
    monkey.patch_all()
from app.app import celery
import socket

if __name__ == "__main__":
    # 获取主机名
    hostname = socket.gethostname()
    celery.conf.task_default_queue = f'nc_server_queue'
    # 定义Celery worker的命令行参数，并指定队列
    argv = [
        'worker',
        '-l', 'INFO',
        '-P', 'gevent',
        '--concurrency=80',
        '-E',
        '-n', f'worker@{hostname}',
        '-Q', f'nc_server_queue'
    ]
    celery.worker_main(argv)

















































