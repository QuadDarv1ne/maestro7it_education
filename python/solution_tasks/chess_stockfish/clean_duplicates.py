#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def clean_duplicates():
    with open('game/chess_game.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find duplicate method declarations
    duplicate_starts = []
    for i, line in enumerate(lines):
        if ('def handle_ai_move_optimized(self):' in line and i > 2800) or \
           ('def _execute_ai_move(self, ai_move):' in line and i > 2800) or \
           ('def start_multithreading(self):' in line and i > 2800) or \
           ('def stop_multithreading(self):' in line and i > 2800) or \
           ('def handle_ai_move_multithreaded(self):' in line and i > 2800) or \
           ('def _process_ai_move(self):' in line and i > 2800) or \
           ('def _compute_ai_move_v2(self):' in line):
            duplicate_starts.append(i)
    
    # Remove duplicate method blocks
    cleaned_lines = []
    skip_until = -1
    
    for i, line in enumerate(lines):
        if i < skip_until:
            continue
            
        if i in duplicate_starts:
            # Skip this method block
            indent_level = len(line) - len(line.lstrip())
            skip_until = i + 1
            
            # Skip until we find a line with same or lower indent level
            while skip_until < len(lines):
                next_line = lines[skip_until]
                next_indent = len(next_line) - len(next_line.lstrip())
                
                # If next line is not indented or is a new method definition, stop skipping
                if next_indent <= indent_level and next_line.strip() and not next_line.lstrip().startswith('#'):
                    break
                skip_until += 1
            continue
            
        cleaned_lines.append(line)
    
    # Fix _annotate_move_internal calls
    for i, line in enumerate(cleaned_lines):
        if '_annotate_move_internal(' in line:
            cleaned_lines[i] = line.replace('_annotate_move_internal(', '_annotate_move(')
    
    with open('game/chess_game_clean.py', 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print("Cleaned file written to game/chess_game_clean.py")

if __name__ == '__main__':
    clean_duplicates()