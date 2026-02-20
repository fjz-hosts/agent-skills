#!/usr/bin/env python3
"""
Create File - Create new files with specified content

Usage:
    python create_file.py --path "C:\\Users\\User\\Documents\\test.txt" --content "Hello World"
    python create_file.py --path "test.txt" --content "Sample content"
"""

import sys
import argparse
from pathlib import Path


def create_file(file_path, content=""):
    """
    Create a new file with specified content.

    Args:
        file_path: Path to the file to create
        content: Content to write to the file (default: empty)
    """
    try:
        path = Path(file_path)
        
        print(f"📄 Creating file: {file_path}")
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        
        print("✅ File created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Create a new file with content')
    parser.add_argument('--path', required=True, help='Path to the file to create')
    parser.add_argument('--content', default='', help='Content to write to the file')
    
    args = parser.parse_args()
    
    create_file(args.path, args.content)


if __name__ == "__main__":
    main()
