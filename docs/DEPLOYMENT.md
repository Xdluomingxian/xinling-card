# 部署指南

## 本地部署

### 1. 克隆项目

```bash
git clone https://github.com/Xdluomingxian/xinling-card.git
cd xinling-card
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动后端服务

```bash
cd src
python main.py
```

服务启动后访问：http://localhost:8000

### 5. 打开前端页面

在浏览器中打开：`frontend/index.html`

或直接访问 API 文档：http://localhost:8000/docs

---

## 云服务器部署（推荐）

### 使用 Docker 部署

#### 1. 创建 Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["python", "src/main.py"]
```

#### 2. 构建镜像

```bash
docker build -t xinling-card .
```

#### 3. 运行容器

```bash
docker run -d -p 8000:8000 --name xinling-card xinling-card
```

---

## 使用 Nginx 反向代理

### 1. 安装 Nginx

```bash
sudo apt update
sudo apt install nginx
```

### 2. 配置 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/xinling-card/frontend;
    }
}
```

### 3. 重启 Nginx

```bash
sudo systemctl restart nginx
```

---

## 使用 systemd 管理服务

### 1. 创建服务文件

```bash
sudo nano /etc/systemd/system/xinling-card.service
```

### 2. 添加以下内容

```ini
[Unit]
Description=心灵卡片 API 服务
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/projects/xinling-card
Environment="PATH=/home/ubuntu/projects/xinling-card/venv/bin"
ExecStart=/home/ubuntu/projects/xinling-card/venv/bin/python /home/ubuntu/projects/xinling-card/src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl start xinling-card
sudo systemctl enable xinling-card
```

### 4. 查看状态

```bash
sudo systemctl status xinling-card
```

---

## 环境变量配置（可选）

创建 `.env` 文件：

```bash
# 服务配置
HOST=0.0.0.0
PORT=8000
DEBUG=false

# API 配置（如需扩展 AI 功能）
AI_API_KEY=your_api_key
AI_BASE_URL=https://api.example.com
```

---

## 性能优化建议

### 1. 使用 Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
```

### 2. 使用 Redis 缓存

```bash
# 安装 Redis
sudo apt install redis-server

# 在代码中添加缓存逻辑
```

### 3. 数据库优化

- 使用 PostgreSQL 替代 SQLite
- 添加索引优化查询
- 使用连接池

---

## 监控与日志

### 1. 查看日志

```bash
# systemd 服务日志
sudo journalctl -u xinling-card -f

# 应用日志
tail -f /path/to/logs/app.log
```

### 2. 性能监控

- 使用 Prometheus + Grafana
- 使用 New Relic
- 使用 Datadog

---

## 故障排查

### 常见问题

#### 1. 端口被占用

```bash
# 查看占用端口的进程
sudo lsof -i :8000

# 杀死进程
sudo kill -9 <PID>
```

#### 2. 权限问题

```bash
# 修改文件权限
sudo chown -R ubuntu:ubuntu /home/ubuntu/projects/xinling-card
```

#### 3. 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

---

## 更新部署

```bash
# 拉取最新代码
git pull origin main

# 重启服务
sudo systemctl restart xinling-card

# 或 Docker 容器
docker restart xinling-card
```

---

*最后更新：2026-03-17*
