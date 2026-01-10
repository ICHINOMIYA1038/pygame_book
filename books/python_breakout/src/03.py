import pygame
import sys

# 画面サイズ
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
RED = (255, 100, 100)

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
        self.reset()

    def reset(self):
        """ボールを初期位置に戻す"""
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2
        self.dx = 4
        self.dy = -4

    def update(self):
        """ボールを動かして、壁で跳ね返す"""
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 左右の壁で跳ね返る
        if self.rect.left <= 0:
            self.rect.left = 0
            self.dx = -self.dx
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.dx = -self.dx

        # 上の壁で跳ね返る
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dy = -self.dy

    def is_out(self):
        """ボールが画面下に落ちたか判定"""
        return self.rect.top >= SCREEN_HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ブロック崩し - 03")

    # フォントの準備
    font = pygame.font.Font(None, 48)

    # パドルとボールを作成
    paddle = Paddle()
    ball = Ball()
    paddle_group = pygame.sprite.Group(paddle)
    ball_group = pygame.sprite.Group(ball)

    clock = pygame.time.Clock()

    # ゲームの状態
    game_over = False

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # ゲームオーバー時にRキーでリスタート
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    ball.reset()
                    game_over = False

        if not game_over:
            # 更新
            paddle_group.update()
            ball_group.update()

            # パドルとボールの衝突判定
            if ball.rect.colliderect(paddle.rect):
                # ボールをパドルの上に押し戻す
                ball.rect.bottom = paddle.rect.top
                # 上方向に跳ね返す
                ball.dy = -abs(ball.dy)

            # ボールが落ちたらゲームオーバー
            if ball.is_out():
                game_over = True

        # 描画
        screen.fill(BLACK)
        paddle_group.draw(screen)
        ball_group.draw(screen)

        # ゲームオーバー表示
        if game_over:
            text = font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

            restart_text = font.render("Press R to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()
