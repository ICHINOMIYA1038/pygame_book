#!/usr/bin/env python3
"""
RPGゲームのスクリーンショットを撮影するスクリプト
"""
import subprocess
import time
import os
import sys

def take_screenshot(game_file, output_file, wait_time=5, input_sequence=None):
    """
    ゲームを起動してスクリーンショットを撮影
    
    Args:
        game_file: 実行するPythonファイル
        output_file: 出力する画像ファイルパス
        wait_time: スクリーンショット撮影までの待機時間
        input_sequence: キー入力のシーケンス（オプション）
    """
    print(f"Starting {game_file}...")
    
    # ゲームをバックグラウンドで起動
    process = subprocess.Popen(
        ['uv', 'run', 'python', game_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 起動を待つ
    time.sleep(3)
    
    # 必要に応じてキー入力をシミュレート
    if input_sequence:
        for action in input_sequence:
            if action['type'] == 'type':
                # テキスト入力（AppleScriptを使用）
                script = f'''
                tell application "System Events"
                    keystroke "{action['text']}"
                end tell
                '''
                subprocess.run(['osascript', '-e', script])
            elif action['type'] == 'key':
                # 特殊キー入力
                script = f'''
                tell application "System Events"
                    key code {action['code']}
                end tell
                '''
                subprocess.run(['osascript', '-e', script])
            elif action['type'] == 'wait':
                time.sleep(action['time'])
    
    # スクリーンショット撮影前に待機
    time.sleep(wait_time)
    
    # スクリーンショットを撮影
    print(f"Taking screenshot to {output_file}...")
    
    # ウィンドウをアクティブにしてからスクリーンショット
    script = '''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        if frontApp contains "Python" then
            tell application process frontApp
                set frontmost to true
            end tell
        end if
    end tell
    '''
    subprocess.run(['osascript', '-e', script])
    time.sleep(0.5)
    
    # スクリーンショット撮影
    subprocess.run(['screencapture', '-w', '-o', output_file])
    
    # プロセスを終了
    process.terminate()
    process.wait()
    
    print(f"Screenshot saved: {output_file}")

def main():
    """各章のスクリーンショットを撮影"""
    base_dir = "/Users/ichinomiya/zenn-books/books/python-rpg-game"
    src_dir = os.path.join(base_dir, "src")
    images_dir = os.path.join(base_dir, "images")
    
    # 画像ディレクトリを作成
    os.makedirs(images_dir, exist_ok=True)
    
    # 各章のスクリーンショット設定
    screenshots = [
        {
            'file': '01_rpg_start_pygame.py',
            'output': '01_name_input.png',
            'wait': 5,
            'input': [
                {'type': 'wait', 'time': 2},
                {'type': 'type', 'text': 'ゆうしゃ'},
                {'type': 'wait', 'time': 1},
            ]
        },
        {
            'file': '02_battle_pygame.py',
            'output': '02_battle.png',
            'wait': 5,
            'input': [
                {'type': 'wait', 'time': 2},
                {'type': 'type', 'text': 'ゆうしゃ'},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 2},
            ]
        },
        {
            'file': '03_multiple_battles_pygame.py',
            'output': '03_multiple_battles.png',
            'wait': 5,
            'input': [
                {'type': 'wait', 'time': 2},
                {'type': 'type', 'text': 'ゆうしゃ'},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 1},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 2},
            ]
        },
        {
            'file': '04_magic_pygame.py',
            'output': '04_magic.png',
            'wait': 5,
            'input': [
                {'type': 'wait', 'time': 2},
                {'type': 'type', 'text': 'まほうつかい'},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 1},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 1},
                {'type': 'key', 'code': 125},  # Down arrow
                {'type': 'wait', 'time': 1},
            ]
        },
        {
            'file': '05_items_pygame.py',
            'output': '05_items.png',
            'wait': 5,
            'input': [
                {'type': 'wait', 'time': 2},
                {'type': 'type', 'text': 'ゆうしゃ'},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 1},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 1},
                {'type': 'key', 'code': 125},  # Down arrow
                {'type': 'key', 'code': 125},  # Down arrow
                {'type': 'wait', 'time': 1},
            ]
        },
        {
            'file': '06_levelup_pygame.py',
            'output': '06_levelup.png',
            'wait': 5,
            'input': [
                {'type': 'wait', 'time': 2},
                {'type': 'type', 'text': 'ゆうしゃ'},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 1},
                {'type': 'key', 'code': 36},  # Enter
                {'type': 'wait', 'time': 2},
            ]
        },
    ]
    
    # 作業ディレクトリを変更
    os.chdir(src_dir)
    
    # 各スクリーンショットを撮影
    for config in screenshots:
        output_path = os.path.join(images_dir, config['output'])
        take_screenshot(
            config['file'],
            output_path,
            config['wait'],
            config.get('input')
        )
        time.sleep(2)  # 次のスクリーンショットまで待機

if __name__ == '__main__':
    main()