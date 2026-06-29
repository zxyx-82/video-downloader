# Video Downloader

一个带 GUI 界面的视频下载工具，支持 B站 / YouTube / 抖音 / X(Twitter) 四个平台。

## 功能

- 四平台视频下载
- 画质选择（最优 / 1080p / 720p / 480p / 360p）
- 批量下载（每行一个链接）
- 实时进度显示（速度 / 百分比 / 剩余时间）
- 抖音无水印下载
- X/Twitter 文字+图片+视频一起保存
- B站 Cookie 登录解锁 1080p
- 多线程不卡 UI

## 快速开始

```bash
git clone https://github.com/zxyx-82/video-downloader.git
cd video-downloader
python -m venv venv
source venv/Scripts/activate    # Windows Git Bash
pip install -r requirements.txt
python main.py
```

## 使用

1. 选择平台（Bilibili / 抖音 / YouTube / X）
2. 粘贴链接（每行一个，支持批量）
3. 选择画质
4. 点下载

### B站 Cookie（可选）

登录 B站后，F12 → Network → 刷新 → 复制 Cookie 到 `cookie.txt`，不设置也能下载但限 720p。

## 依赖

- Python 3.10+
- requests
- yt-dlp
- pyinstaller（打包用）

## 打包

```bash
pip install pyinstaller
pyinstaller --onefile --name 下载器 main.py
```

## 项目结构

```
bili-crawler/
├── main.py              # GUI 界面
├── crawler.py           # B站下载
├── x_crawler.py         # X/Twitter 下载
├── ytdlp_crawler.py     # YouTube 下载
├── douyin_crawler.py    # 抖音下载
├── downloader.py        # 抖音引擎
├── utils.py             # 抖音工具
└── cookie.txt           # B站 Cookie
```

## 免责声明

本项目仅供学习编程使用，下载内容请遵守各平台服务条款。
