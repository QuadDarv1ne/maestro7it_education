#!/usr/bin/env python3
"""
Clean fix script for board_renderer.py
"""

def clean_file():
    with open('ui/board_renderer.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the problematic areas
    # Look for the duplicate module docstring
    cleaned_lines = []
    skip_module_doc = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if we're at the duplicate module docstring
        if (line.strip() == '"""' and 
            i + 1 < len(lines) and 
            lines[i+1].strip().startswith('Модуль: ui/board_renderer.py')):
            # Skip until the end of this docstring
            while i < len(lines) and not lines[i].strip().endswith('"""'):
                i += 1
            if i < len(lines):  # Skip the closing """
                i += 1
            continue
            
        # Check for duplicate CoordinateMapper class
        if (line.strip() == 'class CoordinateMapper:' and 
            len([l for l in cleaned_lines if l.strip() == 'class CoordinateMapper:']) > 0):
            # Skip this duplicate class
            # Find the end of the class (next class or end of file)
            while i < len(lines) and not (lines[i].strip().startswith('class ') and 'CoordinateMapper' not in lines[i]):
                i += 1
            continue
            
        cleaned_lines.append(line)
        i += 1
    
    # Write back to file
    with open('ui/board_renderer.py', 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print("Cleaned file")

if __name__ == "__main__":
    clean_file()