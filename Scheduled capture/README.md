# Hacker News 智能筛选器

自动抓取 Hacker News Top 文章，通过 AI 智能筛选特定技术主题，并发送到指定邮箱。

## ✨ 功能特性

- 🤖 **AI 智能筛选** - 使用 DeepSeek/OpenAI API 智能识别技术文章
- 📧 **邮件推送** - 自动发送筛选结果到邮箱
- 🎯 **主题定制** - 支持自定义筛选主题（前端、AI、后端等）
- ⏰ **定时任务** - 支持每日定时执行（可开关）
- 🔒 **隐私保护** - 敏感信息通过环境变量管理

## 📁 项目结构

```
.
├── config.py          # 配置管理
├── hn_fetcher.py      # Hacker News 数据抓取
├── ai_filter.py       # AI 筛选模块（可自定义主题）
├── email_sender.py    # 邮件发送模块
├── main.py            # 主程序入口
├── requirements.txt   # Python 依赖
├── .env.example       # 环境变量模板
└── .gitignore         # Git 忽略配置
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/luohaixin/todo-app.git
cd todo-app
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置：

```env
# 邮件配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@example.com

# AI 配置 (支持 DeepSeek、OpenAI 等)
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# 定时配置
SCHEDULE_TIME=09:00
```

### 4. 运行

**立即执行一次：**
```bash
python main.py --now
```

**启用定时任务：**
```bash
# 修改 main.py 中的 ENABLE_SCHEDULER = True
python main.py
```

## ⚙️ 自定义筛选主题

默认筛选 **Web 前端** 相关文章，你可以修改为其他主题。

编辑 [ai_filter.py](ai_filter.py) 中的以下变量：

```python
# 第 28 行：设置筛选主题
FILTER_TOPIC = "Web 前端开发"

# 第 34-47 行：设置相关关键词
FILTER_KEYWORDS = """
前端相关主题包括但不限于：
- JavaScript/TypeScript
- React/Vue/Angular/Svelte 等前端框架
- CSS/HTML
- Web 性能优化
...
"""

# 第 52 行：设置 AI 角色描述
SYSTEM_PROMPT = "你是一个技术内容筛选专家，擅长识别前端开发相关的技术文章。"
```

### 示例：改为筛选 AI 相关文章

```python
FILTER_TOPIC = "人工智能/AI"

FILTER_KEYWORDS = """
AI 相关主题包括但不限于：
- 机器学习/深度学习
- 大语言模型 (LLM)
- 自然语言处理 (NLP)
- 计算机视觉
- 强化学习
- AI 工具和框架 (PyTorch, TensorFlow 等)
- AI 应用和产品
"""

SYSTEM_PROMPT = "你是一个技术内容筛选专家，擅长识别人工智能相关的技术文章。"
```

## ⏰ 定时任务设置

### 修改定时时间

编辑 `.env` 文件：
```env
SCHEDULE_TIME=09:00  # 每天 09:00 执行
```

### 启用/禁用定时

编辑 [main.py](main.py) 第 35 行：

```python
ENABLE_SCHEDULER = False  # False = 禁用，True = 启用
```

## 📝 依赖说明

| 包名 | 用途 |
|------|------|
| requests | HTTP 请求，抓取 HN 数据 |
| openai | AI API 调用 |
| schedule | 定时任务调度 |
| python-dotenv | 环境变量管理 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License


