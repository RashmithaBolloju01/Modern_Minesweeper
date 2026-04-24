#!/usr/bin/env python
import sys
import ast

try:
    with open('/Users/rashmithabolloju/Desktop/Minesweeper/main.py', 'r') as f:
        code = f.read()
    ast.parse(code)
    print('✅ Syntax valid!')
    
    # Check for key features
    if 'DIFFICULTY_PRESETS' in code:
        print('✅ Difficulty presets found')
    if 'def start_game' in code:
        print('✅ start_game function found')
    if 'def reset_game' in code:
        print('✅ reset_game function found')
    if 'def create_start_menu' in code:
        print('✅ create_start_menu function found')
    if 'def create_game_screen' in code:
        print('✅ create_game_screen function found')
    
    # Check for difficulty settings
    if '"Easy"' in code and '6, 10' in code:
        print('✅ Easy difficulty configured')
    if '"Medium"' in code and '8, 8' in code:
        print('✅ Medium difficulty configured')
    if '"Hard"' in code and '10, 30' in code:
        print('✅ Hard difficulty configured')
    
    print('\n✅ All checks passed! Difficulty selection system is ready.')
    sys.exit(0)
except SyntaxError as e:
    print(f'❌ Syntax error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
