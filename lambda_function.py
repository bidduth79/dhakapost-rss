import requests
from bs4 import BeautifulSoup
from datetime import datetime
from feedgen.feed import FeedGenerator
import os

RSS_FILE = "rss/news.xml"
os.makedirs(os.path.dirname(RSS_FILE), exist_ok=True)

url = "https://www.dhakapost.com/latest-news"
resp = requests.get(url, timeout=10)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# CSS selector for news headlines
links = soup.select(".td-module-title a")

fg = FeedGenerator()
fg.title("Dhaka Post – Latest News")
fg.link(href=url, rel='alternate')
fg.description("Auto-generated RSS feed for Dhaka Post latest news")

seen = set()
for a in links:
    href = a.get("href")
    title = a.get_text(strip=True)
    if not href or not title:
        continue
    if href.startswith("/"):
        href = "https://www.dhakapost.com" + href
    if href in seen:
        continue
    seen.add(href)

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=href)
    fe.pubDate(datetime.utcnow())

rssstr = fg.rss_str(pretty=True)
with open(RSS_FILE, "wb") as f:
    f.write(rssstr)

