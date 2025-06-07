import pygame
import sys

# タイルサイズ
TILE_SIZE = 32  # 少し大きめにすると見やすいです

# 小さなマップデータ（W: 壁, F: 床）
MAP_DATA = [
    "WWWWWWWW",
    "WFFFFFFW",
    "WFWWFFFW",
    "WFFFFFFW",
    "WFWWFFFW",
    "WFFFFFFW",
    "WWWWWWWW",
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

        # 移動前の位置を保存
        old_x, old_y = self.rect.x, self.rect.y
        
        # 移動
        self.rect.x += dx
        self.rect.y += dy

        # 壁との衝突があれば元に戻す
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x = old_x
                self.rect.y = old_y
                break

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Demo 01 - 小さなマップでプレイヤー移動")

    # 壁スプライトグループを用意
    wall_group = pygame.sprite.Group()
    for row_idx, row in enumerate(MAP_DATA):
        for col_idx, tile in enumerate(row):
            if tile == "W":
                wall = Wall(col_idx * TILE_SIZE, row_idx * TILE_SIZE)
                wall_group.add(wall)

    # プレイヤーを配置
    # ここでは (1,1) タイル目あたりを開始座標にしています
    player = Player(1 * TILE_SIZE, 1 * TILE_SIZE)
    player_group = pygame.sprite.Group(player)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # プレイヤー更新（壁との当たり判定含む）
        player_group.update(wall_group)

        # 画面クリア（背景を黒で塗りつぶし）
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

        # 壁とプレイヤーの描画
        wall_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
