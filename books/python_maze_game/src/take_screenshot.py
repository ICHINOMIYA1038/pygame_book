#!/usr/bin/env python3
"""
スクリーンショット撮影用スクリプト
main.pyを起動して3秒後にスクリーンショットを撮影する
"""
import subprocess
import time
import pygame
import sys
import os

def take_pygame_screenshot():
    """Pygameのウィンドウのスクリーンショットを撮影"""
    # main.pyを別プロセスで起動
    process = subprocess.Popen([sys.executable, 'main.py'])
    
    # ゲームが起動するまで待機
    time.sleep(3)
    
    # Pygameの画面を取得してスクリーンショットを保存
    try:
        # 現在のPygameウィンドウを探す
        pygame.init()
        info = pygame.display.get_wm_info()
        
        # スクリーンショットを保存
        screenshot_path = "/Users/ichinomiya/zenn-books/images/python_maze_game/main_game.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        
        # macOSのscreencaptureコマンドを使用
        subprocess.run(['screencapture', '-w', screenshot_path])
        print(f"スクリーンショットを保存しました: {screenshot_path}")
        
    except Exception as e:
        print(f"エラー: {e}")
    finally:
        # プロセスを終了
        process.terminate()

if __name__ == "__main__":
    print("main.pyを起動してスクリーンショットを撮影します...")
    print("ゲームウィンドウをクリックしてください！")
    take_pygame_screenshot()