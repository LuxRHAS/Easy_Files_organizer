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
CONFIG_FILENAME = 'config.json'


current_language = 'zh'


def load_language_config() -> str:
    """加载语言配置"""
    config_file = Path(CONFIG_FILENAME)
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('language', 'zh')
        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            return 'zh'
    return 'zh'


def save_language_config(language: str) -> bool:
    """保存语言配置"""
    config_file = Path(CONFIG_FILENAME)
    try:
        config = {}
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        config['language'] = language
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except (OSError, json.JSONEncodeError, TypeError):
        return False


TEXT = {}


def init_translations():
    """初始化翻译字典"""
    global TEXT
    TEXT = {
        'zh': {
            'app_title': '文件分类整理程序 v3.5',
            'app_title_view_log': '文件分类整理程序 v3.5 - 查看日志',
            'app_title_rollback': '文件分类整理程序 v3.5 - 回滚模式',
            'select_mode': '请选择操作模式：',
            'mode_organize': '整理模式 (对文件进行分类整理)',
            'mode_rollback': '回滚模式 (基于 log 文件撤销整理操作)',
            'mode_view_log': '查看日志 (查看整理记录和文件移动情况)',
            'mode_change_language': 'Change Language to English',
            'input_option': '请输入选项 ({options}): ',
            'select_source_dir': '请选择源目录：',
            'source_current_dir': '使用当前目录 (使用程序当前所在目录)',
            'source_custom_dir': '指定目录 (手动输入目录路径)',
            'select_target_dir': '请选择目标目录：',
            'target_in_source': '在源目录下创建新文件夹 (推荐，便于管理)',
            'target_custom_dir': '指定目录 (手动输入目标目录路径)',
            'input_folder_name': '请输入新文件夹名称 (默认：organized_files): ',
            'warning_dir_exists': '警告：目录已存在：{dir}',
            'confirm_use_dir': '是否使用该目录？(y/n): ',
            'select_organize_mode': '请选择整理模式：',
            'organize_by_time': '按照时间整理 (年/月/文件类型 三级目录)',
            'organize_by_type': '按照类型整理 (直接按文件类型分类)',
            'process_folders': '是否要处理源目录中的文件夹？(y/n): ',
            'recursive_process': '是否递归处理所有子文件夹中的文件？(y/n): ',
            'select_operation_mode': '请选择操作模式：',
            'op_copy': '复制文件 (保留原文件)',
            'op_move': '移动文件 (原文件会被删除)',
            'warning_move_mode': '警告：移动模式将会删除源文件，请确保已备份重要文件！',
            'confirm_start': '确认开始整理？',
            'source_directory': '源目录',
            'target_directory': '目标目录',
            'organize_mode_label': '整理模式',
            'process_folders_label': '处理文件夹',
            'recursive_label': '递归处理',
            'operation_mode_label': '操作模式',
            'input_confirm': '请输入 y 确认：',
            'cancel_operation': '已取消操作',
            'program_exited': '程序已退出',
            'log_updated': '已更新整理 log 文件：{file}',
            'log_save_error': '错误：保存 log 文件失败：{error}',
            'log_save_warning': '警告：log 文件保存失败，回滚功能可能无法使用',
            'created_target_dir': '已创建目标目录：{dir}',
            'error_target_dir': '错误：无法创建目标目录：{error}',
            'error_same_dir': '错误：源目录和目标目录不能相同',
            'start_processing': '开始处理源目录：{dir}',
            'target_dir_label': '目标目录',
            'process_folders_label_detail': '是否处理文件夹',
            'recursive_label_detail': '是否递归处理子文件夹',
            'operation_mode_label_detail': '操作模式',
            'will_recursive_process': '将递归处理所有子文件夹中的文件...',
            'skip_target_dir': '跳过目标目录：{name}',
            'skip_self_file': '跳过程序自身文件：{name}',
            'skip_excluded_file': '跳过排除的文件：{name}',
            'skip_unsupported_type': '跳过不支持的文件类型：{name}',
            'moved_file': '已移动：{name} -> {dest}',
            'copied_file': '已复制：{name} -> {dest}',
            'moved_folder': '已移动文件夹：{name} -> {dest}',
            'copied_folder': '已复制文件夹：{name} -> {dest}',
            'error_process_file': '错误处理文件 {name}: {error}',
            'error_process_folder': '错误处理文件夹 {name}: {error}',
            'process_completed': '处理完成！成功处理：{success} 个项目，错误：{error} 个',
            'folder_preview_title': '文件夹整理预览：',
            'folder_preview_content': '以下文件夹将被整理到：',
            'folder_preview_item': '  {name} -> {dest}',
            'confirm_start_organize': '是否确认开始整理？(y/n): ',
            'moved_empty_folder': '已移动空文件夹到：空文件夹/{name}',
            'deleted_empty_folder': '已删除空文件夹：{name}',
            'keep_empty_folder': '保留空文件夹：{name} (复制模式)',
            'error_process_empty_folder': '处理空文件夹时出错 {name}: {error}',
            'rollback_title': '开始回滚操作...',
            'rollback_target': '回滚目标：{target}',
            'rollback_mode': '整理模式：{mode}',
            'rollback_count': '处理项目数：{count}',
            'rollback_file': '已回滚文件：{name} -> {dest}',
            'rollback_folder': '已回滚文件夹：{name} -> {dest}',
            'delete_copied_file': '已删除复制的文件：{name}',
            'delete_copied_folder': '已删除复制的文件夹：{name}',
            'warning_file_not_exist': '警告：文件不存在，跳过：{path}',
            'warning_folder_not_exist': '警告：文件夹不存在：{path}',
            'error_rollback': '错误回滚 {name}: {error}',
            'rollback_completed': '回滚完成！成功回滚：{success} 个项目，错误：{error} 个',
            'remove_log_record': '是否从 log 中删除此条整理记录？(y/n): ',
            'log_record_removed': '已删除该条整理记录',
            'select_log_location': '请选择要查看的日志位置:',
            'log_current_dir': '当前目录 (查看程序当前所在目录的日志)',
            'log_custom_dir': '指定目录 (手动输入目录路径)',
            'error_log_not_exist': '错误：log 文件不存在：{file}',
            'no_log_records': '该目录没有整理记录',
            'error_no_records': '错误：没有找到整理记录',
            'log_location': '目录：{dir}',
            'log_records_found': '找到 {count} 条整理记录：',
            'log_record_title': '记录 {num}:',
            'log_time': '时间',
            'log_source_dir': '源目录',
            'log_organize_mode': '整理模式',
            'log_operation_mode': '操作模式',
            'log_process_count': '处理项目',
            'log_unit': '个',
            'log_move_details': '移动情况：',
            'log_item_num': '  {num}. {name}',
            'log_source_path': '     源路径',
            'log_dest_path': '     目标路径',
            'log_action': '     操作',
            'enter_rollback': '是否进入回滚模式？(y/n): ',
            'rollback_history_title': '找到以下整理记录：',
            'rollback_select_record': '请选择要回滚的记录编号 ({range})，或输入 q 取消：',
            'rollback_invalid_input': '错误：无效的编号，请输入 {range} 之间的数字，或输入 q 取消',
            'rollback_invalid_number': '错误：无效的输入，请输入 {range} 之间的数字，或输入 q 取消',
            'rollback_confirm_title': '确认回滚操作：',
            'rollback_source_dir': '源目录',
            'rollback_warning': '⚠️ 警告：回滚移动操作将会把文件移回源目录！',
            'rollback_confirm': '是否确认回滚？(y/n): ',
            'rollback_cancelled': '已取消回滚操作',
            'error_source_not_exist': '错误：源目录不存在：{dir}',
            'error_target_not_exist': '错误：目标目录不存在：{dir}',
            'error_invalid_option': '错误：无效的选项，请输入 {options} 中的一个',
            'error_path_not_exist': '错误：路径不存在：{path}',
            'error_path_not_dir': '错误：路径不是目录：{path}',
            'error_empty_path': '错误：路径不能为空',
            'input_path': '请输入目录路径：',
            'input_target_path': '请输入目标目录路径：',
            'input_source_path': '请输入源目录路径：',
            'select_rollback_target': '请选择目标目录:',
            'rollback_current_dir': '使用当前目录 (使用程序当前所在目录)',
            'rollback_custom_dir': '指定目录 (手动输入目录路径)',
            'error_log_not_exist_rollback': '该目录没有整理记录，无法回滚',
            'cancel_rollback': '已取消回滚操作',
            'language_changed': '语言已切换为 {lang}',
            'language_change_failed': '语言切换失败',
        },
        'en': {
            'app_title': 'File Organizer v3.5',
            'app_title_view_log': 'File Organizer v3.5 - View Log',
            'app_title_rollback': 'File Organizer v3.5 - Rollback Mode',
            'select_mode': 'Please select operation mode:',
            'mode_organize': 'Organize Mode (Organize files by classification)',
            'mode_rollback': 'Rollback Mode (Undo organization based on log file)',
            'mode_view_log': 'View Log (View organization records and file movements)',
            'mode_change_language': '切换语言到中文',
            'input_option': 'Please enter option ({options}): ',
            'select_source_dir': 'Please select source directory:',
            'source_current_dir': 'Use current directory (Use program\'s current directory)',
            'source_custom_dir': 'Custom directory (Manually enter directory path)',
            'select_target_dir': 'Please select target directory:',
            'target_in_source': 'Create new folder under source directory (Recommended)',
            'target_custom_dir': 'Custom directory (Manually enter target directory path)',
            'input_folder_name': 'Please enter new folder name (default: organized_files): ',
            'warning_dir_exists': 'Warning: Directory already exists: {dir}',
            'confirm_use_dir': 'Use this directory? (y/n): ',
            'select_organize_mode': 'Please select organization mode:',
            'organize_by_time': 'Organize by Time (Year/Month/File Type 3-level directory)',
            'organize_by_type': 'Organize by Type (Direct classification by file type)',
            'process_folders': 'Process folders in source directory? (y/n): ',
            'recursive_process': 'Recursively process files in all subfolders? (y/n): ',
            'select_operation_mode': 'Please select operation mode:',
            'op_copy': 'Copy files (Keep original files)',
            'op_move': 'Move files (Original files will be deleted)',
            'warning_move_mode': 'Warning: Move mode will delete source files, ensure backups!',
            'confirm_start': 'Confirm to start organization?',
            'source_directory': 'Source Directory',
            'target_directory': 'Target Directory',
            'organize_mode_label': 'Organization Mode',
            'process_folders_label': 'Process Folders',
            'recursive_label': 'Recursive Processing',
            'operation_mode_label': 'Operation Mode',
            'input_confirm': 'Please enter y to confirm: ',
            'cancel_operation': 'Operation cancelled',
            'program_exited': 'Program exited',
            'log_updated': 'Updated organization log file: {file}',
            'log_save_error': 'Error: Failed to save log file: {error}',
            'log_save_warning': 'Warning: Log file save failed, rollback may not work',
            'created_target_dir': 'Created target directory: {dir}',
            'error_target_dir': 'Error: Cannot create target directory: {error}',
            'error_same_dir': 'Error: Source and target directories cannot be same',
            'start_processing': 'Start processing source directory: {dir}',
            'target_dir_label': 'Target Directory',
            'process_folders_label_detail': 'Process Folders',
            'recursive_label_detail': 'Recursive Processing',
            'operation_mode_label_detail': 'Operation Mode',
            'will_recursive_process': 'Will recursively process files in all subfolders...',
            'skip_target_dir': 'Skip target directory: {name}',
            'skip_self_file': 'Skip program file: {name}',
            'skip_excluded_file': 'Skip excluded file: {name}',
            'skip_unsupported_type': 'Skip unsupported file type: {name}',
            'moved_file': 'Moved: {name} -> {dest}',
            'copied_file': 'Copied: {name} -> {dest}',
            'moved_folder': 'Moved folder: {name} -> {dest}',
            'copied_folder': 'Copied folder: {name} -> {dest}',
            'error_process_file': 'Error processing file {name}: {error}',
            'error_process_folder': 'Error processing folder {name}: {error}',
            'process_completed': 'Processing completed! Success: {success}, Errors: {error}',
            'folder_preview_title': 'Folder Organization Preview:',
            'folder_preview_content': 'Following folders will be organized to:',
            'folder_preview_item': '  {name} -> {dest}',
            'confirm_start_organize': 'Confirm to start organization? (y/n): ',
            'moved_empty_folder': 'Moved empty folder to: Empty Folders/{name}',
            'deleted_empty_folder': 'Deleted empty folder: {name}',
            'keep_empty_folder': 'Keep empty folder: {name} (Copy mode)',
            'error_process_empty_folder': 'Error processing empty folder {name}: {error}',
            'rollback_title': 'Start rollback operation...',
            'rollback_target': 'Rollback target: {target}',
            'rollback_mode': 'Organization mode: {mode}',
            'rollback_count': 'Number of items: {count}',
            'rollback_file': 'Rolled back file: {name} -> {dest}',
            'rollback_folder': 'Rolled back folder: {name} -> {dest}',
            'delete_copied_file': 'Deleted copied file: {name}',
            'delete_copied_folder': 'Deleted copied folder: {name}',
            'warning_file_not_exist': 'Warning: File not found, skipping: {path}',
            'warning_folder_not_exist': 'Warning: Folder not found: {path}',
            'error_rollback': 'Error rolling back {name}: {error}',
            'rollback_completed': 'Rollback completed! Success: {success}, Errors: {error}',
            'remove_log_record': 'Delete this organization record from log? (y/n): ',
            'log_record_removed': 'Organization record deleted',
            'select_log_location': 'Please select log location:',
            'log_current_dir': 'Current directory (View log in program\'s current directory)',
            'log_custom_dir': 'Custom directory (Manually enter directory path)',
            'error_log_not_exist': 'Error: Log file not found: {file}',
            'no_log_records': 'No organization records in this directory',
            'error_no_records': 'Error: No organization records found',
            'log_location': 'Directory: {dir}',
            'log_records_found': 'Found {count} organization record(s):',
            'log_record_title': 'Record {num}:',
            'log_time': 'Time',
            'log_source_dir': 'Source Directory',
            'log_organize_mode': 'Organization Mode',
            'log_operation_mode': 'Operation Mode',
            'log_process_count': 'Items',
            'log_unit': '',
            'log_move_details': 'Movement Details:',
            'log_item_num': '  {num}. {name}',
            'log_source_path': '     Source Path',
            'log_dest_path': '     Destination Path',
            'log_action': '     Action',
            'enter_rollback': 'Enter rollback mode? (y/n): ',
            'rollback_history_title': 'Found following organization records:',
            'rollback_select_record': 'Please select record number ({range}), or enter q to cancel: ',
            'rollback_invalid_input': 'Error: Invalid number, enter number between {range}, or q to cancel',
            'rollback_invalid_number': 'Error: Invalid input, enter number between {range}, or q to cancel',
            'rollback_confirm_title': 'Confirm rollback operation:',
            'rollback_source_dir': 'Source Directory',
            'rollback_warning': '⚠️ Warning: Rollback will move files back to source directory!',
            'rollback_confirm': 'Confirm rollback? (y/n): ',
            'rollback_cancelled': 'Rollback cancelled',
            'error_source_not_exist': 'Error: Source directory not found: {dir}',
            'error_target_not_exist': 'Error: Target directory not found: {dir}',
            'error_invalid_option': 'Error: Invalid option, enter one of {options}',
            'error_path_not_exist': 'Error: Path does not exist: {path}',
            'error_path_not_dir': 'Error: Path is not a directory: {path}',
            'error_empty_path': 'Error: Path cannot be empty',
            'input_path': 'Please enter directory path: ',
            'input_target_path': 'Please enter target directory path: ',
            'input_source_path': 'Please enter source directory path: ',
            'select_rollback_target': 'Please select target directory:',
            'rollback_current_dir': 'Use current directory (Use program\'s current directory)',
            'rollback_custom_dir': 'Custom directory (Manually enter directory path)',
            'error_log_not_exist_rollback': 'No organization records in this directory, cannot rollback',
            'cancel_rollback': 'Rollback cancelled',
            'language_changed': 'Language changed to {lang}',
            'language_change_failed': 'Failed to change language',
        }
    }


def get_text(key: str) -> str:
    """获取翻译文本"""
    return TEXT.get(current_language, TEXT['zh']).get(key, key)


def format_text(key: str, **kwargs) -> str:
    """获取格式化的翻译文本"""
    text = get_text(key)
    return text.format(**kwargs)


# 初始化翻译字典
init_translations()


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
        
        print(format_text('error_invalid_option', options='/'.join(valid_choices)) + ("，或输入 q 退出" if allow_quit else ""))


def get_valid_directory(prompt: str, must_exist: bool = True, allow_quit: bool = True) -> str:
    while True:
        dir_path = input(prompt).strip()
        
        if allow_quit and dir_path.lower() in ['q', 'quit', '退出']:
            raise UserExitException("用户选择退出程序")
        
        if not dir_path:
            print(format_text('error_empty_path') + ("，或输入 q 退出" if allow_quit else ""))
            continue
        
        path = Path(dir_path)
        if must_exist and not path.exists():
            print(format_text('error_path_not_exist', path=dir_path) + ("，或输入 q 退出" if allow_quit else ""))
            continue
        
        if must_exist and not path.is_dir():
            print(format_text('error_path_not_dir', path=dir_path) + ("，或输入 q 退出" if allow_quit else ""))
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
        
        print(format_text('input_confirm').replace('Please enter y to confirm: ', '').replace('请输入 y 确认：', '') + ("，或输入 q 退出" if allow_quit else ""))


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

        print(format_text('log_updated', file=str(get_log_file_path(target_dir))))
        return True
    except (OSError, json.JSONEncodeError, TypeError) as e:
        print(format_text('log_save_error', error=str(e)))
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
                print(format_text('error_process_file', name=item.name, error=str(e)))
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
                        print(format_text('moved_empty_folder', name=dest_empty.name))
                        processed_items.append({
                            'type': 'folder',
                            'name': item.name,
                            'destination': f"空文件夹/{dest_empty.name}",
                            'action': format_text('op_move'),
                            'source': str(item)
                        })
                    elif move_files:
                        shutil.rmtree(str(item))
                        print(format_text('deleted_empty_folder', name=item.name))
                    else:
                        print(format_text('keep_empty_folder', name=item.name))
            except (OSError, PermissionError, shutil.Error) as e:
                print(format_text('error_process_empty_folder', name=item.name, error=str(e)))
    
    return processed_count, error_count


def organize_by_time(source_dir: str, target_dir: str, process_folders: bool, 
                    move_files: bool, recursive: bool = False, 
                    show_preview: bool = False) -> tuple:
    source_path = Path(source_dir).resolve()
    target_path = Path(target_dir).resolve()
    
    if not source_path.exists():
        print(format_text('error_source_not_exist', dir=str(source_path)))
        return False, []
    
    if not target_path.exists():
        try:
            target_path.mkdir(parents=True, exist_ok=True)
            print(format_text('created_target_dir', dir=str(target_path)))
        except Exception as e:
            print(format_text('error_target_dir', error=str(e)))
            return False, []
    
    if source_path == target_path:
        print(format_text('error_same_dir'))
        return False, []
    
    processed_count = 0
    error_count = 0
    action = format_text('op_move') if move_files else format_text('op_copy')
    processed_items = []
    
    print(format_text('start_processing', dir=str(source_path)))
    print(format_text('target_dir_label') + ": " + str(target_path))
    print(format_text('process_folders_label_detail') + ": " + str(process_folders))
    print(format_text('recursive_label_detail') + ": " + str(recursive))
    print(format_text('operation_mode_label_detail') + ": " + action)
    print("-" * 60)
    
    empty_folder_target = None
    if process_folders and move_files:
        empty_folder_target = target_path / "空文件夹"
    
    if process_folders and show_preview:
        print(format_text('folder_preview_title'))
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
                preview_items.append(format_text('folder_preview_item', name=item.name, dest=str(dest_folder.relative_to(target_path))))
        
        if preview_items:
            print(format_text('folder_preview_content'))
            for preview in preview_items:
                print(preview)
            print()
            
            confirm = input(format_text('confirm_start_organize')).strip().lower()
            if confirm in ['q', 'quit', '退出']:
                raise UserExitException("用户选择退出程序")
            if confirm != 'y':
                print(format_text('cancel_operation'))
                return False, []
        print("-" * 60)
    
    if process_folders and recursive:
        print(format_text('will_recursive_process'))
        processed_count, error_count = process_folder_recursive_time(
            source_path, target_path, move_files, processed_items, empty_folder_target
        )
    else:
        for item in source_path.iterdir():
            if item.resolve() == target_path or is_path_relative_to(item.resolve(), target_path):
                print(format_text('skip_target_dir', name=item.name))
                continue
            if is_self_file(str(item)):
                print(format_text('skip_self_file', name=item.name))
                continue
            
            if item.is_file():
                if should_exclude_file(str(item)):
                    print(format_text('skip_excluded_file', name=item.name))
                    continue
                
                file_type = get_file_type(str(item))
                if file_type is None:
                    print(format_text('skip_unsupported_type', name=item.name))
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
                        print(format_text('moved_file', name=item.name, dest=str(dest_folder.relative_to(target_path) / dest_file.name)))
                    else:
                        shutil.copy2(str(item), str(dest_file))
                        print(format_text('copied_file', name=item.name, dest=str(dest_folder.relative_to(target_path) / dest_file.name)))
                    
                    processed_items.append({
                        'type': 'file',
                        'name': item.name,
                        'destination': str(dest_folder.relative_to(target_path) / dest_file.name),
                        'action': format_text('op_move') if move_files else format_text('op_copy'),
                        'source': str(item)
                    })
                    processed_count += 1
                    
                except (OSError, PermissionError, shutil.Error) as e:
                    print(format_text('error_process_file', name=item.name, error=str(e)))
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
                        print(format_text('moved_folder', name=item.name, dest=str(dest_folder.relative_to(target_path) / dest_dir.name)))
                    else:
                        shutil.copytree(str(item), str(dest_dir))
                        print(format_text('copied_folder', name=item.name, dest=str(dest_folder.relative_to(target_path) / dest_dir.name)))
                    
                    processed_items.append({
                        'type': 'folder',
                        'name': item.name,
                        'destination': str(dest_folder.relative_to(target_path) / dest_dir.name),
                        'action': format_text('op_move') if move_files else format_text('op_copy'),
                        'source': str(item)
                    })
                    processed_count += 1
                    
                except (OSError, PermissionError, shutil.Error) as e:
                    print(format_text('error_process_folder', name=item.name, error=str(e)))
                    error_count += 1
    
    print("-" * 60)
    print(format_text('process_completed', success=processed_count, error=error_count))
    
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
                    print(format_text('moved_file', name=item.name, dest=f"{file_type}/{dest_file.name}"))
                else:
                    shutil.copy2(str(item), str(dest_file))
                    print(format_text('copied_file', name=item.name, dest=f"{file_type}/{dest_file.name}"))
                
                processed_items.append({
                    'type': 'file',
                    'name': item.name,
                    'destination': f"{file_type}/{dest_file.name}",
                    'action': format_text('op_move') if move_files else format_text('op_copy'),
                    'source': str(item)
                })
                processed_count += 1
                
            except (OSError, PermissionError, shutil.Error) as e:
                print(format_text('error_process_file', name=item.name, error=str(e)))
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
                        print(format_text('moved_empty_folder', name=dest_empty.name))
                        processed_items.append({
                            'type': 'folder',
                            'name': item.name,
                            'destination': f"空文件夹/{dest_empty.name}",
                            'action': format_text('op_move'),
                            'source': str(item)
                        })
                    elif move_files:
                        shutil.rmtree(str(item))
                        print(format_text('deleted_empty_folder', name=item.name))
                    else:
                        print(format_text('keep_empty_folder', name=item.name))
            except (OSError, PermissionError, shutil.Error) as e:
                print(format_text('error_process_empty_folder', name=item.name, error=str(e)))

    return processed_count, error_count


def organize_by_type(source_dir: str, target_dir: str, process_folders: bool, 
                    move_files: bool) -> tuple:
    source_path = Path(source_dir).resolve()
    target_path = Path(target_dir).resolve()
    
    if not source_path.exists():
        print(format_text('error_source_not_exist', dir=str(source_path)))
        return False, []
    
    if not target_path.exists():
        try:
            target_path.mkdir(parents=True, exist_ok=True)
            print(format_text('created_target_dir', dir=str(target_path)))
        except Exception as e:
            print(format_text('error_target_dir', error=str(e)))
            return False, []
    
    if source_path == target_path:
        print(format_text('error_same_dir'))
        return False, []
    
    processed_count = 0
    error_count = 0
    action = format_text('op_move') if move_files else format_text('op_copy')
    processed_items = []
    
    print(format_text('start_processing', dir=str(source_path)))
    print(format_text('target_dir_label') + ": " + str(target_path))
    print(format_text('process_folders_label_detail') + ": " + str(process_folders))
    print(format_text('operation_mode_label_detail') + ": " + action)
    print("-" * 60)
    
    if process_folders:
        print(format_text('will_recursive_process'))
        processed_count, error_count = process_folder_recursive(
            source_path, target_path, get_simple_file_type, move_files, processed_items
        )
    else:
        for item in source_path.iterdir():
            if item.resolve() == target_path or is_path_relative_to(item.resolve(), target_path):
                print(format_text('skip_target_dir', name=item.name))
                continue
            if is_self_file(str(item)):
                print(format_text('skip_self_file', name=item.name))
                continue
            
            if item.is_file():
                if should_exclude_file(str(item)):
                    print(format_text('skip_excluded_file', name=item.name))
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
                        print(format_text('moved_file', name=item.name, dest=f"{file_type}/{dest_file.name}"))
                    else:
                        shutil.copy2(str(item), str(dest_file))
                        print(format_text('copied_file', name=item.name, dest=f"{file_type}/{dest_file.name}"))
                    
                    processed_items.append({
                        'type': 'file',
                        'name': item.name,
                        'destination': f"{file_type}/{dest_file.name}",
                        'action': format_text('op_move') if move_files else format_text('op_copy'),
                        'source': str(item)
                    })
                    processed_count += 1
                    
                except (OSError, PermissionError, shutil.Error) as e:
                    print(format_text('error_process_file', name=item.name, error=str(e)))
                    error_count += 1
    
    print("-" * 60)
    print(format_text('process_completed', success=processed_count, error=error_count))
    
    return True, processed_items


def rollback_operation(target_dir: str, record_index: int) -> bool:
    log_file = get_log_file_path(target_dir)
    if not log_file.exists():
        print(format_text('error_log_not_exist', file=str(log_file)))
        return False
    
    history = load_log_history(target_dir)
    if not history:
        print(format_text('error_no_records'))
        return False
    
    if record_index < 0 or record_index >= len(history):
        print(format_text('error_invalid_option', options='1-' + str(len(history))))
        return False
    
    record = history[record_index]
    target_path = Path(target_dir).resolve()
    
    print(format_text('rollback_title'))
    print(format_text('rollback_target', target=record['timestamp']))
    print(format_text('rollback_mode', mode=record['organize_mode']))
    print(format_text('rollback_count', count=record['processed_count']))
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    
    for item in reversed(record['processed_items']):
        try:
            dest_path = target_path / item['destination']
            
            if not dest_path.exists():
                print(format_text('warning_file_not_exist', path=str(dest_path)))
                continue
            
            if item['type'] == 'file':
                if item['action'] == format_text('op_move'):
                    source_path = Path(item['source'])
                    source_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dest_path), str(source_path))
                    print(format_text('rollback_file', name=item['name'], dest=str(source_path)))
                else:
                    dest_path.unlink()
                    print(format_text('delete_copied_file', name=item['name']))
                success_count += 1
                
            elif item['type'] == 'folder':
                if item['action'] == format_text('op_move'):
                    source_path = Path(item['source'])
                    if dest_path.is_dir():
                        source_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(dest_path), str(source_path))
                        print(format_text('rollback_folder', name=item['name'], dest=str(source_path)))
                    else:
                        print(format_text('warning_folder_not_exist', path=str(dest_path)))
                else:
                    if dest_path.is_dir():
                        shutil.rmtree(str(dest_path))
                        print(format_text('delete_copied_folder', name=item['name']))
                    else:
                        print(format_text('warning_folder_not_exist', path=str(dest_path)))
                success_count += 1
                
        except (OSError, PermissionError, shutil.Error) as e:
            print(format_text('error_rollback', name=item['name'], error=str(e)))
            error_count += 1
    
    print("-" * 60)
    print(format_text('rollback_completed', success=success_count, error=error_count))
    
    remove_record = input(format_text('remove_log_record')).strip().lower()
    if remove_record in ['q', 'quit', '退出']:
        raise UserExitException("用户选择退出程序")
    if remove_record == 'y':
        history.pop(record_index)
        save_log_history(target_dir, history)
        print(format_text('log_record_removed'))
    
    return error_count == 0


def view_log_mode():
    print("=" * 60)
    print(format_text('app_title_view_log'))
    print("=" * 60)
    print()
    
    try:
        print(format_text('select_log_location'))
        print("1. " + format_text('log_current_dir'))
        print("2. " + format_text('log_custom_dir'))
        choice = get_valid_choice(format_text('input_option', options='1/2'), ['1', '2'])
        
        if choice == '1':
            target_dir = os.getcwd()
        else:
            target_dir = get_valid_directory(format_text('input_path'), must_exist=True)
        target_path = Path(target_dir).resolve()
        
        log_file = get_log_file_path(target_dir)
        if not log_file.exists():
            print(format_text('error_log_not_exist', file=str(log_file)))
            print(format_text('no_log_records'))
            return
        
        history = load_log_history(target_dir)
        if not history:
            print(format_text('error_no_records'))
            return
        
        print(format_text('log_location', dir=str(target_path)))
        print(format_text('log_records_found', count=len(history)))
        print("=" * 60)
        
        for i, record in enumerate(history):
            print(format_text('log_record_title', num=i + 1))
            print(format_text('log_time') + ": " + record['timestamp'])
            print(format_text('log_source_dir') + ": " + record['source_directory'])
            print(format_text('log_organize_mode') + ": " + record['organize_mode'])
            print(format_text('log_operation_mode') + ": " + (format_text('op_move') if record['move_files'] else format_text('op_copy')))
            print(format_text('log_process_count') + ": " + str(record['processed_count']) + format_text('log_unit'))
            print()
            print(format_text('log_move_details'))
            
            for j, item in enumerate(record['processed_items'], 1):
                print(format_text('log_item_num', num=j, name=item['name']))
                print(format_text('log_source_path') + ": " + item['source'])
                print(format_text('log_dest_path') + ": " + item['destination'])
                print(format_text('log_action') + ": " + item['action'])
                print()
            
            print("=" * 60)
        
        enter_rollback = get_valid_confirmation(format_text('enter_rollback'))
        
        if enter_rollback:
            print()
            rollback_mode(target_dir)
    
    except UserExitException:
        print(format_text('program_exited'))


def rollback_mode(target_dir: str = None):
    print("=" * 60)
    print(format_text('app_title_rollback'))
    print("=" * 60)
    print()
    
    try:
        if target_dir is None:
            print(format_text('select_rollback_target'))
            print("1. " + format_text('rollback_current_dir'))
            print("2. " + format_text('rollback_custom_dir'))
            choice = get_valid_choice(format_text('input_option', options='1/2'), ['1', '2'])
            
            if choice == '1':
                target_dir = os.getcwd()
            else:
                target_dir = get_valid_directory(format_text('input_target_path'), must_exist=True)
        
        target_path = Path(target_dir).resolve()
        
        log_file = get_log_file_path(target_dir)
        if not log_file.exists():
            print(format_text('error_log_not_exist', file=str(log_file)))
            print(format_text('error_log_not_exist_rollback'))
            return
        
        history = load_log_history(target_dir)
        if not history:
            print(format_text('error_no_records'))
            return
        
        print(format_text('rollback_history_title'))
        print("-" * 60)
        for i, record in enumerate(history):
            print(f"{i + 1}. " + format_text('log_time') + ": " + record['timestamp'])
            print("   " + format_text('log_source_dir') + ": " + record['source_directory'])
            print("   " + format_text('log_organize_mode') + ": " + record['organize_mode'])
            print("   " + format_text('log_process_count') + ": " + str(record['processed_count']) + format_text('log_unit'))
            print("   " + format_text('log_operation_mode') + ": " + (format_text('op_move') if record['move_files'] else format_text('op_copy')))
            print()
        
        print("-" * 60)
        
        while True:
            choice = input(format_text('rollback_select_record', range='1-' + str(len(history)))).strip()
            
            if choice.lower() in ['q', 'quit', '退出']:
                print(format_text('rollback_cancelled'))
                return
            
            try:
                record_index = int(choice) - 1
                if record_index < 0 or record_index >= len(history):
                    print(format_text('rollback_invalid_input', range='1-' + str(len(history))))
                    continue
                break
            except ValueError:
                print(format_text('rollback_invalid_number', range='1-' + str(len(history))))
        
        record = history[record_index]
        print(format_text('rollback_confirm_title'))
        print(format_text('rollback_target', target=record['timestamp']))
        print(format_text('rollback_source_dir') + ": " + record['source_directory'])
        print(format_text('log_organize_mode') + ": " + record['organize_mode'])
        print(format_text('log_operation_mode') + ": " + (format_text('op_move') if record['move_files'] else format_text('op_copy')))
        print()
        
        if record['move_files']:
            print(format_text('rollback_warning'))
        
        confirm = get_valid_confirmation(format_text('rollback_confirm'))
        
        if confirm:
            rollback_operation(target_dir, record_index)
        else:
            print(format_text('rollback_cancelled'))
    
    except UserExitException:
        print(format_text('program_exited'))


def main():
    global current_language
    current_language = load_language_config()
    
    print("=" * 60)
    print(format_text('app_title'))
    print("=" * 60)
    print()
    
    try:
        while True:
            print(format_text('select_mode'))
            print("1. " + format_text('mode_organize'))
            print("2. " + format_text('mode_rollback'))
            print("3. " + format_text('mode_view_log'))
            print("4. " + format_text('mode_change_language'))
            mode = get_valid_choice(format_text('input_option', options='1/2/3/4'), ['1', '2', '3', '4'])
            
            if mode == '4':
                new_lang = 'en' if current_language == 'zh' else 'zh'
                if save_language_config(new_lang):
                    current_language = new_lang
                    lang_name = 'English' if new_lang == 'en' else '中文'
                    print(format_text('language_changed', lang=lang_name))
                    print()
                else:
                    print(format_text('language_change_failed'))
                    print()
                continue
            
            break
        
        if mode == '2':
            rollback_mode()
            return
        elif mode == '3':
            view_log_mode()
            return
        
        print()
        print(format_text('select_source_dir'))
        print("1. " + format_text('source_current_dir'))
        print("2. " + format_text('source_custom_dir'))
        choice = get_valid_choice(format_text('input_option', options='1/2'), ['1', '2'])
        
        if choice == '1':
            source_dir = os.getcwd()
        else:
            source_dir = get_valid_directory(format_text('input_source_path'), must_exist=True)
        
        print()
        print(format_text('select_target_dir'))
        print("1. " + format_text('target_in_source'))
        print("2. " + format_text('target_custom_dir'))
        choice = get_valid_choice(format_text('input_option', options='1/2'), ['1', '2'])
        
        if choice == '1':
            while True:
                folder_name = input(format_text('input_folder_name')).strip()
                if not folder_name:
                    folder_name = 'organized_files'
                
                target_dir = os.path.join(source_dir, folder_name)
                target_path = Path(target_dir)
                
                if target_path.exists():
                    print(format_text('warning_dir_exists', dir=target_dir))
                    overwrite = get_valid_confirmation(format_text('confirm_use_dir'))
                    if overwrite:
                        break
                else:
                    break
        else:
            while True:
                target_dir = get_valid_directory(format_text('input_target_path'), must_exist=False)
                target_path = Path(target_dir)
                
                if target_path.exists():
                    print(format_text('warning_dir_exists', dir=target_dir))
                    overwrite = get_valid_confirmation(format_text('confirm_use_dir'))
                    if overwrite:
                        break
                else:
                    break
        
        print()
        print(format_text('select_organize_mode'))
        print("1. " + format_text('organize_by_time'))
        print("2. " + format_text('organize_by_type'))
        mode_choice = get_valid_choice(format_text('input_option', options='1/2'), ['1', '2'])
        
        organize_mode_key = 'organize_by_time' if mode_choice == '1' else 'organize_by_type'
        organize_mode = format_text(organize_mode_key)
        
        print()
        process_folders = get_valid_confirmation(format_text('process_folders'))
        
        recursive = False
        if process_folders and mode_choice == '1':
            print()
            recursive = get_valid_confirmation(format_text('recursive_process'))
        
        print()
        print(format_text('select_operation_mode'))
        print("1. " + format_text('op_copy'))
        print("2. " + format_text('op_move'))
        op_choice = get_valid_choice(format_text('input_option', options='1/2'), ['1', '2'])
        move_files = op_choice == '2'
        
        if move_files:
            print("\n" + format_text('warning_move_mode'))
        
        print()
        confirm = get_valid_confirmation(
            format_text('confirm_start') + "\n" +
            format_text('source_directory') + ": " + source_dir + "\n" +
            format_text('target_directory') + ": " + target_dir + "\n" +
            format_text('organize_mode_label') + ": " + organize_mode + "\n" +
            format_text('process_folders_label') + ": " + str(process_folders) + "\n" +
            format_text('recursive_label') + ": " + str(recursive) + "\n" +
            format_text('operation_mode_label') + ": " + (format_text('op_move') if move_files else format_text('op_copy')) + "\n" +
            format_text('input_confirm')
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
                    print(format_text('log_save_warning'))
        else:
            print(format_text('cancel_operation'))
    
    except UserExitException:
        print(format_text('program_exited'))


if __name__ == '__main__':
    main()
