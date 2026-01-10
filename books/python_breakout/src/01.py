import pygame
import sys

# 画面サイズ
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)

# パドルの設定
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15


class Paddle(pygame.sprite.Sprite):
    """プレイヤーが操作するパドル（板）"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # 画面の下の方、中央に配置
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        self.speed = 8

    def update(self):
        """キー入力でパドルを左右に動かす"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # 画面の外に出ないようにする
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ブロック崩し - 01")

    # パドルを作成
    paddle = Paddle()
    paddle_group = pygame.sprite.Group(paddle)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # パドルを更新
        paddle_group.update()

        # 画面を黒でクリア
        screen.fill(BLACK)

        # パドルを描画
        paddle_group.draw(screen)

        # 画面を更新
        pygame.display.flip()


if __name__ == "__main__":
    main()
