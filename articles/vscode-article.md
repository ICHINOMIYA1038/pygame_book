---
title: "VSCodeの見た目を好きなアニメのテーマカラーにカスタマイズする方法"
emoji: "⚡"
type: "tech"
topics: ["vscode", "theme", "extension", "tips"]
published: false
---

:::message
この記事は「COUNTER WORKS Advent Calendar 2025」の 15 日目の記事です。
:::

## はじめに

株式会社カウンターワークスで DevOps 業務を行っている一ノ宮です。

今回は弊社で行われている Tips 共有会についての紹介と、そのつながりで個人的に挑んだ VSCode の独自テーマの作成の取り組みを紹介したいと思います。

## 開発 Tips 共有会について

弊社では、開発 Tips の共有会を不定期で開催しています。

Tips 共有会は、開発に関しての新しい技術や知識、気づきを共有することを目的にしています。

前回の Tips 共有会は、今年の 8 月に行いました。

会社として AI に関する予算を多く使おうという方針もあり、前回は AI に関する共有が多く、特に claude code の使い方の知識やアイデア、失敗談などが多かったです。

他にも、こんなショートカット知ってますか？　とか　詳しいログの確認方法など内容が多岐にわたっていました。

全部で 35 もの Tips が繰り広げられる盛り上がりを見せました。

今回の記事は、そんな Tips 会にて、私の共有した Tips に関連するものです。

私の共有した Tips は

**「VSCode の色を好きなアニメの色に変えてモチベーションを上げる」** でした。

このテーマにより、どんな Tips でも共有していいんだという気持ちになるのではないでしょうか。それを狙っています。（何も思いつきませんでした。）

その時に作ったカラーは以下のようになります！

![自作カラーテーマ1](/images/vscode-anime-theme.png)

![自作カラーテーマ2](/images/vscode-pokemon-theme.png)

![自作カラーテーマ3](/images/vscode-dark-theme-settings.png)

何のアニメかはぜひ、ご想像ください。

作ったきっかけは、Claude Code で何か面白いことできないかなと思い、`settings.json` の色を変えてもらえれば、自作テーマも余裕のでは？と思って作りました。（設定ファイルをいじらせることになるので、真似する際には要注意）

クオリティは見ての通りなんですが、楽しかったので満足しています。

ただ、作った過程でこんな課題がありました。

:::message alert
**シンタックスハイライト、見にくい問題**
無理やり UI を変えるのはいいんですが、シンタックスハイライトのこととかを気にしていないので、文字によっては見にくくなります。
:::

そこで、もっと見やすいカラーテーマを作るために VSCode のカラーテーマやシンタックスハイライトの色の仕組みについて詳しく調べてみて、さらに実際の独自のカラーテーマを作成してみました。

## 私の環境

MacBook Pro 　 OS Sequoia 15.5
Cursor Version: 2.1.26
VSCode Version: 1.105.1
＊ 今回の記事のタイトルは VSCode ですが、VSCode をフォークした Cursor を利用しています。

## 公式のドキュメントを読む

まず、VSCode のカラーテーマを作るための資料です。
https://code.visualstudio.com/api/extension-guides/color-theme?ref=trap.jp#create-a-new-color-theme

この記事によると、**一番簡単な方法は既存のカラーテーマをカスタマイズすること**です。

VSCode の設定画面から `workbench.colorCustomizations` を検索

![colorCustomizations の設定画面](/images/vscode-color-customizations-setting.png)

`setting.json` で以下を記載すると、タイトルバーの色が赤くなるのがわかります。

```json
{
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#ff0000"
  }
}
```

![タイトルバーが赤くなった例](/images/vscode-titlebar-red.png)

このようにテーマカラーに関しては、**`setting.json` を変更するだけで変更できる**ことがわかります。
これは、私が冒頭に述べた Claude Code にやらせていた方法ですね。

どの設定がどの部分の色に対応するかは以下のドキュメントを参考にしてください。
https://code.visualstudio.com/api/references/theme-color

:::details 設定可能なオプション一覧（クリックで展開）

#### 基本色 (Base colors)

全体的な前景色や背景色、フォーカス時のボーダー色などを設定できます。

| オプション             | 説明                                     |
| ---------------------- | ---------------------------------------- |
| `focusBorder`          | フォーカスされた要素の全体的なボーダー色 |
| `foreground`           | 全体的な前景色（テキストの色）           |
| `widget.shadow`        | ウィジェット（検索/置換など）の影の色    |
| `selection.background` | ワークベンチ内のテキスト選択の背景色     |
| `errorForeground`      | エラーメッセージの前景色                 |

#### アクティビティバー (Activity Bar)

左端のアイコンが並んでいるバーの色を設定できます。

| オプション                    | 説明                         |
| ----------------------------- | ---------------------------- |
| `activityBar.background`      | アクティビティバーの背景色   |
| `activityBar.foreground`      | アクティブ時のアイコン前景色 |
| `activityBarBadge.background` | バッジ（通知数など）の背景色 |
| `activityBarBadge.foreground` | バッジの前景色               |

#### サイドバー (Side Bar)

ファイルエクスプローラーなどが表示されるサイドバーの色を設定できます。

| オプション                        | 説明                       |
| --------------------------------- | -------------------------- |
| `sideBar.background`              | サイドバーの背景色         |
| `sideBar.foreground`              | サイドバーの前景色         |
| `sideBarTitle.foreground`         | サイドバータイトルの前景色 |
| `sideBarSectionHeader.background` | セクションヘッダーの背景色 |

#### エディター (Editor colors)

コードを編集するメインエリアの色を設定できます。

| オプション                       | 説明                         |
| -------------------------------- | ---------------------------- |
| `editor.background`              | エディターの背景色           |
| `editor.foreground`              | エディターのデフォルト前景色 |
| `editorCursor.foreground`        | カーソルの色                 |
| `editor.lineHighlightBackground` | カーソル行のハイライト背景色 |
| `editorLineNumber.foreground`    | 行番号の色                   |
| `editor.selectionBackground`     | 選択範囲の背景色             |

#### ステータスバー (Status Bar)

画面下部のステータスバーの色を設定できます。

| オプション                      | 説明                             |
| ------------------------------- | -------------------------------- |
| `statusBar.background`          | 標準時のステータスバー背景色     |
| `statusBar.foreground`          | ステータスバーの前景色           |
| `statusBar.debuggingBackground` | デバッグ中のステータスバー背景色 |
| `statusBar.noFolderBackground`  | フォルダを開いていない時の背景色 |

#### ターミナル (Integrated Terminal)

統合ターミナルの色を設定できます。

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

#### タブ (Editor Groups & Tabs)

エディタのタブの色を設定できます。

| オプション                         | 説明                       |
| ---------------------------------- | -------------------------- |
| `editorGroupHeader.tabsBackground` | タブコンテナの背景色       |
| `tab.activeBackground`             | アクティブなタブの背景色   |
| `tab.activeForeground`             | アクティブなタブの前景色   |
| `tab.inactiveBackground`           | 非アクティブなタブの背景色 |
| `tab.inactiveForeground`           | 非アクティブなタブの前景色 |
| `tab.border`                       | タブ間のボーダー色         |

:::

### 複数の設定をまとめて適用する例

実際にカスタムテーマを作る場合は、これらを組み合わせて使用します。

```json
{
  "workbench.colorCustomizations": {
    // タイトルバー
    "titleBar.activeBackground": "#282c34",
    "titleBar.activeForeground": "#9da5b4",

    // アクティビティバー
    "activityBar.background": "#21252b",
    "activityBar.foreground": "#d7dae0",

    // サイドバー
    "sideBar.background": "#21252b",
    "sideBar.foreground": "#abb2bf",

    // エディター
    "editor.background": "#282c34",
    "editor.foreground": "#abb2bf",

    // ステータスバー
    "statusBar.background": "#21252b",
    "statusBar.foreground": "#9da5b4"
  }
}
```

:::message
色の形式は `#RGB`、`#RGBA`、`#RRGGBB`、`#RRGGBBAA` が使用できます。
アルファ値（透明度）を指定する場合は `#RRGGBBAA` 形式を使用します（例: `#00000050` は 50%の透明度）。
:::

すべてのテーマカラーの一覧は[公式ドキュメント](https://code.visualstudio.com/api/references/theme-color)を参照してください。

## シンタックスハイライト

次は、**シンタックスハイライトの色**を変えます。

シンタックスハイライトの色については**二つの方法**があります。

1. `-color-theme.json` を使ってテーマ自体を変える方法
2. `editor.tokenColorCustomizations` を使ってテーマを上から部分的に変える方法

今回はテーマの自作ですので、`-color-theme.json` の変更を考えますが、参考までに `editor.tokenColorCustomizations` の方法も紹介します。

### editor.tokenColorCustomizations でテーマを上書きする

例えば、以下のような設定を `setting.json` に書くと、コメントの色がオレンジ色に変化します。

```json
{
  "editor.tokenColorCustomizations": {
    "comments": "#ee7800", // コメント: オレンジ
    "strings": "#00FF00" // 文字列: 緑
  }
}
```

![tokenColorCustomizations の適用例](/images/vscode-token-color-example.png)

### シンタックスハイライトの仕組み

テーマファイルを変える前にシンタックスハイライトの説明をさせてください。

シンタックスハイライトは、特定のキーワードに色をつける仕組みです。

文章の中で特定のキーワードを検出するためにはある程度、意味ごとの塊でソースコードを読んでもらう必要があります。

そこで、シンタックスハイライトは一般的なトークンタイプを参考にしています。

トークンというのは簡単にいうと、**ソースコードの中で、意味を持つ最小の単位に分解したもの**です。

例えば以下のコードをトークンに分解すると次のようになります。

```
const msg = "hello";
```

| トークン  | 種類 　    |
| --------- | ---------- |
| `const`   | キーワード |
| `msg`     | 変数名     |
| `=`       | 演算子     |
| `"hello"` | 文字列 　  |
| `;`       | 記号 　    |

VSCode はトークン化のエンジンとして、**TextMate 文法**を使用しています。
TextMate 文法では、正規表現を用いてコード解析してトークンを識別しています。

:::details 参考: TextMate の文法の仕組み
TextMate の文法の仕組みは以下のドキュメントが参考になりました。
https://macromates.com/manual/en/language_grammars?utm_source=chatgpt.com
:::

トークン解析のルールは、**`.tmLanguage.json`** ファイルを変更することで変更できます。

しかし、言語によってキーワードの種類が違うため、どの文字にどの色をつけていいか、どうやって判断しているのでしょうか？

それは**言語ごとに `.tmLanguage.json` が用意されている**からです。

拡張機能でシンタックスハイライトを入れている方も多いかと思いますが、
そのシンタックスハイライトプラグインは、TextMate 文法ファイル（`.tmLanguage.json` など）を提供しています。

:::details 参考: .tmLanguage.json について詳しく
`.tmLanguage.json` に関しては、以下の記事がとても参考になりました。
https://techblog.kayac.com/vscode-extension-syntax-highlight
:::

特定の言語にどの拡張機能がハイライトしているかを確認するには以下の方法がおすすめです。

1. `Cmd + Shift + P` → **「Extensions: Show Built-in Extensions」**
2. 言語名で検索（例: "python"）

検索した上で、その拡張機能の実体を見に行くと、`.tmLanguage.json` のファイルを見つけることができます。

:::message
**拡張機能のファイルの場所（Mac の場合）**
`/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/`
:::

## 文法定義ファイル（.tmLanguage.json）について掘り下げ

文法定義ファイルは **「どの文字列がどのスコープに該当するか」を正規表現で定義** しています。ここでは Python の文法定義（MagicPython.tmLanguage.json）を例に、その構造を詳しく見ていきます。

:::message
**トークンのスコープを確認する方法**

1. `Cmd + Shift + P` でコマンドパレットを開く
2. **「Developer: Inspect Editor Tokens and Scopes」** を実行
3. カーソル位置のトークンに適用されているスコープが表示される
   :::

### 全体の構造を理解する

まず、`.tmLanguage.json` の全体像を把握しましょう。大きく分けて 4 つのパートがあります：

```json
{
  "name": "MagicPython",           // ① 文法の名前
  "scopeName": "source.python",    // ② この文法ファイルの名前
  "patterns": [ ... ],             // ③ 解析の入り口
  "repository": { ... }            // ④ 再利用可能なルールの定義
}
```

#### ① name - 文法の名前

人間が読むための名前です。VS Code の内部では特に使われません。

#### ② scopeName - この文法ファイルの名前

この文法ファイル全体を識別するための名前です。VS Code が「どの文法ファイルを使うか」を判断するときに使います。

#### ③ patterns - 解析の入り口

VS Code がソースコードを解析するときの**入り口**です。ここに書かれたルールを上から順に試していきます。

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

解析の流れをイメージすると：

```
patterns（入り口）
├── #comment を調べる → コメントならスコープを付ける
├── #string を調べる → 文字列ならスコープを付ける
└── #keyword を調べる
    ├── #keyword-if を調べる
    └── #keyword-for を調べる
```

このように、`patterns` は最初の入り口で、そこから `repository` のルールを辿っていく構造になっています。

#### ④ repository - 具体的なルールの定義

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

| キー    | 説明                             |
| ------- | -------------------------------- |
| `name`  | マッチした部分に付けるスコープ名 |
| `match` | マッチさせる正規表現             |

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
  "patterns": [{ "include": "#string-escape" }]
}
```

| キー            | 説明                                                               |
| --------------- | ------------------------------------------------------------------ |
| `begin`         | 開始パターンの正規表現                                             |
| `end`           | 終了パターンの正規表現（`\1` は begin のキャプチャグループを参照） |
| `beginCaptures` | 開始パターンのキャプチャグループに付けるスコープ                   |
| `endCaptures`   | 終了パターンのキャプチャグループに付けるスコープ                   |
| `patterns`      | 開始〜終了の間に適用するルール                                     |

この例では：

- `'''` または `"""` で始まり
- 同じ記号で終わる
- その間は `string.quoted.docstring.multi.python` スコープが付く

Python で書くとこういうコードです：

```python
def greet(name):
    """
    この関数は挨拶を返します。
    name: 名前
    """
    return f"Hello, {name}!"
```

`"""` で囲まれた部分全体の色が変わることになります。

### スコープ名の命名規則

少しややこしいのですが、文法ファイル(.tmLanguage.json の冒頭に書かれたスコープ名)とは別にマッチングルールごとにスコープ名があります。

以下のルールでは、"keyword.control.flow.python"をスコープ名と呼ぶことにします。

このスコープ名をもとに色付けがなされます。

```json
{
  "name": "keyword.control.flow.python",
  "match": "\\b(if|for|while|return|try|except)\\b"
}
```

スコープ名は階層的な命名規則に従っています。

```
keyword.control.flow.python
├── keyword           ← 大分類（キーワード）
├── control           ← 中分類（制御）
├── flow              ← 小分類（フロー制御）
└── python            ← 言語名
```

これで、`.tmLanguage.json`の説明は以上です。この後、実際にこの定義したスコープに応じて色をつけていきます。

## テーマファイルでの色の割り当て

`.tmLanguage.json` が決めたスコープに対して、テーマファイル（`-color-theme.json`）が色を割り当てます。

:::message
**ファイルの役割分担**
| ファイル | 役割 | 説明 |
| --- | --- | --- |
| **`.tmLanguage.json`** | 文法定義（Grammar） | コードを解析して「どの部分が何か」を判別する |
| **`-color-theme.json`** | 配色定義（Theme） | 文法で分類されたトークンに色を割り当てる |
:::

## テーマファイルの作成

今回は **`yo code`（Yeoman + generator-code）** を使ってカラーテーマを作ります。
`yo code` は VSCode の拡張機能やカラーテーマを簡単に作ることができるツールです。

### 1. yo code のインストール確認

```bash
yo --version
# 5.x.x などが表示されれば OK
```

### 2. テーマの雛形を生成

作業用ディレクトリに移動して、ジェネレーターを実行します：

```bash
mkdir ~/vscode-themes
cd ~/vscode-themes
yo code
```

### 3. 対話形式で設定

yes / no で質問が聞かれるので、お好みで設定します。
**What type of extension do you want to create?** に対しては、
**New Color Theme** を選択します。

### 4. ファイルの確認

`themes/My Test Theme-color-theme.json` を開いてみましょう
このファイルが、説明してきたスコープに対して色をつける役割をするファイルです。

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

:::message
**テーマをプレビューする手順**

1. **F5** を押す（デバッグ実行）
2. 新しい VS Code ウィンドウが開く
3. `Cmd + K, Cmd + T`（テーマ選択）
4. 「My Test Theme（自分でつけた名前）」を選択
5. テーマファイルに編集を入れた場合、`Cmd + Shift + R` でリロード
   :::

例えば、上述の Python の複数行コメント（docstring）の色を変える場合には以下のように書きます。

```json
{
  "name": "長いコメントをピンク色にしてみる",
  "scope": ["string.quoted.docstring.multi.python"],
  "settings": {
    "foreground": "#FF69B4" // ピンク
  }
}
```

わかりやすいように他の色の設定を消したので、該当部分以外は黒くなっています。

![docstring がピンク色に変化](/images/vscode-docstring-pink.png)

ということで、これで好きなようにカラーテーマを設定できるようにしました。

最終的に私が作成したテーマはこちらです！

![完成したカラーテーマ](/images/vscode-final-theme.png)

このようにカラーテーマの仕組みを理解することで、**VSCode の色を自由自在に変えることができます**。

## おまけ: アスキーアートに色をつけてみた

好きな文字を好きな色に変えることができるということは、**アスキーアートに好きな色をつけることができるんじゃないか**と閃いたので、作ってみました。

**1. まず、絵を描きます。猫にしました。**

![手描きの猫](/images/cat-drawing.jpg)

**2. Gemini を使って色をつけます。**

![Gemini で生成した猫画像](/images/gemini-cat-image.png)

**3. Claude Code にアスキーアートを生成させます。**

**4. Claude Code にカラーテーマを調整させます。**

**5. 完成！**

![アスキーアートの猫](/images/vscode-ascii-art-cat.png)

---

いかがだったでしょうか。今回の内容は AI とは直接関係がありませんが、**AI を使いこなすためには遊び心が大事**だと思っています。
今回のような遊びは AI があるからこそできる研究でした。ぜひ皆さんも自分だけのカラーテーマを作ってみてください！

## 参考文献

- [VS Code Color Theme Guide（公式）](https://code.visualstudio.com/api/extension-guides/color-theme)
- [Theme Color Reference（公式）](https://code.visualstudio.com/api/references/theme-color)
- [TextMate Language Grammars](https://macromates.com/manual/en/language_grammars)
- [VSCode 拡張機能でシンタックスハイライトを作る（カヤック）](https://techblog.kayac.com/vscode-extension-syntax-highlight)

## We are hiring!!

カウンターワークスでは、積極的に AI の活用をしたいというエンジニアも募集しています！

少しでも興味があれば、ぜひ気軽にお声がけください！
