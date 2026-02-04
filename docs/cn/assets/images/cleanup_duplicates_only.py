#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仅删除重复图片（*_1, *_1_2 等）并根据主文件重建 download_log.json。
不发起网络请求。补全下载请再运行: python download_images.py
"""

import re
import json
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.absolute()
DOCS_DIR = SCRIPT_DIR.parent.parent
IMAGES_DIR = SCRIPT_DIR
LOG_FILE = SCRIPT_DIR / "download_log.json"
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}
DUPLICATE_STEM_PATTERN = re.compile(r'_\d+(_\d+)*$')


def stem_is_duplicate(stem: str) -> bool:
    return bool(DUPLICATE_STEM_PATTERN.search(stem))


def main():
    print("=" * 60)
    print("🧹 删除重复图片并重建 download_log.json")
    print("=" * 60)

    deleted = []
    for f in list(IMAGES_DIR.iterdir()):
        if not f.is_file() or f.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if f.name.startswith('.') or f.suffix.lower() in ('.py', '.json'):
            continue
        if stem_is_duplicate(f.stem):
            f.unlink()
            deleted.append(f.name)
    print(f"\n已删除 {len(deleted)} 个重复文件（*_1, *_1_2 等）")
    for name in deleted[:20]:
        print(f"  - {name}")
    if len(deleted) > 20:
        print(f"  ... 共 {len(deleted)} 个")

    mapping = {}
    for f in IMAGES_DIR.iterdir():
        if not f.is_file() or f.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if stem_is_duplicate(f.stem):
            continue
        stem = f.stem
        ext = f.suffix.lower()
        m = re.match(r'^\d{2}_\d{3}_([a-f0-9-]+)$', stem)
        if not m:
            continue
        uuid_part = m.group(1)
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
    print(f"\n已重建 download_log.json，共 {len(mapping)} 条映射")
    print("=" * 60)
    print("补全下载请运行: python download_images.py")
    print("替换笔记中的 URL 请运行: python replace_image_urls.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
