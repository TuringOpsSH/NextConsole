#!/bin/bash




# 启动 Gunicorn 服务（前台运行）
gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 4 --worker-connections 8000 app:app -c next_console_admin_conf.py
