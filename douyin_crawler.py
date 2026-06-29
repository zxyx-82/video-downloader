import os
from downloader import DouyinDownloader


def download_douyin(url, log_callback=print):
    log_callback("解析抖音链接...")

    dl = DouyinDownloader(output_dir="downloads")

    try:
        result = dl.download_from_share_url(url, mode="video", show_progress=False)
        size = os.path.getsize(result.file_path)
        log_callback(f"标题: {result.title}")
        log_callback(f"完成！{size/1024/1024:.1f}MB | downloads/{result.file_path.name}")
    except Exception as e:
        log_callback(f"下载失败: {str(e)[:100]}")
    finally:
        dl.close()
