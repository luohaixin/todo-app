import json
from typing import List, Dict
from openai import OpenAI
from config import config


class AIFilter:
    """
    AI 过滤器类 - 使用 AI 模型筛选符合条件的技术文章
    
    ========================================
    如何修改过滤条件：
    ========================================
    
    1. 修改 FILTER_TOPIC 变量 - 设置你要过滤的主题名称
    2. 修改 FILTER_KEYWORDS 变量 - 设置相关的关键词列表
    3. 修改 SYSTEM_PROMPT 变量 - 设置 AI 的角色描述
    
    示例：
    - 过滤 AI 相关：FILTER_TOPIC = "人工智能/AI"
    - 过滤后端相关：FILTER_TOPIC = "后端开发"
    - 过滤安全相关：FILTER_TOPIC = "网络安全"
    """
    
    # ============================================
    # 【修改这里】设置你要过滤的主题
    # ============================================
    FILTER_TOPIC = "Web 前端开发"
    
    # ============================================
    # 【修改这里】设置相关的关键词和主题描述
    # AI 会根据这些关键词来判断文章是否相关
    # ============================================
    FILTER_KEYWORDS = """
前端相关主题包括但不限于：
- JavaScript/TypeScript
- React/Vue/Angular/Svelte 等前端框架
- CSS/HTML
- Web 性能优化
- 浏览器技术
- Web APIs
- 前端工具链（构建工具、打包工具等）
- Web 动画
- 响应式设计
- Web 可访问性
- 前端架构
"""
    
    # ============================================
    # 【修改这里】设置 AI 的角色描述
    # ============================================
    SYSTEM_PROMPT = "你是一个技术内容筛选专家，擅长识别前端开发相关的技术文章。"
    
    def __init__(self):
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL
        )
    
    def filter_web_frontend_stories(self, stories: List[Dict]) -> List[Dict]:
        """
        过滤出符合条件的故事
        
        Args:
            stories: 故事列表
            
        Returns:
            过滤后的故事列表
        """
        if not stories:
            return []
        
        stories_text = "\n".join([
            f"{i+1}. {story['title']}"
            for i, story in enumerate(stories)
        ])
        
        # ============================================
        # AI 提示词模板 - 自动使用上面的配置
        # ============================================
        prompt = f"""你是一个技术内容筛选专家。请从以下 Hacker News 文章标题中，筛选出与 {self.FILTER_TOPIC} 相关的文章。

{self.FILTER_KEYWORDS}

文章标题列表：
{stories_text}

请返回一个 JSON 数组，包含所有相关文章的序号（从1开始）。格式如下：
{{"indices": [1, 3, 5]}}

只返回 JSON，不要其他内容。"""

        try:
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            result = json.loads(content)
            indices = result.get("indices", [])
            
            filtered_stories = [stories[i-1] for i in indices if 0 < i <= len(stories)]
            return filtered_stories
            
        except Exception as e:
            print(f"AI filtering error: {e}")
            return []


if __name__ == "__main__":
    from hn_fetcher import HNFetcher
    
    fetcher = HNFetcher()
    stories = fetcher.fetch_top_stories()
    
    ai_filter = AIFilter()
    filtered = ai_filter.filter_web_frontend_stories(stories)
    
    print(f"Total stories: {len(stories)}")
    print(f"Filtered stories: {len(filtered)}")
    for story in filtered:
        print(f"- {story['title']}")
