# 使用官方Node.js镜像作为基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json到工作目录
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目文件到工作目录
COPY . .

# 构建项目
RUN npm run build

# 安装静态文件服务器
RUN npm install -g serve

# 暴露端口
EXPOSE 3000

# 运行项目
CMD ["serve", "-s", "dist"]