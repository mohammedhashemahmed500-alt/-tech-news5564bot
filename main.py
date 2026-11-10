import os
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]

def get_news():
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({
        "q": "technology OR artificial intelligence",
        "hl": "ar",
        "gl": "EG",
        "ceid": "EG:ar"
    })

    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        root = ET.fromstring(response.read())

    for item in root.findall("./channel/item"):
        title = item.findtext("title")
        link = item.findtext("link")

        if title and link:
            return f"📰 {title}\n\n🔗 {link}"

    return None


def send_news(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": CHANNEL,
        "text": message
    }).encode()

    request = urllib.request.Request(url, data=data)

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read())

    if not result.get("ok"):
        raise RuntimeError("Telegram failed to send the message")


if __name__ == "__main__":
    news = get_news()

    if news:
        send_news(news)
        print("News published successfully!")
    else:
        print("No news available.")
