# 🌐 心灵卡片 - 本地部署信息

## ✅ 服务状态

| 服务 | 状态 | 端口 | 访问地址 |
|------|------|------|---------|
| **前端页面** | ✅ 运行中 | 8080 | http://10.3.0.14:8080 |
| **后端 API** | ✅ 运行中 | 8000 | http://10.3.0.14:8000 |
| **API 文档** | ✅ 运行中 | 8000 | http://10.3.0.14:8000/docs |

---

## 🔗 快速访问

### 前端页面（推荐）
```
http://10.3.0.14:8080
```

### 后端 API 文档
```
http://10.3.0.14:8000/docs
```

### 健康检查
```
http://10.3.0.14:8000/health
```

---

## ⚙️ API 配置

前端页面已自动配置 API 地址为：`http://10.3.0.14:8000`

如果需要修改：
1. 打开前端页面
2. 点击右上角齿轮图标 ⚙️
3. 输入新的 API 地址
4. 刷新页面

---

## 🛠️ 服务管理

### 查看服务状态

```bash
# 前端服务
ps aux | grep "http.server 8080"

# 后端服务
ps aux | grep "python main.py"
```

### 重启服务

```bash
# 停止前端
pkill -f "http.server 8080"

# 启动前端
cd /home/ubuntu/projects/xinling-card/frontend
python3 -m http.server 8080 &

# 停止后端
pkill -f "python main.py"

# 启动后端
cd /home/ubuntu/projects/xinling-card/src
source ../venv/bin/activate
python main.py &
```

### 查看日志

```bash
# 前端日志
tail -f /tmp/xinling-frontend.log

# 后端日志
# 在启动终端中查看
```

---

## 🔒 防火墙设置（如需外网访问）

```bash
# 开放端口
sudo ufw allow 8080/tcp
sudo ufw allow 8000/tcp

# 查看状态
sudo ufw status
```

---

## 📊 测试验证

### 测试前端
```bash
curl http://10.3.0.14:8080
```

### 测试后端
```bash
curl http://10.3.0.14:8000/health
```

### 测试完整流程
```bash
curl -X POST http://10.3.0.14:8000/card \
  -H "Content-Type: application/json" \
  -d '{"user_input": "测试", "quote_source": "mao"}'
```

---

## 📱 移动端访问

在手机上访问：
```
http://10.3.0.14:8080
```

确保手机和服务器在同一网络。

---

## ⚠️ 注意事项

1. **内网访问** - 当前仅支持内网访问（10.3.0.14）
2. **HTTPS** - 生产环境建议配置 HTTPS
3. **域名** - 生产环境建议绑定域名
4. **监控** - 建议添加服务监控和自动重启

---

## 🆘 故障排查

### 前端无法访问
```bash
# 检查服务是否运行
ps aux | grep "http.server 8080"

# 检查端口是否监听
netstat -tlnp | grep 8080

# 重启服务
pkill -f "http.server 8080"
cd /home/ubuntu/projects/xinling-card/frontend
python3 -m http.server 8080 &
```

### 后端无法访问
```bash
# 检查服务是否运行
ps aux | grep "python main.py"

# 检查端口是否监听
netstat -tlnp | grep 8000

# 查看后端日志
# 在启动终端中查看
```

### API 连接失败
1. 确认后端服务正在运行
2. 检查防火墙设置
3. 在前端页面点击齿轮图标重新配置 API 地址

---

*部署时间：2026-03-17 22:21*  
*服务器 IP: 10.3.0.14*  
*状态：✅ 运行中*
