# main.py：大きな 迷路（めいろ）で ぼうけんしよう！

このしょうでは、いままで つくってきた いろいろな しかけを ぜんぶ いれて、  
大きな 迷路（めいろ）で ぼうけんできる ゲームの かんせいバージョンを しょうかいします。

## できること

- ひろい 迷路（めいろ）の中を、青（あお）いプレイヤーで ぼうけんできます。
- グレーの「かべ」に ぶつからないように すすみます。
- 赤（あか）い「てき」も うごいています。ぶつかると ゲームオーバーです。
- 金色（きんいろ）の「ゴール」に たどりつくと、クリアです。
- 「R」キーで もういちど やりなおせます。

## コードのポイント

### 1. マップデータのつくりかた

```python
MAP_DATA = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ...（中略）...
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]
```

- たくさんの「W（かべ）」「F（ゆか）」「G（ゴール）」の文字で、ひろい迷路をつくっています。
- 1 文字が 1 マスになり、プログラムが自動でマップをよみこみます。

### 2. プレイヤーのクラス

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        ...（中略）...
    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -self.speed
        ...（中略）...
        # 壁にぶつかったら元の場所にもどる
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x = old_x
                self.rect.y = old_y
                break
```

- プレイヤーは上下左右キーでうごきます。
- かべ（Wall）にぶつかったら、もとにもどるので、かべをすりぬけられません。

### 3. てき（Enemy）のクラス

```python
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        ...（中略）...
    def update(self, walls):
        # きまった時間ごとにランダムにうごく
        ...（中略）...
        # かべにぶつかったら元にもどる
```

- てきはじぶんでランダムにうごきます。
- かべにぶつかったら、もとにもどります。

### 4. ゲームの流れ

- まず、マップデータから「かべ」「ゴール」「プレイヤー」「てき」をつくります。
- ずっとくりかえし（ループ）で、プレイヤーやてきをうごかします。
- プレイヤーがゴールにふれたら「Game Clear!」と表示。
- てきにぶつかったら「Game Over!」と表示。
- 「R」キーで、またさいしょからやりなおせます。

### 5. 画面の描画

```python
for row_idx, row in enumerate(MAP_DATA):
    for col_idx, tile in enumerate(row):
        if tile == 'F':
            pygame.draw.rect(
                screen,
                (100, 200, 100),
                (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
```

- まっぷの「F」のところに、みどり色の「ゆか」をかきます。
- かべやゴール、プレイヤー、てきはスプライトでかきます。

## まとめ

このバージョンで、いろいろな しかけが そろった 迷路ゲームが かんせいです！  
じぶんだけの 迷路や しかけを つくって、もっと たのしい ゲームに してみましょう。
