#!/bin/bash


# 启动 Celery Worker
#python run_celery_worker.py >> celery_worker.log 2>&1 &

# 启动 Celery Beat（如果不需要定时任务，可以注释掉这行）
#python run_celery_beat.py >> celery_beat.log 2>&1 &

# 启动 Gunicorn 服务（前台运行）
gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 4 --worker-connections 8000 app:app -c next_console_conf.py >> gunicorn.log
