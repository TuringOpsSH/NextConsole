# 使用官方 Python 运行时作为父镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 先复制 requirements.txt 并安装依赖
COPY requirements.txt /app/
#RUN pip install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN playwright install
RUN playwright install-deps
RUN apt install libreoffice fonts-wqy-zenhei fonts-wqy-microhei -y

# 复制当前目录内容到工作目录
COPY ./server/. /app/server/
COPY ./admin/. /app/admin/

# 脱敏工作
RUN rm -rf /app/server/.git && \
    rm -rf /app/admin/.git

RUN rm -f /app/server/app/config/config_prod.py && rm -f /app/server/app/config/config_dev.py && rm -f /app/server/app/config/config_local.py && rm -f /app/admin/app/config/config_prod.py && rm -f /app/admin/app/config/config_dev.py && rm -f /app/admin/app/config/config_local.py

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
