
FROM nginx:alpine

# 移除 Nginx 默认配置文件
RUN rm /etc/nginx/nginx.conf
 

# 将自定义的 Nginx 配置文件复制到容器中
RUN mkdir -p /data/downloads && chown -R nginx:nginx /data/downloads
COPY nginx.conf /etc/nginx/nginx.conf

# 将 Vue 3 项目构建后的静态文件复制到 Nginx 静态资源目录
COPY server_dist/ /usr/share/nginx/html/server/
COPY admin_dist/ /usr/share/nginx/html/admin/

# 暴露 Nginx 默认端口
EXPOSE 6668 6669

# 启动 Nginx 服务
CMD ["nginx", "-g", "daemon off;"]
