#!/usr/bin/env python3
"""
Fix the header of board_renderer.py
"""

def fix_header():
    with open('ui/board_renderer.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the first actual Python code (import statement)
    import_line = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('import '):
            import_line = i
            break
    
    if import_line == -1:
        print("No import statement found")
        return
    
    # Create the proper header
    header = '"""\n' + ''.join(lines[:import_line]) + '"""\n\n'
    
    # Combine header with the rest of the file
    fixed_lines = [header] + lines[import_line:]
    
    # Write back to file
    with open('ui/board_renderer.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Fixed header")

if __name__ == "__main__":
    fix_header()