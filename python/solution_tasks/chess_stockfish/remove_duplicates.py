#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def remove_duplicates():
    with open('game/chess_game.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Create a new list of lines without duplicates
    cleaned_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a duplicate method declaration
        if (i > 2800 and 'def handle_ai_move_optimized(self):' in line) or \
           (i > 2800 and 'def _execute_ai_move(self, ai_move):' in line) or \
           (i > 2800 and 'def start_multithreading(self):' in line) or \
           (i > 2800 and 'def stop_multithreading(self):' in line) or \
           (i > 2800 and 'def handle_ai_move_multithreaded(self):' in line) or \
           (i > 2800 and 'def _process_ai_move(self):' in line) or \
           ('def _compute_ai_move_v2(self):' in line):
            
            # Skip this method and all its content
            i += 1
            # Skip indented lines (method body)
            while i < len(lines) and (lines[i].startswith('    ') or lines[i].startswith('\t') or lines[i].strip() == ''):
                i += 1
            continue
        
        # Fix _annotate_move_internal calls
        if '_annotate_move_internal(' in line:
            line = line.replace('_annotate_move_internal(', '_annotate_move(')
            
        cleaned_lines.append(line)
        i += 1
    
    with open('game/chess_game_fixed.py', 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print("Fixed file written to game/chess_game_fixed.py")

if __name__ == '__main__':
    remove_duplicates()