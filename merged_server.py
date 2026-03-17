"""
心灵卡片 - 合并启动脚本（前端+API）

使用 FastAPI 同时提供前端页面和 API 服务
端口：8080
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import random
import json

# 导入项目模块
from analyzer.emotion import EmotionAnalyzer
from matcher.content import ContentMatcher

# 加载语录库
QUOTES_FILE = ROOT_DIR / "data" / "mao_quotes.json"
with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
    QUOTES_DATA = json.load(f)

# 前端目录
FRONTEND_DIR = ROOT_DIR / "frontend"

# 初始化
app = FastAPI(title="心灵卡片", version="1.0.0")
analyzer = EmotionAnalyzer()
matcher = ContentMatcher(QUOTES_DATA)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载前端静态文件
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ==================== 数据模型 ====================

class CardRequest(BaseModel):
    user_input: str = Field(..., description="用户输入的心理状态描述")
    quote_source: Optional[str] = Field(default="mao", description="语录来源")
    emotion_override: Optional[str] = Field(default=None, description="手动指定情绪类型")


class QuoteCard(BaseModel):
    quote_text: str
    quote_source: str
    emotion_type: str
    tags: List[str]
    interpretation: str
    action: str
    generated_at: str


class EmotionAnalysis(BaseModel):
    emotion: str
    confidence: float
    keywords: List[str]
    description: str


class CardResponse(BaseModel):
    success: bool
    emotion: EmotionAnalysis
    card: QuoteCard
    message: str = ""


# ==================== API 路由 ====================

@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "quotes_loaded": len(QUOTES_DATA["quotes"])
    }


@app.post("/api/card", response_model=CardResponse)
async def generate_card(request: CardRequest):
    """生成心灵卡片"""
    try:
        # 1. 分析情绪
        emotion_result = analyzer.analyze(request.user_input)
        
        # 2. 如果有手动覆盖，使用手动指定的情绪
        if request.emotion_override:
            emotion_result["emotion"] = request.emotion_override
        
        # 3. 匹配内容
        quote = matcher.match(
            emotion=emotion_result["emotion"],
            source=request.quote_source
        )
        
        if not quote:
            quote = random.choice(QUOTES_DATA["quotes"])
        
        # 4. 生成卡片
        card = QuoteCard(
            quote_text=quote["text"],
            quote_source=quote["source"],
            emotion_type=quote["emotion"],
            tags=quote["tags"],
            interpretation=quote["interpretation"],
            action=quote["action"],
            generated_at=datetime.now().isoformat()
        )
        
        return CardResponse(
            success=True,
            emotion=EmotionAnalysis(**emotion_result),
            card=card,
            message="希望这张卡片能给你带来力量 🌟"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze", response_model=EmotionAnalysis)
async def analyze_emotion(user_input: str):
    """分析情绪"""
    result = analyzer.analyze(user_input)
    return EmotionAnalysis(**result)


@app.get("/api/quotes")
async def list_quotes(emotion: Optional[str] = None, limit: int = 20):
    """获取语录列表"""
    quotes = QUOTES_DATA["quotes"]
    if emotion:
        quotes = [q for q in quotes if q["emotion"] == emotion]
    return {"total": len(quotes[:limit]), "quotes": quotes[:limit]}


@app.get("/api/emotions")
async def list_emotions():
    """获取情绪类型"""
    return {
        "emotions": [
            {"type": "低谷鼓励", "description": "当你感到失落、沮丧、迷茫时，给你力量和希望"},
            {"type": "得意提醒", "description": "当你取得成功、顺风顺水时，提醒你保持谦逊"},
            {"type": "迷茫指引", "description": "当你迷失方向、不知如何选择时，给你指引"}
        ]
    }


# ==================== 主程序 ====================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("💡 心灵卡片 - 启动中...")
    print("="*60)
    print(f"📍 服务地址：http://0.0.0.0:8080")
    print(f"📁 前端目录：{FRONTEND_DIR}")
    print(f"📊 语录数量：{len(QUOTES_DATA['quotes'])} 条")
    print("="*60 + "\n")
    
    uvicorn.run(
        "merged_server:app",
        host="0.0.0.0",
        port=8080,
        reload=False
    )
