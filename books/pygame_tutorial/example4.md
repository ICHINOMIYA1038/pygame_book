---
title: "Pygame 基礎編"
---

## Pygame の導入

いよいよ Pygame を利用してゲームを作成します。最初に以下を実行してみましょう。

## 最初に使うコード

```python:01.py
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
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()  #pygameのウィンドウを閉じる
                sys.exit() #システム終了

if __name__=="__main__":
    main()
```

これで黒い画面に赤い色の円が作成されます。

![赤い円の作成](/pygame_tutorial/images/pygame_tutorial/01.png)

コードを読んで、以下の問題を解いてみましょう

1. 円の色を変えるにはどうしますか？まずは白色にしてみましょう。
2. 画面のサイズを変えるにはどうしますか？
3. 背景の色を変えるにはどうしますか？好きな色に変えてみましょう。
4. event という変数は何のクラスのインスタンスでしょうか？ print(type(hoge)) を利用すると hoge 変数のクラスを確認することができます。
5. ドキュメント(https://westplain.sakura.ne.jp/translate/pygame/Draw.cgi#pygame.draw.line) を読んで、好きな位置に赤い線を書いてみましょう。
6. 次に、ドキュメント(https://westplain.sakura.ne.jp/translate/pygame/) を読んだ上で青色の四角を好きな場所に表示してみましょう。このとき、Rect クラスが出てくるので Rect についても調べてみましょう

### ものを動かす

次にキーボードでものを動かすことを考えます。このとき大事なのは、サンプルコードをすぐに見るのではなくて自分でドキュメントを読むことです。

キーボードで動かすので、ドキュメントの Key を見てみます。

[pygame.key.get_pressed ドキュメント](https://westplain.sakura.ne.jp/translate/pygame/Key.cgi)

`pygame.key.get_pressed`　で全てのキーの入力状態を取得できるとあります。

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

```python:02.py
import pygame
import sys


def main():
    pygame.init()  # 初期化
    screen = pygame.display.set_mode((400, 330))  # 画面を作成

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    circle_x = 100
    circle_y = 200

    running = True
    # メインループ
    while running:
        screen.fill(BLACK)  # 画面を黒で塗りつぶす

        # 円を描画
        pygame.draw.circle(screen, RED, (circle_x, circle_y), 10)


        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()

        # キー状態を取得
        keys = pygame.key.get_pressed()

        # 上キーの状態をテキストとして画面に表示
        font = pygame.font.Font(None, 18)
        key_state = "UP Key: " + ("Pressed" if keys[pygame.K_UP] else "Not Pressed")
        text = font.render(key_state, True, RED)
        screen.blit(text, (10, 10))

        pygame.display.update()  # 画面を更新

if __name__ == "__main__":
    main()
```

上記のコードを実行すると、画面上に上矢印キーの状態が表示されます。
このようにキーボードが押されているかどうかが、keys という配列で取得されているのです。
押されている場合には、keys[pygame.K_UP] が true になり 押されていない時には false になります。

![pygameのチュートリアル](/pygame_tutorial/images/pygame_tutorial/02.png)

これを元に赤い円を動かすコードを書いてみましょう。書き終わったら、以下のお手本のコードと見比べてみてください。

```python:03.py
import pygame
import sys

# 円の初期位置と速度
circle_x = 100
circle_y = 200
circle_speed = 0.5

# 円の移動関数
def move_circle(keys):
    global circle_x, circle_y
    if keys[pygame.K_LEFT]:  # 左キー
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT]:  # 右キー
        circle_x += circle_speed
    if keys[pygame.K_UP]:  # 上キー
        circle_y -= circle_speed
    if keys[pygame.K_DOWN]:  # 下キー
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
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()

        # キー状態を取得し、円を移動
        keys = pygame.key.get_pressed()
        move_circle(keys)

if __name__ == "__main__":
    main()
```

これで円が動くようになったはずです。

### 画像を表示する

円は動かせましたが、ゲームを作るなら自分の好きなものを動かしたいですね。自分の好きな画像を表示してそれを動かすコードを作成してみましょう。

画像の読み込みをしたいのでドキュメントの image の部分を参考にします。

[pygame.image.load ドキュメント](https://westplain.sakura.ne.jp/translate/pygame/Image.cgi)

```python
pygame.image.load("images/character.png")
```

上記のコードで画像を読み込むことができます。この時、画像の**パス** に気をつけてください。相対パスで指定します。相対パスが何かわからない人は**コンピュータの基礎**をもう一度学習してください。

ドキュメントを読むと、`pygame.image.load("images/character.png")`の返り値は Surface クラスです。`screen = pygame.display.set_mode((400, 330))`で定義される screen も Surface クラスでした。

Surface のドキュメントを読むと、画像を他の画像上に描写するには `Surface.blit` を用いればいいことがわかります。

[pygame.Surface.blit ドキュメント](https://westplain.sakura.ne.jp/translate/pygame/Surface.cgi)

そこで`screen`に自分で用意した画像を貼り付けた上で screen を表示します。

```python:04.py
import pygame
import sys

# 円の初期位置と速度
character_x = 100
character_y = 200
character_speed = 0.5

# キャラクター画像の読み込み
def load_character():
    character = pygame.image.load("images/character.png")
    character = pygame.transform.scale(character, (50, 60)) # 画像サイズを変更
    character = pygame.transform.rotate(character, -90) # 画像を回転
    return character

# 円の移動関数
def move_character(keys):
    global character_x, character_y
    if keys[pygame.K_LEFT]:  # 左キー
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:  # 右キー
        character_x += character_speed
    if keys[pygame.K_UP]:  # 上キー
        character_y -= character_speed
    if keys[pygame.K_DOWN]:  # 下キー
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
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()

        # キー状態を取得し、キャラクターを移動
        keys = pygame.key.get_pressed()
        move_character(keys)

if __name__ == "__main__":
    main()
```

![pygameのチュートリアル](/pygame_tutorial/images/pygame_tutorial/04.png)

### コードを整理する。

これから、敵や弾丸を作っていきます。
しかし、このまま書いていくとコードが長く、分かりにくくなってしまうので、クラスというものを使います。

クラスというのは簡単にいうと設計図のことです。

敵や弾丸などたくさん出てくるものは数が多いので毎回作るのは大変なので設計図を元に作るのです。

今回はまず、自分の動かしている player についてクラスにしてみます。
player は一体しか作らないので、ありがたみはわからないかもしれませんが、敵や弾丸を作る準備だと思って作成してみましょう。

`__init__`という関数は設計図から実際のオブジェクト(インスタンス)を作成するときに実行される関数です。
ここでは最初の位置や速度などが入ります。

```python:05.py
import pygame
import sys

# プレイヤーの設計図
class Player:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/character.png")
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.image = pygame.transform.rotate(self.image, -90)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.x += self.speed_x
        if keys[pygame.K_UP]:
            self.y -= self.speed_y
        if keys[pygame.K_DOWN]:
            self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def main():
    pygame.init()  # 初期化
    screen = pygame.display.set_mode((400, 330))  # 画面を作成
    BLACK = (0, 0, 0)

    # プレイヤーのインスタンスを作成
    player = Player(100, 200, 0.1, 0.1)

    running = True
    # メインループ
    while running:
        screen.fill(BLACK)  # 画面を黒で塗りつぶす

        # キャラクターを描画
        player.draw(screen)

        pygame.display.update()  # 画面を更新

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()

        # キー状態を取得し、キャラクターを移動
        keys = pygame.key.get_pressed()
        player.move(keys)

if __name__ == "__main__":
    main()
```

### 敵を作る

それでは敵を作ってみましょう。敵は `images/enemy.png` という名前で作成します。
player と同じように enemy も最初に設計図を作りそれをもとに作成します。

```python:06.py
import pygame
import sys
import random

# プレイヤーの設計図
class Player:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/character.png")
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.image = pygame.transform.rotate(self.image, -90)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.x += self.speed_x
        if keys[pygame.K_UP]:
            self.y -= self.speed_y
        if keys[pygame.K_DOWN]:
            self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 敵の設計図
class Enemy:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.image = pygame.transform.rotate(self.image, 0) # 画像に合わせて回転させる

    def move(self):
        self.x += self.speed_x
        return self.x < -50  # 画面外に出たら削除

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def main():
    pygame.init()  # 初期化
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 330
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 画面を作成
    BLACK = (0, 0, 0)

    # 敵の生成イベントを設定
    ENEMY_SPAWN_TIME = 3000  # 3秒ごとに敵を追加
    ENEMY_SPAWN_EVENT = pygame.USEREVENT
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_TIME)

    # プレイヤーのインスタンスを作成
    player = Player(100, 200, 2, 2)

    # 敵のリストを作成
    enemies = []

    running = True
    clock = pygame.time.Clock()
    # メインループ
    while running:
        screen.fill(BLACK)  # 画面を黒で塗りつぶす

        # キャラクターを描画
        player.draw(screen)

        # 敵の更新と描画
        enemies = [enemy for enemy in enemies if not enemy.move()]
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.update()  # 画面を更新
        clock.tick(60)  # フレームレートを60に設定

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == ENEMY_SPAWN_EVENT:
                # 新しい敵を生成
                enemies.append(Enemy(SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT - 60), -1, 0))

        # キー状態を取得し、キャラクターを移動
        keys = pygame.key.get_pressed()
        player.move(keys)

if __name__ == "__main__":
    main()
```

![pygameのチュートリアル](/pygame_tutorial/images/pygame_tutorial/06.png)

これでランダムで敵が出てくるようになりました。
まだ、ぶつかってもゲームオーバーにはなりません。
先にプレイヤーが出す弾丸を作りましょう。

### 弾丸を作る

それでは次に弾丸を作ります。
弾丸も敵と同じように設計図から作成します。

```python:07.py
import pygame
import sys
import random

# プレイヤーの設計図
class Player:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/character.png")
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.image = pygame.transform.rotate(self.image, -90)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.x += self.speed_x
        if keys[pygame.K_UP]:
            self.y -= self.speed_y
        if keys[pygame.K_DOWN]:
            self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 敵の設計図
class Enemy:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.image = pygame.transform.rotate(self.image, 0) # 画像に合わせて回転させる

    def move(self):
        self.x += self.speed_x
        return self.x < -50  # 画面外に出たら削除

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 弾の設計図
class Bullet:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 0)

    def move(self):
        self.x += self.speed_x
        return self.x > 400  # 画面外に出たら削除

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def main():
    pygame.init()  # 初期化
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 330
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 画面を作成
    BLACK = (0, 0, 0)

    # 敵の生成イベントを設定
    ENEMY_SPAWN_TIME = 3000  # 3秒ごとに敵を追加
    ENEMY_SPAWN_EVENT = pygame.USEREVENT
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_TIME)

    # プレイヤーのインスタンスを作成
    player = Player(100, 200, 2, 2)

    # 敵のリストを作成
    enemies = []

    # 弾のリストを作成
    bullets = []

    running = True
    clock = pygame.time.Clock()
    # メインループ
    while running:
        screen.fill(BLACK)  # 画面を黒で塗りつぶす

        # キャラクターを描画
        player.draw(screen)

        # 敵の更新と描画
        enemies = [enemy for enemy in enemies if not enemy.move()]
        for enemy in enemies:
            enemy.draw(screen)

        # 弾の更新と描画
        bullets = [bullet for bullet in bullets if not bullet.move()]
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.update()  # 画面を更新
        clock.tick(60)  # フレームレートを60に設定

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == ENEMY_SPAWN_EVENT:
                # 新しい敵を生成
                enemies.append(Enemy(SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT - 60), -1, 0))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # スペースキーで弾を発射
                    bullets.append(Bullet(player.x + 50, player.y + 15, 5, 0))

        # キー状態を取得し、キャラクターを移動
        keys = pygame.key.get_pressed()
        player.move(keys)

if __name__ == "__main__":
    main()

```

これで player の位置から炎を出せるようになりました。
しかし、まだ当たり判定がないので敵を倒すことはできません。

![pygameのチュートリアル](/pygame_tutorial/images/pygame_tutorial/07.png)

### 当たり判定とスコアを実装

次に当たり判定を作りましょう。

当たり判定の考え方は初めての人にとっては少し難しいです。

```python
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (enemy.x < bullet.x < enemy.x + 50) and (enemy.y < bullet.y < enemy.y + 60):
                bullets.remove(bullet)
                enemies.remove(enemy)
```

上記のように位置関係を用いてぶつかったかどうかを判定します。
ゲームでは矩形(くけい)と呼ばれる四角形の位置関係で当たったかどうかを判定しているのです。

```python:main.py
import pygame
import sys
import random

# プレイヤーの設計図
class Player:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/character.png")
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.image = pygame.transform.rotate(self.image, -90)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.x += self.speed_x
        if keys[pygame.K_UP]:
            self.y -= self.speed_y
        if keys[pygame.K_DOWN]:
            self.y += self.speed_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# 敵の設計図
class Enemy:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.image = pygame.transform.rotate(self.image, 0) # 画像に合わせて回転させる

    def move(self):
        self.x += self.speed_x
        return self.x < -50  # 画面外に出たら削除

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 弾の設計図
class Bullet:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, 0)

    def move(self):
        self.x += self.speed_x
        return self.x > 400  # 画面外に出たら削除

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 衝突管理クラス
class CollisionManager:
    @staticmethod
    def check_collision_bullet(bullets, enemies):
        global score
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (enemy.x < bullet.x < enemy.x + 50) and (enemy.y < bullet.y < enemy.y + 60):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 5  # スコア加算

    @staticmethod
    def check_collision_player(player, enemies):
        """敵に当たったか判定"""
        for enemy in enemies:
            if (enemy.x < player.x < enemy.x + 50) and (enemy.y < player.y < enemy.y + 60):
                return True
        return False

# スコアを描画する関数
def draw_score(screen, score, font):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # 白色
    screen.blit(score_text, (10, 10))  # 左上に表示

# メッセージを画面に表示する関数
def show_message(screen, font, message):
    screen.fill((0, 0, 0))  # 画面を黒くする
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(400 // 2, 330 // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)  # 3秒間メッセージを表示
    pygame.quit()
    sys.exit()

def main():
    global score
    pygame.init()  # 初期化
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 330
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 画面を作成
    BLACK = (0, 0, 0)

    # 敵の生成イベントを設定
    ENEMY_SPAWN_TIME = 3000  # 3秒ごとに敵を追加
    ENEMY_SPAWN_EVENT = pygame.USEREVENT
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_TIME)

    # フォントの設定
    font = pygame.font.Font(None, 36)

    # プレイヤーのインスタンスを作成
    player = Player(100, 200, 2, 2)

    # 敵のリストを作成
    enemies = []

    # 弾のリストを作成
    bullets = []

    # スコアを初期化
    score = 0

    running = True
    clock = pygame.time.Clock()
    # メインループ
    while running:
        screen.fill(BLACK)  # 画面を黒で塗りつぶす

        # キャラクターを描画
        player.draw(screen)

        # 敵の更新と描画
        enemies = [enemy for enemy in enemies if not enemy.move()]
        for enemy in enemies:
            enemy.draw(screen)

        # 弾の更新と描画
        bullets = [bullet for bullet in bullets if not bullet.move()]
        for bullet in bullets:
            bullet.draw(screen)

        # 衝突判定
        CollisionManager.check_collision_bullet(bullets, enemies)

        # ゲームクリアの判定
        if score >= 50:
            show_message(screen, font, "Game Clear!")

        # ゲームオーバーの判定
        if CollisionManager.check_collision_player(player, enemies):
            show_message(screen, font, "Game Over")

        # スコアを描画
        draw_score(screen, score, font)

        pygame.display.update()  # 画面を更新
        clock.tick(60)  # フレームレートを60に設定

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == ENEMY_SPAWN_EVENT:
                # 新しい敵を生成
                enemies.append(Enemy(SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT - 60), -1, 0))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # スペースキーで弾を発射
                    bullets.append(Bullet(player.x + 50, player.y + 15, 5, 0))

        # キー状態を取得し、キャラクターを移動
        keys = pygame.key.get_pressed()
        player.move(keys)

if __name__ == "__main__":
    main()
```

これで最低限のシューティングゲームが完成しました。
敵を増やしたり、難易度を調整したり自分で工夫して遊んでみましょう。

![pygameのチュートリアル](/pygame_tutorial/images/pygame_tutorial/08.png)

## 参考ドキュメント

英語版のドキュメント

[pygame 英語版ドキュメント](https://www.pygame.org/docs/)

日本語化されたドキュメント

[pygame 日本語版ドキュメント](https://westplain.sakura.ne.jp/translate/pygame/)
