#!/usr/bin/env python3
"""
Script to fix syntax errors in board_renderer.py
"""

def fix_board_renderer():
    file_path = 'ui/board_renderer.py'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Fix the syntax error with triple quotes
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for the problematic triple quotes pattern
        if line.strip() == '```' and i + 1 < len(lines):
            # Check if the next line is a triple quoted string
            next_line = lines[i + 1]
            if next_line.strip().startswith('"""'):
                # Skip the erroneous line
                i += 1
                line = next_line
            else:
                # Just skip this line
                i += 1
                continue
        
        fixed_lines.append(line)
        i += 1
    
    # Write the fixed content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Fixed syntax errors in board_renderer.py")

if __name__ == "__main__":
    fix_board_renderer()