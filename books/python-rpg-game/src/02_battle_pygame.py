"""
第2章：敵があらわれた！ - スライムとたたかおう（pygame版）
"""
import pygame
import random
from game_utils import GameBase, WHITE, BLACK, BLUE, GREEN, RED, YELLOW, GRAY

class BattleGame(GameBase):
    def __init__(self):
        super().__init__("RPGゲーム - スライムとたたかおう！")
        
        # ゲームの状態
        self.state = "NAME_INPUT"  # NAME_INPUT, BATTLE, VICTORY, GAME_OVER
        
        # 勇者のステータス
        self.hero_name = ""
        self.hero_hp = 100
        self.hero_max_hp = 100
        self.hero_attack = 15
        
        # 敵のステータス
        self.enemy_name = "スライム"
        self.enemy_hp = 30
        self.enemy_max_hp = 30
        self.enemy_attack = 5
        
        # バトル関連
        self.selected_action = 0  # 0:こうげき, 1:にげる
        self.message_queue = []
        self.message_timer = 0
        self.turn_phase = "SELECT"  # SELECT, HERO_ACTION, ENEMY_ACTION, CHECK
        
        # アニメーション
        self.hero_x = 200
        self.hero_y = 300
        self.enemy_x = 600
        self.enemy_y = 300
        self.shake_timer = 0
        self.shake_target = None  # "hero" or "enemy"
        
        # エフェクト
        self.effects = []  # [(type, x, y, timer)]
        
        # 簡易名前入力
        self.input_text = ""
        self.input_active = True
    
    def reset_battle(self):
        """バトルをリセット"""
        self.hero_hp = self.hero_max_hp
        self.enemy_hp = self.enemy_max_hp
        self.selected_action = 0
        self.message_queue = [f"{self.enemy_name}があらわれた！"]
        self.turn_phase = "SELECT"
        self.effects = []
    
    def on_event(self, event):
        """イベント処理"""
        if self.state == "NAME_INPUT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.input_text:
                    self.hero_name = self.input_text
                    self.state = "BATTLE"
                    self.reset_battle()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    if len(self.input_text) < 20:
                        self.input_text += event.unicode
        
        elif self.state == "BATTLE":
            if self.turn_phase == "SELECT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.selected_action = 1 - self.selected_action
                    elif event.key == pygame.K_RETURN:
                        self.execute_action()
        
        elif self.state in ["VICTORY", "GAME_OVER"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = "BATTLE"
                    self.reset_battle()
                elif event.key == pygame.K_q:
                    self.running = False
    
    def execute_action(self):
        """選択したアクションを実行"""
        if self.selected_action == 0:  # こうげき
            damage = random.randint(self.hero_attack - 5, self.hero_attack + 5)
            self.enemy_hp -= damage
            self.message_queue = [
                f"{self.hero_name}のこうげき！",
                f"{self.enemy_name}に{damage}のダメージ！"
            ]
            self.shake_target = "enemy"
            self.shake_timer = 20
            self.add_effect("slash", self.enemy_x, self.enemy_y)
            self.turn_phase = "HERO_ACTION"
        
        elif self.selected_action == 1:  # にげる
            self.message_queue = [f"{self.hero_name}はにげだした！"]
            self.state = "GAME_OVER"
    
    def enemy_turn(self):
        """敵のターン"""
        damage = random.randint(self.enemy_attack - 2, self.enemy_attack + 2)
        self.hero_hp -= damage
        self.message_queue = [
            f"{self.enemy_name}のこうげき！",
            f"{self.hero_name}に{damage}のダメージ！"
        ]
        self.shake_target = "hero"
        self.shake_timer = 20
        self.add_effect("hit", self.hero_x, self.hero_y)
        self.turn_phase = "ENEMY_ACTION"
    
    def add_effect(self, effect_type, x, y):
        """エフェクトを追加"""
        self.effects.append({
            "type": effect_type,
            "x": x,
            "y": y,
            "timer": 30
        })
    
    def update(self):
        """更新処理"""
        if self.state == "BATTLE":
            # メッセージタイマー
            if self.message_timer > 0:
                self.message_timer -= 1
                if self.message_timer == 0:
                    # 次のフェーズへ
                    if self.turn_phase == "HERO_ACTION":
                        if self.enemy_hp <= 0:
                            self.message_queue.append(f"{self.enemy_name}をたおした！")
                            self.state = "VICTORY"
                        else:
                            self.enemy_turn()
                            self.message_timer = 60
                    elif self.turn_phase == "ENEMY_ACTION":
                        if self.hero_hp <= 0:
                            self.message_queue.append(f"{self.hero_name}はたおれてしまった...")
                            self.state = "GAME_OVER"
                        else:
                            self.turn_phase = "SELECT"
            
            # アクション実行後のタイマー開始
            elif self.turn_phase in ["HERO_ACTION", "ENEMY_ACTION"]:
                self.message_timer = 60
        
        # 画面の揺れ
        if self.shake_timer > 0:
            self.shake_timer -= 1
        
        # エフェクトの更新
        self.effects = [e for e in self.effects if e["timer"] > 0]
        for effect in self.effects:
            effect["timer"] -= 1
    
    def draw(self):
        """描画処理"""
        # 背景
        self.screen.fill(BLACK)
        self.draw_battle_background()
        
        if self.state == "NAME_INPUT":
            self.draw_name_input()
        elif self.state in ["BATTLE", "VICTORY", "GAME_OVER"]:
            self.draw_battle_screen()
    
    def draw_battle_background(self):
        """バトル背景を描画"""
        # グリッド模様
        for x in range(0, 800, 50):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, 600))
        for y in range(0, 600, 50):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (800, y))
    
    def draw_name_input(self):
        """名前入力画面"""
        self.draw_text("勇者の名前を入力してください", 400, 200, WHITE, 
                      self.font_jp_large, center=True, use_jp=True)
        
        # 入力欄
        input_rect = pygame.Rect(250, 250, 300, 50)
        pygame.draw.rect(self.screen, WHITE, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 3)
        
        # 入力テキスト
        self.draw_text(self.input_text, 260, 265, BLACK, self.font_large)
        
        # カーソル
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = 260 + self.font_large.size(self.input_text)[0]
            pygame.draw.line(self.screen, BLACK, (cursor_x, 260), (cursor_x, 290), 2)
        
        self.draw_text("Enterキーで決定", 400, 350, GRAY, 
                      self.font_jp_medium, center=True, use_jp=True)
    
    def draw_battle_screen(self):
        """バトル画面"""
        # ステータスバー
        self.draw_status_bar(self.hero_name, self.hero_hp, self.hero_max_hp, 0, 0, x=10, y=10)
        self.draw_enemy_status_bar()
        
        # キャラクター
        self.draw_hero()
        self.draw_enemy()
        
        # エフェクト
        self.draw_effects()
        
        # メッセージボックス
        self.draw_message_box(self.message_queue)
        
        # コマンドメニュー
        if self.state == "BATTLE" and self.turn_phase == "SELECT":
            self.draw_command_menu()
        
        # 結果表示
        if self.state == "VICTORY":
            self.draw_victory_screen()
        elif self.state == "GAME_OVER":
            self.draw_game_over_screen()
    
    def draw_enemy_status_bar(self):
        """敵のステータスバー"""
        x = 490
        y = 10
        self.draw_rect(x, y, 300, 80, (40, 40, 40))
        self.draw_rect(x, y, 300, 80, WHITE, 2)
        
        # 名前
        self.draw_text(self.enemy_name, x + 10, y + 10, WHITE, use_jp=True)
        
        # HPバー
        hp_ratio = self.enemy_hp / self.enemy_max_hp if self.enemy_max_hp > 0 else 0
        self.draw_text("HP:", x + 10, y + 40, WHITE)
        self.draw_rect(x + 50, y + 40, 200, 20, (40, 40, 40))
        self.draw_rect(x + 50, y + 40, int(200 * hp_ratio), 20, RED)
        self.draw_rect(x + 50, y + 40, 200, 20, WHITE, 2)
        self.draw_text(f"{self.enemy_hp}/{self.enemy_max_hp}", x + 260, y + 40, WHITE)
    
    def draw_hero(self):
        """勇者を描画"""
        x = self.hero_x
        y = self.hero_y
        
        # 画面の揺れ
        if self.shake_target == "hero" and self.shake_timer > 0:
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
        
        # 体
        pygame.draw.rect(self.screen, BLUE, (x - 25, y - 25, 50, 50))
        pygame.draw.rect(self.screen, WHITE, (x - 25, y - 25, 50, 50), 2)
        
        # 顔
        pygame.draw.circle(self.screen, (255, 220, 177), (x, y - 35), 15)
        pygame.draw.circle(self.screen, BLACK, (x, y - 35), 15, 2)
        
        # 目
        pygame.draw.circle(self.screen, BLACK, (x - 5, y - 38), 2)
        pygame.draw.circle(self.screen, BLACK, (x + 5, y - 38), 2)
        
        # 剣
        pygame.draw.line(self.screen, (192, 192, 192), 
                        (x + 25, y - 10), (x + 35, y - 30), 3)
        pygame.draw.circle(self.screen, (139, 69, 19), (x + 25, y - 10), 5)
    
    def draw_enemy(self):
        """敵（スライム）を描画"""
        x = self.enemy_x
        y = self.enemy_y
        
        # 画面の揺れ
        if self.shake_target == "enemy" and self.shake_timer > 0:
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
        
        # スライムの体
        points = []
        for angle in range(0, 360, 30):
            rad = angle * 3.14159 / 180
            radius = 40 + random.randint(-5, 5)
            px = x + radius * pygame.math.cos(rad)
            py = y + radius * pygame.math.sin(rad) * 0.8  # 縦に少し潰す
            points.append((px, py))
        
        pygame.draw.polygon(self.screen, GREEN, points)
        pygame.draw.polygon(self.screen, (0, 150, 0), points, 2)
        
        # 目
        pygame.draw.circle(self.screen, BLACK, (x - 10, y - 10), 5)
        pygame.draw.circle(self.screen, BLACK, (x + 10, y - 10), 5)
        pygame.draw.circle(self.screen, WHITE, (x - 8, y - 12), 2)
        pygame.draw.circle(self.screen, WHITE, (x + 12, y - 12), 2)
    
    def draw_effects(self):
        """エフェクトを描画"""
        for effect in self.effects:
            alpha = effect["timer"] / 30.0
            
            if effect["type"] == "slash":
                # 斬撃エフェクト
                for i in range(3):
                    start_x = effect["x"] - 30 + i * 20
                    start_y = effect["y"] - 30
                    end_x = effect["x"] + 30 - i * 20
                    end_y = effect["y"] + 30
                    color = (255, int(255 * alpha), int(255 * alpha))
                    pygame.draw.line(self.screen, color, 
                                   (start_x, start_y), (end_x, end_y), 3)
            
            elif effect["type"] == "hit":
                # ヒットエフェクト
                radius = int(20 * (1 - alpha))
                color = (255, int(200 * alpha), 0)
                pygame.draw.circle(self.screen, color, 
                                 (int(effect["x"]), int(effect["y"])), radius, 3)
    
    def draw_command_menu(self):
        """コマンドメニュー"""
        menu_x = 50
        menu_y = 450
        menu_width = 200
        
        commands = ["こうげき", "にげる"]
        for i, command in enumerate(commands):
            y = menu_y + i * 40
            
            # 選択中の項目はハイライト
            if i == self.selected_action:
                pygame.draw.rect(self.screen, BLUE, 
                               (menu_x - 5, y - 5, menu_width + 10, 35))
            
            self.draw_rect(menu_x, y, menu_width, 30, GRAY)
            self.draw_rect(menu_x, y, menu_width, 30, WHITE, 2)
            self.draw_text(command, menu_x + menu_width // 2, y + 15, 
                          WHITE, self.font_jp_medium, center=True, use_jp=True)
    
    def draw_victory_screen(self):
        """勝利画面"""
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        self.draw_text("VICTORY!", 400, 250, YELLOW, self.font_xlarge, center=True)
        self.draw_text("戦闘に勝利しました！", 400, 320, WHITE, 
                      self.font_jp_large, center=True, use_jp=True)
        self.draw_text("Rキーでもう一度 / Qキーで終了", 400, 400, GRAY, 
                      self.font_jp_medium, center=True, use_jp=True)
    
    def draw_game_over_screen(self):
        """ゲームオーバー画面"""
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        self.draw_text("GAME OVER", 400, 250, RED, self.font_xlarge, center=True)
        self.draw_text("Rキーでもう一度 / Qキーで終了", 400, 350, GRAY, 
                      self.font_jp_medium, center=True, use_jp=True)

def main():
    game = BattleGame()
    game.run()

if __name__ == "__main__":
    main()