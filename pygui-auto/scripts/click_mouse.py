#!/usr/bin/env python3
"""
Click Mouse - Simulate mouse clicks at specific coordinates

Usage:
    python click_mouse.py --x 100 --y 200
    python click_mouse.py --x 100 --y 200 --button right
    python click_mouse.py --button middle --double
"""

import sys
import argparse


def click_at(x, y, button='left', double_click=False):
    """
    Click at specific coordinates.

    Args:
        x: X coordinate
        y: Y coordinate
        button: Mouse button ('left', 'right', 'middle')
        double_click: Perform double click
    """
    try:
        import pyautogui
        
        print(f"🖱️  Clicking at ({x}, {y}) with {button} button")
        
        pyautogui.click(x, y, button=button, clicks=2 if double_click else 1)
        print("✅ Click performed successfully")
        return True
    except ImportError:
        print("❌ Error: pyautogui not installed. Install with: pip install pyautogui")
        return False
    except Exception as e:
        print(f"❌ Error clicking: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Click mouse at specific coordinates')
    parser.add_argument('--x', type=int, help='X coordinate')
    parser.add_argument('--y', type=int, help='Y coordinate')
    parser.add_argument('--button', default='left', choices=['left', 'right', 'middle'], help='Mouse button')
    parser.add_argument('--double', action='store_true', help='Perform double click')
    
    args = parser.parse_args()
    
    if args.x is None or args.y is None:
        parser.print_help()
        sys.exit(1)
    
    click_at(args.x, args.y, args.button, args.double)


if __name__ == "__main__":
    main()
