# Screenshot Slash Command

指定したプログラムを実行してスクリーンショットを撮影するコマンドです。

## 使用方法

```
/screenshot <実行ファイル> [オプション]
```

## オプション

- `--output, -o`: 出力ファイルパス（デフォルト: ./screenshot.png）
- `--delay, -d`: 撮影までの待機時間（秒）（デフォルト: 3）
- `--window, -w`: ウィンドウ撮影モード（デフォルト）
- `--fullscreen, -f`: 全画面撮影モード
- `--timeout, -t`: プロセスのタイムアウト時間（秒）（デフォルト: 10）

## 使用例

### Pythonスクリプトのスクリーンショット
```
/screenshot python main.py -o images/game.png
```

### フルスクリーン撮影
```
/screenshot python app.py -f -o screenshots/fullscreen.png
```

### 待機時間を変更
```
/screenshot npm run dev -d 5 -o build/preview.png
```

## 実行手順

1. 指定したコマンドでプログラムを起動
2. 指定した秒数待機（デフォルト3秒）
3. スクリーンショットを撮影
   - ウィンドウモード: 対象ウィンドウをクリック
   - フルスクリーンモード: 自動で全画面撮影
4. 指定したパスに画像を保存

## 実際の実行

```bash
python /Users/ichinomiya/zenn-books/scripts/screenshot.py $@
```