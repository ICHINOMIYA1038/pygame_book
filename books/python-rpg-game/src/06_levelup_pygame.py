"""
第6章：レベルアップ！ - 経験値をためて強くなろう（pygame版）
"""
import pygame
import random
import math
from game_utils import GameBase, WHITE, BLACK, BLUE, GREEN, RED, YELLOW, GRAY, DARK_GRAY

class Hero:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.next_exp = 30  # 次のレベルまでの経験値
        
        # 基本ステータス
        self.base_hp = 100
        self.base_mp = 30
        self.base_attack = 15
        self.base_magic_power = 25
        self.base_defense = 10
        
        # 現在のステータス
        self.hp = self.base_hp
        self.max_hp = self.base_hp
        self.mp = self.base_mp
        self.max_mp = self.base_mp
        self.attack = self.base_attack
        self.magic_power = self.base_magic_power
        self.defense = self.base_defense
        
        self.magic_list = ["ファイア", "ヒール"]
        
        # アイテム所持数
        self.items = {
            "ポーション": 3,
            "エーテル": 2,
            "ハイポーション": 1
        }
    
    def gain_exp(self, exp):
        """経験値を獲得"""
        self.exp += exp
        level_ups = 0
        
        while self.exp >= self.next_exp:
            self.exp -= self.next_exp
            self.level_up()
            level_ups += 1
        
        return level_ups
    
    def level_up(self):
        """レベルアップ処理"""
        self.level += 1
        self.next_exp = int(self.next_exp * 1.5)  # 次の必要経験値
        
        # ステータス上昇
        hp_up = random.randint(15, 25)
        mp_up = random.randint(5, 10)
        atk_up = random.randint(3, 5)
        mag_up = random.randint(2, 4)
        def_up = random.randint(2, 3)
        
        self.base_hp += hp_up
        self.base_mp += mp_up
        self.base_attack += atk_up
        self.base_magic_power += mag_up
        self.base_defense += def_up
        
        # 最大値を更新
        self.max_hp = self.base_hp
        self.max_mp = self.base_mp
        self.attack = self.base_attack
        self.magic_power = self.base_magic_power
        self.defense = self.base_defense
        
        # 全回復
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # 新しい魔法を習得
        if self.level == 3:
            self.magic_list.append("サンダー")
        elif self.level == 5:
            self.magic_list.append("ブリザード")
        
        return {
            "hp": hp_up,
            "mp": mp_up,
            "attack": atk_up,
            "magic_power": mag_up,
            "defense": def_up
        }

class Enemy:
    def __init__(self, name, hp, attack, exp, color, weakness=None, drop_item=None, level=1):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.exp = exp
        self.color = color
        self.weakness = weakness
        self.drop_item = drop_item
        self.level = level

class LevelUpGame(GameBase):
    def __init__(self):
        super().__init__("RPGゲーム - レベルアップシステム！")
        
        # ゲームの状態
        self.state = "NAME_INPUT"
        
        # 勇者
        self.hero = None
        
        # 敵のリスト（強化版）
        self.enemy_list = [
            Enemy("アイススライム", 40, 6, 20, (100, 200, 255), "炎", "ポーション", 1),
            Enemy("ゴブリンメイジ", 60, 10, 35, (150, 100, 200), None, "エーテル", 2),
            Enemy("フレイムオーガ", 100, 15, 60, (255, 100, 50), "氷", "ハイポーション", 3),
            Enemy("ダークナイト", 150, 20, 100, (50, 0, 50), "光", "エリクサー", 5)
        ]
        self.current_enemy_index = 0
        self.current_enemy = None
        
        # バトル関連
        self.selected_action = 0
        self.selected_magic = 0
        self.selected_item = 0
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
        self.particles = []
        self.item_effect_particles = []
        self.levelup_particles = []  # レベルアップエフェクト用
        
        # 入力
        self.input_text = ""
        
        # ドロップアイテム表示
        self.dropped_item = None
        self.drop_timer = 0
        
        # レベルアップ関連
        self.levelup_info = None
        self.levelup_timer = 0
        self.stat_increases = None
    
    def start_new_battle(self):
        """新しいバトルを開始"""
        if self.current_enemy_index < len(self.enemy_list):
            self.current_enemy = self.enemy_list[self.current_enemy_index]
            self.message_queue = [f"{self.current_enemy.name}があらわれた！"]
            if self.current_enemy.weakness:
                self.message_queue.append(f"（弱点：{self.current_enemy.weakness}）")
            self.message_queue.append(f"（レベル {self.current_enemy.level}）")
            self.turn_phase = "SELECT"
            self.selected_action = 0
            self.selected_magic = 0
            self.selected_item = 0
            self.effects = []
            self.particles = []
            self.item_effect_particles = []
            self.levelup_particles = []
            self.shake_timer = 0
            self.dropped_item = None
            self.drop_timer = 0
            self.levelup_timer = 0
    
    def on_event(self, event):
        """イベント処理"""
        if self.state == "NAME_INPUT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.input_text:
                    self.hero = Hero(self.input_text)
                    self.state = "INTRO"
                    self.message_queue = [
                        f"{self.hero.name}のぼうけんが始まります！",
                        "経験値をためてレベルアップしよう！"
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
                        self.selected_action = (self.selected_action - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        self.selected_action = (self.selected_action + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        if self.selected_action == 1:  # まほう
                            self.turn_phase = "MAGIC_SELECT"
                        elif self.selected_action == 2:  # アイテム
                            self.turn_phase = "ITEM_SELECT"
                            self.selected_item = 0
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
            
            elif self.turn_phase == "ITEM_SELECT":
                if event.type == pygame.KEYDOWN:
                    available_items = [(name, count) for name, count in self.hero.items.items() if count > 0]
                    if event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % (len(available_items) + 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % (len(available_items) + 1)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item == len(available_items):  # もどる
                            self.turn_phase = "SELECT"
                        else:
                            self.execute_item(available_items[self.selected_item][0])
                    elif event.key == pygame.K_ESCAPE:
                        self.turn_phase = "SELECT"
        
        elif self.state == "BATTLE_END":
            if event.type == pygame.KEYDOWN and self.drop_timer <= 0 and self.levelup_timer <= 0:
                self.current_enemy_index += 1
                if self.current_enemy_index < len(self.enemy_list):
                    self.state = "BATTLE"
                    self.start_new_battle()
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
            # 防御力を考慮
            damage = max(1, damage - self.current_enemy.level * 2)
            self.current_enemy.hp -= damage
            self.message_queue = [
                f"{self.hero.name}のこうげき！",
                f"{self.current_enemy.name}に{damage}のダメージ！"
            ]
            self.shake_target = "enemy"
            self.shake_timer = 20
            self.add_effect("slash", self.enemy_x, self.enemy_y)
            self.turn_phase = "HERO_ACTION"
        
        elif self.selected_action == 3:  # にげる
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
        
        elif magic_name == "サンダー":
            mp_cost = 10
            if self.hero.mp >= mp_cost:
                self.hero.mp -= mp_cost
                damage = random.randint(self.hero.magic_power + 10, self.hero.magic_power + 30)
                
                self.message_queue = [
                    f"{self.hero.name}はサンダーをとなえた！",
                    f"{self.current_enemy.name}に{damage}のダメージ！"
                ]
                
                self.current_enemy.hp -= damage
                self.add_magic_effect("thunder", self.enemy_x, self.enemy_y)
                self.shake_target = "enemy"
                self.shake_timer = 40
                self.turn_phase = "HERO_ACTION"
            else:
                self.message_queue = ["MPが足りない！"]
                self.turn_phase = "SELECT"
        
        elif magic_name == "ブリザード":
            mp_cost = 12
            if self.hero.mp >= mp_cost:
                self.hero.mp -= mp_cost
                damage = random.randint(self.hero.magic_power + 5, self.hero.magic_power + 25)
                
                # 弱点なら1.5倍
                if self.current_enemy.weakness == "氷":
                    damage = int(damage * 1.5)
                    self.message_queue = [
                        f"{self.hero.name}はブリザードをとなえた！",
                        "弱点をついた！",
                        f"{self.current_enemy.name}に{damage}のダメージ！"
                    ]
                else:
                    self.message_queue = [
                        f"{self.hero.name}はブリザードをとなえた！",
                        f"{self.current_enemy.name}に{damage}のダメージ！"
                    ]
                
                self.current_enemy.hp -= damage
                self.add_magic_effect("ice", self.enemy_x, self.enemy_y)
                self.shake_target = "enemy"
                self.shake_timer = 35
                self.turn_phase = "HERO_ACTION"
            else:
                self.message_queue = ["MPが足りない！"]
                self.turn_phase = "SELECT"
    
    def execute_item(self, item_name):
        """アイテムを使用"""
        if self.hero.items[item_name] > 0:
            self.hero.items[item_name] -= 1
            
            if item_name == "ポーション":
                heal = 30
                old_hp = self.hero.hp
                self.hero.hp = min(self.hero.hp + heal, self.hero.max_hp)
                actual_heal = self.hero.hp - old_hp
                
                self.message_queue = [
                    f"{self.hero.name}はポーションを使った！",
                    f"HPが{actual_heal}回復した！"
                ]
                self.add_item_effect("potion", self.hero_x, self.hero_y)
            
            elif item_name == "エーテル":
                mp_heal = 15
                old_mp = self.hero.mp
                self.hero.mp = min(self.hero.mp + mp_heal, self.hero.max_mp)
                actual_heal = self.hero.mp - old_mp
                
                self.message_queue = [
                    f"{self.hero.name}はエーテルを使った！",
                    f"MPが{actual_heal}回復した！"
                ]
                self.add_item_effect("ether", self.hero_x, self.hero_y)
            
            elif item_name == "ハイポーション":
                heal = 60
                old_hp = self.hero.hp
                self.hero.hp = min(self.hero.hp + heal, self.hero.max_hp)
                actual_heal = self.hero.hp - old_hp
                
                self.message_queue = [
                    f"{self.hero.name}はハイポーションを使った！",
                    f"HPが{actual_heal}回復した！"
                ]
                self.add_item_effect("hi_potion", self.hero_x, self.hero_y)
            
            elif item_name == "エリクサー":
                self.hero.hp = self.hero.max_hp
                self.hero.mp = self.hero.max_mp
                
                self.message_queue = [
                    f"{self.hero.name}はエリクサーを使った！",
                    "HPとMPが全回復した！"
                ]
                self.add_item_effect("elixir", self.hero_x, self.hero_y)
            
            self.turn_phase = "HERO_ACTION"
    
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
        
        elif magic_type == "thunder":
            # 雷のエフェクト
            self.particles.append({
                "type": "thunder",
                "x": x,
                "y": y - 200,
                "target_y": y,
                "life": 30,
                "branches": []
            })
        
        elif magic_type == "ice":
            # 氷のパーティクル
            for i in range(15):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                self.particles.append({
                    "type": "ice",
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": 50,
                    "size": random.randint(10, 20),
                    "rotation": random.uniform(0, 360)
                })
    
    def add_item_effect(self, item_type, x, y):
        """アイテムエフェクトを追加"""
        if item_type == "potion":
            # 緑の光
            for i in range(10):
                angle = random.uniform(0, 2 * math.pi)
                self.item_effect_particles.append({
                    "type": "potion",
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * 2,
                    "vy": -3,
                    "life": 30,
                    "color": (0, 255, 0)
                })
        
        elif item_type == "ether":
            # 青い光
            for i in range(10):
                angle = random.uniform(0, 2 * math.pi)
                self.item_effect_particles.append({
                    "type": "ether",
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * 2,
                    "vy": -3,
                    "life": 30,
                    "color": (0, 100, 255)
                })
        
        elif item_type == "hi_potion":
            # 金色の光
            for i in range(15):
                angle = random.uniform(0, 2 * math.pi)
                self.item_effect_particles.append({
                    "type": "hi_potion",
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * 3,
                    "vy": -4,
                    "life": 40,
                    "color": (255, 215, 0)
                })
        
        elif item_type == "elixir":
            # 虹色の光
            for i in range(20):
                angle = i * (2 * math.pi / 20)
                color_angle = i * 360 / 20
                r = int(127.5 * (1 + math.sin(math.radians(color_angle))))
                g = int(127.5 * (1 + math.sin(math.radians(color_angle + 120))))
                b = int(127.5 * (1 + math.sin(math.radians(color_angle + 240))))
                self.item_effect_particles.append({
                    "type": "elixir",
                    "x": x + math.cos(angle) * 50,
                    "y": y + math.sin(angle) * 50,
                    "vx": -math.cos(angle) * 2,
                    "vy": -math.sin(angle) * 2 - 1,
                    "life": 50,
                    "color": (r, g, b)
                })
    
    def add_levelup_effect(self):
        """レベルアップエフェクトを追加"""
        # 星のパーティクル
        for i in range(30):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(50, 100)
            self.levelup_particles.append({
                "x": self.hero_x + math.cos(angle) * radius,
                "y": self.hero_y + math.sin(angle) * radius,
                "vx": -math.cos(angle) * 2,
                "vy": -2,
                "life": 60,
                "size": random.randint(5, 10)
            })
    
    def enemy_turn(self):
        """敵のターン"""
        damage = random.randint(self.current_enemy.attack - 2, self.current_enemy.attack + 2)
        # 防御力を考慮
        damage = max(1, damage - self.hero.defense // 2)
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
                            
                            # 経験値獲得とレベルアップチェック
                            old_level = self.hero.level
                            level_ups = self.hero.gain_exp(self.current_enemy.exp)
                            
                            if level_ups > 0:
                                self.message_queue.append(f"レベルが{old_level}から{self.hero.level}に上がった！")
                                self.levelup_timer = 120
                                self.add_levelup_effect()
                                
                                # 最新のレベルアップのステータス上昇を記録
                                self.stat_increases = self.hero.level_up()
                                
                                # 新しい魔法を覚えた場合
                                if self.hero.level == 3:
                                    self.message_queue.append("サンダーを覚えた！")
                                elif self.hero.level == 5:
                                    self.message_queue.append("ブリザードを覚えた！")
                            
                            # アイテムドロップ
                            if self.current_enemy.drop_item:
                                if random.random() < 0.7:  # 70%の確率でドロップ
                                    self.dropped_item = self.current_enemy.drop_item
                                    if self.dropped_item == "エリクサー":
                                        self.hero.items["エリクサー"] = self.hero.items.get("エリクサー", 0) + 1
                                    else:
                                        self.hero.items[self.dropped_item] = self.hero.items.get(self.dropped_item, 0) + 1
                                    self.message_queue.append(f"{self.dropped_item}を手に入れた！")
                                    self.drop_timer = 60
                            
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
            if particle["type"] == "thunder":
                particle["life"] -= 1
            else:
                particle["x"] += particle["vx"]
                particle["y"] += particle["vy"]
                particle["life"] -= 1
                if particle["type"] == "fire":
                    particle["vy"] += 0.2  # 重力
                elif particle["type"] == "ice":
                    particle["rotation"] += 5
        
        self.particles = [p for p in self.particles if p["life"] > 0]
        
        # アイテムエフェクトパーティクルの更新
        for particle in self.item_effect_particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            particle["vy"] += 0.1  # 軽い重力
        
        self.item_effect_particles = [p for p in self.item_effect_particles if p["life"] > 0]
        
        # レベルアップパーティクルの更新
        for particle in self.levelup_particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            particle["vy"] -= 0.1  # 上昇
        
        self.levelup_particles = [p for p in self.levelup_particles if p["life"] > 0]
        
        # タイマーの更新
        if self.drop_timer > 0:
            self.drop_timer -= 1
        if self.levelup_timer > 0:
            self.levelup_timer -= 1
    
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
        # レベルアップ風の背景
        center_x, center_y = 400, 300
        for i in range(5):
            radius = 100 + i * 100
            alpha = 20 - i * 3
            color = (alpha, alpha, alpha * 2)
            pygame.draw.circle(self.screen, color, (center_x, center_y), radius, 1)
    
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
        self.draw_text(f"第 {self.current_enemy_index + 1} 戦 / 4", 400, 30, WHITE,
                      self.font_jp_medium, center=True, use_jp=True)
        
        # ステータスバー（レベル表示付き）
        self.draw_level_status_bar()
        
        # 経験値バー
        self.draw_exp_bar()
        
        # アイテム所持数
        self.draw_item_inventory()
        
        # 敵のステータス
        if self.current_enemy:
            self.draw_enemy_status()
        
        # キャラクター
        self.draw_hero()
        if self.current_enemy and self.current_enemy.hp > 0:
            self.draw_enemy()
        
        # パーティクル（エフェクトの後ろ）
        self.draw_particles()
        self.draw_item_particles()
        self.draw_levelup_particles()
        
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
            elif self.turn_phase == "ITEM_SELECT":
                self.draw_item_menu()
        
        # ドロップアイテム表示
        if self.dropped_item and self.drop_timer > 0:
            self.draw_dropped_item()
        
        # レベルアップ表示
        if self.levelup_timer > 0:
            self.draw_levelup_display()
        
        # バトル終了メッセージ
        if self.state == "BATTLE_END":
            if self.levelup_timer <= 0 and self.drop_timer <= 0:
                self.draw_text("何かキーを押して次へ", 400, 550, GRAY,
                              self.font_jp_small, center=True, use_jp=True)
    
    def draw_level_status_bar(self):
        """レベル付きステータスバー"""
        x = 10
        y = 60
        self.draw_rect(x, y, 300, 100, DARK_GRAY)
        self.draw_rect(x, y, 300, 100, WHITE, 2)
        
        # 名前とレベル
        self.draw_text(f"{self.hero.name} Lv.{self.hero.level}", x + 10, y + 10, WHITE, use_jp=True)
        
        # HPバー
        hp_ratio = self.hero.hp / self.hero.max_hp if self.hero.max_hp > 0 else 0
        self.draw_text("HP:", x + 10, y + 35, WHITE)
        self.draw_rect(x + 50, y + 35, 200, 20, DARK_GRAY)
        self.draw_rect(x + 50, y + 35, int(200 * hp_ratio), 20, GREEN)
        self.draw_rect(x + 50, y + 35, 200, 20, WHITE, 2)
        self.draw_text(f"{self.hero.hp}/{self.hero.max_hp}", x + 260, y + 35, WHITE)
        
        # MPバー
        mp_ratio = self.hero.mp / self.hero.max_mp if self.hero.max_mp > 0 else 0
        self.draw_text("MP:", x + 10, y + 60, WHITE)
        self.draw_rect(x + 50, y + 60, 200, 20, DARK_GRAY)
        self.draw_rect(x + 50, y + 60, int(200 * mp_ratio), 20, BLUE)
        self.draw_rect(x + 50, y + 60, 200, 20, WHITE, 2)
        self.draw_text(f"{self.hero.mp}/{self.hero.max_mp}", x + 260, y + 60, WHITE)
    
    def draw_exp_bar(self):
        """経験値バー"""
        x = 320
        y = 60
        self.draw_rect(x, y, 160, 50, DARK_GRAY)
        self.draw_rect(x, y, 160, 50, WHITE, 2)
        
        self.draw_text("EXP", x + 10, y + 5, WHITE, self.font_small)
        
        # 経験値バー
        exp_ratio = self.hero.exp / self.hero.next_exp if self.hero.next_exp > 0 else 0
        self.draw_rect(x + 10, y + 25, 140, 15, DARK_GRAY)
        self.draw_rect(x + 10, y + 25, int(140 * exp_ratio), 15, YELLOW)
        self.draw_rect(x + 10, y + 25, 140, 15, WHITE, 2)
        
        # 数値
        self.draw_text(f"{self.hero.exp}/{self.hero.next_exp}", x + 80, y + 26,
                      WHITE, self.font_small, center=True)
    
    def draw_item_inventory(self):
        """アイテム所持数を表示"""
        x = 10
        y = 170
        self.draw_rect(x, y, 180, 100, DARK_GRAY)
        self.draw_rect(x, y, 180, 100, WHITE, 2)
        
        self.draw_text("アイテム", x + 10, y + 5, WHITE, self.font_jp_small, use_jp=True)
        
        i = 0
        for name, count in self.hero.items.items():
            if count > 0:
                item_y = y + 25 + i * 18
                if i < 4:  # 最大4個まで表示
                    self.draw_text(f"{name}：{count}", x + 10, item_y, WHITE, 
                                  self.font_jp_small, use_jp=True)
                i += 1
    
    def draw_particles(self):
        """パーティクルを描画"""
        for particle in self.particles:
            if particle["type"] == "fire":
                # 炎のパーティクル
                alpha = particle["life"] / 40.0
                color = (255, int(200 * alpha), int(50 * alpha))
                size = int(particle["size"] * alpha)
                pygame.draw.circle(self.screen, color,
                                 (int(particle["x"]), int(particle["y"])),
                                 size)
            
            elif particle["type"] == "heal":
                # 回復のパーティクル
                alpha = particle["life"] / 30.0
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
            
            elif particle["type"] == "thunder":
                # 雷のエフェクト
                if particle["life"] > 20:
                    # メインの雷
                    points = []
                    y = particle["y"]
                    while y < particle["target_y"]:
                        x = particle["x"] + random.randint(-20, 20)
                        points.append((x, y))
                        y += 20
                    points.append((particle["x"], particle["target_y"]))
                    
                    if len(points) > 1:
                        pygame.draw.lines(self.screen, YELLOW, False, points, 3)
                        pygame.draw.lines(self.screen, WHITE, False, points, 1)
                else:
                    # 残光
                    alpha = particle["life"] / 20.0
                    color = (255, 255, int(255 * alpha))
                    pygame.draw.circle(self.screen, color,
                                     (int(particle["x"]), int(particle["target_y"])),
                                     int(30 * alpha), 2)
            
            elif particle["type"] == "ice":
                # 氷のパーティクル
                alpha = particle["life"] / 50.0
                size = int(particle["size"] * alpha)
                color = (int(200 * alpha), int(200 * alpha), 255)
                
                # 六角形の氷の結晶
                angle = particle["rotation"]
                points = []
                for i in range(6):
                    a = angle + i * 60
                    x = particle["x"] + size * math.cos(math.radians(a))
                    y = particle["y"] + size * math.sin(math.radians(a))
                    points.append((x, y))
                
                if len(points) > 2:
                    pygame.draw.polygon(self.screen, color, points, 2)
    
    def draw_levelup_particles(self):
        """レベルアップパーティクルを描画"""
        for particle in self.levelup_particles:
            alpha = particle["life"] / 60.0
            color = (255, int(255 * alpha), int(100 * alpha))
            
            # 星型
            x, y = int(particle["x"]), int(particle["y"])
            size = particle["size"]
            
            # 星の頂点を計算
            points = []
            for i in range(10):
                angle = i * 36 - 90
                if i % 2 == 0:
                    radius = size
                else:
                    radius = size // 2
                px = x + radius * math.cos(math.radians(angle))
                py = y + radius * math.sin(math.radians(angle))
                points.append((px, py))
            
            if len(points) > 2:
                pygame.draw.polygon(self.screen, color, points)
    
    def draw_levelup_display(self):
        """レベルアップ表示"""
        alpha = min(255, self.levelup_timer * 4)
        
        # 背景
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(alpha // 2)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # LEVEL UP!
        text_surface = self.font_xlarge.render("LEVEL UP!", True, YELLOW)
        text_surface.set_alpha(alpha)
        rect = text_surface.get_rect(center=(400, 200))
        self.screen.blit(text_surface, rect)
        
        # ステータス上昇（最新のもののみ表示）
        if self.stat_increases and self.levelup_timer > 30:
            y = 280
            stat_names = {
                "hp": "HP",
                "mp": "MP",
                "attack": "こうげき力",
                "magic_power": "まほう力",
                "defense": "ぼうぎょ力"
            }
            
            for stat, value in self.stat_increases.items():
                if stat in stat_names:
                    text = f"{stat_names[stat]} +{value}"
                    text_surface = self.font_jp_medium.render(text, True, GREEN)
                    text_surface.set_alpha(alpha)
                    rect = text_surface.get_rect(center=(400, y))
                    self.screen.blit(text_surface, rect)
                    y += 40
    
    def draw_command_menu(self):
        """コマンドメニュー"""
        commands = ["こうげき", "まほう", "アイテム", "にげる"]
        self.draw_menu("コマンド", commands, 50, 400, 200,
                      selected_index=self.selected_action, use_jp=True)
    
    def draw_magic_menu(self):
        """魔法メニュー"""
        x = 300
        y = 150
        width = 200
        height = 300
        
        # 背景
        self.draw_rect(x - 10, y - 10, width + 20, height + 20, DARK_GRAY)
        self.draw_rect(x - 10, y - 10, width + 20, height + 20, WHITE, 2)
        
        # タイトル
        self.draw_text("魔法を選んでください", x + width // 2, y - 30,
                      WHITE, self.font_jp_medium, center=True, use_jp=True)
        
        # 魔法リスト
        magic_info = {
            "ファイア": ("MP5", "敵に炎のダメージ"),
            "ヒール": ("MP8", "自分のHPを回復"),
            "サンダー": ("MP10", "敵に雷のダメージ"),
            "ブリザード": ("MP12", "敵に氷のダメージ")
        }
        
        y_offset = 30
        for i, magic_name in enumerate(self.hero.magic_list):
            if magic_name in magic_info:
                cost, desc = magic_info[magic_name]
                item_y = y + y_offset
                
                # 選択中の項目はハイライト
                if i == self.selected_magic:
                    self.draw_rect(x, item_y - 5, width, 40, BLUE)
                
                self.draw_text(f"{magic_name} ({cost})", x + 10, item_y,
                              WHITE, self.font_jp_medium, use_jp=True)
                self.draw_text(desc, x + 10, item_y + 20,
                              GRAY, self.font_jp_small, use_jp=True)
                
                y_offset += 50
        
        # もどる
        back_y = y + y_offset
        if self.selected_magic == len(self.hero.magic_list):
            self.draw_rect(x, back_y - 5, width, 30, BLUE)
        self.draw_text("もどる", x + 10, back_y,
                      WHITE, self.font_jp_medium, use_jp=True)
    
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
        
        elif "オーガ" in self.current_enemy.name:
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
        
        else:
            # ダークナイト
            # 鎧
            pygame.draw.rect(self.screen, self.current_enemy.color,
                           (x - 30, y - 30, 60, 60))
            pygame.draw.rect(self.screen, (100, 100, 100),
                           (x - 30, y - 30, 60, 60), 3)
            
            # 兜
            pygame.draw.polygon(self.screen, (30, 0, 30),
                              [(x - 25, y - 40), (x + 25, y - 40),
                               (x + 20, y - 60), (x - 20, y - 60)])
            pygame.draw.polygon(self.screen, (100, 100, 100),
                              [(x - 25, y - 40), (x + 25, y - 40),
                               (x + 20, y - 60), (x - 20, y - 60)], 2)
            
            # 目（赤く光る）
            pygame.draw.circle(self.screen, (255, 0, 0), (x - 10, y - 45), 5)
            pygame.draw.circle(self.screen, (255, 0, 0), (x + 10, y - 45), 5)
            
            # 剣
            pygame.draw.line(self.screen, (150, 150, 150),
                           (x + 35, y - 60), (x + 45, y + 20), 5)
            pygame.draw.line(self.screen, (200, 200, 200),
                           (x + 35, y - 60), (x + 45, y + 20), 2)
    
    def draw_enemy_status(self):
        """敵のステータスバー"""
        x = 490
        y = 60
        self.draw_rect(x, y, 300, 120, DARK_GRAY)
        self.draw_rect(x, y, 300, 120, WHITE, 2)
        
        # 名前とレベル
        self.draw_text(f"{self.current_enemy.name} Lv.{self.current_enemy.level}",
                      x + 10, y + 10, WHITE, use_jp=True)
        
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
        
        # 獲得経験値
        self.draw_text(f"EXP: {self.current_enemy.exp}", x + 10, y + 90,
                      YELLOW, self.font_small)
    
    def draw_all_clear(self):
        """全クリア画面"""
        self.draw_text("ALL CLEAR!", 400, 100, YELLOW, self.font_xlarge, center=True)
        self.draw_text("すべての敵をたおした！", 400, 180, WHITE,
                      self.font_jp_large, center=True, use_jp=True)
        
        # 結果表示
        self.draw_rect(150, 230, 500, 300, DARK_GRAY)
        self.draw_rect(150, 230, 500, 300, WHITE, 2)
        
        self.draw_text(f"{self.hero.name}の勝利！", 400, 260, WHITE,
                      self.font_jp_medium, center=True, use_jp=True)
        
        # 最終ステータス
        self.draw_text(f"最終レベル：{self.hero.level}", 400, 310, YELLOW,
                      self.font_jp_medium, center=True, use_jp=True)
        self.draw_text(f"獲得した総経験値：{self.hero.exp + sum(int(self.hero.next_exp / 1.5**i) for i in range(self.hero.level-1, 0, -1))}",
                      400, 350, WHITE, self.font_jp_medium, center=True, use_jp=True)
        
        # ステータス表示
        stats = [
            f"HP: {self.hero.max_hp}",
            f"MP: {self.hero.max_mp}",
            f"こうげき力: {self.hero.attack}",
            f"まほう力: {self.hero.magic_power}",
            f"ぼうぎょ力: {self.hero.defense}"
        ]
        
        y = 400
        for stat in stats:
            self.draw_text(stat, 400, y, GREEN,
                          self.font_jp_small, center=True, use_jp=True)
            y += 25
        
        self.draw_text("Rキーでもう一度 / Qキーで終了", 400, 550, GRAY,
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
    
    def draw_intro(self):
        """イントロ画面"""
        self.draw_message_box(self.message_queue)
        self.draw_text("何かキーを押してください", 400, 500, GRAY,
                      self.font_jp_medium, center=True, use_jp=True)
    
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
        
        # レベルに応じた装飾
        if self.hero.level >= 3:
            # 肩当て
            pygame.draw.polygon(self.screen, (192, 192, 192),
                              [(x - 30, y - 20), (x - 25, y - 15),
                               (x - 25, y - 5), (x - 35, y - 10)])
            pygame.draw.polygon(self.screen, (192, 192, 192),
                              [(x + 30, y - 20), (x + 25, y - 15),
                               (x + 25, y - 5), (x + 35, y - 10)])
        
        # 顔
        pygame.draw.circle(self.screen, (255, 220, 177), (x, y - 35), 15)
        pygame.draw.circle(self.screen, BLACK, (x, y - 35), 15, 2)
        
        # 目
        pygame.draw.circle(self.screen, BLACK, (x - 5, y - 38), 2)
        pygame.draw.circle(self.screen, BLACK, (x + 5, y - 38), 2)
        
        # アイテムポーチ
        pygame.draw.rect(self.screen, (139, 69, 19), (x - 30, y + 5, 10, 15))
        pygame.draw.rect(self.screen, BLACK, (x - 30, y + 5, 10, 15), 1)
        
        # 杖（レベルに応じて豪華に）
        staff_color = (139, 69, 19) if self.hero.level < 5 else (255, 215, 0)
        pygame.draw.line(self.screen, staff_color,
                        (x + 25, y + 10), (x + 35, y - 40), 4)
        
        # 杖の先の宝石
        gem_color = (255, 0, 255) if self.hero.level < 5 else (0, 255, 255)
        pygame.draw.circle(self.screen, gem_color, (x + 35, y - 40), 6 + self.hero.level // 2)
        pygame.draw.circle(self.screen, WHITE, (x + 35, y - 40), 6 + self.hero.level // 2, 2)
    
    def draw_dropped_item(self):
        """ドロップアイテムの表示"""
        alpha = min(255, self.drop_timer * 8)
        
        # アイテムアイコン
        x, y = 400, 250
        size = 40
        
        # 背景の光
        for i in range(3):
            radius = size + i * 10
            color = (255, 215, 0, alpha // (i + 1))
            glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow, color, (radius, radius), radius)
            self.screen.blit(glow, (x - radius, y - radius))
        
        # アイテムボックス
        box_color = (200, 150, 100) if self.dropped_item != "エリクサー" else (150, 100, 200)
        pygame.draw.rect(self.screen, box_color, (x - size//2, y - size//2, size, size))
        pygame.draw.rect(self.screen, WHITE, (x - size//2, y - size//2, size, size), 2)
        
        # アイテム名
        text_surface = self.font_jp_medium.render(self.dropped_item, True, WHITE)
        text_surface.set_alpha(alpha)
        rect = text_surface.get_rect(center=(x, y + size))
        self.screen.blit(text_surface, rect)
    
    def draw_item_menu(self):
        """アイテムメニュー"""
        x = 250
        y = 150
        width = 300
        height = 300
        
        # 背景
        self.draw_rect(x - 10, y - 10, width + 20, height + 20, DARK_GRAY)
        self.draw_rect(x - 10, y - 10, width + 20, height + 20, WHITE, 2)
        
        # タイトル
        self.draw_text("アイテムを選んでください", x + width // 2, y - 30,
                      WHITE, self.font_jp_medium, center=True, use_jp=True)
        
        # 使用可能なアイテム
        available_items = [(name, count) for name, count in self.hero.items.items() if count > 0]
        
        if not available_items:
            self.draw_text("使えるアイテムがありません", x + width // 2, y + 50,
                          GRAY, self.font_jp_medium, center=True, use_jp=True)
        else:
            item_info = {
                "ポーション": "HPを30回復",
                "エーテル": "MPを15回復",
                "ハイポーション": "HPを60回復",
                "エリクサー": "HPとMPを全回復"
            }
            
            for i, (name, count) in enumerate(available_items):
                item_y = y + 30 + i * 60
                
                # 選択中の項目はハイライト
                if i == self.selected_item:
                    self.draw_rect(x, item_y - 5, width, 50, BLUE)
                
                self.draw_text(f"{name} (×{count})", x + 10, item_y,
                              WHITE, self.font_jp_medium, use_jp=True)
                desc = item_info.get(name, "")
                self.draw_text(desc, x + 10, item_y + 25,
                              GRAY, self.font_jp_small, use_jp=True)
        
        # もどる
        back_y = y + 30 + len(available_items) * 60
        if self.selected_item == len(available_items):
            self.draw_rect(x, back_y - 5, width, 30, BLUE)
        self.draw_text("もどる", x + 10, back_y,
                      WHITE, self.font_jp_medium, use_jp=True)
    
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
    
    def draw_item_particles(self):
        """アイテムエフェクトパーティクルを描画"""
        for particle in self.item_effect_particles:
            alpha = particle["life"] / 30.0
            color = tuple(int(c * alpha) for c in particle["color"])
            
            pygame.draw.circle(self.screen, color,
                             (int(particle["x"]), int(particle["y"])),
                             5)
            
            # 光の尾
            tail_color = tuple(int(c * alpha * 0.5) for c in particle["color"])
            pygame.draw.line(self.screen, tail_color,
                           (particle["x"], particle["y"]),
                           (particle["x"] - particle["vx"] * 3,
                            particle["y"] - particle["vy"] * 3), 2)

def main():
    game = LevelUpGame()
    game.run()

if __name__ == "__main__":
    main()