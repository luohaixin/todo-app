import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime
from config import config


class EmailSender:
    def __init__(self):
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.username = config.SMTP_USERNAME
        self.password = config.SMTP_PASSWORD
        self.from_email = config.EMAIL_FROM
        self.to_email = config.EMAIL_TO
    
    def format_stories_html(self, stories: List[Dict]) -> str:
        if not stories:
            return "<p>今天没有找到前端相关的文章。</p>"
        
        html = "<ul>"
        for story in stories:
            html += f"""
            <li style="margin-bottom: 15px;">
                <a href="{story['url']}" style="font-size: 16px; color: #1a0dab; text-decoration: none;">
                    {story['title']}
                </a>
                <br>
                <span style="color: #666; font-size: 12px;">
                    👍 {story['score']} points | 
                    by {story['by']} | 
                    💬 {story.get('descendants', 0)} comments
                </span>
            </li>
            """
        html += "</ul>"
        return html
    
    def send_email(self, stories: List[Dict]) -> bool:
        if not self.username or not self.password:
            print("Email credentials not configured")
            return False
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"HN 前端精选 - {datetime.now().strftime('%Y-%m-%d')}"
        msg["From"] = self.from_email or self.username
        msg["To"] = self.to_email
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #ff6600; }}
                ul {{ list-style: none; padding: 0; }}
            </style>
        </head>
        <body>
            <h1>🚀 Hacker News 前端精选</h1>
            <p style="color: #666;">为您精选 {len(stories)} 篇前端相关文章</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            {self.format_stories_html(stories)}
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">
                此邮件由自动程序发送，数据来源于 Hacker News
            </p>
        </body>
        </html>
        """
        
        text_content = f"Hacker News 前端精选 - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        for story in stories:
            text_content += f"- {story['title']}\n  {story['url']}\n  Score: {story['score']}\n\n"
        
        msg.attach(MIMEText(text_content, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(
                    self.from_email or self.username,
                    self.to_email,
                    msg.as_string()
                )
            print(f"Email sent successfully to {self.to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


if __name__ == "__main__":
    test_stories = [
        {
            "title": "React 19 Released",
            "url": "https://example.com/react19",
            "score": 500,
            "by": "user1",
            "descendants": 100
        }
    ]
    sender = EmailSender()
    sender.send_email(test_stories)
