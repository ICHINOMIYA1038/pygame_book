import pygame
import sys
import random
import os
import math

# サウンドファイルのパスを設定
SOUND_DIR = "assets/sounds"
if not os.path.exists(SOUND_DIR):
    os.makedirs(SOUND_DIR)

# タイルサイズ
TILE_SIZE = 48

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
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE + 50

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'coin': pygame.mixer.Sound(os.path.join(SOUND_DIR, 'coin.wav')),
            'gameover': pygame.mixer.Sound(os.path.join(SOUND_DIR, 'gameover.wav')),
            'clear': pygame.mixer.Sound(os.path.join(SOUND_DIR, 'clear.wav'))
        }
        # BGMの設定
        pygame.mixer.music.load(os.path.join(SOUND_DIR, 'bgm.wav'))
        pygame.mixer.music.set_volume(0.5)
        
    def play_sound(self, sound_name):
        self.sounds[sound_name].play()
        
    def play_bgm(self):
        pygame.mixer.music.play(-1)  # -1で無限ループ
        
    def stop_bgm(self):
        pygame.mixer.music.stop()

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [random.randint(-2, 2), random.randint(-2, 2)]
        self.lifetime = 30  # フレーム数でパーティクルの寿命を設定

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

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
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x + TILE_SIZE//4
        self.rect.y = y + TILE_SIZE//4
        self.initial_y = self.rect.y  # 初期Y座標を保存
        self.animation_frame = 0

    def update(self):
        # コインのアニメーション（上下に浮かぶような動き）
        self.animation_frame = (self.animation_frame + 1) % 60
        offset = abs(math.sin(self.animation_frame * 0.1)) * 5
        self.rect.y = self.initial_y + offset

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4
        self.score = 0

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

def create_particle_effect(x, y, color, particle_group):
    """パーティクルエフェクトを生成"""
    for _ in range(10):  # 10個のパーティクルを生成
        particle = ParticleEffect(x, y, color)
        particle_group.add(particle)

def collect_coins(player, coins, sound_manager, particle_group):
    """コインの収集処理"""
    hits = pygame.sprite.spritecollide(player, coins, True)
    if hits:
        sound_manager.play_sound('coin')
        for coin in hits:
            create_particle_effect(coin.rect.centerx, coin.rect.centery, (255, 255, 0), particle_group)
        player.score += len(hits) * 100
    return len(hits) > 0

def check_game_over(player, enemies):
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            return True
    return False

def check_game_clear(player, goal):
    return player.rect.colliderect(goal.rect)

def show_score(screen, score):
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
    particle_group = pygame.sprite.Group()
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

    return wall_group, goal_sprite, player_group, enemy_group, coin_group, particle_group, player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Demo 08 - サウンドとエフェクトの実装")

    # サウンドマネージャーの初期化
    sound_manager = SoundManager()
    sound_manager.play_bgm()

    global game_over, game_clear
    game_over = False
    game_clear = False
    
    wall_group, goal_sprite, player_group, enemy_group, coin_group, particle_group, player = init_game()
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
                    wall_group, goal_sprite, player_group, enemy_group, coin_group, particle_group, player = init_game()
                    sound_manager.play_bgm()

        if not (game_over or game_clear):
            player_group.update(wall_group)
            enemy_group.update(wall_group)
            coin_group.update()
            particle_group.update()
            
            collect_coins(player, coin_group, sound_manager, particle_group)
            
            if check_game_over(player, enemy_group):
                game_over = True
                sound_manager.play_sound('gameover')
                sound_manager.stop_bgm()
            elif check_game_clear(player, goal_sprite):
                game_clear = True
                sound_manager.play_sound('clear')
                sound_manager.stop_bgm()
                player.score += 1000

        screen.fill((0, 0, 0))

        for row_idx, row in enumerate(MAP_DATA):
            for col_idx, tile in enumerate(row):
                if tile == "F" or tile == "C":
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
        particle_group.draw(screen)

        show_score(screen, player.score)

        if game_over:
            show_game_over(screen, player.score)
        elif game_clear:
            show_game_clear(screen, player.score)

        pygame.display.flip()

if __name__ == "__main__":
    main() 