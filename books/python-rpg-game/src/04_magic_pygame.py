"""
第4章：魔法をつかおう！ - MPを消費して強力なこうげき（pygame版）
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
        self.mp = 30
        self.max_mp = 30
        self.attack = 15
        self.magic_power = 25
        self.exp = 0
        self.magic_list = ["ファイア", "ヒール"]

class Enemy:
    def __init__(self, name, hp, attack, exp, color, weakness=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.exp = exp
        self.color = color
        self.weakness = weakness

class MagicBattleGame(GameBase):
    def __init__(self):
        super().__init__("RPGゲーム - 魔法をつかおう！")
        
        # ゲームの状態
        self.state = "NAME_INPUT"
        
        # 勇者
        self.hero = None
        
        # 敵のリスト
        self.enemy_list = [
            Enemy("アイススライム", 40, 6, 15, (100, 200, 255), "炎"),
            Enemy("ゴブリンメイジ", 60, 10, 25, (150, 100, 200), None),
            Enemy("フレイムオーガ", 100, 15, 40, (255, 100, 50), "氷")
        ]
        self.current_enemy_index = 0
        self.current_enemy = None
        
        # バトル関連
        self.selected_action = 0  # 0:こうげき, 1:まほう, 2:にげる
        self.selected_magic = 0
        self.message_queue = []
        self.message_timer = 0
        self.turn_phase = "SELECT"  # SELECT, MAGIC_SELECT, ACTION, etc
        
        # アニメーション
        self.hero_x = 200
        self.hero_y = 300
        self.enemy_x = 600
        self.enemy_y = 300
        self.shake_timer = 0
        self.shake_target = None
        
        # エフェクト
        self.effects = []
        self.particles = []  # 魔法パーティクル用
        
        # 入力
        self.input_text = ""
    
    def start_new_battle(self):
        """新しいバトルを開始"""
        if self.current_enemy_index < len(self.enemy_list):
            self.current_enemy = self.enemy_list[self.current_enemy_index]
            self.message_queue = [f"{self.current_enemy.name}があらわれた！"]
            if self.current_enemy.weakness:
                self.message_queue.append(f"（弱点：{self.current_enemy.weakness}）")
            self.turn_phase = "SELECT"
            self.selected_action = 0
            self.selected_magic = 0
            self.effects = []
            self.particles = []
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
                        "魔法を上手に使って敵をたおそう！"
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
                    if event.key == pygame.K_UP:
                        self.selected_action = (self.selected_action - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        self.selected_action = (self.selected_action + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        if self.selected_action == 1:  # まほう
                            self.turn_phase = "MAGIC_SELECT"
                        else:
                            self.execute_action()
            
            elif self.turn_phase == "MAGIC_SELECT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_magic = (self.selected_magic - 1) % (len(self.hero.magic_list) + 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_magic = (self.selected_magic + 1) % (len(self.hero.magic_list) + 1)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_magic == len(self.hero.magic_list):  # もどる
                            self.turn_phase = "SELECT"
                        else:
                            self.execute_magic()
                    elif event.key == pygame.K_ESCAPE:
                        self.turn_phase = "SELECT"
        
        elif self.state == "BATTLE_END":
            if event.type == pygame.KEYDOWN:
                self.current_enemy_index += 1
                if self.current_enemy_index < len(self.enemy_list):
                    self.state = "BATTLE"
                    self.start_new_battle()
                    # 回復
                    self.hero.hp = min(self.hero.hp + 15, self.hero.max_hp)
                    self.hero.mp = min(self.hero.mp + 10, self.hero.max_mp)
                    self.message_queue.append("少し休憩した...")
                    self.message_queue.append("HPとMPが少し回復した！")
                else:
                    self.state = "ALL_CLEAR"
        
        elif self.state in ["ALL_CLEAR", "GAME_OVER"]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.__init__()
                elif event.key == pygame.K_q:
                    self.running = False
    
    def execute_action(self):
        """通常アクションを実行"""
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
        
        elif self.selected_action == 2:  # にげる
            self.message_queue = [f"{self.hero.name}はにげだした！"]
            self.state = "GAME_OVER"
    
    def execute_magic(self):
        """魔法を実行"""
        magic_name = self.hero.magic_list[self.selected_magic]
        
        if magic_name == "ファイア":
            mp_cost = 5
            if self.hero.mp >= mp_cost:
                self.hero.mp -= mp_cost
                damage = random.randint(self.hero.magic_power, self.hero.magic_power + 15)
                
                # 弱点なら1.5倍
                if self.current_enemy.weakness == "炎":
                    damage = int(damage * 1.5)
                    self.message_queue = [
                        f"{self.hero.name}はファイアをとなえた！",
                        "弱点をついた！",
                        f"{self.current_enemy.name}に{damage}のダメージ！"
                    ]
                else:
                    self.message_queue = [
                        f"{self.hero.name}はファイアをとなえた！",
                        f"{self.current_enemy.name}に{damage}のダメージ！"
                    ]
                
                self.current_enemy.hp -= damage
                self.add_magic_effect("fire", self.enemy_x, self.enemy_y)
                self.shake_target = "enemy"
                self.shake_timer = 30
                self.turn_phase = "HERO_ACTION"
            else:
                self.message_queue = ["MPが足りない！"]
                self.turn_phase = "SELECT"
        
        elif magic_name == "ヒール":
            mp_cost = 8
            if self.hero.mp >= mp_cost:
                self.hero.mp -= mp_cost
                heal = random.randint(25, 35)
                old_hp = self.hero.hp
                self.hero.hp = min(self.hero.hp + heal, self.hero.max_hp)
                actual_heal = self.hero.hp - old_hp
                
                self.message_queue = [
                    f"{self.hero.name}はヒールをとなえた！",
                    f"HPが{actual_heal}回復した！"
                ]
                
                self.add_magic_effect("heal", self.hero_x, self.hero_y)
                self.turn_phase = "HERO_ACTION"
            else:
                self.message_queue = ["MPが足りない！"]
                self.turn_phase = "SELECT"
    
    def add_effect(self, effect_type, x, y):
        """エフェクトを追加"""
        self.effects.append({
            "type": effect_type,
            "x": x,
            "y": y,
            "timer": 30
        })
    
    def add_magic_effect(self, magic_type, x, y):
        """魔法エフェクトを追加"""
        if magic_type == "fire":
            # 炎のパーティクル
            for i in range(20):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 5)
                self.particles.append({
                    "type": "fire",
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed - 2,
                    "life": 40,
                    "size": random.randint(5, 10)
                })
        
        elif magic_type == "heal":
            # 回復の光
            for i in range(15):
                angle = i * (2 * math.pi / 15)
                self.particles.append({
                    "type": "heal",
                    "x": x + math.cos(angle) * 30,
                    "y": y + math.sin(angle) * 30,
                    "vx": -math.cos(angle) * 1,
                    "vy": -math.sin(angle) * 1 - 1,
                    "life": 30,
                    "size": 8
                })
    
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
                            # MP少し回復
                            mp_recover = 5
                            self.hero.mp = min(self.hero.mp + mp_recover, self.hero.max_mp)
                            self.message_queue.append(f"MPが{mp_recover}回復した！")
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
            
            elif self.turn_phase == "HERO_ACTION":
                self.message_timer = 60
        
        # 画面の揺れ
        if self.shake_timer > 0:
            self.shake_timer -= 1
        
        # エフェクトの更新
        self.effects = [e for e in self.effects if e["timer"] > 0]
        for effect in self.effects:
            effect["timer"] -= 1
        
        # パーティクルの更新
        for particle in self.particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["type"] == "fire":
                particle["vy"] += 0.2  # 重力
        
        self.particles = [p for p in self.particles if p["life"] > 0]
    
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
        # 魔法陣風の背景
        center_x, center_y = 400, 300
        for i in range(3):
            radius = 150 + i * 50
            alpha = 50 - i * 15
            color = (alpha, alpha, alpha * 2)
            pygame.draw.circle(self.screen, color, (center_x, center_y), radius, 2)
    
    def draw_name_input(self):
        """名前入力画面"""
        self.draw_text("勇者の名前を入力してください", 400, 200, WHITE,
                      self.font_jp_large, center=True, use_jp=True)
        
        input_rect = pygame.Rect(250, 250, 300, 50)
        pygame.draw.rect(self.screen, WHITE, input_rect)
        pygame.draw.rect(self.screen, BLACK, input_rect, 3)
        
        self.draw_text(self.input_text, 260, 265, BLACK, self.font_large)
        
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = 260 + self.font_large.size(self.input_text)[0]
            pygame.draw.line(self.screen, BLACK, (cursor_x, 260), (cursor_x, 290), 2)
    
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
        
        # パーティクル（エフェクトの後ろ）
        self.draw_particles()
        
        # エフェクト
        self.draw_effects()
        
        # メッセージボックス
        self.draw_message_box(self.message_queue)
        
        # コマンドメニュー
        if self.state == "BATTLE":
            if self.turn_phase == "SELECT":
                self.draw_command_menu()
            elif self.turn_phase == "MAGIC_SELECT":
                self.draw_magic_menu()
        
        # バトル終了メッセージ
        if self.state == "BATTLE_END":
            self.draw_text("何かキーを押して次へ", 400, 550, GRAY,
                          self.font_jp_small, center=True, use_jp=True)
    
    def draw_enemy_status(self):
        """敵のステータスバー"""
        x = 490
        y = 60
        self.draw_rect(x, y, 300, 100, DARK_GRAY)
        self.draw_rect(x, y, 300, 100, WHITE, 2)
        
        self.draw_text(self.current_enemy.name, x + 10, y + 10, WHITE, use_jp=True)
        
        # 弱点表示
        if self.current_enemy.weakness:
            self.draw_text(f"弱点：{self.current_enemy.weakness}", x + 10, y + 35,
                          YELLOW, self.font_jp_small, use_jp=True)
        
        # HPバー
        hp_ratio = self.current_enemy.hp / self.current_enemy.max_hp if self.current_enemy.max_hp > 0 else 0
        self.draw_text("HP:", x + 10, y + 60, WHITE)
        self.draw_rect(x + 50, y + 60, 200, 20, DARK_GRAY)
        self.draw_rect(x + 50, y + 60, int(200 * hp_ratio), 20, RED)
        self.draw_rect(x + 50, y + 60, 200, 20, WHITE, 2)
        self.draw_text(f"{self.current_enemy.hp}/{self.current_enemy.max_hp}", x + 260, y + 60, WHITE)
    
    def draw_particles(self):
        """パーティクルを描画"""
        for particle in self.particles:
            alpha = particle["life"] / 40.0
            
            if particle["type"] == "fire":
                # 炎のパーティクル
                color = (255, int(200 * alpha), int(50 * alpha))
                size = int(particle["size"] * alpha)
                pygame.draw.circle(self.screen, color,
                                 (int(particle["x"]), int(particle["y"])),
                                 size)
            
            elif particle["type"] == "heal":
                # 回復のパーティクル
                color = (int(100 * alpha), 255, int(100 * alpha))
                size = int(particle["size"] * alpha)
                pygame.draw.circle(self.screen, color,
                                 (int(particle["x"]), int(particle["y"])),
                                 size)
                # 光の尾
                pygame.draw.line(self.screen, color,
                               (particle["x"], particle["y"]),
                               (particle["x"] - particle["vx"] * 5,
                                particle["y"] - particle["vy"] * 5), 2)
    
    def draw_command_menu(self):
        """コマンドメニュー"""
        commands = ["こうげき", "まほう", "にげる"]
        self.draw_menu("コマンド", commands, 50, 450, 200,
                      selected_index=self.selected_action, use_jp=True)
    
    def draw_magic_menu(self):
        """魔法メニュー"""
        x = 300
        y = 200
        width = 200
        height = 200
        
        # 背景
        self.draw_rect(x - 10, y - 10, width + 20, height + 20, DARK_GRAY)
        self.draw_rect(x - 10, y - 10, width + 20, height + 20, WHITE, 2)
        
        # タイトル
        self.draw_text("魔法を選んでください", x + width // 2, y - 30,
                      WHITE, self.font_jp_medium, center=True, use_jp=True)
        
        # 魔法リスト
        magic_info = [
            ("ファイア", "MP5", "敵に炎のダメージ"),
            ("ヒール", "MP8", "自分のHPを回復")
        ]
        
        for i, (name, cost, desc) in enumerate(magic_info):
            item_y = y + 30 + i * 50
            
            # 選択中の項目はハイライト
            if i == self.selected_magic:
                self.draw_rect(x, item_y - 5, width, 40, BLUE)
            
            self.draw_text(f"{name} ({cost})", x + 10, item_y,
                          WHITE, self.font_jp_medium, use_jp=True)
            self.draw_text(desc, x + 10, item_y + 20,
                          GRAY, self.font_jp_small, use_jp=True)
        
        # もどる
        back_y = y + 30 + len(magic_info) * 50
        if self.selected_magic == len(self.hero.magic_list):
            self.draw_rect(x, back_y - 5, width, 30, BLUE)
        self.draw_text("もどる", x + 10, back_y,
                      WHITE, self.font_jp_medium, use_jp=True)
    
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
        
        # 杖（魔法使い風）
        pygame.draw.line(self.screen, (139, 69, 19),
                        (x + 25, y + 10), (x + 35, y - 40), 4)
        # 杖の先の宝石
        pygame.draw.circle(self.screen, (255, 0, 255), (x + 35, y - 40), 6)
        pygame.draw.circle(self.screen, WHITE, (x + 35, y - 40), 6, 2)
    
    def draw_enemy(self):
        """敵を描画"""
        x = self.enemy_x
        y = self.enemy_y
        
        if self.shake_target == "enemy" and self.shake_timer > 0:
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)
        
        # 敵の種類に応じて描画
        if "スライム" in self.current_enemy.name:
            # スライム系
            points = []
            for angle in range(0, 360, 20):
                rad = angle * 3.14159 / 180
                radius = 45 + random.randint(-3, 3)
                px = x + radius * math.cos(rad)
                py = y + radius * math.sin(rad) * 0.7
                points.append((px, py))
            
            pygame.draw.polygon(self.screen, self.current_enemy.color, points)
            pygame.draw.polygon(self.screen, BLACK, points, 2)
            
            # 目
            pygame.draw.circle(self.screen, BLACK, (x - 12, y - 10), 6)
            pygame.draw.circle(self.screen, BLACK, (x + 12, y - 10), 6)
            pygame.draw.circle(self.screen, WHITE, (x - 10, y - 12), 3)
            pygame.draw.circle(self.screen, WHITE, (x + 14, y - 12), 3)
        
        elif "ゴブリン" in self.current_enemy.name:
            # ゴブリンメイジ
            # ローブ
            pygame.draw.polygon(self.screen, self.current_enemy.color,
                              [(x - 25, y + 20), (x + 25, y + 20),
                               (x + 15, y - 20), (x - 15, y - 20)])
            pygame.draw.polygon(self.screen, BLACK,
                              [(x - 25, y + 20), (x + 25, y + 20),
                               (x + 15, y - 20), (x - 15, y - 20)], 2)
            
            # 頭
            pygame.draw.circle(self.screen, (100, 150, 100), (x, y - 30), 20)
            pygame.draw.circle(self.screen, BLACK, (x, y - 30), 20, 2)
            
            # 目
            pygame.draw.circle(self.screen, (200, 0, 200), (x - 8, y - 30), 4)
            pygame.draw.circle(self.screen, (200, 0, 200), (x + 8, y - 30), 4)
            
            # 杖
            pygame.draw.line(self.screen, (100, 50, 0),
                           (x - 30, y), (x - 40, y - 40), 3)
            pygame.draw.circle(self.screen, (255, 255, 0), (x - 40, y - 40), 5)
        
        else:
            # フレイムオーガ
            # 体（大きめ）
            pygame.draw.rect(self.screen, self.current_enemy.color,
                           (x - 35, y - 35, 70, 70))
            pygame.draw.rect(self.screen, BLACK, (x - 35, y - 35, 70, 70), 2)
            
            # 炎のオーラ
            for i in range(5):
                flame_x = x + random.randint(-40, 40)
                flame_y = y - 35 + random.randint(-10, 10)
                pygame.draw.circle(self.screen, (255, 200, 0), (flame_x, flame_y), 8)
            
            # 頭
            pygame.draw.circle(self.screen, (200, 100, 50), (x, y - 45), 25)
            pygame.draw.circle(self.screen, BLACK, (x, y - 45), 25, 2)
            
            # 目（燃える目）
            pygame.draw.circle(self.screen, (255, 100, 0), (x - 10, y - 45), 5)
            pygame.draw.circle(self.screen, (255, 100, 0), (x + 10, y - 45), 5)
    
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
    
    def draw_all_clear(self):
        """全クリア画面"""
        self.draw_text("ALL CLEAR!", 400, 150, YELLOW, self.font_xlarge, center=True)
        self.draw_text("すべての敵をたおした！", 400, 230, WHITE,
                      self.font_jp_large, center=True, use_jp=True)
        
        # 結果表示
        self.draw_rect(200, 280, 400, 200, DARK_GRAY)
        self.draw_rect(200, 280, 400, 200, WHITE, 2)
        
        self.draw_text(f"{self.hero.name}の勝利！", 400, 320, WHITE,
                      self.font_jp_medium, center=True, use_jp=True)
        self.draw_text(f"獲得した経験値：{self.hero.exp}", 400, 360, WHITE,
                      self.font_jp_medium, center=True, use_jp=True)
        self.draw_text("魔法使いとしての才能が開花した！", 400, 420, GREEN,
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
    game = MagicBattleGame()
    game.run()

if __name__ == "__main__":
    main()