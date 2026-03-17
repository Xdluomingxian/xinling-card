# API 使用指南

## 基础信息

**Base URL**: `http://localhost:8000`

**API 文档**: `http://localhost:8000/docs` (Swagger UI)

---

## 接口列表

### 1. 生成心灵卡片

**POST** `/card`

根据用户输入的情绪状态，生成专属心灵卡片。

#### 请求参数

```json
{
  "user_input": "string (必填) - 用户输入的心理状态描述",
  "quote_source": "string (可选) - 语录来源：mao=毛选，all=全部，默认 mao",
  "emotion_override": "string (可选) - 手动指定情绪类型"
}
```

#### 情绪类型

- `低谷鼓励` - 当你感到失落、沮丧、迷茫时
- `得意提醒` - 当你取得成功、顺风顺水时
- `迷茫指引` - 当你迷失方向、不知如何选择时

#### 请求示例

```bash
curl -X POST http://localhost:8000/card \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "最近工作压力很大，感觉很累，想要放弃",
    "quote_source": "mao",
    "emotion_override": null
  }'
```

#### 响应示例

```json
{
  "success": true,
  "emotion": {
    "emotion": "低谷鼓励",
    "confidence": 0.67,
    "keywords": ["累", "放弃", "压力"],
    "description": "你正在经历一段艰难的时光..."
  },
  "card": {
    "quote_text": "决定战争胜负的是人，而不是物。",
    "quote_source": "《论持久战》",
    "emotion_type": "低谷鼓励",
    "tags": ["人", "信念", "本质"],
    "interpretation": "最终决定成败的是人的意志和能力...",
    "action": "专注提升自己的能力，而不是抱怨条件不足。",
    "generated_at": "2026-03-17T21:36:18"
  },
  "message": "希望这张卡片能给你带来力量 🌟"
}
```

---

### 2. 情绪分析

**POST** `/analyze`

仅分析用户情绪，不生成卡片。

#### 请求参数

```json
{
  "user_input": "string (必填) - 用户输入的心理状态描述"
}
```

#### 请求示例

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "今天项目成功了，团队都很兴奋"
  }'
```

#### 响应示例

```json
{
  "emotion": "得意提醒",
  "confidence": 0.85,
  "keywords": ["成功", "兴奋"],
  "description": "恭喜你取得了成功！这是你努力的结果..."
}
```

---

### 3. 获取语录列表

**GET** `/quotes`

获取语录库中的语录列表。

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `emotion` | string | 否 | 情绪类型过滤 |
| `source` | string | 否 | 来源过滤 |
| `limit` | int | 否 | 返回数量限制，默认 20 |

#### 请求示例

```bash
# 获取所有语录
curl http://localhost:8000/quotes

# 获取低谷鼓励类型的语录
curl "http://localhost:8000/quotes?emotion=低谷鼓励"

# 获取毛选语录，限制 10 条
curl "http://localhost:8000/quotes?source=毛选&limit=10"
```

#### 响应示例

```json
{
  "total": 20,
  "quotes": [
    {
      "id": 1,
      "text": "星星之火，可以燎原。",
      "source": "《星星之火，可以燎原》",
      "emotion": "低谷鼓励",
      "tags": ["希望", "坚持", "信念"],
      "interpretation": "即使现在力量微小...",
      "action": "相信自己的选择..."
    }
  ]
}
```

---

### 4. 获取情绪类型

**GET** `/emotions`

获取系统支持的情绪类型列表。

#### 请求示例

```bash
curl http://localhost:8000/emotions
```

#### 响应示例

```json
{
  "emotions": [
    {
      "type": "低谷鼓励",
      "description": "当你感到失落、沮丧、迷茫时，给你力量和希望"
    },
    {
      "type": "得意提醒",
      "description": "当你取得成功、顺风顺水时，提醒你保持谦逊"
    },
    {
      "type": "迷茫指引",
      "description": "当你迷失方向、不知如何选择时，给你指引"
    }
  ]
}
```

---

### 5. 健康检查

**GET** `/health`

检查服务健康状态。

#### 请求示例

```bash
curl http://localhost:8000/health
```

#### 响应示例

```json
{
  "status": "healthy",
  "timestamp": "2026-03-17T21:36:18",
  "quotes_loaded": 20
}
```

---

### 6. 根路径

**GET** `/`

获取系统信息。

#### 请求示例

```bash
curl http://localhost:8000/
```

#### 响应示例

```json
{
  "name": "心灵卡片",
  "version": "1.0.0",
  "status": "running",
  "description": "用经典著作的智慧，为你提供情绪价值和人生指引",
  "quote_count": 20,
  "sources": ["毛泽东选集"]
}
```

---

## 错误处理

### 错误响应格式

```json
{
  "detail": "错误信息描述"
}
```

### 常见错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 使用示例（Python）

### 生成卡片

```python
import requests

# API 地址
API_BASE = "http://localhost:8000"

# 生成卡片
response = requests.post(
    f"{API_BASE}/card",
    json={
        "user_input": "最近工作压力很大，感觉很累",
        "quote_source": "mao"
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"情绪：{data['emotion']['emotion']}")
    print(f"名言：{data['card']['quote_text']}")
    print(f"解读：{data['card']['interpretation']}")
    print(f"建议：{data['card']['action']}")
else:
    print(f"错误：{response.json()}")
```

### 情绪分析

```python
import requests

response = requests.post(
    f"{API_BASE}/analyze",
    json={
        "user_input": "今天升职了，很开心"
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"情绪：{data['emotion']}")
    print(f"置信度：{data['confidence']}")
    print(f"关键词：{data['keywords']}")
```

---

## 使用示例（JavaScript）

### 生成卡片

```javascript
const API_BASE = 'http://localhost:8000';

async function generateCard(userInput) {
  try {
    const response = await fetch(`${API_BASE}/card`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_input: userInput,
        quote_source: 'mao'
      })
    });

    if (!response.ok) {
      throw new Error('生成失败');
    }

    const data = await response.json();
    console.log('情绪:', data.emotion.emotion);
    console.log('名言:', data.card.quote_text);
    console.log('解读:', data.card.interpretation);
    console.log('建议:', data.card.action);
    
    return data;
  } catch (error) {
    console.error('错误:', error);
  }
}

// 调用
generateCard('最近感觉很迷茫，不知道该怎么办');
```

---

## 限流说明

当前版本**无限流**，生产环境建议添加限流：

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/card")
@limiter.limit("10/minute")
async def generate_card(request: CardRequest):
    ...
```

---

## 最佳实践

1. **错误处理**: 始终检查响应状态码
2. **超时设置**: 建议设置 10 秒超时
3. **重试机制**: 网络错误时重试 2-3 次
4. **缓存**: 相同输入可缓存结果
5. **日志**: 记录请求和响应便于排查

---

*最后更新：2026-03-17*
