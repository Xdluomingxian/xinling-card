# 心灵卡片 - 前端部署指南

## 🌐 GitHub Pages 部署

### 自动部署

本项目已配置 GitHub Actions，推送到 `main` 分支后会自动部署到 GitHub Pages。

**访问地址**: `https://Xdluomingxian.github.io/xinling-card/`

### 手动触发部署

1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 选择 **Deploy to GitHub Pages** 工作流
4. 点击 **Run workflow**
5. 等待部署完成（约 1-2 分钟）

---

## ⚙️ API 地址配置

由于 GitHub Pages 是静态托管，需要配置后端 API 地址。

### 方式 1：浏览器配置（推荐）

1. 打开前端页面
2. 点击右上角的 **齿轮图标** ⚙️
3. 输入 API 服务器地址
4. 刷新页面

### 方式 2：修改代码

编辑 `frontend/index.html`，找到：

```javascript
const API_BASE = localStorage.getItem('apiBase') || 'http://localhost:8000';
```

修改为实际 API 地址：

```javascript
const API_BASE = 'http://your-api-server.com:8000';
```

---

## 🚀 后端 API 部署选项

### 选项 1：本地运行（开发测试）

```bash
cd /home/ubuntu/projects/xinling-card
source venv/bin/activate
cd src
python main.py
```

访问：http://localhost:8000

### 选项 2：云服务器部署

**推荐平台**：
- 阿里云 ECS
- 腾讯云 CVM
- 华为云
- VPS（DigitalOcean, Linode 等）

**部署步骤**：
1. 购买云服务器（约 ¥50-100/月）
2. 安装 Python 3.10+
3. 克隆项目
4. 安装依赖
5. 启动服务
6. 配置域名和 HTTPS

详见：`docs/DEPLOYMENT.md`

### 选项 3：使用 Serverless 服务

**推荐平台**：
- Vercel（免费）
- Railway（免费额度）
- Render（免费额度）
- 阿里云函数计算

**优势**：
- 无需管理服务器
- 自动扩展
- 按使用量付费

---

## 🔒 HTTPS 配置

生产环境强烈建议使用 HTTPS。

### 使用 Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 使用 Let's Encrypt 免费证书

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 📊 性能优化

### 1. 启用 Gzip 压缩

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

### 2. 使用 CDN

- Cloudflare（免费）
- 阿里云 CDN
- 腾讯云 CDN

### 3. 缓存策略

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## 📱 移动端优化

前端页面已使用 Tailwind CSS，自动适配移动端。

**测试方法**：
1. 打开浏览器开发者工具
2. 切换到移动设备模式
3. 测试不同屏幕尺寸

---

## 🔍 监控与日志

### 1. 访问统计

- Google Analytics
- 百度统计
- Plausible（隐私友好）

### 2. 错误监控

- Sentry
- LogRocket

### 3. 性能监控

- Google PageSpeed Insights
- WebPageTest

---

## 📝 检查清单

部署前请确认：

- [ ] GitHub Pages 已启用
- [ ] API 服务器已部署并可访问
- [ ] API 地址已配置
- [ ] HTTPS 已配置（生产环境）
- [ ] 跨域访问已允许（CORS）
- [ ] 移动端测试通过
- [ ] 错误处理完善

---

## 🆘 故障排查

### 问题 1：页面显示"API 未连接"

**原因**：API 地址配置错误或服务器未启动

**解决**：
1. 点击齿轮图标检查 API 地址
2. 确认 API 服务器正在运行
3. 检查防火墙设置

### 问题 2：跨域错误（CORS）

**原因**：后端未配置 CORS

**解决**：已在 `src/main.py` 中配置 CORS，允许所有来源访问。

### 问题 3：GitHub Pages 404

**原因**：部署失败

**解决**：
1. 检查 GitHub Actions 日志
2. 确认 `frontend/index.html` 存在
3. 重新触发部署

---

## 📞 技术支持

遇到问题？

- **GitHub Issues**: https://github.com/Xdluomingxian/xinling-card/issues
- **API 文档**: http://localhost:8000/docs
- **部署指南**: docs/DEPLOYMENT.md

---

*最后更新：2026-03-17*
