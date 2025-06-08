import pygame
import sys
import random

# タイルサイズ
TILE_SIZE = 32

# マップデータ（W: 壁, F: 床, G: ゴール, C: コイン）
MAP_DATA = [
    "WWWWWWWWW",
    "WFCFFFFFW",
    "WFWWWFWFW",
    "WFCFFFCFW",
    "WFWFWFWFW",
    "WFCFFFGFW",
    "WFWFWFWFW",
    "WFFCFFFFW",
    "WWWWWWWWW",
]

# マップの高さ・幅を MAP_DATA から自動計算
MAP_HEIGHT = len(MAP_DATA)
MAP_WIDTH = len(MAP_DATA[0])

# スクリーンサイズ
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE + 50  # スコア表示用に50ピクセル追加

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
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2))
        self.image.fill((255, 255, 0))  # 黄色いコイン
        self.rect = self.image.get_rect()
        self.rect.x = x + TILE_SIZE//4  # 中央に配置
        self.rect.y = y + TILE_SIZE//4

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4
        self.score = 0  # スコアを追加

    def update(self, walls):
        if not (game_over or game_clear):
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
        if not (game_over or game_clear):
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
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            return True
    return False

def check_game_clear(player, goal):
    return player.rect.colliderect(goal.rect)

def collect_coins(player, coins):
    """コインの収集処理"""
    hits = pygame.sprite.spritecollide(player, coins, True)  # Trueで衝突したコインを消去
    player.score += len(hits) * 100  # 1コイン100点
    return len(hits) > 0

def show_score(screen, score):
    """スコア表示"""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))

def show_game_over(screen, score):
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over', True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
    screen.blit(score_text, score_rect)
    
    retry_text = font.render('Press R to Retry', True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
    screen.blit(retry_text, retry_rect)

def show_game_clear(screen, score):
    font = pygame.font.Font(None, 74)
    text = font.render('Game Clear!', True, (255, 215, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
    screen.blit(score_text, score_rect)
    
    retry_text = font.render('Press R to Retry', True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
    screen.blit(retry_text, retry_rect)

def init_game():
    wall_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    goal_sprite = None
    
    for row_idx, row in enumerate(MAP_DATA):
        for col_idx, tile in enumerate(row):
            if tile == "W":
                wall = Wall(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                wall_group.add(wall)
            elif tile == "G":
                goal_sprite = Goal(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
            elif tile == "C":
                coin = Coin(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                coin_group.add(coin)

    player = Player(TILE_SIZE, TILE_SIZE)
    player_group = pygame.sprite.Group(player)

    enemy_group = pygame.sprite.Group()
    enemy_positions = [(4, 4), (7, 7)]
    for ex, ey in enemy_positions:
        enemy = Enemy(ex * TILE_SIZE, ey * TILE_SIZE)
        enemy_group.add(enemy)

    return wall_group, goal_sprite, player_group, enemy_group, coin_group, player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Demo 07 - スコアとアイテムの実装")

    global game_over, game_clear
    game_over = False
    game_clear = False
    
    wall_group, goal_sprite, player_group, enemy_group, coin_group, player = init_game()
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or game_clear):
                    game_over = False
                    game_clear = False
                    wall_group, goal_sprite, player_group, enemy_group, coin_group, player = init_game()

        if not (game_over or game_clear):
            player_group.update(wall_group)
            enemy_group.update(wall_group)
            
            # コイン収集
            collect_coins(player, coin_group)
            
            if check_game_over(player, enemy_group):
                game_over = True
            elif check_game_clear(player, goal_sprite):
                game_clear = True
                player.score += 1000  # クリアボーナス

        screen.fill((0, 0, 0))

        for row_idx, row in enumerate(MAP_DATA):
            for col_idx, tile in enumerate(row):
                if tile == "F" or tile == "C":  # コインマスも床として描画
                    pygame.draw.rect(
                        screen,
                        (100, 200, 100),
                        (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )

        wall_group.draw(screen)
        coin_group.draw(screen)
        screen.blit(goal_sprite.image, goal_sprite.rect)
        player_group.draw(screen)
        enemy_group.draw(screen)

        # スコア表示
        show_score(screen, player.score)

        if game_over:
            show_game_over(screen, player.score)
        elif game_clear:
            show_game_clear(screen, player.score)

        pygame.display.flip()

if __name__ == "__main__":
    main() 