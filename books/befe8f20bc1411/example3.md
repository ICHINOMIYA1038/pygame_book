---
title: "python 基礎"
---

## Python の基礎

まずは、以下のコードを用意してください。

```python
def main():
    print("Hello World!")

if __name__=="__main__":
    main()
```

以下の部分はおまじないだと考えても大丈夫です。

```python
if __name__=="__main__":
    main()
```

講師用に説明すると、ファイルが実行されるときに`__name__` にはファイル名が入ります。

このファイルが直接実行されるときは、この部分が true になるので main()が実行されますが、プログラムを他の場所で呼び出して使うときは main()は実行されません。

## 組み込み関数と標準ライブラリ

組み込み関数とは、何もしなくても使える関数です。

python の組み込み関数はバージョン 3.11.11 時点で およそ 70 個です。

https://docs.python.org/ja/3.11/library/functions.html#aiter

### abs() 関数

```
def main():
    answer = abs(-10)
    print(answer)

if __name__=="__main__":
    main()
```

### sum() 関数

```
def main():
    answer = sum([2, 4])
    print(answer)

if __name__=="__main__":
    main()
```

### round() 関数

```
def main():
    answer = round(120.24, 1)
    print(answer)

if __name__=="__main__":
    main()
```

### 標準ライブラリ

標準ライブラリは、python に標準で付属している便利な関数たち(モジュール群)です。

組み込み関数と違うのは、import して使う必要がある点です。

import とは、「これを使うよ」と最初に指定することを言います。

```
import モジュール名
```

### random モジュール

```
import random

def main():
    answer = random.randint(0, 10)
    print(answer)

if __name__=="__main__":
    main()
```

### math モジュール

```
from math import pi, sqrt, pow, sin, cos, tan

def main():
    print(pi)
    print(sqrt(4))
    print(pow(2, 10))
    print(sin(0))
    print(cos(0))
    print(tan(0))

if __name__=="__main__":
    main()
```

### sys モジュール

```
import sys

def main():
    print("これは実行される")
    sys.exit()
    print("これは実行されない")

if __name__=="__main__":
    main()
```

### os モジュール

```
import os

def main():
    print(os.getcwd())

if __name__=="__main__":
    main()
```

## 外部ライブラリ

python に標準についているわけではなく、他の開発者が作った便利なものです。

python はこの外部ライブラリが豊富なので、データ分析や AI の開発でよく使われます。

標準ライブラリとは違い、python に標準で付属しているものではないので、`pip install` で install する必要があります。

```
pip install numpy
pip install pandas
pip install matplotlib
```

サンプル

上記の外部ライブラリをインストールしてから実行してください。

コードの内容自体は難しいので教えなくて大丈夫です。

```
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 1. データ生成
    np.random.seed(42)
    months = np.array([f'{i}' for i in range(1, 13)])  # 1月から12月
    sales_data = np.random.randint(100, 500, size=(12, 3))  # 100~500のランダムな整数

    # 2. DataFrameの作成
    df = pd.DataFrame(sales_data, columns=['A', 'B', 'C'])
    df['Month'] = months

    # 3. 基本統計量の確認
    summary = df.describe()

    # 4. 可視化（売上の推移）
    plt.figure(figsize=(10, 6))
    for product in ['A', 'B', 'C']:
        plt.plot(df['Month'], df[product], marker='o', label=product)

    plt.title('Monthly Sales Data')
    plt.xlabel('Month')
    plt.ylabel('Sales Amount')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__=="__main__":
    main()

```

以下のようなグラフが出てきたら成功。

python を使うとこのようなデータ分析が簡単にできます。

便利な機能を簡単に扱えるようになるのが外部ライブラリです。

![スクリーンショット 2025-01-02 3.03.59](/Users/ichinomiya/Library/Application Support/typora-user-images/スクリーンショット 2025-01-02 3.03.59.png)

## 基本的な文法

### 変数とは？

よく使うものに名前をつけることです。

```
name = "太郎"
print(name)
```

### 関数とは？

関数は「便利な道具箱」のようなものです。

よく使う処理をまとめて名前をつけておくことで、必要なときにその名前を呼び出すだけで同じ処理ができます。

```
# 挨拶する関数
def greet():
    print("hello")
```

### 引数とは？

関数には最初に値を渡すことができます。

以下は、動物の名前を渡すことで、その動物の名前を関数の中で使うことができます。

このとき、渡した値のことを引数といいます。

```
# 好きな動物を説明する関数
def greet(animal):
    print("私は" + animal + "が好きです!")

def main():
    greet("ワニ")

if __name__=="__main__":
    main()

```

### 帰り値とは？

関数は特定の値を返すことができます。

返すとは、その関数の実行結果がその特定の値になることを言います。

この特定の値を帰り値といいます。

```
# 好きな動物を説明する関数
def greet(animal):
    return ("私は" + animal + "が好きです!") # 帰り値

def main():
    answer = greet("ワニ") # greet("ワニ")に自己紹介の文章が返ってきている。
    print(answer)

if __name__=="__main__":
    main()

```

### クラスとインスタンス

クラスとは設計図のことだと思ってください。

例えば、ゲームの中にクルマがたくさん出てくるとして、毎回クルマのコードを書くのは大変です。

そこで、設計図を作成し、それをもとに同じものをたくさん作ることで作る手間を省略します。

設計図のことを「クラス」と言い、設計図から作られた一つ一つを「インスタンス」または「オブジェクト」といいます。インスタンスとは、Scratch でいう「クローン」のことだと思ってください。

設計図(クラス) には、**性質**と**動き**があります。

性質は**変数** 動きは**関数**だと思ってください。

例えば、以下の Car クラスには色とスピードの性質(変数)を持っています。

また、スピードを上げ下げする動き(関数)や、走り始めたり止まったりする動き(関数)があります。

```
class Car:
    def __init__(self, color, speed):
        self.color = color
        self.speed = speed

    # 走り始める関数
    def run(self):
        print("走ります！")

    # スピードを上げる関数
    def speed_up(self):
        print("スピードを上げます！")

    # スピードを下げる関数
    def speed_down(self):
        print("スピードを下げます！")

    # 止まる関数
    def stop(self):
        print("止まります！")

```

### コンストラクタとは

先ほどのクラスで以下の関数は何か気になりましたか？

以下はコンストラクタといい、設計図からインスタンスを作る際に最初に呼び出される特殊な関数です。

このコンストラクタでは初期値を決めています。

コンストラクタを利用すると、ピストルクラスのインスタンスができた瞬間に銃声の音を鳴らすということができるようになります。

```
  def __init__(self, color, speed):
        self.color = color
        self.speed = speed

```

### 実際にクラスからインスタンスを作成するコード

```
class Car:
    def __init__(self, color, speed):
        self.color = color
        self.speed = speed
        print(color + "色のクルマが作成されました")

    # 走り始める関数
    def run(self):
        print("走ります！")

    # スピードを上げる関数
    def speed_up(self):
        print("スピードを上げます！")

    # スピードを下げる関数
    def speed_down(self):
        print("スピードを下げます！")

    # 止まる関数
    def stop(self):
        print("止まります！")


def main():
    car = Car("赤", 60)
    car.run()
    car.speed_up()
    car.speed_down()
    car.stop()

if __name__=="__main__":
    main()

```

### 条件分岐 (if)

条件分岐は以下のように書きます。

「もしもテストで 80 点以上 だったらゲームしていいよ」という条件になります。

`elif` は、別の条件を指定します。

それ以外ならというのは`else`を使います。

```
def main():
    score = 90
    if score >= 80: # もし、80点以上なら
        print("ゲームしていいよ！")
    elif score >= 75: # もし、75点以上なら
        print("惜しい！")
    else: #それ以外なら
        print("勉強しなさい！")

if __name__=="__main__":
    main()

```

### **インデントってなに？**

インデントは「行のはじまりをちょっと右にずらすこと」です。
Python では、インデントがとっても大切です。

```
score = 100
if score == 100:
print("ゲームしていいよ！")

```

これだと、エラーになります！
「どこからどこまでが "もしも" の中身かわからないよ！」と Python が困ってしまいます。

### くり返し（for）

for による繰り返しは以下のように書きます。

"何回"繰り返すかを指定する必要があります。

「5 回こんにちはと言ってね」という命令を書いてみましょう。

```
for i in range(5):
    print("こんにちは")
```

### くり返し(while)

while は条件を伴う繰り返しです。

〇〇という条件を満たすまで繰り返すということができます。

「100 点をとるまでがんばる！」というプログラムを作ってみましょう。

```
score = 50  # 最初は50点

while score < 100:  # 100点未満ならくり返す
    print("もっとがんばるぞ！")
    score += 10  # 点数を10点ずつ増やす
```

## 型

型とはデータの種類のことです。

整数、少数、文字列などデータの種類によって型が決まります。

python は動的型つけ言語と言われます。

つまり、型を勝手に決めてくれます。

では、型を意識しなくていいかというとそうではありません。

なぜなら、ドキュメントを読むときに「ある関数の引数や帰り値が何の型か」を意識することが大切だからです。

またエラーが出たときにも型がヒントになる場合があります。

| 型の名前           | 説明                         | 例                         |
| ------------------ | ---------------------------- | -------------------------- |
| `int`（整数）      | 数を表す（小数点なし）       | `10`, `-3`, `1000`         |
| `float`（小数）    | 小数点のある数               | `3.14`, `0.5`, `-2.7`      |
| `str`（文字列）    | 文字や文章を表す             | `"こんにちは"`, `"Python"` |
| `bool`（真偽値）   | `True`か`False`の 2 択       | `True`, `False`            |
| `list`（リスト）   | 複数のデータを順番に入れる箱 | `[1, 2, 3]`, `['A', 'B']`  |
| `dict`（辞書）     | キーと値のセット             | `{'名前': '太郎'}`         |
| `tuple`（タプル）  | 順番があるデータのまとまり   | `(10, 20, 30)`             |
| `set`（セット）    | 重複しないデータの集まり     | `{1, 2, 3}`                |
| `NoneType`（なし） | 「何もない」ことを表す       | `None`                     |

### 型を調べるには？

Python では、組み込み関数の`type()` を使うと変数の型がわかります。

```
python

x = 10
print(type(x))  # <class 'int'>

x = "10"
print(type(x))  # <class 'str'>
```

```
x = "10"  # 文字列の10
y = 10    # 整数の10

if x == y:
    print("同じです！")
else:
    print("違います！")
```

上記のように同じ 10 でも 文字列型の 10 と整数型では型が異なります。

前に話したようなクラスも type()関数で確認することができます。

```
class Car:
    def __init__(self, color, speed):
        self.color = color
        self.speed = speed
        print(color + "色のクルマが作成されました")

    # 走り始める関数
    def run(self):
        print("走ります！")

def main():
    car = Car("赤", 60)
    print(type(car))

if __name__=="__main__":
    main()
```

**結果**

```
<class '__main__.Car'>
```

これは main というファイルの Car クラスであることを意味しています。

繰り返しになりますが、この型やクラスを意識することはドキュメント(資料)を読む上で役に立ちます。

早くレベルアップするためには、変数の型やクラスを必ず意識しましょう。
