---
title: "VSCode カラーテーマの仕組みと作り方"
emoji: "⚡"
type: "tech"
topics: ["vscode", "typescript", "colorscience", "accessibility"]
published: false
---

## はじめに

VS Code のカラーテーマを自作するにあたり、その仕組みを調べました。この記事では、VS Code の色設定がどのように構成されているかを解説します。

公式ドキュメント: https://code.visualstudio.com/api/extension-guides/color-theme

## VS Code の色設定の全体像

VS Code の色は大きく **2 種類** に分かれています。

| 種類               | 何の色か                             | 設定方法                          |
| ------------------ | ------------------------------------ | --------------------------------- |
| **UI カラー**      | エディタの背景、サイドバー、タブなど | `workbench.colorCustomizations`   |
| **トークンカラー** | ソースコードのシンタックスハイライト | `editor.tokenColorCustomizations` |

テーマ拡張機能（`.json` ファイル）では、この両方を `colors` と `tokenColors` で定義します。

## テーマ拡張機能とは

テーマ拡張機能は、**VS Code の見た目（色）を変えるための拡張機能**です。

### テーマの種類

| 種類                   | 何を変えるか                     | 例                    |
| ---------------------- | -------------------------------- | --------------------- |
| **Color Theme**        | UI 全体 + シンタックスハイライト | Monokai, One Dark Pro |
| **File Icon Theme**    | ファイルアイコン                 | Material Icon Theme   |
| **Product Icon Theme** | UI のアイコン（サイドバーなど）  | Fluent Icons          |

### テーマファイルの保存場所

**組み込みテーマ**（VS Code に最初から入っているもの）:

```
/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/
├── theme-monokai/
├── theme-solarized-dark/
├── theme-defaults/    ← Dark+, Light+ など
└── ...
```

**ユーザーがインストールしたテーマ**:

```
~/.vscode/extensions/
```

### テーマファイルの構造

テーマ拡張機能は以下のような構造になっています：

```
theme-monokai/
├── package.json              ← 拡張機能のマニフェスト
└── themes/
    └── monokai-color-theme.json  ← 実際の配色定義
```

配色定義ファイル（`-color-theme.json`）の中身：

```json
{
  "type": "dark",
  "colors": {
    "editor.background": "#272822",
    "editor.foreground": "#f8f8f2",
    "statusBar.background": "#414339"
    // ... UI の色
  },
  "tokenColors": [
    {
      "scope": "comment",
      "settings": { "foreground": "#88846f" }
    },
    {
      "scope": "string",
      "settings": { "foreground": "#E6DB74" }
    }
    // ... トークンの色
  ]
}
```

## tmTheme とは

`tmTheme` は元々 TextMate エディタで使われていた配色定義形式です。

| 項目       | tmTheme          | VS Code テーマ      |
| ---------- | ---------------- | ------------------- |
| **形式**   | XML (plist)      | JSON                |
| **拡張子** | `.tmTheme`       | `-color-theme.json` |
| **内容**   | tokenColors のみ | tokenColors + UI 色 |

VS Code は両方の形式を読み込めますが、現在は JSON 形式が主流です。「tmTheme」という言葉は、**配色定義全般**を指すこともあれば、**XML 形式のファイル**を指すこともあります。

---

# Part 1: UI カラー

UI カラーは `workbench.colorCustomizations` で設定します。

```json
{
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#ff0000"
  }
}
```

すべての設定項目は[公式ドキュメント](https://code.visualstudio.com/api/references/theme-color)を参照してください。以下は代表的な設定項目です。

## 基本色 (Base colors)

| オプション             | 説明                                     |
| ---------------------- | ---------------------------------------- |
| `focusBorder`          | フォーカスされた要素の全体的なボーダー色 |
| `foreground`           | 全体的な前景色（テキストの色）           |
| `widget.shadow`        | ウィジェット（検索/置換など）の影の色    |
| `selection.background` | ワークベンチ内のテキスト選択の背景色     |
| `errorForeground`      | エラーメッセージの前景色                 |

## アクティビティバー (Activity Bar)

左端のアイコンが並んでいるバーの色を設定できます。

| オプション                    | 説明                         |
| ----------------------------- | ---------------------------- |
| `activityBar.background`      | アクティビティバーの背景色   |
| `activityBar.foreground`      | アクティブ時のアイコン前景色 |
| `activityBarBadge.background` | バッジ（通知数など）の背景色 |
| `activityBarBadge.foreground` | バッジの前景色               |

## サイドバー (Side Bar)

| オプション                        | 説明                       |
| --------------------------------- | -------------------------- |
| `sideBar.background`              | サイドバーの背景色         |
| `sideBar.foreground`              | サイドバーの前景色         |
| `sideBarTitle.foreground`         | サイドバータイトルの前景色 |
| `sideBarSectionHeader.background` | セクションヘッダーの背景色 |

## エディター (Editor colors)

| オプション                       | 説明                         |
| -------------------------------- | ---------------------------- |
| `editor.background`              | エディターの背景色           |
| `editor.foreground`              | エディターのデフォルト前景色 |
| `editorCursor.foreground`        | カーソルの色                 |
| `editor.lineHighlightBackground` | カーソル行のハイライト背景色 |
| `editorLineNumber.foreground`    | 行番号の色                   |
| `editor.selectionBackground`     | 選択範囲の背景色             |

## ステータスバー (Status Bar)

| オプション                      | 説明                             |
| ------------------------------- | -------------------------------- |
| `statusBar.background`          | 標準時のステータスバー背景色     |
| `statusBar.foreground`          | ステータスバーの前景色           |
| `statusBar.debuggingBackground` | デバッグ中のステータスバー背景色 |
| `statusBar.noFolderBackground`  | フォルダを開いていない時の背景色 |

## ターミナル (Integrated Terminal)

| オプション            | 説明               |
| --------------------- | ------------------ |
| `terminal.background` | ターミナルの背景色 |
| `terminal.foreground` | ターミナルの前景色 |
| `terminal.ansiBlack`  | ANSI カラー: 黒    |
| `terminal.ansiRed`    | ANSI カラー: 赤    |
| `terminal.ansiGreen`  | ANSI カラー: 緑    |
| `terminal.ansiYellow` | ANSI カラー: 黄    |
| `terminal.ansiBlue`   | ANSI カラー: 青    |
| `terminal.ansiWhite`  | ANSI カラー: 白    |

## タブ (Editor Groups & Tabs)

| オプション                         | 説明                       |
| ---------------------------------- | -------------------------- |
| `editorGroupHeader.tabsBackground` | タブコンテナの背景色       |
| `tab.activeBackground`             | アクティブなタブの背景色   |
| `tab.activeForeground`             | アクティブなタブの前景色   |
| `tab.inactiveBackground`           | 非アクティブなタブの背景色 |
| `tab.inactiveForeground`           | 非アクティブなタブの前景色 |
| `tab.border`                       | タブ間のボーダー色         |

## 複数の設定をまとめて適用する例

```json
{
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#282c34",
    "titleBar.activeForeground": "#9da5b4",
    "activityBar.background": "#21252b",
    "activityBar.foreground": "#d7dae0",
    "sideBar.background": "#21252b",
    "sideBar.foreground": "#abb2bf",
    "editor.background": "#282c34",
    "editor.foreground": "#abb2bf",
    "statusBar.background": "#21252b",
    "statusBar.foreground": "#9da5b4"
  }
}
```

:::message
色の形式は `#RGB`、`#RGBA`、`#RRGGBB`、`#RRGGBBAA` が使用できます。
アルファ値（透明度）を指定する場合は `#RRGGBBAA` 形式を使用します（例: `#00000050` は 50%の透明度）。
:::

---

# Part 2: トークンカラー（シンタックスハイライト）

ソースコードの色付けは、**トークン**という単位で行われます。

## トークンとは

トークンとは、**ソースコードの中で意味を持つ最小の単位**です。

```javascript
const msg = "hello";
```

| トークン  | 種類       |
| --------- | ---------- |
| `const`   | キーワード |
| `msg`     | 変数名     |
| `=`       | 演算子     |
| `"hello"` | 文字列     |
| `;`       | 記号       |

## シンタックスハイライトの仕組み

VS Code のシンタックスハイライトは **2 つのファイル** の連携で成り立っています。

```
ソースコード
    ↓
┌─────────────────────────────────────┐
│ .tmLanguage.json（文法定義）         │
│ 「この文字列は comment スコープ」    │
│ 「この文字列は keyword スコープ」    │
└─────────────────────────────────────┘
    ↓ スコープ名を出力
┌─────────────────────────────────────┐
│ テーマファイル（配色定義）           │
│ 「comment スコープは灰色」           │
│ 「keyword スコープはピンク」         │
└─────────────────────────────────────┘
    ↓
色付けされたコード
```

| ファイル               | 役割                    | 説明                                         |
| ---------------------- | ----------------------- | -------------------------------------------- |
| **`.tmLanguage.json`** | **文法定義（Grammar）** | コードを解析して「どの部分が何か」を判別する |
| **テーマファイル**     | **配色定義（Theme）**   | 文法で分類されたトークンに色を割り当てる     |

## 文法定義ファイル（.tmLanguage.json）

文法定義ファイルは「どの文字列がどのスコープに該当するか」を正規表現で定義しています。ここでは Python の文法定義（MagicPython.tmLanguage.json）を例に、その構造を詳しく見ていきます。

### ファイルの場所

VS Code の組み込み文法定義は以下にあります（Mac の場合）:

```
/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/
├── python/syntaxes/MagicPython.tmLanguage.json
├── javascript/syntaxes/JavaScript.tmLanguage.json
├── markdown-basics/syntaxes/markdown.tmLanguage.json
└── ...
```

:::message
VS Code は文法定義を一から作っているわけではありません。例えば Python の文法は [MagicStack/MagicPython](https://github.com/MagicStack/MagicPython) というサードパーティプロジェクトを採用しています。
:::

### 全体の構造を理解する

まず、`.tmLanguage.json` の全体像を把握しましょう。大きく分けて 4 つのパートがあります：

```json
{
  "name": "MagicPython",           // ① 文法の名前
  "scopeName": "source.python",    // ② この文法の識別子
  "patterns": [ ... ],             // ③ マッチングルール（トップレベル）
  "repository": { ... }            // ④ 再利用可能なルールの定義
}
```

#### ① name - 文法の名前

人間が読むための名前です。VS Code の内部では特に使われません。

#### ② scopeName - 文法の識別子

この文法を一意に識別する名前です。他の文法から参照するときに使います。

- `source.python` - Python
- `source.js` - JavaScript
- `text.html.markdown` - Markdown

#### ③ patterns - トップレベルのマッチングルール

ソースコードに対して適用されるルールの配列です。VS Code はここに書かれたルールを上から順に適用していきます。

```json
{
  "patterns": [
    { "include": "#comment" },
    { "include": "#string" },
    { "include": "#keyword" }
  ]
}
```

`#comment` のように `#` で始まる名前は、`repository` で定義されたルールを参照しています。

#### ④ repository - 再利用可能なルールの定義

ルールを名前付きで定義しておく場所です。`patterns` や他のルールから `#名前` で参照できます。

```json
{
  "repository": {
    "comment": {
      // コメントのマッチングルール
    },
    "string": {
      // 文字列のマッチングルール
    },
    "keyword": {
      // キーワードのマッチングルール
    }
  }
}
```

### マッチングルールの書き方

ルールには主に 2 つのパターンがあります。

#### パターン 1: match（単一行マッチ）

1 行内で完結するトークン（キーワード、数値など）に使います。

```json
{
  "name": "keyword.control.flow.python",
  "match": "\\b(if|for|while|return|try|except)\\b"
}
```

| キー | 説明 |
|------|------|
| `name` | マッチした部分に付けるスコープ名 |
| `match` | マッチさせる正規表現 |

この例では：
- `\\b` - 単語の境界（word boundary）
- `(if|for|while|return|try|except)` - いずれかのキーワード
- マッチしたら `keyword.control.flow.python` というスコープ名が付く

#### パターン 2: begin/end（複数行マッチ）

複数行にまたがるトークン（文字列、コメントブロックなど）に使います。

```json
{
  "name": "string.quoted.docstring.multi.python",
  "begin": "('''|\"\"\")",
  "end": "(\\1)",
  "beginCaptures": {
    "1": { "name": "punctuation.definition.string.begin.python" }
  },
  "endCaptures": {
    "1": { "name": "punctuation.definition.string.end.python" }
  },
  "patterns": [
    { "include": "#string-escape" }
  ]
}
```

| キー | 説明 |
|------|------|
| `begin` | 開始パターンの正規表現 |
| `end` | 終了パターンの正規表現（`\1` は begin のキャプチャグループを参照） |
| `beginCaptures` | 開始パターンのキャプチャグループに付けるスコープ |
| `endCaptures` | 終了パターンのキャプチャグループに付けるスコープ |
| `patterns` | 開始〜終了の間に適用するルール |

この例では：
- `'''` または `"""` で始まり
- 同じ記号で終わる
- その間は `string.quoted.docstring.multi.python` スコープが付く

### 実際のファイルの構造

MagicPython.tmLanguage.json の実際の構造を簡略化すると：

```json
{
  "name": "MagicPython",
  "scopeName": "source.python",
  "patterns": [
    { "include": "#statement" },
    { "include": "#expression" }
  ],
  "repository": {
    "statement": {
      "patterns": [
        { "include": "#import" },
        { "include": "#class-declaration" },
        { "include": "#function-declaration" },
        { "include": "#statement-keyword" }
      ]
    },
    "statement-keyword": {
      "patterns": [
        {
          "name": "keyword.control.flow.python",
          "match": "\\b(if|elif|else|for|while|try|except|finally|with|break|continue|return|raise|pass)\\b"
        },
        {
          "name": "storage.type.class.python",
          "match": "\\b(class)\\b"
        },
        {
          "name": "storage.type.function.python",
          "match": "\\b(def)\\b"
        }
      ]
    },
    "string": {
      "patterns": [
        { "include": "#string-quoted-single-line" },
        { "include": "#string-quoted-multi-line" }
      ]
    }
    // ... 他にも多数のルールが定義されている
  }
}
```

このように、`repository` で細かいルールを定義し、それらを `include` で組み合わせて使います。

### スコープ名の命名規則

スコープ名は階層的な命名規則に従っています。これにより、テーマで柔軟に色を指定できます。

```
keyword.control.flow.python
├── keyword           ← 大分類（キーワード）
├── control           ← 中分類（制御）
├── flow              ← 小分類（フロー制御）
└── python            ← 言語名
```

| スコープ名                        | 対象                            |
| --------------------------------- | ------------------------------- |
| `keyword.control.flow.python`     | 制御フローキーワード（if, for） |
| `storage.type.function.python`    | 関数定義キーワード（def）       |
| `support.function.builtin.python` | 組み込み関数                    |
| `constant.language.python`        | 言語定数（True, False, None）   |
| `string.quoted.single.python`     | シングルクォート文字列          |
| `comment.line.number-sign.python` | コメント                        |

では、これらのスコープがテーマファイルでどのように色付けされるか見てみましょう。

## テーマファイルでの色の割り当て

テーマファイル（例: `monokai-color-theme.json`）の `tokenColors` で、スコープに色を割り当てます。

例えば、上の表にある `keyword.control.flow.python` に色を付けるには、テーマファイルで以下のように設定します：

```json
{
  "tokenColors": [
    {
      "name": "Keyword",
      "scope": "keyword",
      "settings": { "foreground": "#F92672" }
    }
  ]
}
```

`scope: "keyword"` と指定すると、`keyword` で始まるすべてのスコープ（`keyword.control.flow.python` など）にこの色が適用されます。

### 文法定義とテーマの対応関係

具体的に、Python の `if` 文がどのように色付けされるか追ってみましょう：

```
① ソースコード:  if x > 0:
                  ↓
② 文法定義(.tmLanguage.json)が解析:
   「if」→ スコープ名「keyword.control.flow.python」を付与
                  ↓
③ テーマファイルが色を決定:
   「keyword で始まるスコープは #F92672（ピンク）」
                  ↓
④ 結果: 「if」がピンク色で表示される
```

### Monokai テーマの tokenColors 設定例

実際の Monokai テーマファイル（`monokai-color-theme.json`）から抜粋：

```json
{
  "tokenColors": [
    {
      "name": "Keyword",
      "scope": "keyword",
      "settings": { "foreground": "#F92672" }
    }
  ]
}
```

この設定により、`keyword.control.flow.python`（Python の `if`, `for` など）は `keyword` に前方一致して `#F92672`（ピンク）で表示されます。

### より詳細なスコープ指定の例（Dark+ テーマ）

Dark+ テーマでは、`keyword.control` を個別に指定しています：

```json
{
  "tokenColors": [
    {
      "name": "Control flow / Special keywords",
      "scope": [
        "keyword.control",
        "keyword.operator.new",
        "keyword.operator.delete"
      ],
      "settings": { "foreground": "#C586C0" }
    }
  ]
}
```

この場合、`keyword.control.flow.python` は `keyword.control` にマッチして `#C586C0`（紫）で表示されます。

### テーマによる違い

| テーマ  | スコープ指定      | `keyword.control.flow.python` の色 |
| ------- | ----------------- | ---------------------------------- |
| Monokai | `keyword`         | `#F92672` (ピンク)                 |
| Dark+   | `keyword.control` | `#C586C0` (紫)                     |

このように、テーマによってスコープの指定の粒度が異なります。

### 文法定義のスコープとテーマの対応表

| 文法定義のスコープ                | テーマでマッチするスコープ | 色 (Monokai)       |
| --------------------------------- | -------------------------- | ------------------ |
| `keyword.control.flow.python`     | `keyword`                  | `#F92672` (ピンク) |
| `storage.type.function.python`    | `storage.type`             | `#66D9EF` (水色)   |
| `comment.line.number-sign.python` | `comment`                  | `#88846f` (グレー) |
| `string.quoted.single.python`     | `string`                   | `#E6DB74` (黄色)   |
| `constant.language.python`        | `constant.language`        | `#AE81FF` (紫)     |

:::message
テーマのスコープは**前方一致**でマッチします。`keyword` は `keyword.control.flow.python` にマッチし、`keyword.control` を指定すればより限定的にマッチさせることもできます。
:::

## 現在のトークンを確認する方法

どの文字にどのスコープが適用されているかを確認するには：

1. `Cmd + Shift + P` でコマンドパレットを開く
2. 「**Developer: Inspect Editor Tokens and Scopes**」を実行
3. カーソル位置のトークン情報が表示される

## settings.json でトークンカラーを変更する

テーマを変えずに一部の色だけ変更したい場合は `editor.tokenColorCustomizations` を使います：

```json
{
  "editor.tokenColorCustomizations": {
    "comments": "#ee7800",
    "strings": "#00FF00"
  }
}
```

より詳細に設定する場合：

```json
{
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": "keyword.control.flow",
        "settings": { "foreground": "#FF0000" }
      }
    ]
  }
}
```

---

# Part 3: カスタムテーマを作って実験する

実際にカスタムテーマを作成して、スコープと色の対応を実験してみましょう。

## 方法 1: 拡張機能として作成（推奨）

VS Code のジェネレーターを使うと、テーマ拡張機能の雛形を簡単に作成できます。

### 1. 必要なツールをインストール

```bash
npm install -g yo generator-code
```

### 2. テーマの雛形を生成

```bash
yo code
```

対話形式で以下を選択：

```
? What type of extension do you want to create?
  → New Color Theme

? Do you want to import or convert an existing TextMate color theme?
  → No, start fresh

? What's the name of your extension?
  → my-custom-theme

? What's the identifier of your extension?
  → my-custom-theme

? What's the description of your extension?
  → My custom color theme

? What's the name of your theme shown to the user?
  → My Custom Theme

? Select a base theme:
  → Dark
```

### 3. 生成されたファイル構造

```
my-custom-theme/
├── package.json
├── themes/
│   └── my-custom-theme-color-theme.json  ← ここを編集
└── README.md
```

### 4. テーマファイルを編集

`themes/my-custom-theme-color-theme.json` を開いて編集します：

```json
{
  "name": "My Custom Theme",
  "type": "dark",
  "colors": {
    "editor.background": "#1e1e1e",
    "editor.foreground": "#d4d4d4",
    "activityBar.background": "#2d2d2d",
    "sideBar.background": "#252526"
  },
  "tokenColors": [
    {
      "name": "Comment",
      "scope": "comment",
      "settings": {
        "foreground": "#6A9955"
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
      "name": "Keyword Control Flow",
      "scope": "keyword.control",
      "settings": {
        "foreground": "#C586C0"
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
      "name": "Function",
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
    }
  ]
}
```

### 5. テーマをテストする

テーマのフォルダで VS Code を開き、`F5` を押すと新しいウィンドウが開き、テーマが適用されます。

```bash
cd my-custom-theme
code .
# F5 を押してデバッグ実行
```

新しいウィンドウで:

1. `Cmd + K, Cmd + T` でテーマ選択
2. 「My Custom Theme」を選択

### 6. 変更をリアルタイムで確認

テーマファイルを編集して保存すると、デバッグウィンドウに即座に反映されます。これを使って様々なスコープと色の組み合わせを実験できます。

## 方法 2: settings.json で手軽に実験

拡張機能を作らずに、`settings.json` で直接実験することもできます。

### textMateRules で詳細に指定

```json
{
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "name": "Control Flow Keywords (if, for, while)",
        "scope": "keyword.control.flow",
        "settings": {
          "foreground": "#FF6B6B",
          "fontStyle": "bold"
        }
      },
      {
        "name": "Function Definitions",
        "scope": "entity.name.function",
        "settings": {
          "foreground": "#4ECDC4"
        }
      },
      {
        "name": "Python Builtin Functions",
        "scope": "support.function.builtin.python",
        "settings": {
          "foreground": "#FFE66D"
        }
      }
    ]
  }
}
```

### 実験のコツ

1. **Developer: Inspect Editor Tokens and Scopes** でスコープ名を確認
2. `textMateRules` にそのスコープを追加
3. 派手な色（`#FF0000` など）を指定して変化を確認
4. 期待通りに動いたら好みの色に調整

## 実験例: Python の if 文の色を変える

Python ファイルで `if` の色だけを変えたい場合：

### 1. スコープを確認

Python ファイルで `if` にカーソルを置き、**Developer: Inspect Editor Tokens and Scopes** を実行：

```
textmate scopes:
  keyword.control.flow.python
  source.python
```

### 2. settings.json に追加

```json
{
  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": "keyword.control.flow.python",
        "settings": {
          "foreground": "#FF0000",
          "fontStyle": "bold italic"
        }
      }
    ]
  }
}
```

### 3. 結果

Python の `if`, `for`, `while`, `return` などが赤色の太字イタリックで表示されます。

## スコープの優先順位

複数のルールがマッチする場合、**より具体的なスコープが優先**されます：

```json
{
  "textMateRules": [
    {
      "scope": "keyword",
      "settings": { "foreground": "#0000FF" }
    },
    {
      "scope": "keyword.control",
      "settings": { "foreground": "#00FF00" }
    },
    {
      "scope": "keyword.control.flow.python",
      "settings": { "foreground": "#FF0000" }
    }
  ]
}
```

この場合、Python の `if` は:

- `keyword` → マッチ（青）
- `keyword.control` → より具体的にマッチ（緑）
- `keyword.control.flow.python` → 最も具体的にマッチ（赤） ← **これが適用される**

---

## まとめ

| 設定したい内容                         | 設定方法                                                        |
| -------------------------------------- | --------------------------------------------------------------- |
| UI の色（背景、サイドバーなど）        | `workbench.colorCustomizations` または テーマの `colors`        |
| トークンの色（シンタックスハイライト） | `editor.tokenColorCustomizations` または テーマの `tokenColors` |
| 何がどのトークンか（文法）             | `.tmLanguage.json`（通常は変更不要）                            |

テーマを自作する場合は、`colors` と `tokenColors` の両方を定義した JSON ファイルを作成します。

## 参考リンク

- [VS Code Theme Color Reference](https://code.visualstudio.com/api/references/theme-color)
- [VS Code Color Theme Guide](https://code.visualstudio.com/api/extension-guides/color-theme)
- [TextMate Language Grammars](https://macromates.com/manual/en/language_grammars)
- [シンタックスハイライト拡張機能の作り方（KAYAC）](https://techblog.kayac.com/vscode-extension-syntax-highlight)
