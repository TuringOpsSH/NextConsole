# 使用多阶段构建
FROM --platform=$BUILDPLATFORM node:18-bullseye AS builder

# 第一阶段：构建 server_web
WORKDIR /app/server_web
COPY server_web/package*.json ./
RUN npm install
COPY server_web/ .
RUN npm run build:private

# 第二阶段：构建 admin_web
WORKDIR /app/admin_web
COPY admin_web/package*.json ./
RUN npm install
COPY admin_web/ .
RUN npm run build:private

# 最终阶段使用nginx
FROM nginx:alpine

# 移除Nginx默认配置文件
RUN rm /etc/nginx/nginx.conf

# 创建下载目录
RUN mkdir -p /data/downloads && chown -R nginx:nginx /data/downloads

# 复制自定义Nginx配置
COPY docker/build/web/nginx.conf /etc/nginx/nginx.conf

# 从builder阶段复制构建好的dist文件
COPY --from=builder /app/server_web/dist /usr/share/nginx/html/server/
COPY --from=builder /app/admin_web/dist /usr/share/nginx/html/admin/

# 暴露端口
EXPOSE 6668 6669

# 启动Nginx服务
CMD ["nginx", "-g", "daemon off;"]