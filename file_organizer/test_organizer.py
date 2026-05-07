#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

def create_test_files(test_dir: str):
    test_path = Path(test_dir)
    
    file_types = {
        'video.mp4': VIDEO_EXTENSIONS,
        'photo.jpg': PHOTO_EXTENSIONS,
        'document.pdf': DOCUMENT_EXTENSIONS,
        'program.exe': EXCLUDED_EXTENSIONS,
    }
    
    for filename in file_types.keys():
        file_path = test_path / filename
        file_path.touch()
    
    test_subdir = test_path / 'test_folder'
    test_subdir.mkdir()
    (test_subdir / 'nested.txt').touch()
    
    print(f"已创建测试文件于：{test_dir}")

if __name__ == '__main__':
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from file_organizer import VIDEO_EXTENSIONS, PHOTO_EXTENSIONS, DOCUMENT_EXTENSIONS, EXCLUDED_EXTENSIONS
    
    with tempfile.TemporaryDirectory() as temp_dir:
        create_test_files(temp_dir)
        target_dir = os.path.join(temp_dir, 'output')
        
        from file_organizer import organize_files
        organize_files(temp_dir, target_dir, process_folders=True)
        
        print("\n整理后的目录结构：")
        for root, dirs, files in os.walk(target_dir):
            level = root.replace(target_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{subindent}{file}')
