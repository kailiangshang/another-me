"""
数据分析模块
负责：情绪分析、关键词提取、关系分析
"""

from typing import List, Dict
from collections import Counter
import re


class DataAnalyzer:
    """数据分析器 - 独立的技术模块"""
    
    def __init__(self):
        # 简单的情绪词典（实际项目可使用更复杂的模型）
        self.positive_words = {'开心', '快乐', '高兴', '喜欢', '爱', '好', '棒', '赞', '哈哈'}
        self.negative_words = {'难过', '伤心', '痛苦', '讨厌', '恨', '差', '烂', '糟', '唉'}
    
    async def analyze_emotions(self, documents: List[Dict]) -> Dict:
        """
        输入：文档列表
        输出：情绪分析结果
        """
        if not documents:
            return {"overall": "neutral", "distribution": {}, "trend": []}
        
        emotions = []
        distribution = {"positive": 0, "negative": 0, "neutral": 0}
        
        for doc in documents:
            content = doc.get("content", "")
            emotion = self._analyze_single_text(content)
            emotions.append(emotion)
            distribution[emotion] += 1
        
        # 计算整体情绪
        if distribution["positive"] > distribution["negative"]:
            overall = "positive"
        elif distribution["negative"] > distribution["positive"]:
            overall = "negative"
        else:
            overall = "neutral"
        
        return {
            "overall": overall,
            "distribution": distribution,
            "trend": emotions,
            "insights": self._generate_emotion_insights(distribution, len(documents))
        }
    
    async def extract_keywords(self, documents: List[Dict], top_k: int = 50) -> List[Dict]:
        """
        输入：文档列表、返回数量
        输出：关键词列表 [{"word": "...", "weight": 0.9}, ...]
        """
        # 提取所有词
        all_words = []
        for doc in documents:
            content = doc.get("content", "")
            words = self._tokenize(content)
            all_words.extend(words)
        
        # 统计词频
        word_counts = Counter(all_words)
        
        # 过滤停用词和短词
        filtered = {
            word: count for word, count in word_counts.items()
            if len(word) >= 2 and not self._is_stopword(word)
        }
        
        # 归一化权重
        max_count = max(filtered.values()) if filtered else 1
        keywords = [
            {"word": word, "weight": count / max_count}
            for word, count in sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:top_k]
        ]
        
        return keywords
    
    async def extract_topics(self, documents: List[Dict]) -> List[str]:
        """
        输入：文档列表
        输出：主题列表
        """
        keywords = await self.extract_keywords(documents, top_k=10)
        return [kw["word"] for kw in keywords]
    
    async def extract_phrases(self, documents: List[Dict]) -> List[Dict]:
        """
        输入：文档列表
        输出：常用短语
        """
        # 简单实现：提取2-3字的高频词组
        phrases = []
        for doc in documents:
            content = doc.get("content", "")
            # 提取2-3字词组
            for i in range(len(content) - 1):
                phrase = content[i:i+2]
                if len(phrase) == 2 and phrase.strip():
                    phrases.append(phrase)
        
        phrase_counts = Counter(phrases)
        return [
            {"phrase": phrase, "count": count}
            for phrase, count in phrase_counts.most_common(20)
        ]
    
    async def analyze_relationships(self, documents: List[Dict]) -> Dict:
        """
        输入：文档列表
        输出：人际关系分析
        """
        # 提取人名（简单的启发式规则）
        people = []
        for doc in documents:
            content = doc.get("content", "")
            # 查找常见称呼模式
            names = re.findall(r'(?:@|和|跟|与)([\\u4e00-\\u9fff]{2,4})(?:说|聊|一起)', content)
            people.extend(names)
        
        people_counts = Counter(people)
        
        return {
            "people": [
                {"name": name, "frequency": count, "sentiment": 0.5}
                for name, count in people_counts.most_common(10)
            ],
            "network": {},
            "insights": [f"经常提到的人：{', '.join([p[0] for p in people_counts.most_common(3)])}"]
        }
    
    def _analyze_single_text(self, text: str) -> str:
        """分析单个文本的情绪"""
        positive_count = sum(1 for word in self.positive_words if word in text)
        negative_count = sum(1 for word in self.negative_words if word in text)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _tokenize(self, text: str) -> List[str]:
        """简单分词（中文按字符，英文按空格）"""
        # 提取中文词（2-4字）
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        # 提取英文词
        english_words = re.findall(r'[a-zA-Z]{3,}', text.lower())
        return chinese_words + english_words
    
    def _is_stopword(self, word: str) -> bool:
        """判断是否为停用词"""
        stopwords = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', 'the', 'a', 'an', 'and', 'or', 'but'}
        return word in stopwords
    
    def _generate_emotion_insights(self, distribution: Dict, total: int) -> List[str]:
        """生成情绪洞察"""
        insights = []
        
        positive_ratio = distribution["positive"] / total if total > 0 else 0
        negative_ratio = distribution["negative"] / total if total > 0 else 0
        
        if positive_ratio > 0.6:
            insights.append("整体情绪较为积极")
        elif negative_ratio > 0.4:
            insights.append("存在较多负面情绪，需要关注")
        
        return insights
