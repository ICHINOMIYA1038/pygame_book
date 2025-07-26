# Python RPGゲーム チュートリアル

小学生向けのPython RPGゲーム作成チュートリアルです。

## 必要なもの

- Python 3.9以上
- uv（Pythonパッケージマネージャー）
- Task（タスクランナー）

## セットアップ

```bash
# uvのインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Taskのインストール（まだの場合）
brew install go-task/tap/go-task

# プロジェクトのセットアップ
task install
```

## ゲームの実行方法

### 各章を個別に実行

```bash
task run01  # 第1章：勇者の名前を決めよう
task run02  # 第2章：スライムと戦おう
task run03  # 第3章：複数の敵と連続バトル
task run04  # 第4章：魔法を使おう
task run05  # 第5章：アイテムを使おう
task run06  # 第6章：レベルアップシステム
task run07  # 第7章：ダンジョン探索
task run08  # 第8章：完成版RPGゲーム
```

### 完成版を実行

```bash
task run
```

## その他のコマンド

```bash
task test    # コードの構文チェック
task format  # コードのフォーマット
task clean   # クリーンアップ
task help    # ヘルプを表示
```

## ファイル構成

- `01_rpg_start.py` - 基本的な入出力
- `02_battle.py` - シンプルなバトルシステム
- `03_multiple_battles.py` - 複数の敵との戦闘
- `04_magic.py` - 魔法システム
- `05_items.py` - アイテムシステム
- `06_levelup.py` - レベルアップシステム
- `07_dungeon.py` - ダンジョン探索
- `08_complete_rpg.py` - 完成版RPGゲーム