#!/usr/bin/env python3
"""
汎用的なスクリーンショット撮影スクリプト

使用方法:
    python screenshot.py <実行ファイル> [オプション]

オプション:
    --output, -o: 出力ファイルパス（デフォルト: ./screenshot.png）
    --delay, -d: 撮影までの待機時間（秒）（デフォルト: 3）
    --window, -w: ウィンドウ撮影モード（デフォルト: True）
    --fullscreen, -f: 全画面撮影モード
    --timeout, -t: プロセスのタイムアウト時間（秒）（デフォルト: 10）
"""

import subprocess
import time
import sys
import os
import argparse
from pathlib import Path

def take_screenshot(command, output_path, delay=3, window_mode=True, timeout=10):
    """
    指定したコマンドを実行してスクリーンショットを撮影
    
    Args:
        command: 実行するコマンド（文字列またはリスト）
        output_path: 出力ファイルパス
        delay: 撮影までの待機時間（秒）
        window_mode: Trueの場合ウィンドウ撮影、Falseの場合全画面撮影
        timeout: プロセスのタイムアウト時間（秒）
    """
    # 出力ディレクトリを作成
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # コマンドを実行
    if isinstance(command, str):
        command = command.split()
    
    print(f"実行中: {' '.join(command)}")
    process = subprocess.Popen(command)
    
    # 指定された時間待機
    print(f"{delay}秒待機中...")
    time.sleep(delay)
    
    # スクリーンショットを撮影
    try:
        if sys.platform == "darwin":  # macOS
            if window_mode:
                print("ウィンドウをクリックしてください...")
                subprocess.run(['screencapture', '-w', str(output_path)])
            else:
                subprocess.run(['screencapture', '-x', str(output_path)])
        elif sys.platform == "linux":  # Linux
            if window_mode:
                # xwininfoとimportを使用
                subprocess.run(['import', str(output_path)])
            else:
                subprocess.run(['import', '-window', 'root', str(output_path)])
        elif sys.platform == "win32":  # Windows
            # Windows用のスクリーンショットコマンド
            print("Windows環境では手動でスクリーンショットを撮影してください")
        
        print(f"スクリーンショットを保存しました: {output_path}")
        
    except Exception as e:
        print(f"エラー: {e}")
    finally:
        # プロセスを終了
        try:
            process.wait(timeout=timeout - delay)
        except subprocess.TimeoutExpired:
            process.terminate()
            print("プロセスをタイムアウトにより終了しました")

def main():
    parser = argparse.ArgumentParser(description='プログラムを実行してスクリーンショットを撮影')
    parser.add_argument('command', nargs='+', help='実行するコマンド')
    parser.add_argument('-o', '--output', default='./screenshot.png', help='出力ファイルパス')
    parser.add_argument('-d', '--delay', type=int, default=3, help='撮影までの待機時間（秒）')
    parser.add_argument('-w', '--window', action='store_true', default=True, help='ウィンドウ撮影モード')
    parser.add_argument('-f', '--fullscreen', action='store_true', help='全画面撮影モード')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='プロセスのタイムアウト時間（秒）')
    
    args = parser.parse_args()
    
    # fullscreenが指定されたらwindowモードをオフ
    window_mode = not args.fullscreen if args.fullscreen else args.window
    
    take_screenshot(
        command=args.command,
        output_path=args.output,
        delay=args.delay,
        window_mode=window_mode,
        timeout=args.timeout
    )

if __name__ == "__main__":
    main()