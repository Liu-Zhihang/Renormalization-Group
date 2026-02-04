#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. 删除重复下载的图片（文件名后缀为 _1、_1_2、_1_2_3 等）
2. 根据剩余主文件重建 download_log.json
3. 检查笔记中的图片 URL，缺失的重新下载
"""

import re
import json
import requests
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.absolute()
DOCS_DIR = SCRIPT_DIR.parent.parent
IMAGES_DIR = SCRIPT_DIR
LOG_FILE = SCRIPT_DIR / "download_log.json"
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}
REQUEST_TIMEOUT = 15
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'image/*,*/*;q=0.8',
}

# 重复文件：stem 以 _1、_1_2、_1_2_3 结尾
DUPLICATE_STEM_PATTERN = re.compile(r'_\d+(_\d+)*$')


def stem_is_duplicate(stem: str) -> bool:
    """主文件 stem 不含 _1/_1_2；重复文件含 _1 或 _1_2 等"""
    return bool(DUPLICATE_STEM_PATTERN.search(stem))


def delete_duplicate_images():
    """删除重复图片（*_1.png, *_1_2.jpg 等）"""
    deleted = []
    for f in IMAGES_DIR.iterdir():
        if not f.is_file() or f.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if f.name.startswith('.') or f.suffix.lower() == '.py':
            continue
        if stem_is_duplicate(f.stem):
            f.unlink()
            deleted.append(f.name)
    return deleted


def uuid_and_ext_from_primary_filename(filename: str):
    """从主文件名 01_001_748c3bba-f562-45f3-a6c9-a7be7f2d4cb5.jpg 提取 uuid 和 ext"""
    stem = Path(filename).stem
    ext = Path(filename).suffix.lower()
    if ext not in IMAGE_EXTENSIONS:
        return None, None
    # 格式: 01_001_<name_part>
    m = re.match(r'^\d{2}_\d{3}_(.+)$', stem)
    if not m:
        return None, None
    name_part = m.group(1)
    if not re.match(r'^[a-f0-9-]+$', name_part):  # UUID 或短哈希
        return None, None
    return name_part, ext


def rebuild_log_from_primary_files():
    """根据当前主文件重建 download_log.json（mdnice URL -> 本地文件名）"""
    mapping = {}
    for f in IMAGES_DIR.iterdir():
        if not f.is_file() or f.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if stem_is_duplicate(f.stem):
            continue
        uuid_part, ext = uuid_and_ext_from_primary_filename(f.name)
        if not uuid_part:
            continue
        for user_id in ['141272', '129153']:
            url = f"https://files.mdnice.com/user/{user_id}/{uuid_part}{ext}"
            mapping[url] = f.name
    log = {
        "last_update": datetime.now().isoformat(),
        "processed_files": {},
        "downloaded_urls": mapping
    }
    with open(LOG_FILE, 'w', encoding='utf-8') as out:
        json.dump(log, out, ensure_ascii=False, indent=2)
    return len(mapping)


def extract_image_urls(content: str):
    urls = []
    for m in re.finditer(r'!\[([^\]]*)\]\((https://[^)\s]+)(?:\s+"[^"]*")?\)', content):
        urls.append(m.group(2))
    return urls


def download_one(url: str, save_path: Path) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, stream=True)
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  ✗ 下载失败: {e}")
        return False


def url_to_filename(url: str, index: int, note_name: str) -> str:
    from urllib.parse import urlparse, unquote
    parsed = urlparse(url)
    path = unquote(parsed.path)
    name = Path(path).stem
    ext = Path(path).suffix.lower() or '.png'
    if ext not in IMAGE_EXTENSIONS:
        ext = '.png'
    note_num = re.match(r'^(\d+)', note_name)
    nn = note_num.group(1).zfill(2) if note_num else '00'
    name = re.sub(r'[<>:"/\\|?*]', '_', name)[:30]
    return f"{nn}_{str(index).zfill(3)}_{name}{ext}"


def find_missing_urls_and_download():
    """收集所有 md 中的图片 URL，未在 log 或文件不存在的则下载"""
    if not LOG_FILE.exists():
        return 0
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log = json.load(f)
    mapping = dict(log.get("downloaded_urls", {}))
    all_urls = set()
    for md in sorted(DOCS_DIR.glob("*.md")):
        with open(md, 'r', encoding='utf-8') as f:
            all_urls.update(extract_image_urls(f.read()))
    missing = []
    for url in all_urls:
        if url not in mapping:
            missing.append(url)
        else:
            local = IMAGES_DIR / mapping[url]
            if not local.exists():
                missing.append(url)
    if not missing:
        return 0
    print(f"\n📥 需重新下载 {len(missing)} 张图片")
    url_to_note = {}
    for md in sorted(DOCS_DIR.glob("*.md")):
        with open(md, 'r', encoding='utf-8') as f:
            for u in extract_image_urls(f.read()):
                if u in missing:
                    url_to_note[u] = md.stem
    downloaded = 0
    for i, url in enumerate(missing, 1):
        note_name = url_to_note.get(url, "00")
        filename = url_to_filename(url, i, note_name)
        save_path = IMAGES_DIR / filename
        if save_path.exists():
            mapping[url] = filename
            downloaded += 1
            continue
        print(f"  [{i}/{len(missing)}] {filename[:55]}...")
        if download_one(url, save_path):
            mapping[url] = filename
            downloaded += 1
            print("  ✓")
    if downloaded > 0:
        log["downloaded_urls"] = mapping
        log["last_update"] = datetime.now().isoformat()
        with open(LOG_FILE, 'w', encoding='utf-8') as out:
            json.dump(log, out, ensure_ascii=False, indent=2)
    return downloaded


def main():
    print("=" * 60)
    print("🧹 删除重复图片并补全下载")
    print("=" * 60)

    deleted = delete_duplicate_images()
    print(f"\n已删除 {len(deleted)} 个重复文件（*_1, *_1_2 等）")
    if deleted:
        for name in deleted[:15]:
            print(f"  - {name}")
        if len(deleted) > 15:
            print(f"  ... 共 {len(deleted)} 个")

    n = rebuild_log_from_primary_files()
    print(f"\n已根据主文件重建 download_log.json，共 {n} 条映射")

    redownloaded = find_missing_urls_and_download()
    print(f"\n补全下载：{redownloaded} 张")
    print("=" * 60)
    print("请再运行: python replace_image_urls.py  将笔记中的 URL 替换为本地路径")
    print("=" * 60)


if __name__ == "__main__":
    main()
