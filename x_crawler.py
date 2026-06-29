import requests
import os
import re
import sys


if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def extract_tweet_id(url):
    match = re.search(r'/status/(\d+)', url)
    if not match:
        raise ValueError("无法从链接中提取推文 ID")
    return match.group(1)


def fetch_tweet(tweet_id):
    url = f"https://api.vxtwitter.com/Twitter/status/{tweet_id}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def download_tweet(url, log_callback=print):
    tweet_id = extract_tweet_id(url)
    log_callback(f"获取推文数据...")
    data = fetch_tweet(tweet_id)

    author = data["user_name"]
    text = data["text"]
    log_callback(f"作者: {author}")
    log_callback(f"文字内容: {text[:80]}...")

    safe_name = f"{author}_{tweet_id}"
    safe_name = re.sub(r'[\\/*?:"<>|]', "", safe_name)
    os.makedirs(f"downloads/{safe_name}", exist_ok=True)

    with open(f"downloads/{safe_name}/tweet.txt", "w", encoding="utf-8") as f:
        f.write(text)
    log_callback("文字已保存")

    for i, media in enumerate(data.get("media_extended", [])):
        media_url = media["url"]
        ext = "mp4" if media["type"] == "video" else "jpg"
        filename = f"downloads/{safe_name}/{i+1}.{ext}"
        log_callback(f"下载媒体 {i+1}: {media['type']}")
        r = requests.get(media_url, stream=True)
        total = int(r.headers.get("Content-Length", 0))
        down, last_pct = 0, 0
        with open(filename, "wb") as f:
            for chunk in r.iter_content(8192):
                if not chunk:
                    continue
                f.write(chunk)
                down += len(chunk)
                if total > 0:
                    pct = down * 100 // total
                    if pct - last_pct >= 5:
                        last_pct = pct
                        log_callback(f"  进度: {pct}%")
        log_callback(f"  {media['type']} 完成 ({down/1024:.0f}KB)")

    log_callback(f"完成！保存在 downloads/{safe_name}/")


if __name__ == "__main__":
    url = input("粘贴 X 推文链接: ")
    download_tweet(url)
