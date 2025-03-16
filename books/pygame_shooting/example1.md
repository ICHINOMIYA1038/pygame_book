---
title: "pygameでシューティングゲームを作成しよう。"
---

## 利用するファイル

- main.py

以下のファイルをコピーして main.py を作成してください。
実行する時には python main.py としてください。

```python
#pygametで画面を表示するためのプログラム

import pygame
import sys

def main():
    #初期化
    pygame.init()

    #画面のサイズを設定
    screen = pygame.display.set_mode((640, 480))

    #タイトルを設定
    pygame.display.set_caption("サンプルプログラム")

    #背景を黒塗り
    screen.fill((0, 0, 0))

    #文字を表示
    font = pygame.font.Font(None, 36)
    text = font.render("Hello, Pygame!", True, (255, 255, 255))
    screen.blit(text, (0, 0))

    #画像を表示
    image = pygame.image.load("img/1.png")
    screen.blit(image, (100, 100))


    #画面を更新
    pygame.display.update()

    #メインループ
    while True:
        #イベント処理
        for event in pygame.event.get():
            #閉じるボタンが押されたら終了
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    #pygameの終了
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```
