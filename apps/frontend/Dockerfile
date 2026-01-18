# 使用多阶段构建：第一阶段 - 构建前端项目
FROM node:18-alpine AS build-stage

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json到工作目录
COPY package*.json ./

# 安装依赖（使用--no-cache-dir减少镜像大小）
RUN npm install --no-cache-dir

# 复制项目文件到工作目录
COPY . .

# 构建项目
RUN npm run build

# 第二阶段 - 使用Nginx作为静态文件服务器
FROM nginx:alpine AS production-stage

# 复制Nginx配置文件（如果需要自定义配置）
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制构建后的静态文件到Nginx的默认目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]