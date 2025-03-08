---
title: "レベル5"
---

## レベル 5

この章では、以下のことを学びます

- None
- int 型と文字列の混合配列
- type 関数
- 配列の操作
- 例外処理
- 二次元配列
- enumerate 関数

### None

Python では、`None`は何もないことを表す特別な値です。変数に何も値を持たせたくないときに使います。

```python
x = None
print(x)
```

```
実行結果:
None
```

### int 型と文字列の混合配列

Python では、配列（リスト）に異なる型のデータを混ぜて入れることができます。

```python
mixed_list = [1, "apple", 3.14, "banana"]
print(mixed_list)
```

```
実行結果:
[1, 'apple', 3.14, 'banana']
```

### type 関数

`type`関数を使うと、変数の型を調べることができます。

```python
x = 10
print(type(x))

y = "hello"
print(type(y))
```

```
実行結果:
<class 'int'>
<class 'str'>
```

### 配列の操作

Python の配列には、便利なメソッド(関数)がたくさんあります。

#### arr.insert()

リストの指定した位置に要素を挿入します。

```python
fruits = ["apple", "banana"]
fruits.insert(1, "orange")
print(fruits)
```

```
実行結果:
['apple', 'orange', 'banana']
```

#### arr.reverse()

リストの要素を逆順にします。

```python
numbers = [1, 2, 3, 4]
numbers.reverse()
print(numbers)
```

```
実行結果:
[4, 3, 2, 1]
```

#### arr.sort()

リストの要素を昇順に並べ替えます。

```python
numbers = [3, 1, 4, 2]
numbers.sort()
print(numbers)
```

```
実行結果:
[1, 2, 3, 4]
```

#### len(arr)

リストの要素数を取得します。

```python
fruits = ["apple", "banana", "orange"]
print(len(fruits))
```

```
実行結果:
3
```

### None が混じった配列

リストには`None`も含めることができます。

```python
mixed_list = [1, None, "apple", None]
print(mixed_list)
```

```
実行結果:
[1, None, 'apple', None]
```

### 例外処理

例外処理とは、エラーが発生したときに、そのエラーを処理することです。
どんなプログラムでも、エラーが発生する可能性があります。
そのため、エラーが発生したときに、そのエラーを処理することが重要です。
エラーが発生した時に、プログラムがクラッシュしないようにするためには、例外処理を使います。
Exception は、エラーの種類を表すクラスです。
except の後に Exception を指定することで、エラーの種類を指定します。

```python
try:
    result = 10 / 0
except Exception as e:
    print("エラーが発生しました:", e)
```

上記の場合だと、数字を 0 で割ることは、数学的に不可能なので、エラーが発生します。

```
実行結果:
エラーが発生しました: division by zero
```

### 二次元配列

配列の中に配列を入れることで、二次元配列を作ることができます。

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix)
```

```
実行結果:
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

#### 二次元配列の繰り返し処理

二次元配列の繰り返し処理は、for 文を二重に使うことで実現できます。

```python

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for row in matrix:
    for element in row:
        print(element)

```

```
実行結果:
1
2
3
4
5
```

あるいは、

```python
for i, j in matrix:
    print(i, j)
```

```
実行結果:
1 2 3
4 5 6
7 8 9
```

#### enumerate 関数

enumerate 関数は、配列の要素とそのインデックスを同時に取得するための関数です。

```python
for i, j in enumerate(matrix):
    print(i, j)
```

```
実行結果:
0 [1, 2, 3]
1 [4, 5, 6]
2 [7, 8, 9]
```

## まとめ

- None: 何もないことを表す特別な値
- int 型と文字列の混合配列: 配列に異なる型のデータを混ぜて入れることができる
- type 関数: 変数の型を調べることができる
- 配列の操作: 配列の要素を操作することができる
- 例外処理: エラーが発生したときに、そのエラーを処理することができる
