#!/usr/bin/env python3
"""
Press Key - Simulate keyboard key presses

Usage:
    python press_key.py --key "enter"
    python press_key.py --key "ctrl+c" --combo
"""

import sys
import argparse


def press_key(key, is_combo=False):
    """
    Press a single key or key combination.

    Args:
        key: Key name or combination (e.g., "enter", "ctrl+c", "alt+tab")
        is_combo: True if key is a combination (e.g., "ctrl+c")
    """
    try:
        import pyautogui
        
        print(f"⌨️  Pressing key: {key}")
        
        if is_combo or '+' in key:
            pyautogui.hotkey(*key.split('+'))
        else:
            pyautogui.press(key)
        
        print("✅ Key pressed successfully")
        return True
    except ImportError:
        print("❌ Error: pyautogui not installed. Install with: pip install pyautogui")
        return False
    except Exception as e:
        print(f"❌ Error pressing key: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Press keyboard keys')
    parser.add_argument('--key', required=True, help='Key name or combination (e.g., "enter", "ctrl+c")')
    parser.add_argument('--combo', action='store_true', help='Treat key as combination (e.g., ctrl+c)')
    
    args = parser.parse_args()
    
    press_key(args.key, args.combo)


if __name__ == "__main__":
    main()
