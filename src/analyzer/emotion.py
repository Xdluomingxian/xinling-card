"""
心灵卡片 - 情绪分析模块

分析用户输入的情绪状态，判断属于哪种类型
"""
import re
from typing import Dict, List, Any


class EmotionAnalyzer:
    """情绪分析器"""
    
    # 情绪关键词库
    EMOTION_KEYWORDS = {
        "低谷鼓励": [
            # 负面情绪词
            "难过", "伤心", "沮丧", "失落", "绝望", "痛苦", "悲伤", "痛苦",
            "焦虑", "迷茫", "困惑", "无助", "疲惫", "累", "压力大",
            "失败", "挫折", "打击", "失望", "委屈", "孤独", "寂寞",
            "失业", "失恋", "离婚", "破产", "负债", "生病", "住院",
            "放弃", "想放弃", "撑不住", "受不了", "太难了", "没办法",
            # 低能量表达
            "不想", "不想动", "不想说话", "没意思", "没意义", "好累",
            "为什么", "凭什么", "不公平", "倒霉", "运气不好"
        ],
        "得意提醒": [
            # 正面情绪词
            "开心", "高兴", "兴奋", "激动", "自豪", "骄傲", "得意",
            "成功", "胜利", "达成", "实现", "完成", "突破", "进步",
            "升职", "加薪", "获奖", "表扬", "认可", "赞赏",
            "顺利", "好运", "幸运", "幸福", "满足", "满意",
            # 高能量表达
            "太棒了", "太好了", "终于", "做到了", "成功了", "厉害",
            "牛逼", "牛", "强", "完美", "优秀", "出色"
        ],
        "迷茫指引": [
            # 不确定性词
            "不知道", "不清楚", "不确定", "犹豫", "纠结", "选择",
            "怎么办", "如何做", "怎么", "哪个", "哪里", "何时",
            "方向", "目标", "规划", "计划", "未来", "前途",
            "想", "思考", "考虑", "权衡", "比较", "分析",
            "改变", "转行", "跳槽", "创业", "学习", "提升"
        ]
    }
    
    # 情绪描述
    EMOTION_DESCRIPTIONS = {
        "低谷鼓励": "你正在经历一段艰难的时光，这很正常。请记住，挫折是成长的必经之路。",
        "得意提醒": "恭喜你取得了成功！这是你努力的结果。同时，保持谦逊会让你走得更远。",
        "迷茫指引": "你正在思考人生的方向，这是成长的开始。迷茫说明你在寻求突破。"
    }
    
    def analyze(self, user_input: str) -> Dict[str, Any]:
        """
        分析用户情绪
        
        Args:
            user_input: 用户输入文本
        
        Returns:
            情绪分析结果字典
        """
        # 转为小写
        text = user_input.lower()
        
        # 统计各情绪类型的匹配度
        emotion_scores = {}
        matched_keywords = {}
        
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            score = 0
            matches = []
            
            for keyword in keywords:
                if keyword in text:
                    score += 1
                    matches.append(keyword)
            
            emotion_scores[emotion] = score
            matched_keywords[emotion] = matches
        
        # 确定主要情绪
        if max(emotion_scores.values()) == 0:
            # 没有匹配到关键词，默认返回迷茫指引
            main_emotion = "迷茫指引"
            confidence = 0.5
        else:
            main_emotion = max(emotion_scores, key=emotion_scores.get)
            total_matches = sum(emotion_scores.values())
            confidence = emotion_scores[main_emotion] / total_matches if total_matches > 0 else 0.5
        
        # 构建结果
        result = {
            "emotion": main_emotion,
            "confidence": round(confidence, 2),
            "keywords": matched_keywords[main_emotion],
            "description": self.EMOTION_DESCRIPTIONS[main_emotion],
            "all_scores": emotion_scores,
            "all_keywords": matched_keywords
        }
        
        return result
    
    def get_emotion_list(self) -> List[Dict[str, str]]:
        """获取支持的情绪类型列表"""
        return [
            {"type": emotion, "description": desc}
            for emotion, desc in self.EMOTION_DESCRIPTIONS.items()
        ]


# 使用示例
if __name__ == "__main__":
    analyzer = EmotionAnalyzer()
    
    test_cases = [
        "我最近失业了，感觉很迷茫，不知道该怎么办",
        "我今天升职了，太开心了！",
        "我在考虑要不要转行，很纠结",
        "最近压力好大，好想放弃",
        "项目终于成功了，团队都很兴奋"
    ]
    
    print("=== 情绪分析测试 ===\n")
    for text in test_cases:
        result = analyzer.analyze(text)
        print(f"输入：{text}")
        print(f"情绪：{result['emotion']}")
        print(f"置信度：{result['confidence']}")
        print(f"关键词：{result['keywords']}")
        print(f"描述：{result['description']}")
        print("-" * 50)
