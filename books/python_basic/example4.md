---
title: "レベル4"
---

## レベル 4

この章では、以下のことを学びます

- 定数の使い方
- const.price の使い方
- while ループの基本と応用
- match 文の使い方
- 配列の応用 (num[len(num) + 1] など)
- 配列操作: array.pop, array.append
- ループ制御: break と continue
- value in array で要素の存在確認
- array.index(value) で位置を調べる

### 定数の使い方

定数とは、変更しない値のことです。
変数とは違い、定数は再び代入することはできません。

定数は慣習的に大文字で書かれます。

python では厳密には定数は存在しません。
しかし、const モジュールを使って定数のように振る舞うことができます。

```python
import const

const.PI = 3.14159
const.MAX_SPEED = 120
```

### while ループの基本と応用

while ループは、条件が真の間繰り返す処理です。

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

count は 0 から 4 まで 1 ずつ増えていきます。
for ループとは違い、自動には増えないので、count += 1 をしないと無限ループになります。
ゲームでは意図的に無限ループを使うこともあります。

```
実行結果:
0
1
2
3
4
```

### match 文の使い方

match 文は、条件分岐を簡潔に書くための文です。

```python
match 変数:
    case 値1:
        処理1
    case 値2:
        処理2
    case _:
        処理3
```

case \_ は、どの case にも当てはまらない場合の処理です。

例

```python
num = 1

match num:
    case 1:
        print("1です")
    case 2:
        print("2です")
    case _:
        print("1でも2でもありません")
```

実行結果:

```
1です
```

### 配列の応用 (num[len(num) + 1] など)

配列にはインデックスを指定することで値を取得することができます。
インデックスには int を指定しますが、関数の帰り値を利用したり、演算子を使ったりすることもできます。

例:

```python
num = [10, 20, 30, 40, 50]
print(num[0]) # 最初の要素
print(num[-1]) # 最後の要素
print(num[len(num) - 1]) # 最後の要素
```

```
実行結果:
10
50
50
```

最後の要素は、num[-1] と書くこともできますし、num[len(num) - 1] と書くこともできます。
len 関数は、配列の長さを返す関数です。
そのため、num[len(num) - 1] と書くことで、最後の要素を取得することができます。

### 配列操作

配列の要素を操作するための便利な関数を紹介します。

#### append 関数

append 関数は、配列の最後に要素を追加する関数です。

例:

```python
fruits = ["apple", "banana"]
fruits.append("cherry")
print(fruits)
```

実行結果:

```
['apple', 'banana', 'cherry']
```

#### pop 関数

pop 関数は、配列の最後の要素を削除する関数です。

例:

```python
fruits = ["apple", "banana"]
fruits.append("cherry")
print(fruits)
```

実行結果:

```
['apple', 'banana', 'cherry']
```

### ループ制御

ループ制御は、ループを制御するための関数です。

#### break 関数

break 関数は、ループを終了する関数です。

```python
for i in range(5):
if i == 3:
break
print(i)
```

実行結果:

```
0
1
2
```

#### continue 関数

continue 関数は、次のループにスキップする関数です。

```python
for i in range(5):
if i == 3:
continue
print(i)
```

実行結果:

```
0
1
2
4
```

### value in array で要素の存在確認

value in array は、特定の値が配列に含まれているか確認する関数です。

```python
colors = ["red", "green", "blue"]
print("red" in colors) # True
print("yellow" in colors) # False
```

実行結果:

```
True
False
```

### array.index(value) で位置を調べる

array.index(value) は、特定の値が配列の何番目にあるかを調べる関数です。
存在しない場合はエラーになります。

```python
colors = ["red", "green", "blue"]
print(colors.index("red")) # 0
print(colors.index("yellow")) # ValueError: 'yellow' is not in list
```

```
0
ValueError: 'yellow' is not in list
```

array.index(value) で位置を調べる
特定の値がどの位置にあるかを返します。存在しない場合はエラーになります。

```python
numbers = [10, 20, 30, 40]
print(numbers.index(30))
```

実行結果:

```
2
```

エラーになる例:

```python
print(numbers.index(50)) # ValueError: 50 is not in list
```

応用例: 配列とループ、条件分岐を組み合わせる

```python
scores = [75, 85, 90, 70, 60]

for score in scores:
if score < 70:
print(f"{score} は不合格です")
continue
print(f"{score} は合格です")
実行結果:

```

75 は合格です
85 は合格です
90 は合格です
70 は合格です
60 は不合格です

```

まとめ

- 定数: 書き換えない変数として使う
- while ループ: 繰り返し処理
- match 文: 条件分岐を簡潔に
- 配列の応用: インデックスを使った操作
- append と pop: 要素の追加と削除
- break と continue: ループの制御
- in と index: 要素の存在確認と位置取得
```
