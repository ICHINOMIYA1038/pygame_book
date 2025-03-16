from pygame.locals import *
import pygame
import sys

# 円の初期位置と速度
character_x = 100
character_y = 200
character_speed = 0.1

# 球のリストを初期化
bullets = []

# キャラクター画像の読み込み
def load_character():
    character = pygame.image.load("img/1.png")
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

def fire_bullet():
    bullet = pygame.image.load("img/4.png")
    bullet = pygame.transform.scale(bullet, (100, 100)) # 画像サイズを変更
    bullet = pygame.transform.rotate(bullet, -90) # 画像を回転
    return bullet

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

        # 球を描画
        for bullet in bullets:
            screen.blit(bullet['image'], (bullet['x'], bullet['y']))
            bullet['x'] += 5  # 球を右に移動

        pygame.display.update()  # 画面を更新

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 終了イベント
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:  # スペースキーが押されたとき
                    bullet_image = fire_bullet()
                    bullets.append({'image': bullet_image, 'x': character_x, 'y': character_y})

        # キー状態を取得し、キャラクターを移動
        keys = pygame.key.get_pressed()
        move_character(keys)

if __name__ == "__main__":
    main()