import requests
import subprocess
import os
import re


def download_bilibili(bvid, quality="最优", cookie="", log_callback=print):
    # 支持 BVID 或完整链接
    match = re.search(r'BV[a-zA-Z0-9]+', bvid)
    if match:
        bvid = match.group()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    if cookie:
        headers["Cookie"] = cookie
        log_callback("Cookie 已加载，长度: " + str(len(cookie)))
    else:
        log_callback("未使用 Cookie")

    log_callback("获取视频信息...")
    url1 = "https://api.bilibili.com/x/web-interface/view"
    resp1 = requests.get(url1, params={"bvid": bvid}, headers=headers)
    data1 = resp1.json()
    if data1["code"] != 0:
        log_callback(f"API 错误: {data1['message']}")
        return
    cid = data1["data"]["cid"]
    title = data1["data"]["title"]
    log_callback(f"标题: {title}")

    qn_map = {"最优": 120, "1080p": 80, "720p": 64, "480p": 32, "360p": 16}
    qn = qn_map.get(quality, 120)
    log_callback(f"获取视频流地址 (画质: {quality}, qn={qn})...")
    url2 = "https://api.bilibili.com/x/player/playurl"
    params2 = {"bvid": bvid, "cid": cid, "qn": qn, "fnval": 16}
    resp2 = requests.get(url2, params=params2, headers=headers)
    data2 = resp2.json()

    best = data2['data']['quality']
    log_callback(f"当前画质: {best}, 可用画质: {data2['data']['accept_quality']}")

    video_url = data2["data"]["dash"]["video"][0]["baseUrl"]
    audio_url = data2["data"]["dash"]["audio"][0]["baseUrl"]

    for name, url in [("视频", video_url), ("音频", audio_url)]:
        for retry in range(3):
            try:
                log_callback(f"下载{name}流 (尝试 {retry+1}/3)...")
                r = requests.get(url, headers=headers, stream=True, timeout=60)
                total = int(r.headers.get("Content-Length", 0))
                down = 0
                last_pct = 0
                import time
                start = time.time()
                tmp = "video_temp.m4s" if name == "视频" else "audio_temp.m4s"
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(8192):
                        if not chunk:
                            continue
                        f.write(chunk)
                        down += len(chunk)
                        if total > 0:
                            pct = down * 100 // total
                            if pct - last_pct >= 5 or pct == 0:
                                last_pct = pct
                                elapsed = time.time() - start
                                speed = down / elapsed / 1024 if elapsed > 0 else 0
                                log_callback(f"  进度: {pct}% | {speed:.0f}KB/s")
                break
            except Exception as e:
                log_callback(f"{name}下载中断: {str(e)[:50]}")
                if retry == 2:
                    raise
                log_callback("重试...")

    log_callback("合并中...")
    os.makedirs("downloads", exist_ok=True)
    out_name = f"downloads/{title}.mp4"
    subprocess.run([
        "ffmpeg", "-i", "video_temp.m4s", "-i", "audio_temp.m4s",
        "-c", "copy", out_name
    ], check=True)

    os.remove("video_temp.m4s")
    os.remove("audio_temp.m4s")
    log_callback(f"完成: {out_name}")


if __name__ == "__main__":
    cookie = ""
    cpath = os.path.join(os.path.dirname(__file__), "cookie.txt")
    if os.path.exists(cpath):
        with open(cpath) as f:
            cookie = f.read().strip()
    download_bilibili("BV1Xj7N6mEa3", cookie=cookie)
