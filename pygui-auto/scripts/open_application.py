#!/usr/bin/env python3
"""
Open Application - Launch applications by name or path

Usage:
    python open_application.py --app "Notepad"
    python open_application.py --path "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
"""

import sys
import subprocess
import argparse
import time
import os
import webbrowser

try:
    import win32gui
    import win32con
    import psutil
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

try:
    import win32com.client
    HAS_WIN32COM = True
except ImportError:
    HAS_WIN32COM = False


def resolve_shortcut(shortcut_path):
    """
    Resolve Windows shortcut (.lnk) to its target path.

    Args:
        shortcut_path: Path to the .lnk file

    Returns:
        Target path if successful, None otherwise
    """
    if not HAS_WIN32COM:
        return None

    if not shortcut_path.lower().endswith('.lnk'):
        return None

    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        target_path = shortcut.Targetpath

        if target_path and os.path.exists(target_path):
            print(f"  📁 解析快捷方式: {shortcut_path}")
            print(f"  ➡️  目标文件: {target_path}")
            return target_path
        else:
            print(f"  ⚠️  快捷方式目标不存在: {target_path}")
            return None
    except Exception as e:
        print(f"  ⚠️  解析快捷方式失败: {e}")
        return None


def kill_existing_process(app_path):
    """
    Kill existing process if running.
    
    Args:
        app_path: Full path to the executable
    """
    if not HAS_WIN32:
        return
    
    try:
        app_name = os.path.basename(app_path)
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == app_name:
                print(f"  终止现有进程 PID: {proc.info['pid']}")
                proc.kill()
        time.sleep(1)
    except Exception as e:
        pass


def activate_window_by_keywords(keywords):
    """
    Find and activate window by keywords in title.
    
    Args:
        keywords: List of keywords to search in window title
    """
    if not HAS_WIN32:
        return False
    
    try:
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and any(keyword in title for keyword in keywords):
                    windows.append((hwnd, title))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            for hwnd, title in windows:
                try:
                    win32gui.SetForegroundWindow(hwnd)
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    print(f"  ✅ 已激活窗口: {title}")
                    return True
                except Exception as e:
                    pass
    except Exception as e:
        pass
    
    return False


def open_application_by_name(app_name):
    """
    Open application by name using Windows start command.

    Args:
        app_name: Name of the application (e.g., "Notepad", "Chrome", "calc")
    """
    try:
        subprocess.Popen(['start', app_name], shell=True)
        print(f"✅ Opening application: {app_name}")
        
        if HAS_WIN32:
            time.sleep(2)
            keywords = [app_name]
            activate_window_by_keywords(keywords)
        
        return True
    except Exception as e:
        print(f"❌ Error opening {app_name}: {e}")
        return False


def is_url(path):
    """
    Check if the path is a URL (browser link).

    Args:
        path: Path or URL string

    Returns:
        True if it's a URL, False otherwise
    """
    url_prefixes = ['http://', 'https://', 'www.']
    return any(path.lower().startswith(prefix) for prefix in url_prefixes)


def open_url_in_browser(url):
    """
    Open URL in default browser.

    Args:
        url: URL to open
    """
    try:
        print(f"🌐 检测到浏览器链接，正在打开...")
        print(f"  📎 URL: {url}")
        webbrowser.open(url)
        print(f"  ✅ 已在默认浏览器中打开")
        return True
    except Exception as e:
        print(f"  ❌ 打开浏览器失败: {e}")
        return False


def open_application_by_path(app_path):
    """
    Open application by full executable path with window activation.
    For URLs, opens in default browser without window management.

    Args:
        app_path: Full path to the executable, shortcut, or URL (e.g., "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", "C:\\Users\\User\\Desktop\\app.lnk", or "https://www.example.com")
    """
    try:
        if is_url(app_path):
            return open_url_in_browser(app_path)

        actual_path = app_path

        if app_path.lower().endswith('.lnk'):
            print(f"检测到快捷方式，正在解析...")
            resolved_path = resolve_shortcut(app_path)
            if resolved_path:
                actual_path = resolved_path
            else:
                print(f"⚠️  无法解析快捷方式，尝试直接打开")

        print(f"步骤1: 检查并终止现有进程...")
        kill_existing_process(actual_path)

        print(f"步骤2: 启动程序: {actual_path}")
        subprocess.Popen([actual_path], shell=True)
        print(f"  ✅ 程序已启动")

        if HAS_WIN32:
            print(f"步骤3: 等待窗口加载...")
            time.sleep(3)

            print(f"步骤4: 查找并激活窗口...")
            app_name = os.path.basename(actual_path)
            keywords = [os.path.splitext(app_name)[0], app_name]

            if activate_window_by_keywords(keywords):
                print(f"✅ 程序已成功打开并显示")
            else:
                print(f"⚠️  程序已启动，但未找到窗口")
        else:
            print(f"⚠️  未安装 pywin32/psutil，无法激活窗口")
            print(f"   安装命令: pip install pywin32 psutil")

        return True
    except Exception as e:
        print(f"❌ Error opening {app_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Open applications by name or path')
    parser.add_argument('--app', help='Application name (e.g., "Notepad", "Chrome", "calc")')
    parser.add_argument('--path', help='Full path to executable')
    
    args = parser.parse_args()
    
    if args.app:
        open_application_by_name(args.app)
    elif args.path:
        open_application_by_path(args.path)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
