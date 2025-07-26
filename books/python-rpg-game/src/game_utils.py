"""
RPGゲーム共通ユーティリティ
"""
import pygame
import sys

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# 画面サイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# フォントサイズ
FONT_SMALL = 16
FONT_MEDIUM = 24
FONT_LARGE = 32
FONT_XLARGE = 48

class GameBase:
    """ゲームの基本クラス"""
    def __init__(self, title="RPGゲーム"):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # フォントの初期化
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        self.font_xlarge = pygame.font.Font(None, FONT_XLARGE)
        
        # 日本語フォントを探す
        font_paths = [
            # macOS標準の日本語フォント
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
            # 代替フォント
            "/System/Library/Fonts/Helvetica.ttc",
            # プロジェクト内のフォント
            "assets/fonts/NotoSansJP-Regular.ttf",
        ]
        
        font_found = False
        for font_path in font_paths:
            try:
                self.font_jp_small = pygame.font.Font(font_path, FONT_SMALL)
                self.font_jp_medium = pygame.font.Font(font_path, FONT_MEDIUM)
                self.font_jp_large = pygame.font.Font(font_path, FONT_LARGE)
                font_found = True
                print(f"日本語フォントを読み込みました: {font_path}")
                break
            except:
                continue
        
        if not font_found:
            # 日本語フォントがない場合はシステムフォントを使用
            print("警告: 日本語フォントが見つかりません。デフォルトフォントを使用します。")
            self.font_jp_small = self.font_small
            self.font_jp_medium = self.font_medium
            self.font_jp_large = self.font_large
    
    def handle_events(self):
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            self.on_event(event)
        return True
    
    def on_event(self, event):
        """イベントハンドラ（オーバーライド用）"""
        pass
    
    def update(self):
        """更新処理（オーバーライド用）"""
        pass
    
    def draw(self):
        """描画処理（オーバーライド用）"""
        self.screen.fill(BLACK)
    
    def draw_text(self, text, x, y, color=WHITE, font=None, center=False, use_jp=False):
        """テキストを描画"""
        if font is None:
            font = self.font_jp_medium if use_jp else self.font_medium
        
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        
        self.screen.blit(surface, rect)
        return rect
    
    def draw_rect(self, x, y, width, height, color, border_width=0):
        """矩形を描画"""
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, border_width)
        return rect
    
    def draw_button(self, text, x, y, width, height, 
                   bg_color=GRAY, text_color=WHITE, 
                   hover_color=LIGHT_GRAY, border_color=WHITE,
                   use_jp=False):
        """ボタンを描画"""
        mouse_pos = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, width, height)
        
        # ホバー判定
        is_hover = rect.collidepoint(mouse_pos)
        color = hover_color if is_hover else bg_color
        
        # ボタン背景
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, border_color, rect, 2)
        
        # テキスト
        font = self.font_jp_medium if use_jp else self.font_medium
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return rect, is_hover
    
    def draw_menu(self, title, items, x, y, width, item_height=50, 
                 selected_index=0, use_jp=False):
        """メニューを描画"""
        # タイトル
        self.draw_text(title, x + width // 2, y - 40, 
                      WHITE, self.font_jp_large if use_jp else self.font_large, 
                      center=True, use_jp=use_jp)
        
        # メニュー項目
        rects = []
        for i, item in enumerate(items):
            item_y = y + i * (item_height + 10)
            
            # 選択中の項目は色を変える
            if i == selected_index:
                bg_color = BLUE
                text_color = WHITE
            else:
                bg_color = GRAY
                text_color = WHITE
            
            rect, _ = self.draw_button(item, x, item_y, width, item_height,
                                     bg_color=bg_color, text_color=text_color,
                                     use_jp=use_jp)
            rects.append(rect)
        
        return rects
    
    def draw_status_bar(self, name, hp, max_hp, mp, max_mp, level=1, x=10, y=10):
        """ステータスバーを描画"""
        # 背景
        self.draw_rect(x, y, 300, 100, DARK_GRAY)
        self.draw_rect(x, y, 300, 100, WHITE, 2)
        
        # 名前とレベル
        self.draw_text(f"{name} Lv.{level}", x + 10, y + 10, WHITE)
        
        # HPバー
        hp_ratio = hp / max_hp if max_hp > 0 else 0
        self.draw_text("HP:", x + 10, y + 35, WHITE)
        self.draw_rect(x + 50, y + 35, 200, 20, DARK_GRAY)
        self.draw_rect(x + 50, y + 35, int(200 * hp_ratio), 20, RED)
        self.draw_rect(x + 50, y + 35, 200, 20, WHITE, 2)
        self.draw_text(f"{hp}/{max_hp}", x + 260, y + 35, WHITE)
        
        # MPバー
        mp_ratio = mp / max_mp if max_mp > 0 else 0
        self.draw_text("MP:", x + 10, y + 65, WHITE)
        self.draw_rect(x + 50, y + 65, 200, 20, DARK_GRAY)
        self.draw_rect(x + 50, y + 65, int(200 * mp_ratio), 20, BLUE)
        self.draw_rect(x + 50, y + 65, 200, 20, WHITE, 2)
        self.draw_text(f"{mp}/{max_mp}", x + 260, y + 65, WHITE)
    
    def draw_message_box(self, messages, x=50, y=400, width=700, height=150):
        """メッセージボックスを描画"""
        # 背景
        self.draw_rect(x, y, width, height, DARK_GRAY)
        self.draw_rect(x, y, width, height, WHITE, 2)
        
        # メッセージ
        if isinstance(messages, str):
            messages = [messages]
        
        for i, message in enumerate(messages[:5]):  # 最大5行
            self.draw_text(message, x + 20, y + 20 + i * 25, WHITE, use_jp=True)
    
    def wait_for_key(self):
        """キー入力を待つ"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    return True
            self.clock.tick(30)
        return False
    
    def run(self):
        """メインループ"""
        while self.running:
            # イベント処理
            if not self.handle_events():
                break
            
            # 更新
            self.update()
            
            # 描画
            self.draw()
            pygame.display.flip()
            
            # FPS制御
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

class TextInput:
    """テキスト入力クラス"""
    def __init__(self, x, y, width, height, font=None, max_length=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = font or pygame.font.Font(None, FONT_MEDIUM)
        self.active = False
        self.max_length = max_length
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def handle_event(self, event):
        """イベント処理"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # クリックで選択/非選択
            self.active = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True  # 入力完了
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < self.max_length:
                    self.text += event.unicode
        
        return False
    
    def update(self):
        """更新処理"""
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer > 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
    
    def draw(self, screen):
        """描画"""
        # 背景
        color = WHITE if self.active else LIGHT_GRAY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # テキスト
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 5, self.rect.centery))
        screen.blit(text_surface, text_rect)
        
        # カーソル
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            pygame.draw.line(screen, BLACK, 
                           (cursor_x, self.rect.y + 5),
                           (cursor_x, self.rect.bottom - 5), 2)