#!/usr/bin/env python3
"""
Script to fix duplicate content in board_renderer.py
"""

import os

def fix_board_renderer():
    file_path = 'ui/board_renderer.py'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if there are duplicate sections
    # Find the first occurrence of the duplicate content
    first_import_pos = content.find('import pygame')
    if first_import_pos == -1:
        print("No import section found")
        return
    
    # Find the second occurrence of the duplicate content
    second_import_pos = content.find('import pygame', first_import_pos + 1)
    if second_import_pos == -1:
        print("No duplicate import section found")
        return
    
    # Find the end of the duplicate section
    # Look for the end of the duplicate module docstring
    duplicate_end = content.find('\"\"\"', second_import_pos)  # End of module docstring
    if duplicate_end != -1:
        # Find the end of the docstring (next occurrence)
        duplicate_end = content.find('\"\"\"', duplicate_end + 3)
        if duplicate_end != -1:
            duplicate_end += 3  # Include the closing quotes
    
    # Remove the duplicate section
    if duplicate_end != -1:
        # Find where the actual duplicate content ends
        # Look for the CoordinateMapper class definition
        coord_mapper_pos = content.find('class CoordinateMapper', second_import_pos)
        if coord_mapper_pos != -1:
            # Remove from second import to CoordinateMapper class
            fixed_content = content[:second_import_pos] + content[coord_mapper_pos:]
            
            # Write the fixed content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print("Fixed duplicate content in board_renderer.py")
        else:
            print("Could not find CoordinateMapper class")
    else:
        print("Could not determine end of duplicate section")

if __name__ == "__main__":
    fix_board_renderer()