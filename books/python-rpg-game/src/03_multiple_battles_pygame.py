"""
第3章：れんぞくバトル！ - 複数の敵とたたかおう（pygame版）
"""
import pygame
import random
import math
from game_utils import GameBase, WHITE, BLACK, BLUE, GREEN, RED, YELLOW, GRAY, DARK_GRAY

class Hero:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.mp = 20
        self.max_mp = 20
        self.attack = 15
        self.exp = 0

class Enemy:
    def __init__(self, name, hp, attack, exp, color):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.exp = exp
        self.color = color

class MultipleBattleGame(GameBase):
    def __init__(self):
        super().__init__("RPGゲーム - 連続バトル！")
        
        # ゲームの状態
        self.state = "NAME_INPUT"
        
        # 勇者
        self.hero = None
        
        # 敵のリスト
        self.enemy_list = [
            Enemy("スライム", 30, 5, 10, GREEN),
            Enemy("ゴブリン", 50, 8, 20, (139, 69, 19)),
            Enemy("オーク", 80, 12, 35, (100, 50, 30))
        ]
        self.current_enemy_index = 0
        self.current_enemy = None
        
        # バトル関連
        self.selected_action = 0
        self.message_queue = []
        self.message_timer = 0
        self.turn_phase = "SELECT"
        
        # アニメーション
        self.hero_x = 200
        self.hero_y = 300
        self.enemy_x = 600
        self.enemy_y = 300
        self.shake_timer = 0
        self.shake_target = None
        
        # エフェクト
        self.effects = []
        
        # 入力
        self.input_text = ""
        
        # バトル間の回復表示
        self.show_recovery = False
        self.recovery_timer = 0
    
    def start_new_battle(self):
        """新しいバトルを開始"""
        if self.current_enemy_index < len(self.enemy_list):
            self.current_enemy = self.enemy_list[self.current_enemy_index]
            self.message_queue = [f"{self.current_enemy.name}があらわれた！"]
            self.turn_phase = "SELECT"
            self.selected_action = 0
            self.effects = []
            self.shake_timer = 0
    
    def on_event(self, event):
        """イベント処理"""
        if self.state == "NAME_INPUT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.input_text:
                    self.hero = Hero(self.input_text)
                    self.state = "INTRO"
                    self.message_queue = [
                        f"{self.hero.name}のぼうけんが始まります！",
                        "3体の敵を倒そう！"
                    ]
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    if len(self.input_text) < 20:
                        self.input_text += event.unicode
        
        elif self.state == "INTRO":
            if event.type == pygame.KEYDOWN:
                self.state = "BATTLE"
                self.start_new_battle()
        
        elif self.state == "BATTLE":
            if self.turn_phase == "SELECT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.selected_action = 1 - self.selected_action
                    elif event.key == pygame.K_RETURN:
                        self.execute_action()
        
        elif self.state == "BATTLE_END":
            if event.type == pygame.KEYDOWN and self.recovery_timer <= 0:
                self.current_enemy_index += 1
                if self.current_enemy_index < len(self.enemy_list):
                    # 次のバトルへ
                    self.state = "BATTLE"
                    self.start_new_battle()
                    # 回復
                    self.hero.hp = min(self.hero.hp + 20, self.hero.max_hp)
                    self.show_recovery = True
                    self.recovery_timer = 60
                else:
                    # すべての敵を倒した
                    self.state = "ALL_CLEAR"
        
        elif self.state in ["ALL_CLEAR", "GAME_OVER"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.__init__()
                elif event.key == pygame.K_q:
                    self.running = False
    
    def execute_action(self):
        """アクションを実行"""
        if self.selected_action == 0:  # こうげき
            damage = random.randint(self.hero.attack - 5, self.hero.attack + 5)
            self.current_enemy.hp -= damage
            self.message_queue = [
                f"{self.hero.name}のこうげき！",
                f"{self.current_enemy.name}に{damage}のダメージ！"
            ]
            self.shake_target = "enemy"
            self.shake_timer = 20
            self.add_effect("slash", self.enemy_x, self.enemy_y)
            self.turn_phase = "HERO_ACTION"
        
        elif self.selected_action == 1:  # にげる
            self.message_queue = [f"{self.hero.name}はにげだした！"]
            self.state = "GAME_OVER"
    
    def enemy_turn(self):
        """敵のターン"""
        damage = random.randint(self.current_enemy.attack - 2, self.current_enemy.attack + 2)
        self.hero.hp -= damage
        self.message_queue = [
            f"{self.current_enemy.name}のこうげき！",
            f"{self.hero.name}に{damage}のダメージ！"
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
                    if self.turn_phase == "HERO_ACTION":
                        if self.current_enemy.hp <= 0:
                            self.message_queue.append(f"{self.current_enemy.name}をたおした！")
                            self.message_queue.append(f"{self.current_enemy.exp}の経験値を手に入れた！")
                            self.hero.exp += self.current_enemy.exp
                            self.state = "BATTLE_END"
                        else:
                            self.enemy_turn()
                            self.message_timer = 60
                    elif self.turn_phase == "ENEMY_ACTION":
                        if self.hero.hp <= 0:
                            self.message_queue.append(f"{self.hero.name}はたおれてしまった...")
                            self.state = "GAME_OVER"
                        else:
                            self.turn_phase = "SELECT"
            
            elif self.turn_phase in ["HERO_ACTION", "ENEMY_ACTION"]:
                self.message_timer = 60
        
        # 回復表示タイマー
        if self.recovery_timer > 0:
            self.recovery_timer -= 1
        
        # 画面の揺れ
        if self.shake_timer > 0:
            self.shake_timer -= 1
        
        # エフェクトの更新
        self.effects = [e for e in self.effects if e["timer"] > 0]
        for effect in self.effects:
            effect["timer"] -= 1
    
    def draw(self):
        """描画処理"""
        self.screen.fill(BLACK)
        self.draw_background()
        
        if self.state == "NAME_INPUT":
            self.draw_name_input()
        elif self.state == "INTRO":
            self.draw_intro()
        elif self.state in ["BATTLE", "BATTLE_END"]:
            self.draw_battle()
        elif self.state == "ALL_CLEAR":
            self.draw_all_clear()
        elif self.state == "GAME_OVER":
            self.draw_game_over()
    
    def draw_background(self):
        """背景描画"""
        for i in range(0, 800, 50):
            for j in range(0, 600, 50):
                color = (20, 20, 30) if (i + j) // 50 % 2 == 0 else (15, 15, 25)
                pygame.draw.rect(self.screen, color, (i, j, 50, 50))
    
    def draw_name_input(self):
        """名前入力画面"""
        self.draw_text("勇者の名前を入力してください", 400, 200, WHITE,
                      self.font_jp_large, center=True, use_jp=True)
        
        # 入力欄
        input_rect = pygame.Rect(250, 250, 300, 50)
        pygame.draw.rect(self.screen, WHITE, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 3)
        
        self.draw_text(self.input_text, 260, 265, BLACK, self.font_large)
        
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = 260 + self.font_large.size(self.input_text)[0]
            pygame.draw.line(self.screen, BLACK, (cursor_x, 260), (cursor_x, 290), 2)
    
    def draw_intro(self):
        """イントロ画面"""
        self.draw_message_box(self.message_queue)
        self.draw_text("何かキーを押してください", 400, 500, GRAY,
                      self.font_jp_medium, center=True, use_jp=True)
    
    def draw_battle(self):
        """バトル画面"""
        # バトル進行状況
        self.draw_text(f"第 {self.current_enemy_index + 1} 戦 / 3", 400, 30, WHITE,
                      self.font_jp_medium, center=True, use_jp=True)
        
        # ステータスバー
        self.draw_status_bar(self.hero.name, self.hero.hp, self.hero.max_hp,
                           self.hero.mp, self.hero.max_mp, x=10, y=60)
        
        # 敵のステータス
        if self.current_enemy:
            self.draw_enemy_status()
        
        # キャラクター
        self.draw_hero()
        if self.current_enemy and self.current_enemy.hp > 0:
            self.draw_enemy()
        
        # エフェクト
        self.draw_effects()
        
        # メッセージボックス
        self.draw_message_box(self.message_queue)
        
        # コマンドメニュー
        if self.state == "BATTLE" and self.turn_phase == "SELECT":
            self.draw_command_menu()
        
        # 回復表示
        if self.show_recovery and self.recovery_timer > 0:
            alpha = min(255, self.recovery_timer * 4)
            text_surface = self.font_jp_medium.render("少し体力が回復した！", True, GREEN)
            text_surface.set_alpha(alpha)
            rect = text_surface.get_rect(center=(400, 200))
            self.screen.blit(text_surface, rect)
            
            if self.recovery_timer <= 0:
                self.show_recovery = False
        
        # バトル終了メッセージ
        if self.state == "BATTLE_END":
            self.draw_text("何かキーを押して次へ", 400, 550, GRAY,
                          self.font_jp_small, center=True, use_jp=True)
    
    def draw_enemy_status(self):
        """敵のステータスバー"""
        x = 490
        y = 60
        self.draw_rect(x, y, 300, 80, DARK_GRAY)
        self.draw_rect(x, y, 300, 80, WHITE, 2)
        
        self.draw_text(self.current_enemy.name, x + 10, y + 10, WHITE, use_jp=True)
        
        # HPバー
        hp_ratio = self.current_enemy.hp / self.current_enemy.max_hp if self.current_enemy.max_hp > 0 else 0
        self.draw_text("HP:", x + 10, y + 40, WHITE)
        self.draw_rect(x + 50, y + 40, 200, 20, DARK_GRAY)
        self.draw_rect(x + 50, y + 40, int(200 * hp_ratio), 20, RED)
        self.draw_rect(x + 50, y + 40, 200, 20, WHITE, 2)
        self.draw_text(f"{self.current_enemy.hp}/{self.current_enemy.max_hp}", x + 260, y + 40, WHITE)
    
    def draw_hero(self):
        """勇者を描画"""
        x = self.hero_x
        y = self.hero_y
        
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
        """敵を描画"""
        x = self.enemy_x
        y = self.enemy_y
        
        if self.shake_target == "enemy" and self.shake_timer > 0:
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
        
        if self.current_enemy.name == "スライム":
            # スライム
            points = []
            for angle in range(0, 360, 30):
                rad = angle * 3.14159 / 180
                radius = 40 + random.randint(-5, 5)
                px = x + radius * math.cos(rad)
                py = y + radius * math.sin(rad) * 0.8
                points.append((px, py))
            
            pygame.draw.polygon(self.screen, self.current_enemy.color, points)
            pygame.draw.polygon(self.screen, (0, 100, 0), points, 2)
            
            # 目
            pygame.draw.circle(self.screen, BLACK, (x - 10, y - 10), 5)
            pygame.draw.circle(self.screen, BLACK, (x + 10, y - 10), 5)
        
        elif self.current_enemy.name == "ゴブリン":
            # ゴブリン
            # 体
            pygame.draw.rect(self.screen, self.current_enemy.color, (x - 20, y - 20, 40, 40))
            pygame.draw.rect(self.screen, BLACK, (x - 20, y - 20, 40, 40), 2)
            
            # 頭
            pygame.draw.circle(self.screen, (100, 150, 100), (x, y - 30), 20)
            pygame.draw.circle(self.screen, BLACK, (x, y - 30), 20, 2)
            
            # 目
            pygame.draw.circle(self.screen, RED, (x - 8, y - 30), 3)
            pygame.draw.circle(self.screen, RED, (x + 8, y - 30), 3)
            
            # 武器
            pygame.draw.line(self.screen, (100, 50, 0), (x - 30, y), (x - 40, y - 20), 5)
        
        elif self.current_enemy.name == "オーク":
            # オーク
            # 体（大きめ）
            pygame.draw.rect(self.screen, self.current_enemy.color, (x - 30, y - 30, 60, 60))
            pygame.draw.rect(self.screen, BLACK, (x - 30, y - 30, 60, 60), 2)
            
            # 頭
            pygame.draw.circle(self.screen, (80, 120, 80), (x, y - 40), 25)
            pygame.draw.circle(self.screen, BLACK, (x, y - 40), 25, 2)
            
            # 目
            pygame.draw.circle(self.screen, RED, (x - 10, y - 40), 4)
            pygame.draw.circle(self.screen, RED, (x + 10, y - 40), 4)
            
            # 牙
            pygame.draw.polygon(self.screen, WHITE, [(x - 10, y - 30), (x - 5, y - 35), (x - 5, y - 30)])
            pygame.draw.polygon(self.screen, WHITE, [(x + 10, y - 30), (x + 5, y - 35), (x + 5, y - 30)])
    
    def draw_effects(self):
        """エフェクトを描画"""
        for effect in self.effects:
            alpha = effect["timer"] / 30.0
            
            if effect["type"] == "slash":
                for i in range(3):
                    start_x = effect["x"] - 30 + i * 20
                    start_y = effect["y"] - 30
                    end_x = effect["x"] + 30 - i * 20
                    end_y = effect["y"] + 30
                    color = (255, int(255 * alpha), int(255 * alpha))
                    pygame.draw.line(self.screen, color,
                                   (start_x, start_y), (end_x, end_y), 3)
            
            elif effect["type"] == "hit":
                radius = int(20 * (1 - alpha))
                color = (255, int(200 * alpha), 0)
                pygame.draw.circle(self.screen, color,
                                 (int(effect["x"]), int(effect["y"])), radius, 3)
    
    def draw_command_menu(self):
        """コマンドメニュー"""
        commands = ["こうげき", "にげる"]
        self.draw_menu("コマンド", commands, 50, 450, 200,
                      selected_index=self.selected_action, use_jp=True)
    
    def draw_all_clear(self):
        """全クリア画面"""
        self.draw_text("ALL CLEAR!", 400, 200, YELLOW, self.font_xlarge, center=True)
        self.draw_text("すべての敵をたおした！", 400, 280, WHITE,
                      self.font_jp_large, center=True, use_jp=True)
        
        # 結果表示
        self.draw_rect(250, 330, 300, 150, DARK_GRAY)
        self.draw_rect(250, 330, 300, 150, WHITE, 2)
        
        self.draw_text(f"{self.hero.name}の勝利！", 400, 360, WHITE,
                      self.font_jp_medium, center=True, use_jp=True)
        self.draw_text(f"獲得した経験値：{self.hero.exp}", 400, 400, WHITE,
                      self.font_jp_medium, center=True, use_jp=True)
        
        self.draw_text("Rキーでもう一度 / Qキーで終了", 400, 530, GRAY,
                      self.font_jp_small, center=True, use_jp=True)
    
    def draw_game_over(self):
        """ゲームオーバー画面"""
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        self.draw_text("GAME OVER", 400, 250, RED, self.font_xlarge, center=True)
        self.draw_text("Rキーでもう一度 / Qキーで終了", 400, 350, GRAY,
                      self.font_jp_medium, center=True, use_jp=True)

def main():
    game = MultipleBattleGame()
    game.run()

if __name__ == "__main__":
    main()