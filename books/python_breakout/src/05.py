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
GREEN = (100, 255, 100)

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
        self.reset()
        self.speed = 8

    def reset(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30

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

    def __init__(self, x, y, color, points):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points  # このブロックを壊したときの得点


def create_blocks():
    """ブロックを並べて作成する"""
    blocks = pygame.sprite.Group()

    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            x = col * (BLOCK_WIDTH + BLOCK_MARGIN) + BLOCK_MARGIN
            y = row * (BLOCK_HEIGHT + BLOCK_MARGIN) + BLOCK_TOP_MARGIN
            color = BLOCK_COLORS[row % len(BLOCK_COLORS)]
            # 上の行ほど得点が高い
            points = (BLOCK_ROWS - row) * 10
            block = Block(x, y, color, points)
            blocks.add(block)

    return blocks


class Game:
    """ゲーム全体を管理するクラス"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ブロック崩し")

        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        self.clock = pygame.time.Clock()

        self.reset_game()

    def reset_game(self):
        """ゲームを初期状態にリセット"""
        self.paddle = Paddle()
        self.ball = Ball()
        self.paddle_group = pygame.sprite.Group(self.paddle)
        self.ball_group = pygame.sprite.Group(self.ball)
        self.block_group = create_blocks()

        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_clear = False

    def handle_events(self):
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()

    def update(self):
        """ゲームの状態を更新"""
        if self.game_over or self.game_clear:
            return

        self.paddle_group.update()
        self.ball_group.update()

        # パドルとの衝突
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.rect.bottom = self.paddle.rect.top
            self.ball.dy = -abs(self.ball.dy)

            # パドルの当たった位置で角度を変える
            hit_pos = (self.ball.rect.centerx - self.paddle.rect.left) / PADDLE_WIDTH
            self.ball.dx = (hit_pos - 0.5) * 8

        # ブロックとの衝突
        hit_blocks = pygame.sprite.spritecollide(self.ball, self.block_group, True)
        for block in hit_blocks:
            self.score += block.points
        if hit_blocks:
            self.ball.dy = -self.ball.dy

        # ボールが落ちた
        if self.ball.is_out():
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.reset()
                self.paddle.reset()

        # 全ブロック破壊でクリア
        if len(self.block_group) == 0:
            self.game_clear = True

    def draw(self):
        """画面を描画"""
        self.screen.fill(BLACK)

        # ゲームオブジェクトを描画
        self.block_group.draw(self.screen)
        self.paddle_group.draw(self.screen)
        self.ball_group.draw(self.screen)

        # スコアとライフを表示
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))

        # ゲームオーバー表示
        if self.game_over:
            text = self.big_font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

            score_text = self.big_font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(score_text, score_rect)

            restart_text = self.font.render("Press R to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(restart_text, restart_rect)

        # クリア表示
        if self.game_clear:
            text = self.big_font.render("CLEAR!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

            score_text = self.big_font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(score_text, score_rect)

            restart_text = self.font.render("Press R to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """メインループ"""
        while True:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
