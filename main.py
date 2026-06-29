import tkinter as tk
from tkinter import ttk
import os
import threading
from crawler import download_bilibili
from x_crawler import download_tweet
from ytdlp_crawler import download_ytdlp
from douyin_crawler import download_douyin


def read_cookie():
    path = os.path.join(os.path.dirname(__file__), "cookie.txt")
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return ""


def log_print(msg):
    log.insert("end", msg + "\n")
    log.see("end")


def start_progress():
    progress.start(10)
    win.update()


def stop_progress():
    progress.stop()
    win.update()


def run_download():
    text = url_text.get("1.0", "end").strip()
    urls = [u.strip() for u in text.split("\n") if u.strip()]
    if not urls:
        log_print("请输入链接（每行一个）")
        win.after(0, lambda: btn.config(state="normal"))
        win.after(0, stop_progress)
        return

    plat = platform.get()
    q = quality.get()

    for i, url in enumerate(urls):
        log_print(f"\n--- 正在下载 ({i+1}/{len(urls)}) ---")
        try:
            if plat == "Bilibili":
                download_bilibili(url, quality=q, cookie=read_cookie(), log_callback=log_print)
            elif plat == "X(Twitter)":
                download_tweet(url, log_callback=log_print)
            elif plat == "抖音":
                download_douyin(url, log_callback=log_print)
            elif plat == "YouTube":
                download_ytdlp(url, quality=q, log_callback=log_print)
            else:
                log_print(f"平台 {plat} 尚未实现")
        except Exception as e:
            log_print(f"出错: {e}")

    log_print(f"\n全部完成！共 {len(urls)} 个")
    win.after(0, lambda: btn.config(state="normal"))
    win.after(0, stop_progress)


def on_download():
    btn.config(state="disabled")
    start_progress()
    threading.Thread(target=run_download, daemon=True).start()


win = tk.Tk()
win.title("Video Downloader")
win.geometry("600x580")

# 平台选择
frame_top = tk.Frame(win)
frame_top.pack(pady=10)

ttk.Label(frame_top, text="平台:").grid(row=0, column=0, padx=5)
platform = ttk.Combobox(frame_top, values=["Bilibili", "抖音", "YouTube", "X(Twitter)"], width=14)
platform.grid(row=0, column=1)
platform.current(0)

ttk.Label(frame_top, text="画质:").grid(row=0, column=2, padx=5)
quality = ttk.Combobox(frame_top, values=["最优", "1080p", "720p", "480p", "360p"], width=8)
quality.grid(row=0, column=3)
quality.current(0)

# 输入区域（多行）
frame_input = tk.Frame(win)
frame_input.pack(pady=10)

ttk.Label(frame_input, text="链接:").pack(anchor="w")
url_text = tk.Text(frame_input, height=5, width=60)
url_text.pack()

# 下载按钮
btn = ttk.Button(win, text="下载", command=on_download)
btn.pack(pady=5)

# 进度条
progress = ttk.Progressbar(win, mode="indeterminate", length=400)
progress.pack(pady=5)

# 日志输出区
log = tk.Text(win, height=16)
log.pack(fill="both", expand=True, padx=10, pady=10)

win.mainloop()
