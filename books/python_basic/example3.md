---
title: "レベル3"
---

## レベル 3

この章では、以下のことを学びます

- いろんな標準関数を試してみよう
- import を使って標準関数を使ってみよう
- 関数の定義と利用
- 引数の利用
- 返り値と利用

### いろんな標準関数を試してみよう

標準関数は、python に最初から用意されている関数です。

組み込み関数と違うのは、import を使って読み込む必要があることです。

### import を使って標準関数を使ってみよう

import を使って標準関数を使ってみよう

```python
import math
```

math は、数学の関数をまとめたモジュールです。

math モジュールの floor 関数を使ってみましょう。

```python
math.floor(1.5)
```

```
実行結果:
1
```

floor 関数は、小数点以下を切り捨てる関数です。

さらに math モジュールには他にも便利な関数があります。

:::details 例 1 math モジュールの例 ceil 関数

```python
math.ceil(1.5)
```

:::

:::details 例 2 math モジュールの例 sqrt 関数

```python
math.sqrt(4)
```

:::

:::details 例 3 math モジュールの例 pow 関数

```python
math.pow(2, 3)
```

:::

:::details 例 4 math モジュールの例 sin 関数

```python
math.sin(0)
```

:::

:::details 例 5 math モジュールの例 cos 関数

```python
math.cos(0)
```

:::

:::details 例 6 math モジュールの例 tan 関数

```python
math.tan(0)
```

:::

:::details 例 7 math モジュールの例 pi 関数

```python
math.pi
```

:::

次に別の標準関数を使ってみましょう

```python
import random
```

random モジュールの random 関数を使ってみましょう。

```python
random.randint(1, 10)
```

```
実行結果:
1
```

randint 関数は、1 から 10 までの整数をランダムに返す関数です。

他にも色々な標準関数があります。

:::details 例 1 標準関数の例 datetime モジュール

````python
import datetime

# 現在の日付と時刻を取得
current_datetime = datetime.datetime.now()
print("現在の日付と時刻:", current_datetime)

:::

:::details 例 2 標準関数の例 os モジュール

```python
import os

# カレントディレクトリを取得
current_directory = os.getcwd()
print("カレントディレクトリ:", current_directory)

:::

:::details 例 3 標準関数の例 sys モジュール

```python
import sys

# Pythonのバージョンを取得
python_version = sys.version
print("Pythonのバージョン:", python_version)

:::

:::details 例 4 標準関数の例 statistics モジュール

```python
import statistics

# 平均を計算
data = [1, 2, 3, 4, 5]
mean_value = statistics.mean(data)
print("平均値:", mean_value)
```

```
実行結果:
平均値: 3
```
:::

:::details 例 5 標準関数の例 collections モジュール

```python
import collections

# Counterを使って要素の出現回数を数える
data = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
counter = collections.Counter(data)
print("要素の出現回数:", counter)
```

```
実行結果:
要素の出現回数: Counter({'apple': 3, 'banana': 2, 'orange': 1})
```

:::

### 関数の定義と利用
関数は自分で作ることもできます。
関数は、`def` を使って定義します。
これは、defin「定義する」 の略です。

関数名は、小文字で始めます。

関数の中身は、インデントで書きます。

```python
def 関数名(引数):
    実行する処理
```

```python
def hello():
    print("Hello")
```

関数を呼び出すには、関数名を使います。

```python
hello()
```

```
実行結果:
Hello
```

### 引数の利用

関数には、引数を渡すことができます。

引数は、関数名の後に括弧で囲んで書きます。

```python
def hello(name):
    print("Hello " + name)
```

関数を呼び出すときに、引数を渡します。

```python
hello("太郎")
```


```
実行結果:
Hello 太郎
```

引数は複数渡すこともできます。

```python
def add(a, b):
    return a + b
```

関数を呼び出すときに、引数を渡します。

```python
add(1, 2)
```

```
実行結果:
3
```

引数には、デフォルト値を設定することもできます。
この場合は、関数を呼び出すときに引数を渡さなくても、デフォルト値が使われます。
引数を渡した場合は、渡した値が使われます。

```python
def add(a, b=2):
    return a + b
```

関数を呼び出すときに、引数を渡します。

```python
add(1)
```


```
実行結果:
3
```








````
