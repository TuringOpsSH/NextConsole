FROM ubuntu:22.04

# 设置环境变量（避免交互式安装提示）
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1

# 安装最小化Python环境和必要系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    python3.11-venv \
    # Playwright依赖
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    # 中文字体
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# 创建虚拟环境（更干净的依赖管理）
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


# 设置工作目录
WORKDIR /app

# 先复制 requirements.txt 并安装依赖
COPY server/requirements.txt /app/
#RUN pip install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN playwright install
RUN playwright install-deps
RUN apt install libreoffice fonts-wqy-zenhei fonts-wqy-microhei -y

# 复制当前目录内容到工作目录
COPY server/. /app/server/
COPY admin/. /app/admin/

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
