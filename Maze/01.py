import pygame
import sys

# タイルサイズ
TILE_SIZE = 48

MAP_HEIGHT = 10
MAP_WIDTH = 10

# 画面サイズ
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 128, 255))  # プレイヤーの色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

    def update(self):
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

        # そのまま移動（壁がないので衝突判定はしない）
        self.rect.x += dx
        self.rect.y += dy

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("移動")

    # プレイヤーを生成
    # 座標(1,1)タイル目の位置に配置する
    player = Player(1 * TILE_SIZE, 1 * TILE_SIZE)
    player_group = pygame.sprite.Group(player)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # プレイヤー更新（壁は無いので引数不要）
        player_group.update()

        # 背景クリア（黒で塗りつぶし）
        screen.fill((0, 0, 0))
        # プレイヤーの描画
        player_group.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
