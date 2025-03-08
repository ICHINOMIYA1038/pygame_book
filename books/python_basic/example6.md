---
title: "レベル6"
---

## レベル 6

この章では、以下のことを学びます

1. **辞書型**

   - 辞書の基本操作
   - 辞書のメソッド

2. **クラス**

   - クラスの定義
   - クラスのインスタンス化

3. **`__init__` メソッド**

   - `__init__` メソッドの役割
   - `__init__` メソッドの使い方

4. **`self` の意味**

   - `self` の役割
   - `self` を使ったメソッドの定義

5. **非同期処理**

   - `async` コルーチン
   - `await asyncio`
   - `asyncio.create_task`

### 辞書型

辞書型とは、キーと値のペアを格納するデータ型です。

#### 辞書の基本操作

辞書の作成

```python

person = {
    "name": "太郎",
    "age": 20,
    "city": "東京"
}
```

ここでは、name, age, city がキーで、太郎, 20, 東京がそれぞれの値です。

辞書は配列と違って、キーと値のペアを格納するので、順番はありません。
また、カッコも `[]` ではなく `{}` を使います。

辞書の"キー"は、重複してはいけません。

辞書の"値"は、重複してもかまいません。

辞書の値を取得するには、キーを指定して取得します。

```python

person = {
    "name": "太郎",
    "age": 20,
    "city": "東京"
}

print(person["name"])
```

```
実行結果:
太郎
```

辞書の要素を追加するには、`辞書名[キー] = 値` で追加します。

```python

person = {
    "name": "太郎",
    "age": 20,
    "city": "東京"
}

person["gender"] = "男"

print(person)
```

```
実行結果:
{'name': '太郎', 'age': 20, 'city': '東京', 'gender': '男'}
```

辞書の要素を削除するには、`del 辞書名[キー]` で削除します。

```python

del person["gender"]

print(person)
```

```
実行結果:
{'name': '太郎', 'age': 20, 'city': '東京'}
```

辞書の要素を更新するには、`辞書名[キー] = 値` で更新します。

```python

person["age"] = 21

print(person)
```

### クラスとインスタンス

クラスとは設計図のようなものです。
クラスには変数や関数が定義されます。

```python

class Person:
    name = "太郎"
    age = 20
    city = "東京"

    def say_hello(self):
        print(f"こんにちは、私は{self.name}です。")

    def say_goodbye(self):
        print(f"さようなら、私は{self.name}です。")

```

これは太郎さんの設計図です。

太郎さんの設計図を元に、太郎さんのインスタンスを作ります。

```python

taro = Person()
```

インスタンスとは、設計図を元に作られた具体的なものです。

```python

taro.say_hello()
```

```
実行結果:
こんにちは、私は太郎です。
```

クラスの便利なところは、複数のインスタンスを作ることができることです。
簡単にクローンを生成することができます。

```python

taro = Person()
taro2 = Person()
taro3 = Person()

```

しかし、名前が同じだと使いにくいので次の**init**メソッドを使って名前を変えてみます。

### **init** メソッド

- **init** メソッドの役割

**init** メソッドは、インスタンスを作るときに呼び出されるメソッドです。

- **init** メソッドの使い方

```python
class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city

    def say_hello(self):
        print(f"こんにちは、私は{self.name}です。 年齢は{self.age}歳です。 住所は{self.city}です。")

    def say_goodbye(self):
        print(f"さようなら、私は{self.name}です。")

```

これは、太郎さんのインスタンスを作るときに、名前を太郎、年齢を 20、住所を東京にします。

```python

taro = Person("太郎", 20, "東京")

```

次に、次郎さんのインスタンスを作ります。

```python

次郎 = Person("次郎", 31, "大阪")

```

では、二人に挨拶をさせてみましょう。

```python

taro.say_hello()
次郎.say_hello()

```

```
実行結果:
こんにちは、私は太郎です。 年齢は20歳です。 住所は東京です。
こんにちは、私は次郎です。 年齢は31歳です。 住所は大阪です。
```

### self の意味

self は、インスタンス自身を指すキーワードです。

self をつけることで、インスタンス自身の変数にアクセスすることができます。

例えば、先ほどのクラス定義で、

```python
self.name = name
self.age = age
self.city = city
```

とあったのは、自分自身の変数を使うということを強調するためです。

太郎さんが、次郎さんの名前を変えてしまうと怖いですからね。

### 非同期処理

非同期処理 とは、複数の処理を同時に進行させる方法です
処理 A を実行中に処理 B を待つ必要がないため、効率よくプログラムを動かせます。

同期処理: 処理が順番に実行され、前の処理が終わるまで次の処理は開始されません。
非同期処理: 複数の処理が独立して進行します。待ち時間を有効に使えます。

何も指定せずに書いた場合の処理は、同期処理です。

### Python での非同期処理

Python では async と await を使って非同期処理を実装します。
async とは、非同期処理を実行するためのキーワードです。
await は、非同期処理が終わるまで待つためのキーワードです。

1. async コルーチン (Coroutine)
   async を使って定義された関数は「コルーチン」と呼ばれます。
   コルーチンは途中で一時停止したり再開したりできる特殊な関数です。

```python
async def say_hello():
    print("こんにちは！")
    await asyncio.sleep(1) # 1 秒待機
    print("また会いましょう！")
```

2. await と asyncio
   await を使うと、コルーチンの処理が終わるまで一時停止します。
   await が使えるのは async で定義された関数の中だけです。

```python
async def main():
   print("開始")
   await say_hello() # `say_hello` が終わるまで待つ
   print("終了")
```

```
実行結果:
開始
こんにちは！
（1 秒待機）
また会いましょう！
終了
```

3. asyncio.create_task で並列処理
   asyncio.create_task を使うと、コルーチンを並列に実行できます。

```python
async def task_1():
   print("タスク 1 開始")
   await asyncio.sleep(2)
   print("タスク 1 終了")

async def task_2():
   print("タスク 2 開始")
   await asyncio.sleep(1)
   print("タスク 2 終了")

async def main():
   task1 = asyncio.create_task(task_1())
   task2 = asyncio.create_task(task_2())

   await task1
   await task2
```

```
実行結果:
開始
タスク 1 開始
（2 秒待機）
タスク 1 終了
タスク 2 開始
（1 秒待機）
タスク 2 終了
終了
```

#### タスクのキャンセル (task.cancel())

非同期タスクを途中でキャンセルしたい場合、 .cancel() メソッドを使います。

```python
async def slow_task():
    try:
        print("タスク開始")
        await asyncio.sleep(5)
        print("タスク終了")
    except asyncio.CancelledError:
        print("タスクがキャンセルされました！")

async def main():
    task = asyncio.create_task(slow_task())
    await asyncio.sleep(2)
    task.cancel()  # タスクをキャンセル
    await task  # キャンセル結果を待つ

asyncio.run(main())
```

```
実行結果:
タスク開始
タスクがキャンセルされました！
```
