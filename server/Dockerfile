# 使用官方 Python 运行时作为父镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 先复制 requirements.txt 并安装依赖
COPY requirements.txt /app/
RUN pip install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt-get update
RUN playwright install
RUN playwright install-deps
RUN apt  install libreoffice-common  default-jre


# 复制当前目录内容到工作目录
COPY ./next_console/. /app/server/
COPY ./next_console_admin/. /app/admin/

# 设置环境变量
ENV FLASK_MODEL="private" \
    TZ="Asia/Shanghai"

# 暴露端口
EXPOSE 5123
EXPOSE 5011
# 运行启动脚本
# 复制并设置 entrypoint.sh

RUN chmod +x /app/server/entrypoint.sh
RUN chmod +x /app/admin/entrypoint.sh

# 启动应用和 Celery worker
CMD ["bash"]