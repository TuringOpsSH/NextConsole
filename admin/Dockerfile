# 使用官方 Python 运行时作为父镜像
FROM registry.cn-hangzhou.aliyuncs.com/next_console/python

# 设置工作目录
WORKDIR /app

# 先复制 requirements.txt 并安装依赖
COPY requirements.txt /app/
RUN pip install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN playwright install
# 复制当前目录内容到工作目录
COPY . /app

# 设置环境变量
ENV FLASK_MODEL="private"

# 暴露端口
EXPOSE 5011

# 运行启动脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 启动应用和 Celery worker
ENTRYPOINT ["/entrypoint.sh"]