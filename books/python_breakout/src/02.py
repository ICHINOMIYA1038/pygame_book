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

# ボールの設定
BALL_SIZE = 12


class Paddle(pygame.sprite.Sprite):
    """プレイヤーが操作するパドル（板）"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
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

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    """動き回るボール"""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # 画面の中央に配置
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2
        # ボールの速度（dx: 横方向, dy: 縦方向）
        self.dx = 4
        self.dy = -4

    def update(self):
        """ボールを動かして、壁で跳ね返す"""
        # ボールを移動
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 左右の壁で跳ね返る
        if self.rect.left <= 0:
            self.rect.left = 0
            self.dx = -self.dx  # 横方向の速度を反転
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.dx = -self.dx

        # 上の壁で跳ね返る
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dy = -self.dy  # 縦方向の速度を反転

        # 下に落ちたら上から再スタート（仮）
        if self.rect.top >= SCREEN_HEIGHT:
            self.rect.centerx = SCREEN_WIDTH // 2
            self.rect.centery = SCREEN_HEIGHT // 2
            self.dy = -4


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ブロック崩し - 02")

    # パドルとボールを作成
    paddle = Paddle()
    ball = Ball()
    paddle_group = pygame.sprite.Group(paddle)
    ball_group = pygame.sprite.Group(ball)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 更新
        paddle_group.update()
        ball_group.update()

        # 描画
        screen.fill(BLACK)
        paddle_group.draw(screen)
        ball_group.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
