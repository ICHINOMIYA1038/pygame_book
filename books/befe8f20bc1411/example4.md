---
title: "pygame 基礎編"
---

## Pygame の導入

いよいよ pygame を利用してゲームを作成します。

最初に以下を実行してみましょう。

## 最初に使うコード

```python
from pygame.locals import *
import pygame
import sys

def main():
    pygame.init()    # 初期化
    screen = pygame.display.set_mode((400, 330))  # 画面を作成

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    running = True
    #メインループ
    while running:
        screen.fill(BLACK)  #画面を黒で塗りつぶす

        pygame.draw.circle(screen, RED, (100,200), 10)

        pygame.display.update() #画面を更新

        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()  #pygameのウィンドウを閉じる
                sys.exit() #システム終了

if __name__=="__main__":
    main()
```

これで黒い画面に赤い色の円が作成されます。

まずは上記のコードで何をやっているかを一つ一つ意識してみましょう。

![スクリーンショット 2025-01-02 17.07.58](/Users/ichinomiya/Library/Application Support/typora-user-images/スクリーンショット 2025-01-02 17.07.58.png)

そこで、以下の問題を解いてみましょう

1. 円の色を変えるにはどうしますか ？　まずは白色にしてみましょう。
2. 画面のサイズを変えるにはどうしますか？
3. 背景の色を変えるにはどうしますか？好きな色に変えてみましょう。
4. event という変数は何のクラスのインスタンスでしょうか？
5. ドキュメント(https://westplain.sakura.ne.jp/translate/pygame/Draw.cgi#pygame.draw.line) を読んで、好きな位置に赤い線を書いてみましょう。
6. 次に、ドキュメント(https://westplain.sakura.ne.jp/translate/pygame/) を読んだ上で青色の四角を好きな場所に表示してみましょう。このとき、Rect クラスが出てくるので Rect についても調べてみましょう

### ものを動かす

次にキーボードでものを動かすことを考えます。

このとき大事なのは、サンプルコードをすぐに見るのではなくて自分でドキュメントを読むことです。

キーボードで動かすので、ドキュメントの Key を見てみます。

https://westplain.sakura.ne.jp/translate/pygame/Key.cgi

`pygame.key.get_pressed`　で全てのキーの入力状態を取得できるとあります。

![スクリーンショット 2025-01-02 22.06.05](/Users/ichinomiya/Library/Application Support/typora-user-images/スクリーンショット 2025-01-02 22.06.05.png)

今回は `keys = pygame.key.get_pressed`を使って全てのキーの状態を Keys という変数に入れて使うことにします。

ドキュメントのその先を見ると下記のような記述があります。

> Pygame には入力キーを識別するための多くのキーボード定数があり、 それらを使用してキーボードのどのキーが押されたかを特定します。下記がキーボード定数の一覧です。

今回は、矢印キーでものを動かすので以下の記述を参考にします。

```
K_UP                  up arrow
K_DOWN                down arrow
K_RIGHT               right arrow
K_LEFT                left arrow
```

ここで Keys[K_UP]がどのような値になるかをみてみましょう。

```
from pygame.locals import *
import pygame
import sys


def main():
    pygame.init()  # 初期化
    screen = pygame.display.set_mode((400, 330))  # 画面を作成

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    running = True
    # メインループ
    while running:
        screen.fill(BLACK)  # 画面を黒で塗りつぶす

        # 円を描画
        pygame.draw.circle(screen, RED, (circle_x, circle_y), 10)

        pygame.display.update()  # 画面を更新

        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()

        # キー状態を取得
        keys = pygame.key.get_pressed()
        print(keys[K_UP])

if __name__ == "__main__":
    main()

```

上記のコードを実行すると、ターミナルに false が表示され続けます。

しかし、上矢印を押すと、true に変わるはずです。

このようにキーボードが押されているかどうかが、keys という配列で取得されているのです。

これを元に赤い円を動かすコードを書いてみましょう。

書き終わったら、以下のお手本のコードと見比べてみてください。

```
from pygame.locals import *
import pygame
import sys

# 円の初期位置と速度
circle_x = 100
circle_y = 200
circle_speed = 0.1

# 円の移動関数
def move_circle(keys):
    global circle_x, circle_y
    if keys[K_LEFT]:  # 左キー
        circle_x -= circle_speed
    if keys[K_RIGHT]:  # 右キー
        circle_x += circle_speed
    if keys[K_UP]:  # 上キー
        circle_y -= circle_speed
    if keys[K_DOWN]:  # 下キー
        circle_y += circle_speed


def main():
    pygame.init()  # 初期化
    screen = pygame.display.set_mode((400, 330))  # 画面を作成

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    running = True
    # メインループ
    while running:
        screen.fill(BLACK)  # 画面を黒で塗りつぶす

        # 円を描画
        pygame.draw.circle(screen, RED, (circle_x, circle_y), 10)

        pygame.display.update()  # 画面を更新

        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()

        # キー状態を取得し、円を移動
        keys = pygame.key.get_pressed()
        move_circle(keys)

if __name__ == "__main__":
    main()

```

### 画像を表示する

円は動かせましたが、ゲームを作るなら自分の好きなものを動かしたいですね。

自分の好きな画像を表示してそれを動かすコードを作成してみましょう。

画像の読み込みをしたいのでドキュメントの image の部分を参考にします。

https://westplain.sakura.ne.jp/translate/pygame/Image.cgi

```
pygame.image.load("images/character.png")
```

上記のコードで画像を読み込むことができます。

この時、画像の**パス** に気をつけてください。相対パスで指定します。

相対パスが何かわからない人は**コンピュータの基礎**をもう一度学習してください。

ドキュメントを読むと、`pygame.image.load("images/character.png")`の返り値は Surface クラスです。

`   screen = pygame.display.set_mode((400, 330))`で定義される screen も Surface クラスでした。

Surface のドキュメントを読むと、画像を他の画像上に描写するには `Surface.blit` を用いればいいことがわかります。

https://westplain.sakura.ne.jp/translate/pygame/Surface.cgi

そこで`screen`に自分で用意した画像を貼り付けた上で screen を表示します。

```
from pygame.locals import *
import pygame
import sys

# 円の初期位置と速度
character_x = 100
character_y = 200
character_speed = 0.1

# キャラクター画像の読み込み
def load_character():
    character = pygame.image.load("images/character.png")
    character = pygame.transform.scale(character, (50, 60)) # 画像サイズを変更
    character = pygame.transform.rotate(character, -90) # 画像を回転
    return character

# 円の移動関数
def move_character(keys):
    global character_x, character_y
    if keys[K_LEFT]:  # 左キー
        character_x -= character_speed
    if keys[K_RIGHT]:  # 右キー
        character_x += character_speed
    if keys[K_UP]:  # 上キー
        character_y -= character_speed
    if keys[K_DOWN]:  # 下キー
        character_y += character_speed


def main():
    pygame.init()  # 初期化
    screen = pygame.display.set_mode((400, 330))  # 画面を作成

    BLACK = (0, 0, 0)
    character_image = load_character()

    running = True
    # メインループ
    while running:
        screen.fill(BLACK)  # 画面を黒で塗りつぶす

        # キャラクターを描画
        screen.blit(character_image, (character_x, character_y))

        pygame.display.update()  # 画面を更新

        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()

        # キー状態を取得し、キャラクターを移動
        keys = pygame.key.get_pressed()
        move_character(keys)

if __name__ == "__main__":
    main()

```

## 参考ドキュメント

英語版のドキュメント

https://www.pygame.org/docs/

日本語化されたドキュメント

https://westplain.sakura.ne.jp/translate/pygame/
