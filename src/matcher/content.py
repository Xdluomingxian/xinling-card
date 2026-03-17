"""
心灵卡片 - 内容匹配模块

根据用户情绪，从语录库中匹配最合适的内容
"""
import random
from typing import Dict, List, Any, Optional


class ContentMatcher:
    """内容匹配器"""
    
    def __init__(self, quotes_data: Dict[str, Any]):
        """
        初始化匹配器
        
        Args:
            quotes_data: 语录数据字典
        """
        self.quotes_data = quotes_data
        self.quotes = quotes_data.get("quotes", [])
        
        # 按情绪类型分组
        self.quotes_by_emotion = {}
        for quote in self.quotes:
            emotion = quote.get("emotion", "迷茫指引")
            if emotion not in self.quotes_by_emotion:
                self.quotes_by_emotion[emotion] = []
            self.quotes_by_emotion[emotion].append(quote)
    
    def match(self, emotion: str, source: str = "mao") -> Optional[Dict[str, Any]]:
        """
        根据情绪匹配语录
        
        Args:
            emotion: 情绪类型（低谷鼓励/得意提醒/迷茫指引）
            source: 来源（mao/ancient/all）
        
        Returns:
            匹配的语录，如果没有则返回 None
        """
        # 获取该情绪类型的语录
        candidates = self.quotes_by_emotion.get(emotion, [])
        
        if not candidates:
            # 如果该情绪类型没有语录，返回任意一条
            return random.choice(self.quotes) if self.quotes else None
        
        # 随机选择一条（后续可以优化为更智能的匹配）
        return random.choice(candidates)
    
    def match_by_tags(self, tags: List[str], emotion: str = None) -> List[Dict[str, Any]]:
        """
        根据标签匹配语录
        
        Args:
            tags: 标签列表
            emotion: 情绪类型（可选）
        
        Returns:
            匹配的语录列表
        """
        matches = []
        
        for quote in self.quotes:
            # 情绪过滤
            if emotion and quote.get("emotion") != emotion:
                continue
            
            # 标签匹配
            quote_tags = quote.get("tags", [])
            if any(tag in quote_tags for tag in tags):
                matches.append(quote)
        
        return matches
    
    def get_all_emotions(self) -> List[str]:
        """获取所有情绪类型"""
        return list(self.quotes_by_emotion.keys())
    
    def get_quote_count(self) -> int:
        """获取语录总数"""
        return len(self.quotes)
    
    def get_quote_by_id(self, quote_id: int) -> Optional[Dict[str, Any]]:
        """
        根据 ID 获取语录
        
        Args:
            quote_id: 语录 ID
        
        Returns:
            语录字典，如果不存在则返回 None
        """
        for quote in self.quotes:
            if quote.get("id") == quote_id:
                return quote
        return None
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """
        搜索语录
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的语录列表
        """
        matches = []
        
        for quote in self.quotes:
            # 在原文、出处、标签、解读中搜索
            text = (
                quote.get("text", "") +
                quote.get("source", "") +
                " ".join(quote.get("tags", [])) +
                quote.get("interpretation", "")
            )
            
            if keyword.lower() in text.lower():
                matches.append(quote)
        
        return matches


# 使用示例
if __name__ == "__main__":
    # 测试数据
    test_data = {
        "quotes": [
            {
                "id": 1,
                "text": "星星之火，可以燎原。",
                "source": "《星星之火，可以燎原》",
                "emotion": "低谷鼓励",
                "tags": ["希望", "坚持", "信念"],
                "interpretation": "即使现在力量微小，只要方向正确，坚持下去就能成就大事。",
                "action": "相信自己的选择，继续前行，不要因暂时的弱小而气馁。"
            },
            {
                "id": 2,
                "text": "虚心使人进步，骄傲使人落后。",
                "source": "《中国共产党第八次全国代表大会开幕词》",
                "emotion": "得意提醒",
                "tags": ["谦虚", "警醒", "成长"],
                "interpretation": "成功时保持谦逊，才能持续进步；骄傲自满会导致退步。",
                "action": "回顾来时的路，感恩帮助过你的人，继续保持学习的姿态。"
            }
        ]
    }
    
    matcher = ContentMatcher(test_data)
    
    print("=== 内容匹配测试 ===\n")
    
    # 测试情绪匹配
    print("低谷鼓励匹配:")
    result = matcher.match("低谷鼓励")
    print(f"  {result['text']} - {result['source']}")
    
    print("\n得意提醒匹配:")
    result = matcher.match("得意提醒")
    print(f"  {result['text']} - {result['source']}")
    
    # 测试标签匹配
    print("\n标签匹配（希望）:")
    results = matcher.match_by_tags(["希望"])
    for r in results:
        print(f"  {r['text']}")
    
    # 测试搜索
    print("\n搜索（进步）:")
    results = matcher.search("进步")
    for r in results:
        print(f"  {r['text']}")
