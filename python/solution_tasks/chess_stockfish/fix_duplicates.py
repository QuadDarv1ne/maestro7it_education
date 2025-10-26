#!/usr/bin/env python3
"""
Script to remove duplicate class declarations in board_renderer.py
"""

def fix_duplicates():
    file_path = 'ui/board_renderer.py'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the first and second occurrence of CoordinateMapper class
    first_coord_mapper = -1
    second_coord_mapper = -1
    
    for i, line in enumerate(lines):
        if line.strip() == 'class CoordinateMapper:' or line.strip().startswith('class CoordinateMapper('):
            if first_coord_mapper == -1:
                first_coord_mapper = i
            else:
                second_coord_mapper = i
                break
    
    if second_coord_mapper == -1:
        print("No duplicate CoordinateMapper class found")
        return
    
    # Find the end of the duplicate class (look for the next class or end of file)
    end_of_duplicate = len(lines)
    for i in range(second_coord_mapper + 1, len(lines)):
        if lines[i].strip().startswith('class ') and 'CoordinateMapper' not in lines[i]:
            end_of_duplicate = i
            break
    
    # Remove the duplicate class
    fixed_lines = lines[:second_coord_mapper] + lines[end_of_duplicate:]
    
    # Write the fixed content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Removed duplicate CoordinateMapper class")

if __name__ == "__main__":
    fix_duplicates()