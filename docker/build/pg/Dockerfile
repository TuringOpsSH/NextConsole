# 使用官方的 PostgreSQL 17 镜像作为基础
FROM postgres:17

# 安装编译所需的依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-17

# 克隆 pgvector 仓库
RUN git clone https://github.com/pgvector/pgvector.git
WORKDIR /pgvector

# 编译并安装 pgvector
RUN make
RUN make install
# 禁用自动初始化
ENV POSTGRES_INITDB_ARGS="--no-locale"
ENV PGDATA="/var/lib/postgresql/data/pgdata"
