import requests
from typing import List, Dict
from config import config


class HNFetcher:
    def __init__(self):
        self.session = requests.Session()
    
    def get_top_story_ids(self) -> List[int]:
        response = self.session.get(config.HN_TOP_STORIES_URL)
        response.raise_for_status()
        return response.json()[:config.HN_TOP_COUNT]
    
    def get_story_detail(self, story_id: int) -> Dict:
        url = config.HN_ITEM_URL.format(story_id)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def fetch_top_stories(self) -> List[Dict]:
        story_ids = self.get_top_story_ids()
        stories = []
        
        for story_id in story_ids:
            story = self.get_story_detail(story_id)
            if story and story.get("url"):
                stories.append({
                    "id": story.get("id"),
                    "title": story.get("title", ""),
                    "url": story.get("url", ""),
                    "score": story.get("score", 0),
                    "by": story.get("by", ""),
                    "time": story.get("time", 0),
                    "descendants": story.get("descendants", 0)
                })
        
        return stories


if __name__ == "__main__":
    fetcher = HNFetcher()
    stories = fetcher.fetch_top_stories()
    for story in stories[:5]:
        print(f"Title: {story['title']}")
        print(f"URL: {story['url']}")
        print(f"Score: {story['score']}")
        print("-" * 50)
