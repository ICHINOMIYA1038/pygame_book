import pygame
import sys
import random

TILE_SIZE = 16
MAP_WIDTH = 40
MAP_HEIGHT = 30
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

# マップデータ（W: 壁, F: 床, G: ゴール）
MAP_DATA = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWFFWWWWFFFFFFFFFFFFWWFFFFFFFFFFFFWWFFWW",
    "WWFFWWWWFFFFFFFFFFFFWWFFFFFFFFFFFFWWFFWW",
    "WWFFFFFFWWWWWWFFWWFFFFWWFFWWWWWWFFFFFFWW",
    "WWFFFFFFWWWWWWFFWWFFFFWWFFWWWWWWFFFFFFWW",
    "WWWWWWFFFFFFWWFFFFWWFFWWWWFFFFFFFFWWFFWW",
    "WWWWWWFFFFFFWWFFFFWWFFWWWWFFFFFFFFWWFFWW",
    "WWFFWWWWWWFFFFWWFFWWFFFFWWFFFFWWWWFFFFWW",
    "WWFFWWWWWWFFFFWWFFWWFFFFWWFFFFWWWWFFFFWW",
    "WWFFFFFFFFWWFFWWFFFFWWFFWWFFWWFFFFFFWWWW",
    "WWFFFFFFFFWWFFWWFFFFWWFFWWFFWWFFFFFFWWWW",
    "WWFFWWFFFFFFFFWWFFWWWWFFFFFFWWWWFFWWWWWW",
    "WWFFWWFFFFFFFFWWFFWWWWFFFFFFWWWWFFWWWWWW",
    "WWFFWWFFWWWWWWFFFFFFFFWWWWWWFFFFFFFFWWWW",
    "WWFFWWFFWWWWWWFFFFFFFFWWWWWWFFFFFFFFWWWW",
    "WWWWFFFFWWFFFFFFWWWWFFFFFFFFWWWWWWFFFFWW",
    "WWWWFFFFWWFFFFFFWWWWFFFFFFFFWWWWWWFFFFWW",
    "WWFFFFWWFFWWFFFFWWFFWWWWFFFFFFFFFFWWFFWW",
    "WWFFFFWWFFWWFFFFWWFFWWWWFFFFFFFFFFWWFFWW",
    "WWFFWWFFFFFFFFWWFFFFFFWWFFWWFFWWFFFFFFWW",
    "WWFFWWFFFFFFFFWWFFFFFFWWFFWWFFWWFFFFFFWW",
    "WWFFWWGGWWFFWWFFFFWWFFWWFFFFWWFFWWFFFFWW",
    "WWFFWWGGWWFFWWFFFFWWFFWWFFFFWWFFWWFFFFWW",
    "WWFFWWWWFFWWFFFFWWFFFFFFWWWWFFFFFFFFWWWW",
    "WWFFWWWWFFWWFFFFWWFFFFFFWWWWFFFFFFFFWWWW",
    "WWFFFFFFFFFFFFWWFFFFWWFFFFFFFFWWWWFFFFWW",
    "WWFFFFFFFFFFFFWWFFFFWWFFFFFFFFWWWWFFFFWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 128, 255))  # プレイヤーを示す色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -self.speed
        elif keys[pygame.K_DOWN]:
            dy = self.speed
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        elif keys[pygame.K_RIGHT]:
            dx = self.speed

        # 移動前の位置をバックアップ
        old_x, old_y = self.rect.x, self.rect.y
        
        # 移動してみる
        self.rect.x += dx
        self.rect.y += dy

        # 壁との衝突判定があれば、元の位置に戻す
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x = old_x
                self.rect.y = old_y
                break

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))  # 敵を示す色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_timer = 0
        self.move_interval = 60  # 60フレームごとに方向変更
        self.speed = 2
        # 移動方向 (dx, dy)
        self.dx = 0
        self.dy = 0

    def update(self, walls):
        # 一定間隔でランダムに移動方向を変える
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.dx = random.choice([-1, 0, 1]) * self.speed
            self.dy = random.choice([-1, 0, 1]) * self.speed

        # 移動前の位置を保持
        old_x, old_y = self.rect.x, self.rect.y
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 壁に衝突した場合は元に戻す
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x = old_x
                self.rect.y = old_y
                break

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((50, 50, 50))  # 壁を示す色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 215, 0))  # ゴールを金色で表示
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple RPG Demo")

    def init_game():
        # マップに応じて壁スプライトグループを生成
        wall_group = pygame.sprite.Group()
        # ゴールスプライトグループを生成
        goal_group = pygame.sprite.Group()
        
        for row_idx, row in enumerate(MAP_DATA):
            for col_idx, tile in enumerate(row):
                if tile == "W":  # 壁
                    wall = Wall(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                    wall_group.add(wall)
                elif tile == "G":  # ゴール
                    goal = Goal(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                    goal_group.add(goal)

        # プレイヤーを生成（スタート位置も調整）
        player = Player(2 * TILE_SIZE, 2 * TILE_SIZE)
        player_group = pygame.sprite.Group(player)

        # 敵をいくつか配置（新しいマップサイズに合わせて配置）
        enemy_group = pygame.sprite.Group()
        enemy_positions = [(8, 7), (15, 5), (12, 10)]
        for (ex, ey) in enemy_positions:
            enemy = Enemy(ex * TILE_SIZE, ey * TILE_SIZE)
            enemy_group.add(enemy)

        return wall_group, goal_group, player_group, enemy_group, player

    # ゲーム初期化
    wall_group, goal_group, player_group, enemy_group, player = init_game()
    clock = pygame.time.Clock()
    game_clear = False
    game_over = False

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_clear or game_over):
                    # Rキーでリトライ
                    wall_group, goal_group, player_group, enemy_group, player = init_game()
                    game_clear = False
                    game_over = False

        if not game_clear and not game_over:
            # 更新処理
            player_group.update(wall_group)
            enemy_group.update(wall_group)

        # 描画処理
        screen.fill((0, 0, 0))
        
        # マップ（床）描画
        for row_idx, row in enumerate(MAP_DATA):
            for col_idx, tile in enumerate(row):
                if tile == 'F':
                    pygame.draw.rect(
                        screen,
                        (100, 200, 100),
                        (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )

        wall_group.draw(screen)
        goal_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)

        # ゴール判定
        if pygame.sprite.spritecollide(player, goal_group, False):
            game_clear = True
            font = pygame.font.SysFont(None, 50)
            text = font.render("Game Clear!", True, (255, 255, 255))
            retry_text = font.render("Press R to Retry", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            screen.blit(retry_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 50))
        
        # ゲームオーバー判定
        elif pygame.sprite.spritecollide(player, enemy_group, False):
            game_over = True
            font = pygame.font.SysFont(None, 50)
            text = font.render("Game Over!", True, (255, 255, 255))
            retry_text = font.render("Press R to Retry", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            screen.blit(retry_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 50))
            
        pygame.display.flip()

if __name__ == "__main__":
    main()
