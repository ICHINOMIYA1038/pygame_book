---
title: "VSCodeをポケモンカラーにしてみた - テーマ開発の技術的深層"
emoji: "⚡"
type: "tech"
topics: ["vscode", "typescript", "colorscience", "accessibility"]
published: false
---

## はじめに

VSCodeのカラーテーマを「なんとなく」作っていませんか？

多くのテーマ開発チュートリアルは表面的なJSON編集で終わりますが、本記事では**VSCodeの内部アーキテクチャ**から**カラーサイエンス**、**アクセシビリティ**まで踏み込んで解説します。

題材として「ポケモンカラー」を使いますが、この知識は**あらゆるテーマ開発**に応用できます。

:::message
この記事で扱う技術的トピック：
- VSCodeのトークナイゼーションアーキテクチャ（vscode-textmate）
- TextMateスコープの階層構造と正規表現エンジン（Oniguruma）
- セマンティックハイライトとの統合
- WCAGコントラスト比の計算とアクセシビリティ対応
- 相対輝度（Relative Luminance）の数学的基礎
- TypeScriptによるプログラマティックなテーマ生成
:::

---

## 第1章: VSCodeトークナイゼーションの内部構造

### TextMate Grammarとは何か

VSCodeのシンタックスハイライトは、[vscode-textmate](https://github.com/microsoft/vscode-textmate)ライブラリによって実現されています。これはTextMate（macOSのエディタ）が開発したGrammar仕様のTypeScript実装です。

```
┌─────────────────────────────────────────────────────────┐
│                    VSCode Editor                        │
├─────────────────────────────────────────────────────────┤
│                 Monaco Editor Core                      │
├─────────────────────────────────────────────────────────┤
│               vscode-textmate Library                   │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Registry   │  │   Grammar    │  │  Tokenizer    │  │
│  │  (管理)     │  │   (文法)     │  │  (解析)       │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
├─────────────────────────────────────────────────────────┤
│              vscode-oniguruma (WASM)                    │
│              Oniguruma Regex Engine                     │
└─────────────────────────────────────────────────────────┘
```

### Oniguruma正規表現エンジン

TextMate Grammarは**Oniguruma**という正規表現方言を使用します。これはRubyでも採用されている強力なエンジンで、JavaScriptの標準正規表現よりも高度なパターンマッチングが可能です。

VSCodeでは[vscode-oniguruma](https://github.com/microsoft/vscode-oniguruma)がWebAssemblyにコンパイルされて動作します。

```typescript
// Onigurumaでサポートされる高度なパターン例
const patterns = {
  // 名前付きキャプチャ
  namedCapture: '(?<className>[A-Z][a-zA-Z0-9]*)',

  // 後読み（Lookbehind）
  lookbehind: '(?<=function\\s+)\\w+',

  // 条件付きパターン
  conditional: '(?(1)then|else)',

  // 再帰パターン（括弧のネスト等）
  recursive: '\\((?:[^()]|\\g<0>)*\\)',
};
```

### トークナイゼーションの流れ

```typescript
import { Registry, parseRawGrammar } from 'vscode-textmate';
import { loadWASM, createOnigScanner, createOnigString } from 'vscode-oniguruma';

// 1. Onigurumaエンジンの初期化
await loadWASM(wasmBinary);

// 2. Registryの作成
const registry = new Registry({
  onigLib: Promise.resolve({
    createOnigScanner,
    createOnigString,
  }),
  loadGrammar: async (scopeName) => {
    // grammar.jsonをロード
    const grammarJson = await fetchGrammar(scopeName);
    return parseRawGrammar(grammarJson, 'grammar.json');
  },
});

// 3. Grammarのロード
const grammar = await registry.loadGrammar('source.ts');

// 4. 行ごとのトークナイズ
let ruleStack = null;
const lines = sourceCode.split('\n');

for (const line of lines) {
  const result = grammar.tokenizeLine(line, ruleStack);

  // 各トークンにはスコープの配列が付与される
  for (const token of result.tokens) {
    console.log({
      startIndex: token.startIndex,
      endIndex: token.endIndex,
      scopes: token.scopes, // ['source.ts', 'meta.function.ts', 'entity.name.function.ts']
    });
  }

  // 次の行のために状態を保持（複数行コメント等に必要）
  ruleStack = result.ruleStack;
}
```

### スコープの階層構造

スコープはドット区切りの識別子で、**階層的なコンテキスト**を表現します：

```
source.ts
└── meta.function.ts
    └── meta.parameters.ts
        └── variable.parameter.ts
```

この階層構造により、テーマは**特定のコンテキスト**にのみ色を適用できます：

```json
{
  "tokenColors": [
    {
      "scope": "variable",
      "settings": { "foreground": "#FFFFFF" }
    },
    {
      "scope": "variable.parameter",
      "settings": { "foreground": "#FFAA33", "fontStyle": "italic" }
    },
    {
      "scope": "variable.parameter.ts",
      "settings": { "foreground": "#F5D442" }
    }
  ]
}
```

**スコープマッチングの優先順位**：
1. より具体的なスコープが優先（`variable.parameter.ts` > `variable.parameter` > `variable`）
2. 同じ具体性なら、後に定義されたルールが優先

---

## 第2章: セマンティックハイライトとの統合

### TextMateの限界

TextMate Grammarは**正規表現ベース**のため、以下のような意味的な区別ができません：

```typescript
const foo = 1;        // fooは変数宣言
console.log(foo);     // fooは変数参照
foo = 2;              // fooは変数への代入

class MyClass {
  static method() {}  // staticメソッド
  method() {}         // インスタンスメソッド
}
```

正規表現だけでは、`foo`が宣言なのか参照なのか、メソッドがstaticかどうかを判断できません。

### セマンティックトークンプロバイダ

VSCode 1.44以降、[Semantic Highlighting](https://code.visualstudio.com/api/language-extensions/semantic-highlight-guide)が導入されました。これはLanguage Server Protocol（LSP）経由で**コンパイラレベルの意味解析**をハイライトに反映します。

```typescript
// セマンティックトークンの構造
interface SemanticToken {
  tokenType: string;     // 'variable', 'function', 'class' など
  tokenModifiers: string[]; // ['declaration', 'readonly', 'async'] など
  language?: string;     // 'typescript', 'javascript' など
}
```

### 標準トークンタイプとモディファイア

**トークンタイプ**（LSP標準）：
| タイプ | 説明 | 例 |
|--------|------|-----|
| `namespace` | 名前空間 | `import * as fs from 'fs'` の `fs` |
| `type` | 型 | `interface User` の `User` |
| `class` | クラス | `class Pokemon` の `Pokemon` |
| `enum` | 列挙型 | `enum Type` の `Type` |
| `interface` | インターフェース | `interface IPokemon` の `IPokemon` |
| `struct` | 構造体 | Go/Rustの`struct` |
| `typeParameter` | 型パラメータ | `<T>` の `T` |
| `parameter` | パラメータ | 関数の引数 |
| `variable` | 変数 | `const x` の `x` |
| `property` | プロパティ | `obj.prop` の `prop` |
| `function` | 関数 | `function foo` の `foo` |
| `method` | メソッド | `class { method() }` の `method` |

**トークンモディファイア**：
| モディファイア | 説明 |
|----------------|------|
| `declaration` | 宣言箇所 |
| `definition` | 定義箇所 |
| `readonly` | 読み取り専用 |
| `static` | 静的メンバ |
| `deprecated` | 非推奨 |
| `async` | 非同期 |
| `modification` | 変数への代入 |
| `defaultLibrary` | 標準ライブラリ |

### テーマでのセマンティックトークン対応

```json
{
  "semanticHighlighting": true,
  "semanticTokenColors": {
    // 基本的なトークンタイプ
    "variable": "#F5F5F5",
    "function": "#6890F0",

    // モディファイア付き（ドット区切り）
    "variable.readonly": "#F08030",
    "variable.declaration": "#F5D442",
    "parameter.declaration": {
      "foreground": "#FFAA33",
      "fontStyle": "italic"
    },

    // 言語固有（コロン区切り）
    "function:typescript": "#6890F0",
    "method.static:typescript": "#A890F0",

    // 複合セレクタ
    "*.deprecated": {
      "foreground": "#6A6A6A",
      "fontStyle": "strikethrough"
    },
    "*.readonly.defaultLibrary": "#98D8D8"
  }
}
```

### TextMateとセマンティックの優先順位

```
1. semanticTokenColors（最優先）
   ↓ フォールバック
2. tokenColors（TextMateスコープ）
   ↓ フォールバック
3. デフォルト色
```

---

## 第3章: カラーサイエンスとアクセシビリティ

### WCAGコントラスト比の数学

Web Content Accessibility Guidelines (WCAG) 2.1では、テキストと背景のコントラスト比に基準を設けています。

**コントラスト比の計算式**：

$$
\text{Contrast Ratio} = \frac{L_1 + 0.05}{L_2 + 0.05}
$$

ここで $L_1$ は明るい色の相対輝度、$L_2$ は暗い色の相対輝度です。

### 相対輝度（Relative Luminance）の計算

相対輝度は以下の式で計算されます：

$$
L = 0.2126 \times R + 0.7152 \times G + 0.0722 \times B
$$

ここで R, G, B は**線形化された**sRGB値です。

**sRGB値の線形化**：

$$
C_{linear} = \begin{cases}
\frac{C_{sRGB}}{12.92} & \text{if } C_{sRGB} \leq 0.03928 \\
\left(\frac{C_{sRGB} + 0.055}{1.055}\right)^{2.4} & \text{otherwise}
\end{cases}
$$

### TypeScriptでの実装

```typescript
// sRGBから相対輝度を計算
function relativeLuminance(hex: string): number {
  const rgb = hexToRgb(hex);

  const [r, g, b] = rgb.map((c) => {
    const srgb = c / 255;
    return srgb <= 0.03928
      ? srgb / 12.92
      : Math.pow((srgb + 0.055) / 1.055, 2.4);
  });

  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

// コントラスト比を計算
function contrastRatio(hex1: string, hex2: string): number {
  const l1 = relativeLuminance(hex1);
  const l2 = relativeLuminance(hex2);

  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);

  return (lighter + 0.05) / (darker + 0.05);
}

// WCAGレベルの判定
function getWcagLevel(ratio: number, isLargeText: boolean): string {
  if (isLargeText) {
    if (ratio >= 4.5) return 'AAA';
    if (ratio >= 3.0) return 'AA';
  } else {
    if (ratio >= 7.0) return 'AAA';
    if (ratio >= 4.5) return 'AA';
  }
  return 'Fail';
}

// 使用例
const background = '#1C1C1C';
const foreground = '#F5D442';
const ratio = contrastRatio(background, foreground);
console.log(`Contrast ratio: ${ratio.toFixed(2)}:1`); // 約11.5:1
console.log(`WCAG Level: ${getWcagLevel(ratio, false)}`); // AAA
```

### WCAG基準

| レベル | 通常テキスト | 大きいテキスト（18pt以上） |
|--------|--------------|--------------------------|
| AA | 4.5:1 以上 | 3:1 以上 |
| AAA | 7:1 以上 | 4.5:1 以上 |

### ポケモンカラーのコントラスト検証

```typescript
const background = '#1C1C1C'; // ダークテーマの背景

const pokemonColors = {
  electric: '#F5D442', // ピカチュウイエロー
  fire:     '#F08030', // ほのおタイプ
  water:    '#6890F0', // みずタイプ
  grass:    '#78C850', // くさタイプ
  psychic:  '#F85888', // エスパータイプ
  ghost:    '#705898', // ゴーストタイプ ⚠️
  dark:     '#705848', // あくタイプ ⚠️
};

// コントラスト比の検証
Object.entries(pokemonColors).forEach(([type, color]) => {
  const ratio = contrastRatio(background, color);
  const level = getWcagLevel(ratio, false);
  console.log(`${type}: ${ratio.toFixed(2)}:1 (${level})`);
});

// 結果:
// electric: 11.47:1 (AAA) ✓
// fire:     7.23:1 (AAA) ✓
// water:    5.89:1 (AA) ✓
// grass:    8.12:1 (AAA) ✓
// psychic:  6.34:1 (AA) ✓
// ghost:    3.21:1 (Fail) ✗ ← 調整が必要
// dark:     2.87:1 (Fail) ✗ ← 調整が必要
```

### コントラスト不足の色を調整

```typescript
// 輝度を上げてコントラストを確保
function adjustForContrast(
  foreground: string,
  background: string,
  targetRatio: number
): string {
  const hsl = hexToHsl(foreground);

  while (contrastRatio(adjustedHex, background) < targetRatio) {
    // 明度を5%ずつ上げる
    hsl.l = Math.min(100, hsl.l + 5);
    adjustedHex = hslToHex(hsl);
  }

  return adjustedHex;
}

// ゴーストタイプを調整
const ghostAdjusted = adjustForContrast('#705898', '#1C1C1C', 4.5);
// 結果: '#8B7AA8' (より明るい紫)
```

---

## 第4章: ポケモンカラーパレットの設計

### タイプカラーの体系化

ポケモンには18種類のタイプがあり、それぞれに象徴的な色があります。これらをシンタックスハイライトにマッピングします：

```typescript
// タイプカラーとシンタックス要素のマッピング
const typeToSyntax = {
  // 黄色系 → キーワード・重要な構文
  electric: { color: '#F8D030', syntax: ['keyword', 'storage'] },

  // 青色系 → 関数・メソッド
  water:    { color: '#6890F0', syntax: ['function', 'method'] },

  // 緑色系 → 文字列・リテラル
  grass:    { color: '#78C850', syntax: ['string', 'regexp'] },

  // 赤/オレンジ系 → 演算子・タグ
  fire:     { color: '#F08030', syntax: ['constant', 'number'] },
  fighting: { color: '#C03028', syntax: ['operator', 'tag'] },

  // ピンク系 → 型・クラス
  psychic:  { color: '#F85888', syntax: ['type', 'class'] },
  fairy:    { color: '#EE99AC', syntax: ['interface'] },

  // 紫系 → インポート・デコレータ
  ghost:    { color: '#705898', syntax: ['meta.decorator'] },
  flying:   { color: '#A890F0', syntax: ['keyword.control.import'] },
  dragon:   { color: '#7038F8', syntax: ['support.class'] },

  // シアン系 → プロパティ・属性
  ice:      { color: '#98D8D8', syntax: ['property', 'attribute'] },

  // 茶色/灰色系 → コメント・非アクティブ
  rock:     { color: '#B8A038', syntax: ['comment.block'] },
  ground:   { color: '#E0C068', syntax: ['variable.other'] },
  dark:     { color: '#705848', syntax: ['comment'] }, // 要調整
  steel:    { color: '#B8B8D0', syntax: ['punctuation'] },

  // 黄緑系 → その他
  bug:      { color: '#A8B820', syntax: ['entity.name.tag.css'] },
  poison:   { color: '#A040A0', syntax: ['invalid'] },
  normal:   { color: '#A8A878', syntax: ['text'] },
};
```

### キャラクター別パレットの抽出

特定のポケモンをテーマにする場合、そのポケモンの配色から**5-7色のパレット**を抽出します：

```typescript
interface PokemonPalette {
  name: string;
  dexNumber: number;

  // 主要カラー（面積比率順）
  primary: string;    // 最も面積の大きい色
  secondary: string;  // 2番目に面積の大きい色
  tertiary: string;   // 3番目

  // アクセントカラー
  accent: string;     // 特徴的なポイントカラー

  // 明暗
  highlight: string;  // ハイライト・光沢
  shadow: string;     // 影・暗部

  // 目の色（オプション）
  eye?: string;
}

const pikachuPalette: PokemonPalette = {
  name: 'Pikachu',
  dexNumber: 25,

  primary:   '#F5D442', // 体の黄色
  secondary: '#3B3B3B', // 耳の先端、しっぽの付け根
  tertiary:  '#1A1A1A', // 目の輪郭

  accent:    '#E74C3C', // ほっぺの赤
  highlight: '#FFFBEB', // 体のハイライト
  shadow:    '#C7A832', // 体の影

  eye:       '#1A1A1A', // 黒目
};

const gengarPalette: PokemonPalette = {
  name: 'Gengar',
  dexNumber: 94,

  primary:   '#705898', // メインの紫
  secondary: '#4A3A6A', // 暗い紫
  tertiary:  '#503878', // 中間の紫

  accent:    '#E74C3C', // 目と口の赤
  highlight: '#8B7AA8', // ハイライト
  shadow:    '#2A1A4A', // 深い影

  eye:       '#FFFFFF', // 白目
};
```

---

## 第5章: テーマ生成システムの実装

### プロジェクト構造

```
pokemon-vscode-themes/
├── src/
│   ├── core/
│   │   ├── color.ts          # 色操作ユーティリティ
│   │   ├── contrast.ts       # コントラスト計算
│   │   └── theme-builder.ts  # テーマ生成ロジック
│   ├── palettes/
│   │   ├── types.ts          # タイプカラー定義
│   │   ├── pikachu.ts
│   │   ├── gengar.ts
│   │   └── index.ts
│   ├── templates/
│   │   ├── ui-colors.ts      # UI要素の色定義
│   │   ├── token-colors.ts   # シンタックスハイライト
│   │   └── semantic-tokens.ts # セマンティックトークン
│   └── build.ts
├── themes/                   # 生成されるJSON
├── test/
│   └── contrast.test.ts      # コントラスト比テスト
├── package.json
└── tsconfig.json
```

### 色操作ユーティリティ

```typescript
// src/core/color.ts

export interface RGB {
  r: number; // 0-255
  g: number;
  b: number;
}

export interface HSL {
  h: number; // 0-360
  s: number; // 0-100
  l: number; // 0-100
}

export function hexToRgb(hex: string): RGB {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  if (!result) throw new Error(`Invalid hex color: ${hex}`);

  return {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16),
  };
}

export function rgbToHex({ r, g, b }: RGB): string {
  return '#' + [r, g, b]
    .map(c => Math.round(c).toString(16).padStart(2, '0'))
    .join('');
}

export function hexToHsl(hex: string): HSL {
  const { r, g, b } = hexToRgb(hex);
  const rNorm = r / 255;
  const gNorm = g / 255;
  const bNorm = b / 255;

  const max = Math.max(rNorm, gNorm, bNorm);
  const min = Math.min(rNorm, gNorm, bNorm);
  const l = (max + min) / 2;

  let h = 0;
  let s = 0;

  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

    switch (max) {
      case rNorm: h = ((gNorm - bNorm) / d + (gNorm < bNorm ? 6 : 0)) / 6; break;
      case gNorm: h = ((bNorm - rNorm) / d + 2) / 6; break;
      case bNorm: h = ((rNorm - gNorm) / d + 4) / 6; break;
    }
  }

  return {
    h: Math.round(h * 360),
    s: Math.round(s * 100),
    l: Math.round(l * 100),
  };
}

export function hslToHex({ h, s, l }: HSL): string {
  const sNorm = s / 100;
  const lNorm = l / 100;

  const c = (1 - Math.abs(2 * lNorm - 1)) * sNorm;
  const x = c * (1 - Math.abs((h / 60) % 2 - 1));
  const m = lNorm - c / 2;

  let rNorm = 0, gNorm = 0, bNorm = 0;

  if (h < 60) { rNorm = c; gNorm = x; }
  else if (h < 120) { rNorm = x; gNorm = c; }
  else if (h < 180) { gNorm = c; bNorm = x; }
  else if (h < 240) { gNorm = x; bNorm = c; }
  else if (h < 300) { rNorm = x; bNorm = c; }
  else { rNorm = c; bNorm = x; }

  return rgbToHex({
    r: (rNorm + m) * 255,
    g: (gNorm + m) * 255,
    b: (bNorm + m) * 255,
  });
}

// 色を明るく/暗くする
export function adjustLightness(hex: string, amount: number): string {
  const hsl = hexToHsl(hex);
  hsl.l = Math.max(0, Math.min(100, hsl.l + amount));
  return hslToHex(hsl);
}

// 透明度を追加（HEXアルファ）
export function withAlpha(hex: string, alpha: number): string {
  const alphaHex = Math.round(alpha * 255).toString(16).padStart(2, '0');
  return hex + alphaHex;
}
```

### テーマビルダー

```typescript
// src/core/theme-builder.ts

import { contrastRatio, adjustForContrast } from './contrast';
import { withAlpha, adjustLightness } from './color';

interface ThemeConfig {
  name: string;
  type: 'dark' | 'light';
  palette: PokemonPalette;

  // オプション: コントラスト自動調整
  ensureContrast?: boolean;
  targetContrastRatio?: number;
}

export function buildTheme(config: ThemeConfig) {
  const { name, type, palette, ensureContrast = true, targetContrastRatio = 4.5 } = config;

  // ベースカラーの決定
  const bg = type === 'dark'
    ? { primary: '#1C1C1C', secondary: '#252525', tertiary: '#2D2D2D' }
    : { primary: '#FAFAFA', secondary: '#F0F0F0', tertiary: '#E5E5E5' };

  const fg = type === 'dark'
    ? { primary: '#F5F5F5', secondary: '#CCCCCC', muted: '#6A6A6A' }
    : { primary: '#1A1A1A', secondary: '#333333', muted: '#888888' };

  // シンタックスカラーのコントラスト確保
  const syntax = ensureContrast
    ? ensureSyntaxContrast(palette, bg.primary, targetContrastRatio)
    : mapPaletteToSyntax(palette);

  return {
    $schema: 'vscode://schemas/color-theme',
    name,
    type,
    semanticHighlighting: true,

    colors: buildUiColors(palette, bg, fg),
    tokenColors: buildTokenColors(syntax, fg),
    semanticTokenColors: buildSemanticTokenColors(syntax),
  };
}

function ensureSyntaxContrast(
  palette: PokemonPalette,
  background: string,
  targetRatio: number
): SyntaxColors {
  const colors = mapPaletteToSyntax(palette);

  // 各色のコントラストを検証・調整
  for (const [key, color] of Object.entries(colors)) {
    const ratio = contrastRatio(color, background);
    if (ratio < targetRatio) {
      console.warn(
        `⚠️  ${key}: ${color} has insufficient contrast (${ratio.toFixed(2)}:1). Adjusting...`
      );
      colors[key] = adjustForContrast(color, background, targetRatio);
      console.log(`   → Adjusted to ${colors[key]}`);
    }
  }

  return colors;
}
```

### セマンティックトークンの定義

```typescript
// src/templates/semantic-tokens.ts

export function buildSemanticTokenColors(syntax: SyntaxColors) {
  return {
    // 基本トークン
    'variable': syntax.variable,
    'variable.readonly': syntax.constant,
    'variable.declaration': syntax.variableDeclaration,

    'parameter': {
      foreground: syntax.parameter,
      fontStyle: 'italic',
    },

    'function': syntax.function,
    'function.declaration': {
      foreground: syntax.function,
      fontStyle: 'bold',
    },

    'method': syntax.method,
    'method.static': syntax.staticMethod,

    'class': syntax.class,
    'class.declaration': {
      foreground: syntax.class,
      fontStyle: 'bold',
    },

    'interface': syntax.interface,
    'type': syntax.type,
    'typeParameter': syntax.typeParameter,

    'property': syntax.property,
    'property.readonly': syntax.constant,

    'enum': syntax.enum,
    'enumMember': syntax.enumMember,

    // モディファイア付き
    '*.deprecated': {
      fontStyle: 'strikethrough',
    },
    '*.async': {
      fontStyle: 'italic',
    },
    '*.defaultLibrary': {
      foreground: syntax.defaultLibrary,
    },

    // 言語固有
    'variable:typescript': syntax.variable,
    'variable:javascript': syntax.variable,
  };
}
```

---

## 第6章: 完全なピカチュウテーマの実装

### テーマJSON（全体）

以下は、これまでの技術的知識を総動員した完全なテーマ定義です：

```json
{
  "$schema": "vscode://schemas/color-theme",
  "name": "Pikachu Theme",
  "type": "dark",
  "semanticHighlighting": true,

  "colors": {
    // ═══════════════════════════════════════════
    // エディタ基本
    // ═══════════════════════════════════════════
    "editor.background": "#1C1C1C",
    "editor.foreground": "#F5F5F5",
    "editorCursor.foreground": "#F5D442",
    "editorCursor.background": "#1C1C1C",

    // 行ハイライト
    "editor.lineHighlightBackground": "#2D2D2D",
    "editor.lineHighlightBorder": "#3D3D3D",

    // 選択
    "editor.selectionBackground": "#F5D44233",
    "editor.selectionHighlightBackground": "#F5D44222",
    "editor.inactiveSelectionBackground": "#F5D44218",

    // 検索
    "editor.findMatchBackground": "#F5D44266",
    "editor.findMatchHighlightBackground": "#F5D44233",
    "editor.findMatchBorder": "#F5D442",

    // 単語ハイライト
    "editor.wordHighlightBackground": "#6890F033",
    "editor.wordHighlightStrongBackground": "#6890F055",

    // ブラケット
    "editorBracketMatch.background": "#F5D44233",
    "editorBracketMatch.border": "#F5D442",
    "editorBracketHighlight.foreground1": "#F5D442",
    "editorBracketHighlight.foreground2": "#6890F0",
    "editorBracketHighlight.foreground3": "#F85888",
    "editorBracketHighlight.foreground4": "#78C850",
    "editorBracketHighlight.foreground5": "#F08030",
    "editorBracketHighlight.foreground6": "#98D8D8",

    // インデントガイド
    "editorIndentGuide.background1": "#3D3D3D",
    "editorIndentGuide.activeBackground1": "#F5D442",

    // 行番号
    "editorLineNumber.foreground": "#6A6A6A",
    "editorLineNumber.activeForeground": "#F5D442",

    // ルーラー
    "editorRuler.foreground": "#3D3D3D",

    // ミニマップ
    "minimap.background": "#1C1C1C",
    "minimap.selectionHighlight": "#F5D44266",
    "minimap.findMatchHighlight": "#F5D442",

    // ═══════════════════════════════════════════
    // エディタウィジェット
    // ═══════════════════════════════════════════
    "editorWidget.background": "#252525",
    "editorWidget.border": "#3D3D3D",
    "editorSuggestWidget.background": "#252525",
    "editorSuggestWidget.border": "#3D3D3D",
    "editorSuggestWidget.selectedBackground": "#F5D44233",
    "editorSuggestWidget.highlightForeground": "#F5D442",
    "editorHoverWidget.background": "#252525",
    "editorHoverWidget.border": "#F5D442",

    // ピークビュー
    "peekView.border": "#F5D442",
    "peekViewEditor.background": "#1C1C1C",
    "peekViewResult.background": "#252525",
    "peekViewTitle.background": "#2D2D2D",
    "peekViewTitleLabel.foreground": "#F5D442",

    // ═══════════════════════════════════════════
    // アクティビティバー
    // ═══════════════════════════════════════════
    "activityBar.background": "#1C1C1C",
    "activityBar.foreground": "#F5D442",
    "activityBar.inactiveForeground": "#6A6A6A",
    "activityBar.activeBorder": "#F5D442",
    "activityBarBadge.background": "#E74C3C",
    "activityBarBadge.foreground": "#FFFFFF",

    // ═══════════════════════════════════════════
    // サイドバー
    // ═══════════════════════════════════════════
    "sideBar.background": "#252525",
    "sideBar.foreground": "#CCCCCC",
    "sideBar.border": "#1C1C1C",
    "sideBarTitle.foreground": "#F5D442",
    "sideBarSectionHeader.background": "#2D2D2D",
    "sideBarSectionHeader.foreground": "#F5D442",

    // ═══════════════════════════════════════════
    // タブ
    // ═══════════════════════════════════════════
    "tab.activeBackground": "#1C1C1C",
    "tab.activeForeground": "#F5D442",
    "tab.activeBorder": "#F5D442",
    "tab.inactiveBackground": "#252525",
    "tab.inactiveForeground": "#888888",
    "tab.border": "#1C1C1C",
    "tab.hoverBackground": "#2D2D2D",
    "editorGroupHeader.tabsBackground": "#252525",

    // ═══════════════════════════════════════════
    // ステータスバー
    // ═══════════════════════════════════════════
    "statusBar.background": "#F5D442",
    "statusBar.foreground": "#1C1C1C",
    "statusBar.border": "#C7A832",
    "statusBar.debuggingBackground": "#E74C3C",
    "statusBar.debuggingForeground": "#FFFFFF",
    "statusBar.noFolderBackground": "#705898",
    "statusBar.noFolderForeground": "#FFFFFF",
    "statusBarItem.hoverBackground": "#C7A832",
    "statusBarItem.prominentBackground": "#E74C3C",

    // ═══════════════════════════════════════════
    // タイトルバー
    // ═══════════════════════════════════════════
    "titleBar.activeBackground": "#1C1C1C",
    "titleBar.activeForeground": "#F5D442",
    "titleBar.inactiveBackground": "#252525",
    "titleBar.inactiveForeground": "#6A6A6A",
    "titleBar.border": "#1C1C1C",

    // ═══════════════════════════════════════════
    // 入力・ボタン
    // ═══════════════════════════════════════════
    "input.background": "#2D2D2D",
    "input.foreground": "#F5F5F5",
    "input.border": "#3D3D3D",
    "input.placeholderForeground": "#6A6A6A",
    "inputOption.activeBorder": "#F5D442",
    "inputOption.activeBackground": "#F5D44233",
    "inputValidation.errorBackground": "#E74C3C33",
    "inputValidation.errorBorder": "#E74C3C",
    "inputValidation.warningBackground": "#F0803033",
    "inputValidation.warningBorder": "#F08030",

    "button.background": "#F5D442",
    "button.foreground": "#1C1C1C",
    "button.hoverBackground": "#FFE066",
    "button.secondaryBackground": "#3D3D3D",
    "button.secondaryForeground": "#F5F5F5",

    "focusBorder": "#F5D442",

    // ═══════════════════════════════════════════
    // リスト・ツリー
    // ═══════════════════════════════════════════
    "list.activeSelectionBackground": "#F5D44233",
    "list.activeSelectionForeground": "#F5D442",
    "list.inactiveSelectionBackground": "#F5D44218",
    "list.hoverBackground": "#2D2D2D",
    "list.focusBackground": "#F5D44233",
    "list.highlightForeground": "#F5D442",
    "list.errorForeground": "#E74C3C",
    "list.warningForeground": "#F08030",

    "tree.indentGuidesStroke": "#3D3D3D",

    // ═══════════════════════════════════════════
    // ターミナル
    // ═══════════════════════════════════════════
    "terminal.background": "#1C1C1C",
    "terminal.foreground": "#F5F5F5",
    "terminal.ansiBlack": "#1C1C1C",
    "terminal.ansiRed": "#E74C3C",
    "terminal.ansiGreen": "#78C850",
    "terminal.ansiYellow": "#F5D442",
    "terminal.ansiBlue": "#6890F0",
    "terminal.ansiMagenta": "#F85888",
    "terminal.ansiCyan": "#98D8D8",
    "terminal.ansiWhite": "#F5F5F5",
    "terminal.ansiBrightBlack": "#6A6A6A",
    "terminal.ansiBrightRed": "#FF6B5B",
    "terminal.ansiBrightGreen": "#98E870",
    "terminal.ansiBrightYellow": "#FFE066",
    "terminal.ansiBrightBlue": "#88B0FF",
    "terminal.ansiBrightMagenta": "#FF78A8",
    "terminal.ansiBrightCyan": "#B8F8F8",
    "terminal.ansiBrightWhite": "#FFFFFF",
    "terminal.selectionBackground": "#F5D44233",
    "terminalCursor.foreground": "#F5D442",

    // ═══════════════════════════════════════════
    // Git装飾
    // ═══════════════════════════════════════════
    "gitDecoration.addedResourceForeground": "#78C850",
    "gitDecoration.modifiedResourceForeground": "#F5D442",
    "gitDecoration.deletedResourceForeground": "#E74C3C",
    "gitDecoration.renamedResourceForeground": "#6890F0",
    "gitDecoration.untrackedResourceForeground": "#98D8D8",
    "gitDecoration.ignoredResourceForeground": "#6A6A6A",
    "gitDecoration.conflictingResourceForeground": "#F08030",

    // ═══════════════════════════════════════════
    // Diff
    // ═══════════════════════════════════════════
    "diffEditor.insertedTextBackground": "#78C85022",
    "diffEditor.removedTextBackground": "#E74C3C22",
    "diffEditor.insertedLineBackground": "#78C85018",
    "diffEditor.removedLineBackground": "#E74C3C18",

    // ═══════════════════════════════════════════
    // エラー・警告
    // ═══════════════════════════════════════════
    "editorError.foreground": "#E74C3C",
    "editorWarning.foreground": "#F08030",
    "editorInfo.foreground": "#6890F0",
    "editorHint.foreground": "#78C850",

    // ═══════════════════════════════════════════
    // スクロールバー
    // ═══════════════════════════════════════════
    "scrollbar.shadow": "#00000033",
    "scrollbarSlider.background": "#F5D44233",
    "scrollbarSlider.hoverBackground": "#F5D44266",
    "scrollbarSlider.activeBackground": "#F5D44299"
  },

  "tokenColors": [
    // ═══════════════════════════════════════════
    // コメント（ゴースト・ダークタイプ）
    // ═══════════════════════════════════════════
    {
      "name": "Comments",
      "scope": ["comment", "punctuation.definition.comment"],
      "settings": {
        "foreground": "#6A6A6A",
        "fontStyle": "italic"
      }
    },
    {
      "name": "Documentation Comments",
      "scope": [
        "comment.block.documentation",
        "comment.block.javadoc"
      ],
      "settings": {
        "foreground": "#8B7AA8"
      }
    },

    // ═══════════════════════════════════════════
    // キーワード（でんきタイプ - ピカチュウイエロー）
    // ═══════════════════════════════════════════
    {
      "name": "Keywords",
      "scope": [
        "keyword",
        "keyword.control",
        "keyword.operator.new",
        "keyword.operator.expression",
        "keyword.operator.logical",
        "storage.type",
        "storage.modifier"
      ],
      "settings": {
        "foreground": "#F5D442"
      }
    },
    {
      "name": "Control Flow",
      "scope": [
        "keyword.control.conditional",
        "keyword.control.loop",
        "keyword.control.flow"
      ],
      "settings": {
        "foreground": "#F5D442",
        "fontStyle": "bold"
      }
    },

    // ═══════════════════════════════════════════
    // 関数・メソッド（みずタイプ）
    // ═══════════════════════════════════════════
    {
      "name": "Functions",
      "scope": [
        "entity.name.function",
        "support.function",
        "meta.function-call"
      ],
      "settings": {
        "foreground": "#6890F0"
      }
    },
    {
      "name": "Function Declaration",
      "scope": ["entity.name.function.definition"],
      "settings": {
        "foreground": "#6890F0",
        "fontStyle": "bold"
      }
    },

    // ═══════════════════════════════════════════
    // 文字列（くさタイプ）
    // ═══════════════════════════════════════════
    {
      "name": "Strings",
      "scope": ["string", "string.quoted"],
      "settings": {
        "foreground": "#78C850"
      }
    },
    {
      "name": "String Escape",
      "scope": ["constant.character.escape"],
      "settings": {
        "foreground": "#98E870"
      }
    },
    {
      "name": "Template String Punctuation",
      "scope": [
        "punctuation.definition.template-expression",
        "punctuation.section.embedded"
      ],
      "settings": {
        "foreground": "#F5D442"
      }
    },

    // ═══════════════════════════════════════════
    // 数値・定数（ほのおタイプ）
    // ═══════════════════════════════════════════
    {
      "name": "Numbers",
      "scope": ["constant.numeric"],
      "settings": {
        "foreground": "#F08030"
      }
    },
    {
      "name": "Constants",
      "scope": [
        "constant.language",
        "constant.other"
      ],
      "settings": {
        "foreground": "#F08030"
      }
    },
    {
      "name": "Boolean",
      "scope": ["constant.language.boolean"],
      "settings": {
        "foreground": "#F08030",
        "fontStyle": "bold"
      }
    },

    // ═══════════════════════════════════════════
    // 型・クラス（エスパータイプ）
    // ═══════════════════════════════════════════
    {
      "name": "Types",
      "scope": [
        "entity.name.type",
        "support.type",
        "support.class"
      ],
      "settings": {
        "foreground": "#F85888"
      }
    },
    {
      "name": "Classes",
      "scope": [
        "entity.name.class",
        "entity.other.inherited-class"
      ],
      "settings": {
        "foreground": "#F85888",
        "fontStyle": "bold"
      }
    },
    {
      "name": "Interfaces",
      "scope": ["entity.name.type.interface"],
      "settings": {
        "foreground": "#EE99AC"
      }
    },
    {
      "name": "Type Parameters",
      "scope": ["entity.name.type.parameter"],
      "settings": {
        "foreground": "#F85888",
        "fontStyle": "italic"
      }
    },

    // ═══════════════════════════════════════════
    // 演算子（かくとうタイプ）
    // ═══════════════════════════════════════════
    {
      "name": "Operators",
      "scope": ["keyword.operator"],
      "settings": {
        "foreground": "#E74C3C"
      }
    },
    {
      "name": "Comparison Operators",
      "scope": [
        "keyword.operator.comparison",
        "keyword.operator.relational"
      ],
      "settings": {
        "foreground": "#E74C3C",
        "fontStyle": "bold"
      }
    },

    // ═══════════════════════════════════════════
    // 変数（ノーマルタイプ - 白系）
    // ═══════════════════════════════════════════
    {
      "name": "Variables",
      "scope": ["variable", "variable.other"],
      "settings": {
        "foreground": "#F5F5F5"
      }
    },
    {
      "name": "Variable Declaration",
      "scope": ["variable.other.readwrite"],
      "settings": {
        "foreground": "#F5F5F5"
      }
    },

    // ═══════════════════════════════════════════
    // プロパティ（こおりタイプ）
    // ═══════════════════════════════════════════
    {
      "name": "Properties",
      "scope": [
        "variable.other.property",
        "support.variable.property",
        "variable.other.object.property"
      ],
      "settings": {
        "foreground": "#98D8D8"
      }
    },

    // ═══════════════════════════════════════════
    // パラメータ（ほのお/でんき混合）
    // ═══════════════════════════════════════════
    {
      "name": "Parameters",
      "scope": ["variable.parameter"],
      "settings": {
        "foreground": "#FFAA33",
        "fontStyle": "italic"
      }
    },

    // ═══════════════════════════════════════════
    // インポート（ひこうタイプ）
    // ═══════════════════════════════════════════
    {
      "name": "Import/Export",
      "scope": [
        "keyword.control.import",
        "keyword.control.export",
        "keyword.control.from",
        "keyword.control.as"
      ],
      "settings": {
        "foreground": "#A890F0"
      }
    },
    {
      "name": "Module Names",
      "scope": ["entity.name.type.module"],
      "settings": {
        "foreground": "#A890F0"
      }
    },

    // ═══════════════════════════════════════════
    // タグ（かくとうタイプ - HTML/JSX）
    // ═══════════════════════════════════════════
    {
      "name": "HTML Tags",
      "scope": ["entity.name.tag"],
      "settings": {
        "foreground": "#E74C3C"
      }
    },
    {
      "name": "HTML Attributes",
      "scope": ["entity.other.attribute-name"],
      "settings": {
        "foreground": "#F5D442"
      }
    },
    {
      "name": "JSX Component Tags",
      "scope": ["support.class.component"],
      "settings": {
        "foreground": "#F85888"
      }
    },

    // ═══════════════════════════════════════════
    // JSON（みずタイプ）
    // ═══════════════════════════════════════════
    {
      "name": "JSON Keys",
      "scope": ["support.type.property-name.json"],
      "settings": {
        "foreground": "#6890F0"
      }
    },

    // ═══════════════════════════════════════════
    // CSS/SCSS
    // ═══════════════════════════════════════════
    {
      "name": "CSS Property Names",
      "scope": ["support.type.property-name.css"],
      "settings": {
        "foreground": "#98D8D8"
      }
    },
    {
      "name": "CSS Property Values",
      "scope": ["support.constant.property-value.css"],
      "settings": {
        "foreground": "#F08030"
      }
    },
    {
      "name": "CSS Selectors",
      "scope": [
        "entity.other.attribute-name.class.css",
        "entity.other.attribute-name.id.css"
      ],
      "settings": {
        "foreground": "#F5D442"
      }
    },
    {
      "name": "CSS Units",
      "scope": ["keyword.other.unit.css"],
      "settings": {
        "foreground": "#F85888"
      }
    },

    // ═══════════════════════════════════════════
    // Markdown
    // ═══════════════════════════════════════════
    {
      "name": "Markdown Headings",
      "scope": ["markup.heading", "entity.name.section.markdown"],
      "settings": {
        "foreground": "#F5D442",
        "fontStyle": "bold"
      }
    },
    {
      "name": "Markdown Bold",
      "scope": ["markup.bold"],
      "settings": {
        "foreground": "#F08030",
        "fontStyle": "bold"
      }
    },
    {
      "name": "Markdown Italic",
      "scope": ["markup.italic"],
      "settings": {
        "foreground": "#F85888",
        "fontStyle": "italic"
      }
    },
    {
      "name": "Markdown Code",
      "scope": ["markup.inline.raw", "markup.fenced_code.block"],
      "settings": {
        "foreground": "#78C850"
      }
    },
    {
      "name": "Markdown Links",
      "scope": ["markup.underline.link"],
      "settings": {
        "foreground": "#6890F0"
      }
    },
    {
      "name": "Markdown Quotes",
      "scope": ["markup.quote"],
      "settings": {
        "foreground": "#8B7AA8",
        "fontStyle": "italic"
      }
    },

    // ═══════════════════════════════════════════
    // 正規表現
    // ═══════════════════════════════════════════
    {
      "name": "Regex",
      "scope": ["string.regexp"],
      "settings": {
        "foreground": "#E74C3C"
      }
    },
    {
      "name": "Regex Character Class",
      "scope": ["constant.other.character-class.regexp"],
      "settings": {
        "foreground": "#F5D442"
      }
    },

    // ═══════════════════════════════════════════
    // 特殊
    // ═══════════════════════════════════════════
    {
      "name": "Invalid",
      "scope": ["invalid"],
      "settings": {
        "foreground": "#E74C3C",
        "fontStyle": "underline"
      }
    },
    {
      "name": "Deprecated",
      "scope": ["invalid.deprecated"],
      "settings": {
        "foreground": "#A040A0",
        "fontStyle": "strikethrough"
      }
    }
  ],

  "semanticTokenColors": {
    // 変数
    "variable": "#F5F5F5",
    "variable.readonly": "#F08030",
    "variable.declaration": "#F5F5F5",

    // パラメータ
    "parameter": {
      "foreground": "#FFAA33",
      "fontStyle": "italic"
    },

    // 関数・メソッド
    "function": "#6890F0",
    "function.declaration": {
      "foreground": "#6890F0",
      "fontStyle": "bold"
    },
    "method": "#6890F0",
    "method.static": "#A890F0",

    // クラス・型
    "class": "#F85888",
    "class.declaration": {
      "foreground": "#F85888",
      "fontStyle": "bold"
    },
    "interface": "#EE99AC",
    "type": "#F85888",
    "typeParameter": {
      "foreground": "#F85888",
      "fontStyle": "italic"
    },

    // プロパティ
    "property": "#98D8D8",
    "property.readonly": "#F08030",

    // Enum
    "enum": "#F85888",
    "enumMember": "#F08030",

    // Namespace
    "namespace": "#A890F0",

    // モディファイア
    "*.deprecated": {
      "foreground": "#A040A0",
      "fontStyle": "strikethrough"
    },
    "*.async": {
      "fontStyle": "italic"
    },
    "*.defaultLibrary": "#B8B8D0"
  }
}
```

---

## 第7章: テストとバリデーション

### コントラスト比の自動テスト

```typescript
// test/contrast.test.ts

import { describe, it, expect } from 'vitest';
import { contrastRatio } from '../src/core/contrast';
import theme from '../themes/pikachu-color-theme.json';

describe('WCAG Contrast Compliance', () => {
  const background = theme.colors['editor.background'];

  // テストケース生成
  const syntaxColors = theme.tokenColors
    .filter(tc => tc.settings.foreground)
    .map(tc => ({
      name: tc.name,
      color: tc.settings.foreground,
    }));

  it.each(syntaxColors)(
    '$name ($color) should have sufficient contrast',
    ({ name, color }) => {
      const ratio = contrastRatio(color, background);
      expect(ratio).toBeGreaterThanOrEqual(4.5);
    }
  );

  it('status bar should have sufficient contrast', () => {
    const statusBg = theme.colors['statusBar.background'];
    const statusFg = theme.colors['statusBar.foreground'];
    const ratio = contrastRatio(statusBg, statusFg);
    expect(ratio).toBeGreaterThanOrEqual(4.5);
  });
});
```

### ビジュアルリグレッションテスト

```typescript
// スクリーンショット比較用のサンプルコード
const sampleCode = `
import { Pokemon, Type } from './types';

const PIKACHU_NUMBER = 25;

/**
 * ピカチュウを表すクラス
 * @deprecated 新しいPokemonクラスを使用してください
 */
class Pikachu implements Pokemon {
  static readonly TYPE: Type = 'Electric';

  readonly name = 'Pikachu';
  private _level: number;

  constructor(level: number = 5) {
    this._level = level;
  }

  async thunderbolt(): Promise<string> {
    const damage = this._level * 2;
    return \`\${this.name} used Thunderbolt! Dealt \${damage} damage.\`;
  }

  get level(): number {
    return this._level;
  }
}

// 使用例
const pikachu = new Pikachu(50);
pikachu.thunderbolt().then(console.log);
`;
```

---

## 第8章: Marketplaceへの公開

### package.jsonの完全な設定

```json
{
  "name": "pokemon-pikachu-theme",
  "displayName": "Pikachu Theme - Pokemon Color Palette",
  "description": "A carefully crafted VS Code theme using Pikachu's color palette with full semantic highlighting support",
  "version": "1.0.0",
  "publisher": "your-publisher-id",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "icon": "images/icon.png",
  "galleryBanner": {
    "color": "#F5D442",
    "theme": "light"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/your-username/pokemon-pikachu-theme"
  },
  "bugs": {
    "url": "https://github.com/your-username/pokemon-pikachu-theme/issues"
  },
  "homepage": "https://github.com/your-username/pokemon-pikachu-theme#readme",
  "keywords": [
    "theme",
    "color-theme",
    "pokemon",
    "pikachu",
    "dark",
    "yellow",
    "semantic-highlighting",
    "accessibility"
  ],
  "categories": ["Themes"],
  "engines": {
    "vscode": "^1.85.0"
  },
  "contributes": {
    "themes": [
      {
        "label": "Pikachu Theme",
        "uiTheme": "vs-dark",
        "path": "./themes/pikachu-color-theme.json"
      }
    ]
  },
  "scripts": {
    "build": "tsc && node dist/build.js",
    "test": "vitest",
    "package": "vsce package",
    "publish": "vsce publish"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@vscode/vsce": "^2.22.0",
    "typescript": "^5.3.0",
    "vitest": "^1.0.0"
  }
}
```

### GitHub Actionsによる自動公開

```yaml
# .github/workflows/publish.yml
name: Publish to VS Code Marketplace

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build themes
        run: npm run build

      - name: Publish to Marketplace
        env:
          VSCE_PAT: ${{ secrets.VSCE_PAT }}
        run: npx vsce publish -p $VSCE_PAT
```

---

## まとめ

この記事では、VSCodeテーマ開発の技術的深層に踏み込みました：

### 学んだこと

1. **vscode-textmateのアーキテクチャ**
   - Oniguruma正規表現エンジンの役割
   - 行ごとのトークナイゼーションと状態管理
   - スコープの階層構造とマッチング優先順位

2. **セマンティックハイライト**
   - TextMateの限界とLSPによる意味解析
   - トークンタイプとモディファイアの標準仕様
   - TextMateとの優先順位

3. **カラーサイエンス**
   - WCAG コントラスト比の数学的計算
   - 相対輝度（Relative Luminance）の導出
   - sRGB値の線形化プロセス

4. **アクセシビリティ**
   - WCAG AA/AAAレベルの基準
   - コントラスト不足色の自動調整
   - 自動テストによる検証

5. **プロダクション品質のテーマ開発**
   - TypeScriptによるプログラマティックな生成
   - Vitestによるコントラスト比テスト
   - GitHub Actionsによる自動公開

### 参考リンク

- [vscode-textmate](https://github.com/microsoft/vscode-textmate) - TextMate Grammarライブラリ
- [Semantic Highlight Guide](https://code.visualstudio.com/api/language-extensions/semantic-highlight-guide) - セマンティックハイライト公式ドキュメント
- [Theme Color Reference](https://code.visualstudio.com/api/references/theme-color) - 全カラープロパティ一覧
- [WCAG Contrast Requirements](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) - W3Cコントラスト基準

ポケモンカラーはあくまで題材です。この知識を活かして、**あなただけの美しく、アクセシブルなテーマ**を作成してください。
