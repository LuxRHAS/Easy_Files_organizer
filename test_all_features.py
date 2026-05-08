#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件分类整理程序 - 全面功能测试脚本
测试所有功能确保正常运行
"""

import os
import sys
import shutil
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

TEST_BASE_DIR = '/tmp/file_organizer_test'
TEST_SOURCE_DIR = f'{TEST_BASE_DIR}/test_source'
TEST_TARGET_DIR = f'{TEST_BASE_DIR}/test_target'
PROJECT_DIR = '/Users/fartherrhas/Code/Easy_Files_organizer'

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_pass(self, test_name, details=""):
        self.passed += 1
        self.tests.append(('✓', test_name, details))
        print(f"✓ 通过：{test_name}")
        if details:
            print(f"  {details}")
    
    def add_fail(self, test_name, error):
        self.failed += 1
        self.tests.append(('✗', test_name, error))
        print(f"✗ 失败：{test_name}")
        print(f"  错误：{error}")
    
    def summary(self):
        print("\n" + "="*60)
        print("测试总结")
        print("="*60)
        for status, name, detail in self.tests:
            print(f"{status} {name}")
            if detail and status == '✗':
                print(f"  {detail}")
        print("="*60)
        print(f"通过：{self.passed}, 失败：{self.failed}, 总计：{self.passed + self.failed}")
        return self.failed == 0


def cleanup_test_dirs():
    """清理测试目录"""
    if os.path.exists(TEST_BASE_DIR):
        shutil.rmtree(TEST_BASE_DIR)
    os.makedirs(TEST_SOURCE_DIR, exist_ok=True)


def create_test_files():
    """创建测试文件"""
    test_files = {
        'test1.jpg': '',
        'test2.png': '',
        'test3.mp4': '',
        'test4.avi': '',
        'test5.pdf': '',
        'test6.docx': '',
        'test7.txt': '',
        'test8.mp3': '',
        'test9.wav': '',
        'test10.exe': '',
        'test11.zip': '',
        'test12.rar': '',
    }
    
    for filename, content in test_files.items():
        filepath = os.path.join(TEST_SOURCE_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
    
    os.makedirs(os.path.join(TEST_SOURCE_DIR, 'folder1'), exist_ok=True)
    os.makedirs(os.path.join(TEST_SOURCE_DIR, 'folder2'), exist_ok=True)
    
    with open(os.path.join(TEST_SOURCE_DIR, 'folder1', 'nested1.jpg'), 'w') as f:
        f.write('')
    with open(os.path.join(TEST_SOURCE_DIR, 'folder1', 'nested2.pdf'), 'w') as f:
        f.write('')
    with open(os.path.join(TEST_SOURCE_DIR, 'folder2', 'nested3.mp4'), 'w') as f:
        f.write('')
    with open(os.path.join(TEST_SOURCE_DIR, 'folder2', 'nested4.txt'), 'w') as f:
        f.write('')
    
    print(f"已创建 {len(test_files)} 个测试文件和 2 个测试文件夹")


def run_organizer_with_input(inputs, timeout=30):
    """运行整理程序并提供输入"""
    input_str = '\n'.join(inputs) + '\n'
    try:
        result = subprocess.run(
            ['python3', 'file_organizer.py'],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=PROJECT_DIR
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1
    except Exception as e:
        return "", str(e), -1


def test_organize_by_time_copy(result):
    """测试按时间整理（复制模式）"""
    print("\n" + "="*60)
    print("测试 1: 按时间整理（复制模式）")
    print("="*60)
    
    cleanup_test_dirs()
    create_test_files()
    
    target_dir = os.path.join(TEST_BASE_DIR, 'test_target_time_copy')
    
    inputs = [
        '1',  # 整理模式
        '2',  # 指定源目录
        TEST_SOURCE_DIR,
        '2',  # 指定目标目录
        target_dir,
        '1',  # 按时间整理
        'n',  # 不处理文件夹
        '1',  # 复制模式
        'y',  # 确认
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    if returncode != 0:
        result.add_fail("按时间整理（复制模式）", f"返回码：{returncode}, 错误：{stderr}")
        return False
    
    if os.path.exists(os.path.join(target_dir, 'log.json')):
        result.add_pass("按时间整理（复制模式）", "成功创建 log.json")
    else:
        result.add_fail("按时间整理（复制模式）", "log.json 未创建")
        return False
    
    year = str(datetime.now().year)
    month = f"{datetime.now().month:02d}"
    expected_path = os.path.join(target_dir, year, month, '图片', 'test1.jpg')
    if os.path.exists(expected_path):
        result.add_pass("目录结构验证", f"找到文件：{expected_path}")
    else:
        result.add_fail("目录结构验证", f"文件不存在：{expected_path}")
        return False
    
    source_file = os.path.join(TEST_SOURCE_DIR, 'test1.jpg')
    if os.path.exists(source_file):
        result.add_pass("源文件保留", "复制模式保留了源文件")
    else:
        result.add_fail("源文件保留", "源文件被删除")
        return False
    
    return True


def test_organize_by_type_copy(result):
    """测试按类型整理（复制模式）"""
    print("\n" + "="*60)
    print("测试 2: 按类型整理（复制模式）")
    print("="*60)
    
    cleanup_test_dirs()
    create_test_files()
    
    target_dir = os.path.join(TEST_BASE_DIR, 'test_target_type_copy')
    
    inputs = [
        '1',  # 整理模式
        '2',  # 指定源目录
        TEST_SOURCE_DIR,
        '2',  # 指定目标目录
        target_dir,
        '2',  # 按类型整理
        'n',  # 不处理文件夹
        '1',  # 复制模式
        'y',  # 确认
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    if returncode != 0:
        result.add_fail("按类型整理（复制模式）", f"返回码：{returncode}, 错误：{stderr}")
        return False
    
    expected_paths = [
        os.path.join(target_dir, '图片', 'test1.jpg'),
        os.path.join(target_dir, '视频', 'test3.mp4'),
        os.path.join(target_dir, '文档', 'test5.pdf'),
        os.path.join(target_dir, '音频', 'test8.mp3'),
        os.path.join(target_dir, '应用程序', 'test10.exe'),
        os.path.join(target_dir, '压缩包', 'test11.zip'),
    ]
    
    all_exist = True
    for path in expected_paths:
        if not os.path.exists(path):
            result.add_fail("按类型整理（复制模式）", f"文件不存在：{path}")
            all_exist = False
    
    if all_exist:
        result.add_pass("按类型整理（复制模式）", "所有文件类型分类正确")
    
    return all_exist


def test_organize_by_time_move(result):
    """测试按时间整理（移动模式）"""
    print("\n" + "="*60)
    print("测试 3: 按时间整理（移动模式）")
    print("="*60)
    
    cleanup_test_dirs()
    create_test_files()
    
    target_dir = os.path.join(TEST_BASE_DIR, 'test_target_time_move')
    
    inputs = [
        '1',  # 整理模式
        '2',  # 指定源目录
        TEST_SOURCE_DIR,
        '2',  # 指定目标目录
        target_dir,
        '1',  # 按时间整理
        'n',  # 不处理文件夹
        '2',  # 移动模式
        'y',  # 确认
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    if returncode != 0:
        result.add_fail("按时间整理（移动模式）", f"返回码：{returncode}, 错误：{stderr}")
        return False
    
    year = str(datetime.now().year)
    month = f"{datetime.now().month:02d}"
    expected_path = os.path.join(target_dir, year, month, '图片', 'test1.jpg')
    if os.path.exists(expected_path):
        result.add_pass("按时间整理（移动模式）", f"文件已移动：{expected_path}")
    else:
        result.add_fail("按时间整理（移动模式）", f"文件不存在：{expected_path}")
        return False
    
    source_file = os.path.join(TEST_SOURCE_DIR, 'test1.jpg')
    if not os.path.exists(source_file):
        result.add_pass("源文件删除", "移动模式已删除源文件")
    else:
        result.add_fail("源文件删除", "源文件未被删除")
        return False
    
    return True


def test_folder_processing(result):
    """测试文件夹处理功能"""
    print("\n" + "="*60)
    print("测试 4: 文件夹处理功能")
    print("="*60)
    
    cleanup_test_dirs()
    create_test_files()
    
    target_dir = os.path.join(TEST_BASE_DIR, 'test_target_folders')
    
    inputs = [
        '1',  # 整理模式
        '2',  # 指定源目录
        TEST_SOURCE_DIR,
        '2',  # 指定目标目录
        target_dir,
        '2',  # 按类型整理
        'y',  # 处理文件夹
        '1',  # 复制模式
        'y',  # 确认
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    if returncode != 0:
        result.add_fail("文件夹处理", f"返回码：{returncode}, 错误：{stderr}")
        return False
    
    with open(os.path.join(target_dir, 'log.json'), 'r', encoding='utf-8') as f:
        log_data = json.load(f)
        if log_data['history'] and log_data['history'][0]['processed_count'] > 12:
            result.add_pass("文件夹处理", "文件夹及其内容被处理")
            return True
        else:
            result.add_fail("文件夹处理", "文件夹内容未被正确处理")
            return False


def test_view_log(result):
    """测试查看日志功能"""
    print("\n" + "="*60)
    print("测试 5: 查看日志功能")
    print("="*60)
    
    cleanup_test_dirs()
    create_test_files()
    
    target_dir = os.path.join(TEST_BASE_DIR, 'test_target_log')
    
    inputs = [
        '1',  # 整理模式
        '2',  # 指定源目录
        TEST_SOURCE_DIR,
        '2',  # 指定目标目录
        target_dir,
        '1',  # 按时间整理
        'n',  # 不处理文件夹
        '1',  # 复制模式
        'y',  # 确认
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    if not os.path.exists(os.path.join(target_dir, 'log.json')):
        result.add_fail("查看日志 - 准备", "log.json 未创建")
        return False
    
    inputs = [
        '3',  # 查看日志模式
        '2',  # 指定目录
        target_dir,
        'n',  # 不进入回滚
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    if '记录 1' in stdout or 'Record 1' in stdout:
        result.add_pass("查看日志功能", "成功显示整理记录")
        return True
    else:
        result.add_fail("查看日志功能", f"未显示记录，输出：{stdout[:200]}")
        return False


def test_rollback(result):
    """测试回滚功能"""
    print("\n" + "="*60)
    print("测试 6: 回滚功能")
    print("="*60)
    
    cleanup_test_dirs()
    create_test_files()
    
    target_dir = os.path.join(TEST_BASE_DIR, 'test_target_rollback')
    
    inputs = [
        '1',  # 整理模式
        '2',  # 指定源目录
        TEST_SOURCE_DIR,
        '2',  # 指定目标目录
        target_dir,
        '1',  # 按时间整理
        'n',  # 不处理文件夹
        '2',  # 移动模式
        'y',  # 确认
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    year = str(datetime.now().year)
    month = f"{datetime.now().month:02d}"
    moved_file = os.path.join(target_dir, year, month, '图片', 'test1.jpg')
    
    if not os.path.exists(moved_file):
        result.add_fail("回滚 - 准备", "文件未被移动")
        return False
    
    inputs = [
        '2',  # 回滚模式
        '2',  # 指定目录
        target_dir,
        '1',  # 选择第一条记录
        'y',  # 确认回滚
        'n',  # 不删除记录
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    source_file = os.path.join(TEST_SOURCE_DIR, 'test1.jpg')
    if os.path.exists(source_file):
        result.add_pass("回滚功能", "文件已成功回滚到源目录")
        return True
    else:
        result.add_fail("回滚功能", "文件未回滚")
        return False


def test_language_switch(result):
    """测试语言切换功能"""
    print("\n" + "="*60)
    print("测试 7: 语言切换功能")
    print("="*60)
    
    inputs = [
        '4',  # 切换语言
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    if 'Language changed' in stdout or '语言已切换' in stdout:
        result.add_pass("语言切换功能", "成功切换语言")
        
        inputs = [
            '4',  # 切换回中文
        ]
        stdout2, stderr2, returncode2 = run_organizer_with_input(inputs)
        
        if '语言已切换' in stdout2 or 'Language changed' in stdout2:
            result.add_pass("语言切换回中文", "成功切换回中文")
            return True
        else:
            result.add_fail("语言切换回中文", "切换回中文失败")
            return False
    else:
        result.add_fail("语言切换功能", "语言切换失败")
        return False


def test_exit_keywords(result):
    """测试退出关键词支持"""
    print("\n" + "="*60)
    print("测试 8: 退出关键词支持")
    print("="*60)
    
    inputs = ['q']
    stdout, stderr, returncode = run_organizer_with_input(inputs, timeout=10)
    
    if '退出' in stdout or 'exited' in stdout.lower():
        result.add_pass("退出关键词支持", "输入 q 成功退出")
        return True
    else:
        result.add_fail("退出关键词支持", "q 未能退出程序")
        return False


def test_input_validation(result):
    """测试输入验证"""
    print("\n" + "="*60)
    print("测试 9: 输入验证")
    print("="*60)
    
    inputs = [
        '999',  # 无效选项
        '1',    # 正确选项
        'q',    # 退出
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs, timeout=10)
    
    if '无效' in stdout or 'Invalid' in stdout:
        result.add_pass("输入验证", "正确拒绝无效输入")
        return True
    else:
        result.add_fail("输入验证", "未拒绝无效输入")
        return False


def test_self_file_skip(result):
    """测试程序自身文件跳过"""
    print("\n" + "="*60)
    print("测试 10: 程序自身文件跳过")
    print("="*60)
    
    cleanup_test_dirs()
    
    shutil.copy(os.path.join(PROJECT_DIR, 'file_organizer.py'), 
                os.path.join(TEST_SOURCE_DIR, 'file_organizer.py'))
    shutil.copy(os.path.join(PROJECT_DIR, 'README.md'), 
                os.path.join(TEST_SOURCE_DIR, 'README.md'))
    
    with open(os.path.join(TEST_SOURCE_DIR, 'test.jpg'), 'w') as f:
        f.write('')
    
    target_dir = os.path.join(TEST_BASE_DIR, 'test_target_skip')
    
    inputs = [
        '1',
        '2',
        TEST_SOURCE_DIR,
        '2',
        target_dir,
        '2',
        'n',
        '1',
        'y',
    ]
    
    stdout, stderr, returncode = run_organizer_with_input(inputs)
    
    if os.path.exists(os.path.join(target_dir, '图片', 'test.jpg')):
        if not os.path.exists(os.path.join(target_dir, '图片', 'file_organizer.py')):
            result.add_pass("程序自身文件跳过", "成功跳过 file_organizer.py")
            return True
        else:
            result.add_fail("程序自身文件跳过", "未跳过 file_organizer.py")
            return False
    else:
        result.add_fail("程序自身文件跳过", "test.jpg 未被整理")
        return False


def main():
    print("="*60)
    print("文件分类整理程序 - 全面功能测试")
    print("="*60)
    print(f"测试开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    result = TestResult()
    
    try:
        test_organize_by_time_copy(result)
        test_organize_by_type_copy(result)
        test_organize_by_time_move(result)
        test_folder_processing(result)
        test_view_log(result)
        test_rollback(result)
        test_language_switch(result)
        test_exit_keywords(result)
        test_input_validation(result)
        test_self_file_skip(result)
    except Exception as e:
        print(f"\n测试过程中发生异常：{e}")
        import traceback
        traceback.print_exc()
    
    success = result.summary()
    
    print(f"\n测试完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️ 有 {result.failed} 个测试失败，请检查问题")
        return 1


if __name__ == '__main__':
    sys.exit(main())
