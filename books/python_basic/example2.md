---
title: "レベル２"
---

## レベル２

この章では、以下のことを学びます

- 文字列の結合
- 配列
- 否定の条件文
- and と or の条件文
- 繰り返し(for 文)
- 関数とは
- len 関数(組み込み関数)
- 応用(for 文と if 文の組み合わせ)

### 文字列の結合

文字列の結合は、+ 演算子を使って行います。

```python
print("Hello" + "World")
```

```
実行結果:
HelloWorld
```

変数を組み合わせることもできます

```python
name = "太郎"
age = 20
print("私の名前は" + name + "です。年齢は" + str(age) + "歳です。")
```

```
実行結果:
私の名前は太郎です。年齢は20歳です。
```

### 配列

配列は、複数のデータをまとめて管理するためのものです。

```python
fruits = ["apple", "banana", "cherry"]
```

配列の値を使う時には、インデックスを使います。
インデックスは最初から何番目かを示す数字です。
インデックスは、0 から始まることに注意しましょう。

二番目の配列の値を使う場合には、以下のようにします。

```python
print(fruits[1])
```

```
実行結果:
banana
```

配列の値を変更することもできます。

```python
fruits[1] = "orange"
```

### 否定の条件文

否定の条件文は、not を使って表します。

```python
if not 条件:
    実行する処理
```

例

```python
name = "太郎"
if not name == "太郎":
    print("太郎ではない")
```

また、! を使っても否定を表すことができます。

```python
name = "太郎"
if name != "太郎":
    print("太郎ではない")
```

数字の例

### and と or の条件文

and は、「かつ」という意味の英語です。
and の場合は、条件 1 と 条件 2 が両方とも true の場合に実行されます。
or は、「または」という意味の英語です。
or の場合は、条件 1 と 条件 2 のどちらかが true の場合に実行されます。

```python
if 条件1 and 条件2:
    実行する処理
```

```python
if 条件1 or 条件2:
    実行する処理
```

### 繰り返し(for 文)

for 文は、繰り返しを行うためのものです。

```python
for 変数 in 配列:
    実行する処理
```

例

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

```
実行結果:
apple
banana
cherry
```

次に、for in range(10) は、10 回繰り返しを行います。
for in range(3) なら 3 回繰り返しを行います。
自分で繰り返しの回数を決めることができます。
i は、0 から始まり、1 ずつ自動で増えていきます。
このような変数をカウンタ変数といいます。

```python
for i in range(10):
    print(i)
```

### 関数とは

関数は、プログラムの中で処理をまとめておくためのものです。

```python
def 関数名(引数):
    実行する処理
```

例

```python
def hello():
    print("Hello")
```

```python
hello()
```

```
実行結果:
Hello
```

### 組み込み関数

組み込み関数は、python に最初から用意されている関数です。

len 関数は、文字列や配列の長さを返す関数です。

```python
len("Hello")
```

```
実行結果:
5
```

:::details 例 1 組み込み関数の例 max 関数

```python
print(max(1, 2, 3))
```

```
実行結果:
3
```

:::

:::details 例 2 組み込み関数の例 min 関数

```python
print(min(1, 2, 3))
```

```
実行結果:
1
```

:::

:::details 例 3 組み込み関数の例 sum 関数

```python
print(sum([1, 2, 3]))
```

```
実行結果:
6
```

:::

:::details 例 4 組み込み関数の例 sorted 関数

```python
print(sorted([3, 2, 1]))
```

```
実行結果:
[1, 2, 3]
```

:::

### 応用(for 文と if 文の組み合わせ)

for 文と if 文を組み合わせることで、より複雑な処理を行うことができます。

以下の例は、0 から 9 までの数字を繰り返し処理を行い、偶数の場合には "zip" を、奇数の場合には "zap" を表示します。

```python
for i in range(10):
    if i % 2 == 0:
        print("zip")
    else:
        print("zap")
```

```
実行結果:
zip
zap
zip
zap
zip
zap
```
