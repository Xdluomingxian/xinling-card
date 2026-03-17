"""
心灵卡片 - FastAPI 主入口

用经典著作的智慧，为用户提供情绪价值和人生指引
"""
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import random

# 导入项目模块
from analyzer.emotion import EmotionAnalyzer
from matcher.content import ContentMatcher

# 加载语录库
DATA_DIR = Path(__file__).parent.parent / "data"
QUOTES_FILE = DATA_DIR / "mao_quotes.json"

with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
    QUOTES_DATA = json.load(f)


# ==================== 数据模型 ====================

class CardRequest(BaseModel):
    """卡片生成请求"""
    user_input: str = Field(..., description="用户输入的心理状态描述")
    quote_source: Optional[str] = Field(default="mao", description="语录来源：mao=毛选，ancient=古诗词，all=全部")
    emotion_override: Optional[str] = Field(default=None, description="手动指定情绪类型：低谷鼓励/得意提醒/迷茫指引")


class QuoteCard(BaseModel):
    """知识卡片响应"""
    quote_text: str  # 原文
    quote_source: str  # 出处
    emotion_type: str  # 情绪类型
    tags: List[str]  # 标签
    interpretation: str  # AI 解读
    action: str  # 行动建议
    generated_at: str  # 生成时间


class EmotionAnalysis(BaseModel):
    """情绪分析结果"""
    emotion: str  # 情绪类型
    confidence: float  # 置信度
    keywords: List[str]  # 关键词
    description: str  # 情绪描述


class CardResponse(BaseModel):
    """卡片响应"""
    success: bool
    emotion: EmotionAnalysis
    card: QuoteCard
    message: str = ""


# ==================== 应用初始化 ====================

app = FastAPI(
    title="心灵卡片",
    version="1.0.0",
    description="用经典著作的智慧，为用户提供情绪价值和人生指引"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化分析器和匹配器
analyzer = EmotionAnalyzer()
matcher = ContentMatcher(QUOTES_DATA)


# ==================== API 路由 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "心灵卡片",
        "version": "1.0.0",
        "status": "running",
        "description": "用经典著作的智慧，为你提供情绪价值和人生指引",
        "quote_count": len(QUOTES_DATA["quotes"]),
        "sources": ["毛泽东选集"]
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "quotes_loaded": len(QUOTES_DATA["quotes"])
    }


@app.post("/analyze", response_model=EmotionAnalysis)
async def analyze_emotion(user_input: str):
    """
    分析用户情绪
    
    Args:
        user_input: 用户输入的心理状态描述
    
    Returns:
        情绪分析结果
    """
    result = analyzer.analyze(user_input)
    return EmotionAnalysis(**result)


@app.post("/card", response_model=CardResponse)
async def generate_card(request: CardRequest):
    """
    生成心灵卡片
    
    Args:
        request: 卡片生成请求
    
    Returns:
        知识卡片
    """
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
            # 如果没有匹配到，随机返回一条
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
        
        # 5. 生成响应
        response = CardResponse(
            success=True,
            emotion=EmotionAnalysis(**emotion_result),
            card=card,
            message="希望这张卡片能给你带来力量 🌟"
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/quotes")
async def list_quotes(
    emotion: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 20
):
    """
    获取语录列表
    
    Args:
        emotion: 情绪类型过滤
        source: 来源过滤
        limit: 返回数量限制
    
    Returns:
        语录列表
    """
    quotes = QUOTES_DATA["quotes"]
    
    # 过滤
    if emotion:
        quotes = [q for q in quotes if q["emotion"] == emotion]
    
    if source:
        quotes = [q for q in quotes if source.lower() in q["source"].lower()]
    
    # 限制数量
    quotes = quotes[:limit]
    
    return {
        "total": len(quotes),
        "quotes": quotes
    }


@app.get("/emotions")
async def list_emotions():
    """获取支持的情绪类型"""
    return {
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


# ==================== 主程序 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
