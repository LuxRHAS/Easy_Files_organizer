#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json
from datetime import datetime
from pathlib import Path


VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg', '.3gp'}
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.raw', '.cr2', '.nef'}
DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.rtf', '.odt', '.ods', '.odp'}
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.ape', '.opus', '.aiff'}
APPLICATION_EXTENSIONS = {'.exe', '.app', '.msi', '.pkg', '.dmg', '.deb', '.rpm', '.msix'}
ARCHIVE_EXTENSIONS = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'}

EXCLUDED_EXTENSIONS = {'.lnk', '.dll', '.sys', '.bat', '.cmd', '.sh', '.pif', '.scr'}

SELF_FILE_NAMES = {'readme.md'}

LOG_FILENAME = 'log.json'


def get_self_filename() -> str:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).name
    
    if 'python.app' in sys.executable or 'Contents/MacOS' in sys.executable:
        return Path(sys.executable).name
    
    try:
        if '__file__' in globals():
            return Path(__file__).name
    except (NameError, OSError):
        pass
    
    if sys.argv and sys.argv[0]:
        return Path(sys.argv[0]).name
    
    return ''


SELF_PROGRAM_NAME = get_self_filename()


def is_path_relative_to(child_path: Path, parent_path: Path) -> bool:
    """检查路径是否为另一路径的子路径（兼容 Python 3.6+）"""
    try:
        child_path.relative_to(parent_path)
        return True
    except ValueError:
        return False


def get_file_type(file_path: str) -> str:
    """获取文件类型（按时间整理模式使用）"""
    ext = Path(file_path).suffix.lower()
    if ext in VIDEO_EXTENSIONS:
        return '视频'
    elif ext in PHOTO_EXTENSIONS:
        return '图片'
    elif ext in DOCUMENT_EXTENSIONS:
        return '文档'
    elif ext in AUDIO_EXTENSIONS:
        return '音频'
    elif ext in APPLICATION_EXTENSIONS:
        return '应用程序'
    elif ext in ARCHIVE_EXTENSIONS:
        return '压缩包'
    return None


def get_simple_file_type(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext in PHOTO_EXTENSIONS:
        return '图片'
    elif ext in VIDEO_EXTENSIONS:
        return '视频'
    elif ext in DOCUMENT_EXTENSIONS:
        return '文档'
    elif ext in AUDIO_EXTENSIONS:
        return '音频'
    elif ext in APPLICATION_EXTENSIONS:
        return '应用程序'
    elif ext in ARCHIVE_EXTENSIONS:
        return '压缩包'
    else:
        return '其他'


def should_exclude_file(file_path: str) -> bool:
    ext = Path(file_path).suffix.lower()
    filename = Path(file_path).name.lower()
    
    if ext in EXCLUDED_EXTENSIONS:
        return True
    
    if filename in SELF_FILE_NAMES:
        return True
    
    return False


def is_self_file(file_path: str) -> bool:
    filename = Path(file_path).name.lower()
    
    if filename in SELF_FILE_NAMES:
        return True
    
    if filename == '__main__.py':
        return True
    
    if SELF_PROGRAM_NAME and filename == SELF_PROGRAM_NAME.lower():
        return True
    
    return False


def get_creation_date(path: str) -> datetime:
    try:
        stat = os.stat(path)
        if hasattr(stat, 'st_birthtime'):
            creation_time = stat.st_birthtime
        else:
            creation_time = stat.st_ctime
        return datetime.fromtimestamp(creation_time)
    except (OSError, ValueError, OverflowError):
        return datetime.now()


def get_category_folders(creation_date: datetime, file_type: str) -> tuple:
    year = str(creation_date.year)
    month = f"{creation_date.month:02d}"
    return year, month, file_type


def get_log_file_path(target_dir: str) -> Path:
    return Path(target_dir) / LOG_FILENAME


class UserExitException(Exception):
    pass


def get_valid_choice(prompt: str, valid_choices: list, allow_quit: bool = True) -> str:
    while True:
        choice = input(prompt).strip()
        
        if allow_quit and choice.lower() in ['q', 'quit', '退出']:
            raise UserExitException("用户选择退出程序")
        
        if choice in valid_choices:
            return choice
        
        print(f"错误：无效的选项，请输入 {'/'.join(valid_choices)} 中的一个" + ("，或输入 q 退出" if allow_quit else ""))


def get_valid_directory(prompt: str, must_exist: bool = True, allow_quit: bool = True) -> str:
    while True:
        dir_path = input(prompt).strip()
        
        if allow_quit and dir_path.lower() in ['q', 'quit', '退出']:
            raise UserExitException("用户选择退出程序")
        
        if not dir_path:
            print("错误：路径不能为空" + ("，或输入 q 退出" if allow_quit else ""))
            continue
        
        path = Path(dir_path)
        if must_exist and not path.exists():
            print(f"错误：目录不存在：{dir_path}" + ("，或输入 q 退出" if allow_quit else ""))
            continue
        
        if must_exist and not path.is_dir():
            print(f"错误：路径不是目录：{dir_path}" + ("，或输入 q 退出" if allow_quit else ""))
            continue
        
        return dir_path


def get_valid_confirmation(prompt: str, allow_quit: bool = True) -> bool:
    while True:
        confirm = input(prompt).strip().lower()
        
        if allow_quit and confirm in ['q', 'quit', '退出']:
            raise UserExitException("用户选择退出程序")
        
        if confirm in ['y', 'yes', '是']:
            return True
        elif confirm in ['n', 'no', '否']:
            return False
        
        print("错误：请输入 y（确认）或 n（取消）" + ("，或输入 q 退出" if allow_quit else ""))


def load_log_history(target_dir: str) -> list:
    log_file = get_log_file_path(target_dir)
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('history', [])
        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            return []
    return []


def save_log_history(target_dir: str, history: list):
    log_file = get_log_file_path(target_dir)
    data = {
        'target_directory': str(Path(target_dir).resolve()),
        'history': history
    }
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_log_record(target_dir: str, source_dir: str, process_folders: bool,
                     move_files: bool, organize_mode: str, processed_items: list) -> bool:
    try:
        history = load_log_history(target_dir)

        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_directory': str(Path(source_dir).resolve()),
            'organize_mode': organize_mode,
            'process_folders': process_folders,
            'move_files': move_files,
            'processed_count': len(processed_items),
            'processed_items': processed_items
        }

        history.append(record)
        save_log_history(target_dir, history)

        print(f"\n已更新整理 log 文件：{get_log_file_path(target_dir)}")
        return True
    except (OSError, json.JSONEncodeError, TypeError) as e:
        print(f"\n错误：保存 log 文件失败：{e}")
        return False


def process_folder_recursive_time(source_path: Path, target_path: Path,
                                  move_files: bool, processed_items: list,
                                  empty_folder_target: Path = None) -> tuple:
    processed_count = 0
    error_count = 0

    for item in source_path.iterdir():
        if item.resolve() == target_path or is_path_relative_to(item.resolve(), target_path):
            continue
        if is_self_file(str(item)):
            continue

        if item.is_file():
            if should_exclude_file(str(item)):
                continue

            file_type = get_file_type(str(item))
            if file_type is None:
                continue

            creation_date = get_creation_date(str(item))
            year, month, type_folder = get_category_folders(creation_date, file_type)
            dest_folder = target_path / year / month / type_folder

            try:
                dest_folder.mkdir(parents=True, exist_ok=True)
                dest_file = dest_folder / item.name

                counter = 1
                while dest_file.exists():
                    stem = item.stem
                    suffix = item.suffix
                    dest_file = dest_folder / f"{stem}_{counter}{suffix}"
                    counter += 1

                if move_files:
                    shutil.move(str(item), str(dest_file))
                else:
                    shutil.copy2(str(item), str(dest_file))

                processed_items.append({
                    'type': 'file',
                    'name': item.name,
                    'destination': str(dest_folder.relative_to(target_path) / dest_file.name),
                    'action': '移动' if move_files else '复制',
                    'source': str(item)
                })
                processed_count += 1
                
            except (OSError, PermissionError, shutil.Error) as e:
                print(f"错误处理文件 {item.name}: {e}")
                error_count += 1
        
        elif item.is_dir():
            sub_count, sub_error = process_folder_recursive_time(
                item, target_path, move_files, processed_items, empty_folder_target
            )
            processed_count += sub_count
            error_count += sub_error

            # 修复：检查当前文件夹是否为空，而不是使用累计的processed_count
            try:
                if not any(item.iterdir()):
                    if empty_folder_target and move_files:
                        empty_folder_target.mkdir(parents=True, exist_ok=True)
                        dest_empty = empty_folder_target / item.name
                        if dest_empty.exists():
                            counter = 1
                            while dest_empty.exists():
                                dest_empty = empty_folder_target / f"{item.name}_{counter}"
                                counter += 1
                        shutil.move(str(item), str(dest_empty))
                        print(f"已移动空文件夹到：空文件夹/{dest_empty.name}")
                        processed_items.append({
                            'type': 'folder',
                            'name': item.name,
                            'destination': f"空文件夹/{dest_empty.name}",
                            'action': '移动',
                            'source': str(item)
                        })
                    elif move_files:
                        shutil.rmtree(str(item))
                        print(f"已删除空文件夹：{item.name}")
                    else:
                        print(f"保留空文件夹：{item.name} (复制模式)")
            except (OSError, PermissionError, shutil.Error) as e:
                print(f"处理空文件夹时出错 {item.name}: {e}")
    
    return processed_count, error_count


def organize_by_time(source_dir: str, target_dir: str, process_folders: bool, 
                    move_files: bool, recursive: bool = False, 
                    show_preview: bool = False) -> tuple:
    source_path = Path(source_dir).resolve()
    target_path = Path(target_dir).resolve()
    
    if not source_path.exists():
        print(f"错误：源目录不存在：{source_path}")
        return False, []
    
    if not target_path.exists():
        try:
            target_path.mkdir(parents=True, exist_ok=True)
            print(f"已创建目标目录：{target_path}")
        except Exception as e:
            print(f"错误：无法创建目标目录：{e}")
            return False, []
    
    if source_path == target_path:
        print("错误：源目录和目标目录不能相同")
        return False, []
    
    processed_count = 0
    error_count = 0
    action = "移动" if move_files else "复制"
    processed_items = []
    
    print(f"\n开始处理源目录：{source_path}")
    print(f"目标目录：{target_path}")
    print(f"是否处理文件夹：{process_folders}")
    print(f"是否递归处理子文件夹：{recursive}")
    print(f"操作模式：{action}")
    print("-" * 60)
    
    empty_folder_target = None
    if process_folders and move_files:
        empty_folder_target = target_path / "空文件夹"
    
    if process_folders and show_preview:
        print("\n文件夹整理预览：")
        preview_items = []
        for item in source_path.iterdir():
            if item.resolve() == target_path or is_path_relative_to(item.resolve(), target_path):
                continue
            if is_self_file(str(item)):
                continue
            if item.is_dir():
                creation_date = get_creation_date(str(item))
                year, month, type_folder = get_category_folders(creation_date, '文件夹')
                dest_folder = target_path / year / month / type_folder / item.name
                preview_items.append(f"  {item.name} -> {dest_folder.relative_to(target_path)}")
        
        if preview_items:
            print("\n以下文件夹将被整理到：")
            for preview in preview_items:
                print(preview)
            print()
            
            confirm = input("是否确认开始整理？(y/n): ").strip().lower()
            if confirm in ['q', 'quit', '退出']:
                raise UserExitException("用户选择退出程序")
            if confirm != 'y':
                print("已取消操作")
                return False, []
        print("-" * 60)
    
    if process_folders and recursive:
        print("\n将递归处理所有子文件夹中的文件...")
        processed_count, error_count = process_folder_recursive_time(
            source_path, target_path, move_files, processed_items, empty_folder_target
        )
    else:
        for item in source_path.iterdir():
            if item.resolve() == target_path or is_path_relative_to(item.resolve(), target_path):
                print(f"跳过目标目录：{item.name}")
                continue
            if is_self_file(str(item)):
                print(f"跳过程序自身文件：{item.name}")
                continue
            
            if item.is_file():
                if should_exclude_file(str(item)):
                    print(f"跳过排除的文件：{item.name}")
                    continue
                
                file_type = get_file_type(str(item))
                if file_type is None:
                    print(f"跳过不支持的文件类型：{item.name}")
                    continue
                
                creation_date = get_creation_date(str(item))
                year, month, type_folder = get_category_folders(creation_date, file_type)
                
                dest_folder = target_path / year / month / type_folder
                try:
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    dest_file = dest_folder / item.name
                    
                    counter = 1
                    while dest_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        dest_file = dest_folder / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    if move_files:
                        shutil.move(str(item), str(dest_file))
                        print(f"已移动：{item.name} -> {dest_folder.relative_to(target_path)}/{dest_file.name}")
                    else:
                        shutil.copy2(str(item), str(dest_file))
                        print(f"已复制：{item.name} -> {dest_folder.relative_to(target_path)}/{dest_file.name}")
                    
                    processed_items.append({
                        'type': 'file',
                        'name': item.name,
                        'destination': str(dest_folder.relative_to(target_path) / dest_file.name),
                        'action': '移动' if move_files else '复制',
                        'source': str(item)
                    })
                    processed_count += 1
                    
                except (OSError, PermissionError, shutil.Error) as e:
                    print(f"错误处理文件 {item.name}: {e}")
                    error_count += 1
            
            elif item.is_dir() and process_folders:
                creation_date = get_creation_date(str(item))
                year, month, type_folder = get_category_folders(creation_date, '文件夹')
                
                dest_folder = target_path / year / month / type_folder
                try:
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    dest_dir = dest_folder / item.name
                    
                    if dest_dir.exists():
                        counter = 1
                        while dest_dir.exists():
                            dest_dir = dest_folder / f"{item.name}_{counter}"
                            counter += 1
                    
                    if move_files:
                        shutil.move(str(item), str(dest_dir))
                        print(f"已移动文件夹：{item.name} -> {dest_folder.relative_to(target_path)}/{dest_dir.name}")
                    else:
                        shutil.copytree(str(item), str(dest_dir))
                        print(f"已复制文件夹：{item.name} -> {dest_folder.relative_to(target_path)}/{dest_dir.name}")
                    
                    processed_items.append({
                        'type': 'folder',
                        'name': item.name,
                        'destination': str(dest_folder.relative_to(target_path) / dest_dir.name),
                        'action': '移动' if move_files else '复制',
                        'source': str(item)
                    })
                    processed_count += 1
                    
                except Exception as e:
                    print(f"错误处理文件夹 {item.name}: {e}")
                    error_count += 1
    
    print("-" * 60)
    print(f"处理完成！成功处理：{processed_count} 个项目，错误：{error_count} 个")
    
    return True, processed_items


def process_folder_recursive(source_path: Path, target_path: Path, file_type_func, 
                            move_files: bool, processed_items: list) -> tuple:
    processed_count = 0
    error_count = 0
    
    empty_folder_target = target_path / "空文件夹" if move_files else None
    
    for item in source_path.iterdir():
        if item.resolve() == target_path or is_path_relative_to(item.resolve(), target_path):
            continue
        if is_self_file(str(item)):
            continue
        
        if item.is_file():
            if should_exclude_file(str(item)):
                continue
            
            file_type = file_type_func(str(item))
            dest_folder = target_path / file_type
            
            try:
                dest_folder.mkdir(parents=True, exist_ok=True)
                dest_file = dest_folder / item.name
                
                counter = 1
                while dest_file.exists():
                    stem = item.stem
                    suffix = item.suffix
                    dest_file = dest_folder / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                if move_files:
                    shutil.move(str(item), str(dest_file))
                    print(f"已移动：{item.name} -> {file_type}/{dest_file.name}")
                else:
                    shutil.copy2(str(item), str(dest_file))
                    print(f"已复制：{item.name} -> {file_type}/{dest_file.name}")
                
                processed_items.append({
                    'type': 'file',
                    'name': item.name,
                    'destination': f"{file_type}/{dest_file.name}",
                    'action': '移动' if move_files else '复制',
                    'source': str(item)
                })
                processed_count += 1
                
            except (OSError, PermissionError, shutil.Error) as e:
                print(f"错误处理文件 {item.name}: {e}")
                error_count += 1
        
        elif item.is_dir():
            sub_count, sub_error = process_folder_recursive(item, target_path, file_type_func,
                                                           move_files, processed_items)
            processed_count += sub_count
            error_count += sub_error

            try:
                if not any(item.iterdir()):
                    if empty_folder_target and move_files:
                        empty_folder_target.mkdir(parents=True, exist_ok=True)
                        dest_empty = empty_folder_target / item.name
                        if dest_empty.exists():
                            counter = 1
                            while dest_empty.exists():
                                dest_empty = empty_folder_target / f"{item.name}_{counter}"
                                counter += 1
                        shutil.move(str(item), str(dest_empty))
                        print(f"已移动空文件夹到：空文件夹/{dest_empty.name}")
                        processed_items.append({
                            'type': 'folder',
                            'name': item.name,
                            'destination': f"空文件夹/{dest_empty.name}",
                            'action': '移动',
                            'source': str(item)
                        })
                    elif move_files:
                        shutil.rmtree(str(item))
                        print(f"已删除空文件夹：{item.name}")
                    else:
                        print(f"保留空文件夹：{item.name} (复制模式)")
            except (OSError, PermissionError, shutil.Error) as e:
                print(f"处理空文件夹时出错 {item.name}: {e}")

    return processed_count, error_count


def organize_by_type(source_dir: str, target_dir: str, process_folders: bool, 
                    move_files: bool) -> tuple:
    source_path = Path(source_dir).resolve()
    target_path = Path(target_dir).resolve()
    
    if not source_path.exists():
        print(f"错误：源目录不存在：{source_path}")
        return False, []
    
    if not target_path.exists():
        try:
            target_path.mkdir(parents=True, exist_ok=True)
            print(f"已创建目标目录：{target_path}")
        except Exception as e:
            print(f"错误：无法创建目标目录：{e}")
            return False, []
    
    if source_path == target_path:
        print("错误：源目录和目标目录不能相同")
        return False, []
    
    processed_count = 0
    error_count = 0
    action = "移动" if move_files else "复制"
    processed_items = []
    
    print(f"\n开始处理源目录：{source_path}")
    print(f"目标目录：{target_path}")
    print(f"是否处理文件夹：{process_folders}")
    print(f"操作模式：{action}")
    print("-" * 60)
    
    if process_folders:
        print("\n将递归处理所有子文件夹中的文件...")
        processed_count, error_count = process_folder_recursive(
            source_path, target_path, get_simple_file_type, move_files, processed_items
        )
    else:
        for item in source_path.iterdir():
            if item.resolve() == target_path or is_path_relative_to(item.resolve(), target_path):
                print(f"跳过目标目录：{item.name}")
                continue
            if is_self_file(str(item)):
                print(f"跳过程序自身文件：{item.name}")
                continue
            
            if item.is_file():
                if should_exclude_file(str(item)):
                    print(f"跳过排除的文件：{item.name}")
                    continue
                
                file_type = get_simple_file_type(str(item))
                dest_folder = target_path / file_type
                
                try:
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    dest_file = dest_folder / item.name
                    
                    counter = 1
                    while dest_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        dest_file = dest_folder / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    if move_files:
                        shutil.move(str(item), str(dest_file))
                        print(f"已移动：{item.name} -> {file_type}/{dest_file.name}")
                    else:
                        shutil.copy2(str(item), str(dest_file))
                        print(f"已复制：{item.name} -> {file_type}/{dest_file.name}")
                    
                    processed_items.append({
                        'type': 'file',
                        'name': item.name,
                        'destination': f"{file_type}/{dest_file.name}",
                        'action': '移动' if move_files else '复制',
                        'source': str(item)
                    })
                    processed_count += 1
                    
                except (OSError, PermissionError, shutil.Error) as e:
                    print(f"错误处理文件 {item.name}: {e}")
                    error_count += 1
    
    print("-" * 60)
    print(f"处理完成！成功处理：{processed_count} 个项目，错误：{error_count} 个")
    
    return True, processed_items


def rollback_operation(target_dir: str, record_index: int) -> bool:
    log_file = get_log_file_path(target_dir)
    if not log_file.exists():
        print(f"错误：log 文件不存在：{log_file}")
        return False
    
    history = load_log_history(target_dir)
    if not history:
        print("错误：没有找到整理记录")
        return False
    
    if record_index < 0 or record_index >= len(history):
        print("错误：无效的整理记录编号")
        return False
    
    record = history[record_index]
    target_path = Path(target_dir).resolve()
    
    print(f"\n开始回滚操作...")
    print(f"回滚目标：{record['timestamp']} 的整理记录")
    print(f"整理模式：{record['organize_mode']}")
    print(f"处理项目数：{record['processed_count']}")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    
    for item in reversed(record['processed_items']):
        try:
            dest_path = target_path / item['destination']
            
            if not dest_path.exists():
                print(f"警告：文件不存在，跳过：{dest_path}")
                continue
            
            if item['type'] == 'file':
                if item['action'] == '移动':
                    source_path = Path(item['source'])
                    source_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dest_path), str(source_path))
                    print(f"已回滚文件：{item['name']} -> {source_path}")
                else:
                    dest_path.unlink()
                    print(f"已删除复制的文件：{item['name']}")
                success_count += 1
                
            elif item['type'] == 'folder':
                if item['action'] == '移动':
                    source_path = Path(item['source'])
                    if dest_path.is_dir():
                        source_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(dest_path), str(source_path))
                        print(f"已回滚文件夹：{item['name']} -> {source_path}")
                    else:
                        print(f"警告：文件夹不存在：{dest_path}")
                else:
                    if dest_path.is_dir():
                        shutil.rmtree(str(dest_path))
                        print(f"已删除复制的文件夹：{item['name']}")
                    else:
                        print(f"警告：文件夹不存在：{dest_path}")
                success_count += 1
                
        except (OSError, PermissionError, shutil.Error) as e:
            print(f"错误回滚 {item['name']}: {e}")
            error_count += 1
    
    print("-" * 60)
    print(f"回滚完成！成功回滚：{success_count} 个项目，错误：{error_count} 个")
    
    remove_record = input("\n是否从 log 中删除此条整理记录？(y/n): ").strip().lower()
    if remove_record in ['q', 'quit', '退出']:
        raise UserExitException("用户选择退出程序")
    if remove_record == 'y':
        history.pop(record_index)
        save_log_history(target_dir, history)
        print("已删除该条整理记录")
    
    return error_count == 0


def view_log_mode():
    print("=" * 60)
    print("文件分类整理程序 v3.5 - 查看日志")
    print("=" * 60)
    print()
    
    try:
        print("请选择要查看的日志位置:")
        print("1. 当前目录 (查看程序当前所在目录的日志)")
        print("2. 指定目录 (手动输入目录路径)")
        choice = get_valid_choice("请输入选项 (1/2): ", ['1', '2'])
        
        if choice == '1':
            target_dir = os.getcwd()
        else:
            target_dir = get_valid_directory("请输入目录路径：", must_exist=True)
        target_path = Path(target_dir).resolve()
        
        log_file = get_log_file_path(target_dir)
        if not log_file.exists():
            print(f"\n错误：log 文件不存在：{log_file}")
            print("该目录没有整理记录")
            return
        
        history = load_log_history(target_dir)
        if not history:
            print("\n错误：没有找到整理记录")
            return
        
        print(f"\n目录：{target_path}")
        print(f"找到 {len(history)} 条整理记录：")
        print("=" * 60)
        
        for i, record in enumerate(history):
            print(f"\n记录 {i + 1}:")
            print(f"时间：{record['timestamp']}")
            print(f"源目录：{record['source_directory']}")
            print(f"整理模式：{record['organize_mode']}")
            print(f"操作模式：{'移动' if record['move_files'] else '复制'}")
            print(f"处理项目：{record['processed_count']} 个")
            print()
            print("移动情况：")
            
            for j, item in enumerate(record['processed_items'], 1):
                print(f"  {j}. {item['name']}")
                print(f"     源路径：{item['source']}")
                print(f"     目标路径：{item['destination']}")
                print(f"     操作：{item['action']}")
                print()
            
            print("=" * 60)
        
        enter_rollback = get_valid_confirmation("\n是否进入回滚模式？(y/n): ")
        
        if enter_rollback:
            print()
            rollback_mode(target_dir)
    
    except UserExitException:
        print("\n程序已退出")


def rollback_mode(target_dir: str = None):
    print("=" * 60)
    print("文件分类整理程序 v3.5 - 回滚模式")
    print("=" * 60)
    print()
    
    try:
        if target_dir is None:
            print("请选择目标目录:")
            print("1. 使用当前目录 (使用程序当前所在目录)")
            print("2. 指定目录 (手动输入目录路径)")
            choice = get_valid_choice("请输入选项 (1/2): ", ['1', '2'])
            
            if choice == '1':
                target_dir = os.getcwd()
            else:
                target_dir = get_valid_directory("请输入目标目录路径：", must_exist=True)
        
        target_path = Path(target_dir).resolve()
        
        log_file = get_log_file_path(target_dir)
        if not log_file.exists():
            print(f"错误：log 文件不存在：{log_file}")
            print("该目录没有整理记录，无法回滚")
            return
        
        history = load_log_history(target_dir)
        if not history:
            print("错误：没有找到整理记录")
            return
        
        print("\n找到以下整理记录：")
        print("-" * 60)
        for i, record in enumerate(history):
            print(f"{i + 1}. 时间：{record['timestamp']}")
            print(f"   源目录：{record['source_directory']}")
            print(f"   整理模式：{record['organize_mode']}")
            print(f"   处理项目：{record['processed_count']} 个")
            print(f"   操作模式：{'移动' if record['move_files'] else '复制'}")
            print()
        
        print("-" * 60)
        
        while True:
            choice = input(f"请选择要回滚的记录编号 (1-{len(history)})，或输入 q 取消：").strip()
            
            if choice.lower() in ['q', 'quit', '退出']:
                print("已取消回滚操作")
                return
            
            try:
                record_index = int(choice) - 1
                if record_index < 0 or record_index >= len(history):
                    print(f"错误：无效的编号，请输入 1-{len(history)} 之间的数字，或输入 q 取消")
                    continue
                break
            except ValueError:
                print(f"错误：无效的输入，请输入 1-{len(history)} 之间的数字，或输入 q 取消")
        
        record = history[record_index]
        print(f"\n确认回滚操作：")
        print(f"回滚目标：{record['timestamp']} 的整理记录")
        print(f"源目录：{record['source_directory']}")
        print(f"整理模式：{record['organize_mode']}")
        print(f"操作模式：{'移动' if record['move_files'] else '复制'}")
        print()
        
        if record['move_files']:
            print("⚠️ 警告：回滚移动操作将会把文件移回源目录！")
        
        confirm = get_valid_confirmation("是否确认回滚？(y/n): ")
        
        if confirm:
            rollback_operation(target_dir, record_index)
        else:
            print("已取消回滚操作")
    
    except UserExitException:
        print("\n程序已退出")


def main():
    print("=" * 60)
    print("文件分类整理程序 v3.5")
    print("=" * 60)
    print()
    
    try:
        print("请选择操作模式：")
        print("1. 整理模式 (对文件进行分类整理)")
        print("2. 回滚模式 (基于 log 文件撤销整理操作)")
        print("3. 查看日志 (查看整理记录和文件移动情况)")
        mode = get_valid_choice("请输入选项 (1/2/3): ", ['1', '2', '3'])
        
        if mode == '2':
            rollback_mode()
            return
        elif mode == '3':
            view_log_mode()
            return
        
        print()
        print("请选择源目录：")
        print("1. 使用当前目录 (使用程序当前所在目录)")
        print("2. 指定目录 (手动输入目录路径)")
        choice = get_valid_choice("请输入选项 (1/2): ", ['1', '2'])
        
        if choice == '1':
            source_dir = os.getcwd()
        else:
            source_dir = get_valid_directory("请输入源目录路径：", must_exist=True)
        
        print()
        print("请选择目标目录：")
        print("1. 在源目录下创建新文件夹 (推荐，便于管理)")
        print("2. 指定目录 (手动输入目标目录路径)")
        choice = get_valid_choice("请输入选项 (1/2): ", ['1', '2'])
        
        if choice == '1':
            while True:
                folder_name = input("请输入新文件夹名称 (默认：organized_files): ").strip()
                if not folder_name:
                    folder_name = 'organized_files'
                
                target_dir = os.path.join(source_dir, folder_name)
                target_path = Path(target_dir)
                
                if target_path.exists():
                    print(f"警告：目录已存在：{target_dir}")
                    overwrite = get_valid_confirmation("是否使用该目录？(y/n): ")
                    if overwrite:
                        break
                else:
                    break
        else:
            while True:
                target_dir = get_valid_directory("请输入目标目录路径：", must_exist=False)
                target_path = Path(target_dir)
                
                if target_path.exists():
                    print(f"警告：目录已存在：{target_dir}")
                    overwrite = get_valid_confirmation("是否使用该目录？(y/n): ")
                    if overwrite:
                        break
                else:
                    break
        
        print()
        print("请选择整理模式：")
        print("1. 按照时间整理 (年/月/文件类型 三级目录)")
        print("2. 按照类型整理 (直接按文件类型分类)")
        mode_choice = get_valid_choice("请输入选项 (1/2): ", ['1', '2'])
        
        organize_mode = "按照时间整理" if mode_choice == '1' else "按照类型整理"
        
        print()
        process_folders = get_valid_confirmation("是否要处理源目录中的文件夹？(y/n): ")
        
        recursive = False
        if process_folders and mode_choice == '1':
            print()
            recursive = get_valid_confirmation("是否递归处理所有子文件夹中的文件？(y/n): ")
        
        print()
        print("请选择操作模式：")
        print("1. 复制文件 (保留原文件)")
        print("2. 移动文件 (原文件会被删除)")
        op_choice = get_valid_choice("请输入选项 (1/2): ", ['1', '2'])
        move_files = op_choice == '2'
        
        if move_files:
            print("\n警告：移动模式将会删除源文件，请确保已备份重要文件！")
        
        print()
        confirm = get_valid_confirmation(
            f"确认开始整理？\n源目录：{source_dir}\n目标目录：{target_dir}\n"
            f"整理模式：{organize_mode}\n处理文件夹：{process_folders}\n"
            f"递归处理：{recursive}\n操作模式：{'移动' if move_files else '复制'}\n请输入 y 确认："
        )
        
        if confirm:
            if mode_choice == '1':
                show_preview = process_folders and not recursive
                success, processed_items = organize_by_time(
                    source_dir, target_dir, process_folders, move_files, recursive, show_preview
                )
            else:
                success, processed_items = organize_by_type(
                    source_dir, target_dir, process_folders, move_files
                )
            
            if success:
                log_saved = create_log_record(
                    target_dir, source_dir, process_folders, 
                    move_files, organize_mode, processed_items
                )
                if not log_saved:
                    print("警告：log 文件保存失败，回滚功能可能无法使用")
        else:
            print("已取消操作")
    
    except UserExitException:
        print("\n程序已退出")


if __name__ == '__main__':
    main()
