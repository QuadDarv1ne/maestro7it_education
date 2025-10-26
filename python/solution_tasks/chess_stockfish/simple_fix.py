#!/usr/bin/env python3
"""
Simple script to fix duplicate classes in board_renderer.py
"""

def fix_file():
    with open('ui/board_renderer.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the first occurrence of CoordinateMapper class
    first_pos = content.find('class CoordinateMapper:')
    if first_pos == -1:
        print("CoordinateMapper class not found")
        return
    
    # Find the second occurrence
    second_pos = content.find('class CoordinateMapper:', first_pos + 1)
    if second_pos == -1:
        print("No duplicate CoordinateMapper class found")
        return
    
    # Find the end of the duplicate section (next class or end of file)
    next_class_pos = content.find('class ', second_pos + 1)
    if next_class_pos == -1:
        next_class_pos = len(content)
    
    # Remove the duplicate section
    fixed_content = content[:second_pos] + content[next_class_pos:]
    
    # Write back to file
    with open('ui/board_renderer.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed duplicate CoordinateMapper class")

if __name__ == "__main__":
    fix_file()