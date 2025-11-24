---
title: "VS Code カスタムテーマを yo code で作るチュートリアル"
emoji: "🎨"
type: "tech"
topics: ["vscode", "theme", "yeoman"]
published: false
---

## はじめに

VS Code のカスタムカラーテーマを `yo code`（Yeoman + generator-code）を使って作成するチュートリアルです。

## 1. 必要なツールのインストール

```bash
# Yeoman と VS Code ジェネレーターをインストール
npm install -g yo generator-code
```

確認：

```bash
yo --version
# 5.x.x などが表示されれば OK
```

## 2. テーマの雛形を生成

作業用ディレクトリに移動して、ジェネレーターを実行します：

```bash
mkdir ~/vscode-themes
cd ~/vscode-themes
yo code
```

## 3. 対話形式で設定

以下のように質問に答えていきます：

```
? What type of extension do you want to create?
  → New Color Theme    # ← これを選択

? Do you want to import or convert an existing TextMate color theme?
  → No, start fresh    # ← 新規作成

? What's the name of your extension?
  → my-test-theme      # ← 好きな名前

? What's the identifier of your extension?
  → my-test-theme      # ← Enter でそのまま

? What's the description of your extension?
  → My test color theme    # ← 説明（空でも可）

? What's the name of your theme shown to the user?
  → My Test Theme      # ← テーマ選択時に表示される名前

? Select a base theme:
  → Dark               # ← ベースのテーマ（Dark/Light/High Contrast）

? Initialize a git repository?
  → Yes                # ← お好みで

? Which package manager to use?
  → npm                # ← npm か pnpm か yarn
```

## 4. 生成されたファイル構造

```
my-test-theme/
├── package.json              # 拡張機能のマニフェスト
├── themes/
│   └── My Test Theme-color-theme.json  # ← テーマ定義ファイル（ここを編集）
├── README.md
├── CHANGELOG.md
└── vsc-extension-quickstart.md
```

## 5. テーマファイルを確認

`themes/My Test Theme-color-theme.json` を開いてみましょう：

```json
{
  "name": "My Test Theme",
  "type": "dark",
  "colors": {
    "editor.background": "#1E1E1E",
    "editor.foreground": "#D4D4D4"
    // ... UI の色
  },
  "tokenColors": [
    // ... シンタックスハイライトの色
  ]
}
```

## 6. テーマをテスト実行

生成されたフォルダで VS Code を開きます：

```bash
cd my-test-theme
code .
```

VS Code が開いたら：

1. **F5** を押す（デバッグ実行）
2. 新しい VS Code ウィンドウが開く
3. `Cmd + K, Cmd + T`（テーマ選択）
4. 「My Test Theme」を選択

これでテーマが適用されます！

## 7. テーマを編集して実験

### tokenColors を編集

`themes/My Test Theme-color-theme.json` の `tokenColors` を編集します：

```json
{
  "tokenColors": [
    {
      "name": "Comment",
      "scope": "comment",
      "settings": {
        "foreground": "#6A9955",
        "fontStyle": "italic"
      }
    },
    {
      "name": "Keyword",
      "scope": "keyword",
      "settings": {
        "foreground": "#569CD6"
      }
    },
    {
      "name": "Control Flow (if, for, while)",
      "scope": "keyword.control",
      "settings": {
        "foreground": "#C586C0",
        "fontStyle": "bold"
      }
    },
    {
      "name": "String",
      "scope": "string",
      "settings": {
        "foreground": "#CE9178"
      }
    },
    {
      "name": "Number",
      "scope": "constant.numeric",
      "settings": {
        "foreground": "#B5CEA8"
      }
    },
    {
      "name": "Function Name",
      "scope": "entity.name.function",
      "settings": {
        "foreground": "#DCDCAA"
      }
    },
    {
      "name": "Variable",
      "scope": "variable",
      "settings": {
        "foreground": "#9CDCFE"
      }
    },
    {
      "name": "Python Builtin",
      "scope": "support.function.builtin.python",
      "settings": {
        "foreground": "#4EC9B0"
      }
    }
  ]
}
```

### リアルタイム反映

1. テーマファイルを編集して **保存**
2. デバッグウィンドウに **即座に反映** される
3. 色を変えながら実験できる

## 8. 実験：スコープの確認

デバッグウィンドウで Python ファイルを開き：

1. `Cmd + Shift + P` → **Developer: Inspect Editor Tokens and Scopes**
2. 色を変えたい部分にカーソルを置く
3. 表示される `textmate scopes` を確認
4. そのスコープを `tokenColors` に追加

例：`if` にカーソルを置くと：

```
textmate scopes:
  keyword.control.flow.python
  source.python
```

## 9. テーマを完成させる

満足したら、テーマをパッケージ化して公開できます：

```bash
# vsce をインストール
npm install -g @vscode/vsce

# パッケージ化
vsce package

# → my-test-theme-0.0.1.vsix が生成される
```

生成された `.vsix` ファイルは：

- 他の人に配布できる
- マーケットプレイスに公開できる

## よく使うスコープ一覧

| スコープ               | 対象                              |
| ---------------------- | --------------------------------- |
| `comment`              | コメント                          |
| `string`               | 文字列                            |
| `constant.numeric`     | 数値                              |
| `constant.language`    | `true`, `false`, `null` など      |
| `keyword`              | キーワード全般                    |
| `keyword.control`      | 制御フロー（if, for, while）      |
| `keyword.operator`     | 演算子                            |
| `storage.type`         | `def`, `class`, `var`, `let` など |
| `entity.name.function` | 関数名                            |
| `entity.name.class`    | クラス名                          |
| `variable`             | 変数                              |
| `variable.parameter`   | 関数の引数                        |
| `support.function`     | 組み込み関数                      |

## トラブルシューティング

### F5 を押しても何も起きない

`.vscode/launch.json` があるか確認。なければ：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": ["--extensionDevelopmentPath=${workspaceFolder}"]
    }
  ]
}
```

### テーマが選択肢に出てこない

`package.json` の `contributes.themes` を確認：

```json
{
  "contributes": {
    "themes": [
      {
        "label": "My Test Theme",
        "uiTheme": "vs-dark",
        "path": "./themes/My Test Theme-color-theme.json"
      }
    ]
  }
}
```

### 色が変わらない

1. ファイルを保存したか確認
2. デバッグウィンドウをリロード（`Cmd + R`）
3. JSON の構文エラーがないか確認
