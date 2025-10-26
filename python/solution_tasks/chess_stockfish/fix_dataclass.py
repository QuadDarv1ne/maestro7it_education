#!/usr/bin/env python3
"""
Fix the dataclass decorator placement
"""

def fix_dataclass():
    with open('ui/board_renderer.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the @dataclass decorator and fix its placement
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is the @dataclass decorator
        if line.strip() == '@dataclass':
            # Check if the next line is the class definition
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('class BoardTheme:'):
                # This is correct, keep both lines
                fixed_lines.append(line)
                fixed_lines.append(lines[i + 1])
                i += 2
                continue
            else:
                # The decorator is misplaced, skip it
                i += 1
                continue
        
        # Check if this is the class definition without decorator
        if line.strip().startswith('class BoardTheme:'):
            # Add the decorator before the class
            fixed_lines.append('@dataclass\n')
        
        fixed_lines.append(line)
        i += 1
    
    # Write back to file
    with open('ui/board_renderer.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Fixed dataclass decorator")

if __name__ == "__main__":
    fix_dataclass()