"""
第1章：はじめてのRPGゲーム - 勇者の名前を決めよう！（pygame版）
"""
import pygame
from game_utils import GameBase, TextInput, WHITE, BLACK, BLUE, GREEN

class RPGStart(GameBase):
    def __init__(self):
        super().__init__("RPGゲーム - 勇者の名前を決めよう！")
        
        # ゲームの状態
        self.state = "NAME_INPUT"  # NAME_INPUT, SHOW_STATUS
        
        # テキスト入力
        self.name_input = TextInput(250, 250, 300, 40)
        self.name_input.active = True
        
        # 勇者のステータス
        self.hero_name = ""
        self.hero_hp = 100
        self.hero_mp = 20
        self.hero_attack = 15
        self.hero_defense = 10
        
        # アニメーション用
        self.hero_y = 300
        self.hero_y_speed = 0.5
        self.hero_y_direction = 1
    
    def on_event(self, event):
        """イベント処理"""
        if self.state == "NAME_INPUT":
            # 名前入力
            if self.name_input.handle_event(event):
                if self.name_input.text.strip():
                    self.hero_name = self.name_input.text.strip()
                    self.state = "SHOW_STATUS"
        
        elif self.state == "SHOW_STATUS":
            # ステータス表示中
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # リセット
                    self.state = "NAME_INPUT"
                    self.name_input.text = ""
                    self.name_input.active = True
    
    def update(self):
        """更新処理"""
        if self.state == "NAME_INPUT":
            self.name_input.update()
        
        # 勇者のアニメーション
        self.hero_y += self.hero_y_speed * self.hero_y_direction
        if self.hero_y > 310 or self.hero_y < 290:
            self.hero_y_direction *= -1
    
    def draw(self):
        """描画処理"""
        # 背景
        self.screen.fill(BLACK)
        
        # 背景の装飾
        for i in range(0, 800, 100):
            for j in range(0, 600, 100):
                pygame.draw.circle(self.screen, (20, 20, 40), (i + 50, j + 50), 30, 1)
        
        if self.state == "NAME_INPUT":
            self.draw_name_input_screen()
        elif self.state == "SHOW_STATUS":
            self.draw_status_screen()
    
    def draw_name_input_screen(self):
        """名前入力画面の描画"""
        # タイトル
        self.draw_text("RPG GAME", 400, 100, WHITE, self.font_xlarge, center=True)
        self.draw_text("へようこそ！", 400, 150, WHITE, self.font_jp_large, center=True, use_jp=True)
        
        # 説明
        self.draw_text("あなたの名前を教えてください", 400, 220, WHITE, 
                      self.font_jp_medium, center=True, use_jp=True)
        
        # 名前入力欄
        self.name_input.draw(self.screen)
        
        # ヒント
        self.draw_text("名前を入力してEnterキーを押してください", 400, 320, 
                      (150, 150, 150), self.font_jp_small, center=True, use_jp=True)
        
        # 勇者のプレビュー（簡易的なキャラクター）
        self.draw_hero_sprite(400, 400)
    
    def draw_status_screen(self):
        """ステータス表示画面の描画"""
        # タイトル
        self.draw_text("勇者のステータス", 400, 50, WHITE, 
                      self.font_jp_large, center=True, use_jp=True)
        
        # 勇者のスプライト
        self.draw_hero_sprite(200, int(self.hero_y), size=100)
        
        # ステータス枠
        status_x = 350
        status_y = 150
        self.draw_rect(status_x - 20, status_y - 20, 400, 300, (40, 40, 40))
        self.draw_rect(status_x - 20, status_y - 20, 400, 300, WHITE, 2)
        
        # ステータス表示
        stats = [
            ("名前", self.hero_name),
            ("HP", f"{self.hero_hp}"),
            ("MP", f"{self.hero_mp}"),
            ("こうげき力", f"{self.hero_attack}"),
            ("ぼうぎょ力", f"{self.hero_defense}"),
        ]
        
        for i, (label, value) in enumerate(stats):
            y = status_y + i * 50
            self.draw_text(label + "：", status_x, y, (200, 200, 200), 
                          self.font_jp_medium, use_jp=True)
            self.draw_text(value, status_x + 150, y, WHITE, self.font_large)
        
        # メッセージ
        self.draw_text(f"{self.hero_name}さん、", 400, 480, GREEN, 
                      self.font_jp_medium, center=True, use_jp=True)
        self.draw_text("ぼうけんの準備ができました！", 400, 510, GREEN, 
                      self.font_jp_medium, center=True, use_jp=True)
        
        # 操作説明
        self.draw_text("Rキーでやり直し", 400, 560, (150, 150, 150), 
                      self.font_jp_small, center=True, use_jp=True)
    
    def draw_hero_sprite(self, x, y, size=50):
        """勇者のスプライト（簡易版）を描画"""
        # 体
        body_rect = pygame.Rect(x - size//2, y - size//2, size, size)
        pygame.draw.rect(self.screen, BLUE, body_rect)
        pygame.draw.rect(self.screen, WHITE, body_rect, 2)
        
        # 顔
        face_size = size // 3
        face_rect = pygame.Rect(x - face_size//2, y - size//2 - face_size//2, 
                               face_size, face_size)
        pygame.draw.circle(self.screen, (255, 220, 177), 
                          (x, y - size//2), face_size//2)
        pygame.draw.circle(self.screen, BLACK, 
                          (x, y - size//2), face_size//2, 2)
        
        # 目
        eye_size = 3
        pygame.draw.circle(self.screen, BLACK, 
                          (x - face_size//4, y - size//2 - 5), eye_size)
        pygame.draw.circle(self.screen, BLACK, 
                          (x + face_size//4, y - size//2 - 5), eye_size)
        
        # 剣
        sword_start = (x + size//2, y - size//4)
        sword_end = (x + size//2 + 20, y - size//2 - 20)
        pygame.draw.line(self.screen, (192, 192, 192), sword_start, sword_end, 3)
        # 剣の柄
        pygame.draw.circle(self.screen, (139, 69, 19), sword_start, 5)

def main():
    game = RPGStart()
    game.run()

if __name__ == "__main__":
    main()