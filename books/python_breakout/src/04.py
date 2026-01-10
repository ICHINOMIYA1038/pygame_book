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

# ブロックの色リスト
BLOCK_COLORS = [
    (255, 100, 100),  # 赤
    (255, 200, 100),  # オレンジ
    (255, 255, 100),  # 黄色
    (100, 255, 100),  # 緑
    (100, 200, 255),  # 水色
]

# パドルの設定
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15

# ボールの設定
BALL_SIZE = 12

# ブロックの設定
BLOCK_WIDTH = 58
BLOCK_HEIGHT = 20
BLOCK_ROWS = 5
BLOCK_COLS = 8
BLOCK_MARGIN = 2
BLOCK_TOP_MARGIN = 60


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
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2
        self.dx = 4
        self.dy = -4

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= 0:
            self.rect.left = 0
            self.dx = -self.dx
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dy = -self.dy

    def is_out(self):
        return self.rect.top >= SCREEN_HEIGHT


class Block(pygame.sprite.Sprite):
    """壊されるブロック"""

    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def create_blocks():
    """ブロックを並べて作成する"""
    blocks = pygame.sprite.Group()

    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            # ブロックの位置を計算
            x = col * (BLOCK_WIDTH + BLOCK_MARGIN) + BLOCK_MARGIN
            y = row * (BLOCK_HEIGHT + BLOCK_MARGIN) + BLOCK_TOP_MARGIN

            # 行ごとに色を変える
            color = BLOCK_COLORS[row % len(BLOCK_COLORS)]

            block = Block(x, y, color)
            blocks.add(block)

    return blocks


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ブロック崩し - 04")

    font = pygame.font.Font(None, 48)

    # ゲームオブジェクトを作成
    paddle = Paddle()
    ball = Ball()
    paddle_group = pygame.sprite.Group(paddle)
    ball_group = pygame.sprite.Group(ball)
    block_group = create_blocks()

    clock = pygame.time.Clock()
    game_over = False

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    ball.reset()
                    block_group = create_blocks()
                    game_over = False

        if not game_over:
            paddle_group.update()
            ball_group.update()

            # パドルとの衝突
            if ball.rect.colliderect(paddle.rect):
                ball.rect.bottom = paddle.rect.top
                ball.dy = -abs(ball.dy)

            # ブロックとの衝突
            hit_blocks = pygame.sprite.spritecollide(ball, block_group, True)
            if hit_blocks:
                ball.dy = -ball.dy

            if ball.is_out():
                game_over = True

        # 描画
        screen.fill(BLACK)
        block_group.draw(screen)
        paddle_group.draw(screen)
        ball_group.draw(screen)

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
