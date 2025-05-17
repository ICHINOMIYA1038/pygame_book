import pygame
import sys
import random

# タイルサイズ
TILE_SIZE = 32

# マップデータ（W: 壁, F: 床）
MAP_DATA = [
    "WWWWWWWWW",
    "WFFFFFFFW",
    "WFWWWFWFW",
    "WFFFFFFFW",
    "WFWFWFWFW",
    "WFFFFFFFW",
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
        self.image.fill((50, 50, 50))  # 壁を示す色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.image.fill((255, 0, 0))  # 敵を赤色で表示
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.move_timer = 0
        self.move_interval = 60  # 60フレームごとに方向変更

    def update(self, walls):
        # 一定間隔で移動方向をランダムに変更
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            dx = random.choice([-1, 0, 1]) * self.speed
            dy = random.choice([-1, 0, 1]) * self.speed
            
            # 移動前の位置を保存
            old_x, old_y = self.rect.x, self.rect.y
            self.rect.x += dx
            self.rect.y += dy

            # 壁との衝突判定
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.x = old_x
                    self.rect.y = old_y
                    break

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Demo 04 - 敵の実装")

    # 壁スプライトグループを用意
    wall_group = pygame.sprite.Group()
    for row_idx, row in enumerate(MAP_DATA):
        for col_idx, tile in enumerate(row):
            if tile == "W":
                wall = Wall(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                wall_group.add(wall)

    # プレイヤーを配置
    player = Player(TILE_SIZE, TILE_SIZE)
    player_group = pygame.sprite.Group(player)

    # 敵を配置
    enemy_group = pygame.sprite.Group()
    enemy_positions = [(4, 4), (7, 7)]  # 敵の初期位置
    for ex, ey in enemy_positions:
        enemy = Enemy(ex * TILE_SIZE, ey * TILE_SIZE)
        enemy_group.add(enemy)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # プレイヤーと敵の更新
        player_group.update(wall_group)
        enemy_group.update(wall_group)

        # 画面クリア
        screen.fill((0, 0, 0))

        # 床（F）のタイルを描画
        for row_idx, row in enumerate(MAP_DATA):
            for col_idx, tile in enumerate(row):
                if tile == "F":
                    pygame.draw.rect(
                        screen,
                        (100, 200, 100),
                        (col_idx * TILE_SIZE, row_idx * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )

        # 壁、プレイヤー、敵の描画
        wall_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main() 