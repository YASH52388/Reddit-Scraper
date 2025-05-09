# 🔎 RedditScraper

A powerful and flexible Python-based tool for scraping top Reddit posts using the **PRAW** API. It supports multiple subreddits, time filters, and can export results to **CSV** or **Excel** format.

Ideal for data collection, content analysis, NLP preprocessing, or academic research.

---

## 🧰 Features

- 🔁 Scrape top posts from one or multiple subreddits
- ⏱️ Supports time filters: `day`, `week`, `month`, `year`, `all`
- 📥 Exports data to **CSV** or **Excel**
- 👤 Collects post metadata (author, score, comments, title, selftext, etc.)
- ✅ Handles deleted authors and external link posts
- 🐢 Includes delay to avoid Reddit API rate limits
- 🔧 Command-line interface with full argument support

---

## 🚀 Quick Start

### 🔐 Prerequisites

- Python 3.7+
- A Reddit developer account with:
  - `client_id`
  - `client_secret`
  - `user_agent`

### 📦 Installation

```bash
pip install praw pandas openpyxl
```
### ▶️ Usage
Run from CLI:

```bash
python reddit_scraper.py \
  --subreddits python dataisbeautiful \
  --limit 50 \
  --time-filter month \
  --output data/reddit_data.csv \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --user-agent "RedditScraper/1.0"
```
## 📈 Use Cases
Social media analysis

Topic modeling and NLP

Dataset generation for machine learning

Trend detection across subreddits

## 🧠 Future Improvements
🔎 Add sentiment analysis or keyword extraction

🌐 Multilingual subreddit support

📊 Built-in visualizations of scraped data



