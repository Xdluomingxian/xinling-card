# 🚀 心灵卡片 - 快速部署指南

## 方式 1：GitHub Pages（推荐，免费）

### 步骤

1. **启用 GitHub Pages**
   - 打开 https://github.com/Xdluomingxian/xinling-card/settings/pages
   - Source 选择 **GitHub Actions**
   - 等待自动部署完成

2. **访问前端页面**
   - 地址：`https://Xdluomingxian.github.io/xinling-card/`

3. **配置 API 地址**
   - 点击右上角齿轮图标 ⚙️
   - 输入后端 API 地址
   - 刷新页面

### 优点
- ✅ 完全免费
- ✅ 自动部署
- ✅ 无需服务器

### 缺点
- ❌ 需要单独部署后端 API

---

## 方式 2：本地运行（开发测试）

### 启动后端

```bash
cd /home/ubuntu/projects/xinling-card
source venv/bin/activate
cd src
python main.py
```

### 打开前端

在浏览器中打开：`frontend/index.html`

或直接访问：http://localhost:8000/docs

---

## 方式 3：云服务器部署（生产环境）

### 1. 购买服务器

推荐配置：
- CPU: 1 核
- 内存：1GB
- 带宽：1Mbps
- 价格：约 ¥50-100/月

### 2. 部署后端

```bash
# 克隆项目
git clone https://github.com/Xdluomingxian/xinling-card.git
cd xinling-card

# 安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 启动服务
cd src
python main.py
```

### 3. 配置域名（可选）

- 购买域名（约 ¥60/年）
- 解析到服务器 IP
- 配置 Nginx 反向代理
- 申请 SSL 证书（Let's Encrypt 免费）

---

## 📊 部署状态检查

### GitHub Actions 状态

查看自动部署状态：
https://github.com/Xdluomingxian/xinling-card/actions

### API 健康检查

```bash
curl http://localhost:8000/health
```

---

## 🆘 常见问题

### Q: GitHub Pages 在哪里配置？

A: https://github.com/Xdluomingxian/xinling-card/settings/pages

### Q: 如何修改 API 地址？

A: 点击前端页面右上角的齿轮图标 ⚙️

### Q: 前端页面打不开？

A: 
1. 检查 GitHub Actions 是否部署成功
2. 清除浏览器缓存
3. 尝试无痕模式访问

### Q: API 连接失败？

A:
1. 确认后端服务正在运行
2. 检查防火墙设置
3. 确认 API 地址配置正确

---

## 📞 需要帮助？

- **GitHub Issues**: https://github.com/Xdluomingxian/xinling-card/issues
- **API 文档**: http://localhost:8000/docs
- **完整文档**: docs/ 目录

---

*最后更新：2026-03-17*
