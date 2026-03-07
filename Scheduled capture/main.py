"""
Hacker News 前端精选 - 主程序

========================================
定时任务设置说明：
========================================

1. 定时时间配置在 .env 文件中：
   SCHEDULE_TIME=09:00   # 设置每天执行的时间（24小时制）

2. 要启用定时任务，将下方 ENABLE_SCHEDULER 改为 True
   要禁用定时任务，将下方 ENABLE_SCHEDULER 改为 False

3. 运行方式：
   - python main.py --now    立即执行一次（无论定时是否启用）
   - python main.py          根据定时设置运行

========================================
"""

import schedule
import time
from datetime import datetime
from hn_fetcher import HNFetcher
from ai_filter import AIFilter
from email_sender import EmailSender
from config import config


# ============================================
# 【定时开关】设置是否启用定时任务
# True  = 启用定时任务（每天定时执行）
# False = 禁用定时任务（只能手动执行）
# ============================================
ENABLE_SCHEDULER = False


def job():
    print(f"\n{'='*50}")
    print(f"Starting job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    fetcher = HNFetcher()
    ai_filter = AIFilter()
    email_sender = EmailSender()
    
    print("Fetching top stories from Hacker News...")
    stories = fetcher.fetch_top_stories()
    print(f"Fetched {len(stories)} stories")
    
    print("Filtering web frontend stories with AI...")
    filtered_stories = ai_filter.filter_web_frontend_stories(stories)
    print(f"Found {len(filtered_stories)} frontend-related stories")
    
    if filtered_stories:
        print("\nFiltered stories:")
        for i, story in enumerate(filtered_stories, 1):
            print(f"  {i}. {story['title']}")
    
    print("\nSending email...")
    success = email_sender.send_email(filtered_stories)
    
    if success:
        print("Job completed successfully!")
    else:
        print("Job completed with errors")
    
    print(f"{'='*50}\n")


def run_scheduler():
    """
    启动定时任务调度器
    
    ============================================
    【定时设置】定时执行时间在 .env 文件中配置：
    SCHEDULE_TIME=09:00
    
    也可以直接修改下方代码中的时间：
    schedule.every().day.at("09:00").do(job)
    ============================================
    """
    print(f"Scheduler started. Will run daily at {config.SCHEDULE_TIME}")
    print("Press Ctrl+C to stop.")
    
    schedule.every().day.at(config.SCHEDULE_TIME).do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)


def run_once():
    """立即执行一次任务"""
    job()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--now":
        run_once()
    elif ENABLE_SCHEDULER:
        run_scheduler()
    else:
        print("定时任务已禁用。使用 'python main.py --now' 立即执行一次。")
        print("如需启用定时任务，请修改 main.py 中的 ENABLE_SCHEDULER = True")
