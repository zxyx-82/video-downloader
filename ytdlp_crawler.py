import yt_dlp
import re


def extract_url(text):
    match = re.search(r'https?://[^\s]+', text)
    if match:
        return match.group()
    return text


def _strip_ansi(s):
    return re.sub(r'\x1b\[[0-9;]*m', '', s).strip()


def progress_hook(log_callback):
    last_pct = [0]
    def hook(d):
        if d["status"] == "downloading":
            raw = _strip_ansi(d.get("_percent_str", "0%"))
            speed = _strip_ansi(d.get("_speed_str", "?"))
            eta = _strip_ansi(d.get("_eta_str", "?"))
            try:
                pct_num = float(raw.replace("%", ""))
            except ValueError:
                return
            if pct_num - last_pct[0] >= 5 or pct_num == 0:
                last_pct[0] = pct_num
                log_callback(f"  进度: {raw} | {speed}/s | 剩余 {eta}")
    return hook


def download_ytdlp(url, quality="最优", log_callback=print):
    url = extract_url(url)

    fmt_map = {
        "最优": "bestvideo+bestaudio/best",
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "360p": "bestvideo[height<=360]+bestaudio/best",
    }
    fmt = fmt_map.get(quality, "bestvideo+bestaudio/best")

    log_callback(f"下载中 (画质: {quality})...")

    for client in [None, "android"]:
        opts = {
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "format": fmt,
            "merge_output_format": "mp4",
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [progress_hook(log_callback)],
        }
        if client:
            opts["extractor_args"] = {"youtube": {"player_client": [client]}}

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.extract_info(url, download=True)
                log_callback("完成！保存在 downloads/")
            return
        except Exception as e:
            err = str(e)
            if "Sign in" in err and client is None:
                log_callback("YouTube 风控，切换 Android 模式...")
                continue
            log_callback(f"下载失败: {err[:80]}")
            return
