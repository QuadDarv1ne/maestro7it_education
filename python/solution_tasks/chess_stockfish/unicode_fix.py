#!/usr/bin/env python3
"""
Fix Unicode characters in board_renderer.py
"""

def fix_unicode():
    with open('ui/board_renderer.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the Unicode arrow character with a regular arrow
    content = content.replace('→', '->')
    
    # Write back to file
    with open('ui/board_renderer.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed Unicode characters")

if __name__ == "__main__":
    fix_unicode()