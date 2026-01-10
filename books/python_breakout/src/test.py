#!/usr/bin/env python3
"""
ブロック崩しチュートリアル テストランナー

使い方:
    python test.py        # メニューから選択
    python test.py 1      # チャプター1を実行
    python test.py 5      # チャプター5を実行
    python test.py main   # 完成版を実行
"""

import subprocess
import sys
from pathlib import Path


def get_script_dir():
    """このスクリプトのディレクトリを取得"""
    return Path(__file__).parent


def run_chapter(chapter: str):
    """指定されたチャプターを実行"""
    script_dir = get_script_dir()

    if chapter == "main":
        file_path = script_dir / "main.py"
    else:
        file_path = script_dir / f"{chapter:0>2}.py"

    if not file_path.exists():
        print(f"エラー: {file_path} が見つかりません")
        return False

    print(f"\n{'='*50}")
    print(f"実行中: {file_path.name}")
    print(f"{'='*50}\n")

    try:
        subprocess.run([sys.executable, str(file_path)])
        return True
    except KeyboardInterrupt:
        print("\n中断しました")
        return True


def show_menu():
    """メニューを表示して選択を待つ"""
    print("\n" + "="*50)
    print("ブロック崩しチュートリアル テストランナー")
    print("="*50)
    print()
    print("  1. チャプター01: パドルを動かそう")
    print("  2. チャプター02: ボールを動かそう")
    print("  3. チャプター03: パドルでボールを打ち返そう")
    print("  4. チャプター04: ブロックを並べよう")
    print("  5. チャプター05: ゲームを完成させよう")
    print("  m. 完成版 (main.py)")
    print("  q. 終了")
    print()

    while True:
        choice = input("番号を入力してください: ").strip().lower()

        if choice == "q":
            print("終了します")
            return None
        elif choice == "m":
            return "main"
        elif choice in ["1", "2", "3", "4", "5"]:
            return choice
        else:
            print("1-5, m, または q を入力してください")


def main():
    # コマンドライン引数があればそれを使用
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "main":
            run_chapter("main")
        elif arg in ["1", "2", "3", "4", "5"]:
            run_chapter(arg)
        else:
            print(f"使い方: python test.py [1-5|main]")
            print(f"例: python test.py 3")
        return

    # メニューモード
    while True:
        choice = show_menu()
        if choice is None:
            break
        run_chapter(choice)
        input("\nEnterキーでメニューに戻ります...")


if __name__ == "__main__":
    main()
