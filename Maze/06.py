import pygame
import sys
import random

# タイルサイズ
TILE_SIZE = 32

# マップデータ（W: 壁, F: 床, G: ゴール）
MAP_DATA = [
    "WWWWWWWWW",
    "WFFFFFFFW",
    "WFWWWFWFW",
    "WFFFFFFFW",
    "WFWFWFWFW",
    "WFFFFFFGW",
    "WFWFWFWFW",
    "WFFFFFFFW",
    "WWWWWWWWW",
]

# マップの高さ・幅を MAP_DATA から自動計算
MAP_HEIGHT = len(MAP_DATA)
MAP_WIDTH = len(MAP_DATA[0])

# スクリーンサイズ
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((50, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 215, 0))  # 金色でゴールを表示
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

    def update(self, walls):
        if not (game_over or game_clear):  # ゲームオーバーまたはクリアでない場合のみ移動可能
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

            old_x, old_y = self.rect.x, self.rect.y
            self.rect.x += dx
            self.rect.y += dy

            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.x = old_x
                    self.rect.y = old_y
                    break

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.move_timer = 0
        self.move_interval = 60

    def update(self, walls):
        if not (game_over or game_clear):  # ゲームオーバーまたはクリアでない場合のみ移動
            self.move_timer += 1
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                dx = random.choice([-1, 0, 1]) * self.speed
                dy = random.choice([-1, 0, 1]) * self.speed
                
                old_x, old_y = self.rect.x, self.rect.y
                self.rect.x += dx
                self.rect.y += dy

                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        self.rect.x = old_x
                        self.rect.y = old_y
                        break

def check_game_over(player, enemies):
    """プレイヤーと敵の衝突判定"""
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            return True
    return False

def check_game_clear(player, goal):
    """プレイヤーとゴールの衝突判定"""
    return player.rect.colliderect(goal.rect)

def show_game_over(screen):
    """ゲームオーバー表示"""
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over', True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 36)
    retry_text = font.render('Press R to Retry', True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
    screen.blit(retry_text, retry_rect)

def show_game_clear(screen):
    """ゲームクリア表示"""
    font = pygame.font.Font(None, 74)
    text = font.render('Game Clear!', True, (255, 215, 0))  # 金色でクリアを表示
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 36)
    retry_text = font.render('Press R to Retry', True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
    screen.blit(retry_text, retry_rect)

def init_game():
    """ゲーム状態の初期化"""
    # 壁とゴールの生成
    wall_group = pygame.sprite.Group()
    goal_sprite = None
    
    for row_idx, row in enumerate(MAP_DATA):
        for col_idx, tile in enumerate(row):
            if tile == "W":
                wall = Wall(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                wall_group.add(wall)
            elif tile == "G":
                goal_sprite = Goal(col_idx * TILE_SIZE, row_idx * TILE_SIZE)

    # プレイヤーの生成
    player = Player(TILE_SIZE, TILE_SIZE)
    player_group = pygame.sprite.Group(player)

    # 敵の生成
    enemy_group = pygame.sprite.Group()
    enemy_positions = [(4, 4), (7, 7)]
    for ex, ey in enemy_positions:
        enemy = Enemy(ex * TILE_SIZE, ey * TILE_SIZE)
        enemy_group.add(enemy)

    return wall_group, goal_sprite, player_group, enemy_group, player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Demo 06 - ゴールとクリア判定の実装")

    global game_over, game_clear
    game_over = False
    game_clear = False
    
    # ゲーム初期化
    wall_group, goal_sprite, player_group, enemy_group, player = init_game()
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or game_clear):
                    # Rキーでリトライ
                    game_over = False
                    game_clear = False
                    wall_group, goal_sprite, player_group, enemy_group, player = init_game()

        if not (game_over or game_clear):
            # 更新処理
            player_group.update(wall_group)
            enemy_group.update(wall_group)
            
            # ゲームオーバー判定
            if check_game_over(player, enemy_group):
                game_over = True
            # ゲームクリア判定
            elif check_game_clear(player, goal_sprite):
                game_clear = True

        # 描画処理
        screen.fill((0, 0, 0))

        # 床の描画
        for row_idx, row in enumerate(MAP_DATA):
            for col_idx, tile in enumerate(row):
                if tile == "F":
                    pygame.draw.rect(
                        screen,
                        (100, 200, 100),
                        (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )

        # スプライトの描画
        wall_group.draw(screen)
        screen.blit(goal_sprite.image, goal_sprite.rect)  # ゴールの描画
        player_group.draw(screen)
        enemy_group.draw(screen)

        # ゲームオーバー/クリア表示
        if game_over:
            show_game_over(screen)
        elif game_clear:
            show_game_clear(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main() 