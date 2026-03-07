import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Config:
    HN_TOP_STORIES_URL: str = "https://hacker-news.firebaseio.com/v0/topstories.json"
    HN_ITEM_URL: str = "https://hacker-news.firebaseio.com/v0/item/{}.json"
    HN_TOP_COUNT: int = 30
    
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
    EMAIL_TO: str = os.getenv("EMAIL_TO", "")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    SCHEDULE_TIME: str = os.getenv("SCHEDULE_TIME", "09:00")


config = Config()
