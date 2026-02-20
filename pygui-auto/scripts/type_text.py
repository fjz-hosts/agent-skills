#!/usr/bin/env python3
"""
Type Text - Simulate keyboard typing

Usage:
    python type_text.py --text "Hello World"
    python type_text.py --text "Hello" --delay 0.1
"""

import sys
import time
import argparse


def type_text(text, delay=0.05):
    """
    Type text character by character with optional delay.

    Args:
        text: Text to type
        delay: Delay between characters in seconds (default: 0.05)
    """
    try:
        import pyautogui
        
        print(f"📝 Typing: {text}")
        pyautogui.write(text, interval=delay)
        print("✅ Text typed successfully")
        return True
    except ImportError:
        print("❌ Error: pyautogui not installed. Install with: pip install pyautogui")
        return False
    except Exception as e:
        print(f"❌ Error typing text: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Type text using keyboard simulation')
    parser.add_argument('--text', required=True, help='Text to type')
    parser.add_argument('--delay', type=float, default=0.05, help='Delay between characters in seconds')
    
    args = parser.parse_args()
    
    type_text(args.text, args.delay)


if __name__ == "__main__":
    main()
