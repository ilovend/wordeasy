"""
智能单词难度分类工具
根据单词长度、常见度、词缀等特征自动判断难度等级
优化：添加缓存、改进规则优先级
"""
from functools import lru_cache

@lru_cache(maxsize=1000)
def classify_word_difficulty(word: str) -> int:
    """
    根据单词特征自动分类难度（使用LRU缓存提升性能）
    返回: 1=初级, 2=中级, 3=高级
    
    分类规则优先级：
    1. 高频基础词表 → 难度1
    2. 复杂词缀/词根 → 难度3
    3. 单词长度 → 分级判断
    """
    word_lower = word.lower().strip()
    word_len = len(word_lower)
    
    # 超高频简单词（难度1）
    basic_words = {
        'a', 'an', 'the', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'can', 'will', 'would',
        'good', 'bad', 'big', 'small', 'hot', 'cold', 'new', 'old',
        'cat', 'dog', 'bird', 'fish', 'one', 'two', 'red', 'blue',
        'eat', 'go', 'see', 'get', 'make', 'take', 'know', 'come',
        'yes', 'no', 'ok', 'hello', 'hi', 'bye', 'please', 'sorry',
        'thank', 'thanks', 'love', 'like', 'want', 'need', 'help',
        'day', 'time', 'year', 'home', 'work', 'name', 'man', 'woman',
        'boy', 'girl', 'water', 'food', 'book', 'house', 'car', 'phone',
        'happy', 'sad', 'nice', 'fine', 'well', 'very', 'much', 'many',
        'some', 'any', 'all', 'not', 'but', 'and', 'or', 'with', 'from'
    }
    
    # 高级词汇特征词根/词缀
    advanced_features = [
        'tion', 'sion', 'ment', 'ness', 'ance', 'ence',  # 抽象名词后缀
        'ology', 'graphy', 'metry',  # 学科后缀
        'able', 'ible', 'ive', 'ous', 'ful', 'less',  # 形容词后缀
        'ate', 'ify', 'ize',  # 动词后缀
        'pre', 'post', 'anti', 'pro', 'contra',  # 高级前缀
        'hyper', 'hypo', 'meta', 'pseudo',  # 希腊词根
        'circum', 'trans', 'inter', 'intra'  # 拉丁词根
    ]
    
    # 规则1: 超高频基础词 → 难度1
    if word_lower in basic_words:
        return 1
    
    # 规则2: 3-5字母且无复杂词缀 → 难度1
    if word_len <= 5 and not any(feat in word_lower for feat in advanced_features):
        return 1
    
    # 规则3: 包含高级词缀或词根 → 难度3
    if any(feat in word_lower for feat in advanced_features):
        return 3
    
    # 规则4: 10字母以上 → 难度3
    if word_len >= 10:
        return 3
    
    # 规则5: 6-9字母 → 难度2（中级）
    if 6 <= word_len <= 9:
        return 2
    
    # 默认中级
    return 2


def batch_classify_words(words: list) -> dict:
    """
    批量分类单词
    返回: {1: [...], 2: [...], 3: [...]}
    """
    result = {1: [], 2: [], 3: []}
    
    for word in words:
        difficulty = classify_word_difficulty(word)
        result[difficulty].append(word)
    
    return result
