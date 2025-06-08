# Pygame 迷路ゲーム サンプルコード

これは [Zenn Books: pygame で迷路ゲームを作ろう](https://zenn.dev/ichinomiya/books/python_maze_game) の実装例です。

## ゲームの機能

- キャラクターの移動
- 壁との衝突判定
- 敵キャラクター
- ゴール判定
- コイン収集とスコア
- サウンドエフェクト
- パーティクルエフェクト

## 必要な環境

- Python 3.7 以上
- pygame ライブラリ

## セットアップ

1. Python がインストールされていることを確認してください
2. pygame をインストールします：
   ```bash
   pip install pygame
   ```

## ファイル構成

```
python_maze_game_code/
├── README.md              # このファイル
├── requirements.txt       # 依存関係
├── 01_basic_movement.py   # 第1章: 基本的な移動
├── 02_map_floor.py        # 第2章: マップと床
├── 03_walls.py           # 第3章: 壁と衝突判定
├── 04_goal.py            # 第4章: ゴール判定
├── 05_bigger_map.py      # 第5章: より大きなマップ
├── 06_enemy.py           # 第6章: 敵キャラクター
├── 07_coins_score.py     # 第7章: コインとスコア
├── 08_sound_effects.py   # 第8章: サウンドとエフェクト
├── main.py               # 最終完成版
└── assets/               # ゲーム素材
    └── sounds/           # サウンドファイル（オプション）
        ├── coin.wav
        ├── gameover.wav
        ├── clear.wav
        └── bgm.wav
```

## 実行方法

各章のファイルを個別に実行できます：

```bash
# 第1章のサンプル
python 01_basic_movement.py

# 第2章のサンプル
python 02_map_floor.py

# 最終完成版
python main.py
```

## 章別の学習内容

| 章  | ファイル名             | 学習内容                        |
| --- | ---------------------- | ------------------------------- |
| 01  | `01_basic_movement.py` | Pygame の基本とキャラクター移動 |
| 02  | `02_map_floor.py`      | マップデータと床の描画          |
| 03  | `03_walls.py`          | 壁の実装と衝突判定              |
| 04  | `04_goal.py`           | ゴール判定とゲームクリア        |
| 05  | `05_bigger_map.py`     | 大きなマップでの実装            |
| 06  | `06_enemy.py`          | 敵キャラクターとゲームオーバー  |
| 07  | `07_coins_score.py`    | アイテム収集とスコアシステム    |
| 08  | `08_sound_effects.py`  | サウンドと視覚エフェクト        |

## 注意事項

- サウンドファイル（`.wav`）は含まれていません。必要に応じて自分で用意してください
- 音声なしでもゲームは正常に動作します

## ライセンス

このサンプルコードは学習目的で自由に使用できます。

## 記事リンク

詳しい解説は [Zenn Books](https://zenn.dev/ichinomiya/books/python_maze_game) をご覧ください。
