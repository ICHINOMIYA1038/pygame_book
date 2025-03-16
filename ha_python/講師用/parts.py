#
#   parts.py
#

import pygame
from pygame.locals import *
import pygame.mixer
import sys
import time
import math

# 定数定義（じょうすう／ていすう　ていぎ）
WIDTH = 640          # 画面横幅の設定
HIGHT = 480          # 画面高さの設定

RED = (255, 0, 0)            # 赤
GREEN = (0, 255, 0)          # 緑
BLUE = (0, 0, 255)           # 青
YELLOW = (255, 255, 0)       # 黄
CYAN = (0, 255, 255)         # シアン
MAGENTA = (255, 0, 255)      # マゼンタ
WHITE = (255, 255, 255)      # 白
BLACK = (0, 0, 0)            # 黒
GRAY = (0xe6, 0xf0, 0xff)    # 灰色
DARKGRAY = (0x57, 0x5e, 0x75) # 黒灰色
ORANGE = (255, 0x8c, 0x1a)   # 橙色

#グローバル変数の初期化
class g:
    MODE_MAIN_TITLE = 0
    MODE_RPG = 1
    MODE_SF = 2
    MODE_RPG_START = 4
    MODE_SF_START = 5
    mode = 0
    cursor_pos = (215, 280)
    selected_item = 1
    last_blink_time = 0
    show_image = False
    blink_interval = 500
    key_states = {}
    alpha = 0
    white_alpha = 0
    fade_speed = 25
    fade_in_haikei = False
    fade_out_haikei = False
    text_index = 0
    display_text = ""
    char_interval = 30
    landing_neko_costume = []
    neko_costume_num = 0
    landing_start_time = 0
    angle = 0
    fade_in_white = False
    fade_out_white = False
    bgm_level = 0.5

#
# 初期化処理
#
def parts_init():
    pygame.init()

    g.mode = g.MODE_MAIN_TITLE
    g.clock = pygame.time.Clock()
    g.last_blink_time = pygame.time.get_ticks()

    try:
        pygame.mixer.init()
        g.sound_ok = True
    except Exception as e:
        print(f"サウンド初期化エラーが発生しました: {e}")
        g.sound_ok = False

    g.screen = pygame.display.set_mode((WIDTH, HIGHT))
    g.font = pygame.font.SysFont("meiryo", 20)

    # 画像の準備
    prepare_image()

    # サウンドの準備
    prepare_sound()

    # ウインドウタイトルを設定
    pygame.display.set_icon(g.neko) ####
    pygame.display.set_caption('ゲームタイトル作成') ####

# 画像のサイズ設定処理
# （画像をロードし、サイズを取得後、サイズ変更する）
# load_and_scale_image(画像パス, 変更倍率):
def load_and_scale_image(path, scale_factor):
    image = pygame.image.load(path).convert_alpha()
    original_width, original_height = image.get_size()
    new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
    return pygame.transform.scale(image, new_size)

# スプライト設定処理
# （画像をロードし、サイズ、位置を設定する）
def prepare_sprite(image, scale, init_pos):
    sprite = pygame.sprite.Sprite()
    sprite.image = load_and_scale_image(image, scale)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = init_pos
    sprite.mask = pygame.mask.from_surface(sprite.image)
    return sprite

#
# 画像準備
#
def prepare_image():
    # 背景画像はサイズ指定でロード（手動でサイズを指定）
    g.main_haikei = pygame.image.load("img/白塗り.png").convert()
    g.main_haikei = pygame.transform.scale(g.main_haikei, (WIDTH, HIGHT))
    g.sf_haikei = pygame.image.load("img/title_SF.png").convert_alpha()
    g.sf_haikei = pygame.transform.scale(g.sf_haikei, (WIDTH, HIGHT))
    g.rpg_haikei = pygame.image.load("img/title_RPG.png").convert_alpha()
    g.rpg_haikei = pygame.transform.scale(g.rpg_haikei, (WIDTH, HIGHT))
    g.white_haikei = pygame.image.load("img/白塗り.png").convert_alpha()
    g.white_haikei = pygame.transform.scale(g.white_haikei, (WIDTH, HIGHT))

    g.rpg_image = load_and_scale_image("img/RPG.png", 2/3)
    g.sf_image = load_and_scale_image("img/SF.png", 2/3)
    g.rpg_image_rect = g.rpg_image.get_rect()
    g.sf_image_rect = g.sf_image.get_rect()

    g.dot_neko  = load_and_scale_image("img/ドット_ネコ.png", 1/10)
    g.neko = load_and_scale_image("img/cat-a.png", 1/2)
    g.landing_neko_costume.append(g.neko)
    g.landing_neko_costume.append(load_and_scale_image("img/1.png", 1/2))
    g.landing_neko_costume.append(load_and_scale_image("img/2.png", 1/2))
    g.landing_neko_costume.append(load_and_scale_image("img/3.png", 1/2))
    g.landing_neko_costume.append(load_and_scale_image("img/4.png", 1/2))
    g.landing_neko_costume.append(load_and_scale_image("img/5.png", 1/2))
    g.landing_neko_costume.append(load_and_scale_image("img/6.png", 1/2))
    g.landing_neko_costume.append(load_and_scale_image("img/7.png", 1/2))
    g.landing_neko_costume.append(load_and_scale_image("img/8.png", 1/2))

    g.sf_exit_image = load_and_scale_image("img/SF_EXIT.png", 1)
    g.sf_online_image = load_and_scale_image("img/SF_ONLINE.png", 1)
    g.sf_option_image = load_and_scale_image("img/SF_OPTION.png", 1)
    g.sf_start_image = load_and_scale_image("img/SF_START.png", 1)
    g.sf_exit_small_image = load_and_scale_image("img/SF_EXIT.png", 2/3)
    g.sf_exit_small_image = adjust_brightness(g.sf_exit_small_image, -120)
    g.sf_online_small_image = load_and_scale_image("img/SF_ONLINE.png", 2/3)
    g.sf_online_small_image = adjust_brightness(g.sf_online_small_image, -120)
    g.sf_option_small_image = load_and_scale_image("img/SF_OPTION.png", 2/3)
    g.sf_option_small_image = adjust_brightness(g.sf_option_small_image, -120)
    g.sf_start_small_image = load_and_scale_image("img/SF_START.png", 2/3)
    g.sf_start_small_image = adjust_brightness(g.sf_start_small_image, -120)
    g.cursor = load_and_scale_image("img/カーソル_RPG.png", 1)
    g.hukidashi = load_and_scale_image("img/吹き出し_long.png", 2/3)
    g.inv_hukidashi = pygame.transform.flip(g.hukidashi, True, False)

#
# 音声ファイルの読み出しとボリューム設定
#
def load_sound_and_set_volume(audio_file, volume):
    sound = pygame.mixer.Sound(audio_file)
    sound.set_volume(volume)
    return sound

#
# 音準備
#
def prepare_sound():
    if g.sound_ok:
        g.bgm_rpg_snd = load_sound_and_set_volume("sound/BGM(RPG).wav", 0.5)
        g.bgm_sf_snd = load_sound_and_set_volume("sound/BGM(SF).wav", 0.5)
        g.cursor_move_rpg_snd = load_sound_and_set_volume("sound/カーソル移動(RPG).mp3", 0.5)
        g.cursor_move_sf_snd = load_sound_and_set_volume("sound/カーソル移動(SF).wav", 0.5)
        g.pop_snd = load_sound_and_set_volume("sound/ポップ.wav", 0.5)
        g.message_rpg_snd = load_sound_and_set_volume("sound/メッセージ表示(RPG).mp3", 0.5)
        g.start_rpg_snd = load_sound_and_set_volume("sound/決定ボタン(RPG).mp3", 0.5)
        g.start_sf_snd = load_sound_and_set_volume("sound/決定ボタン(SF).mp3", 0.5)
 
#
# メイン背景の描画
#
def draw_main_haikei():
    g.screen.blit(g.main_haikei, (0,0))

#
# 発光画面の描画
#
def draw_shine():
    if g.fade_in_white == True:
        g.white_alpha += g.fade_speed
        if g.white_alpha >= 255:
            g.white_alpha = 255
            g.fade_in_white = False
    if g.fade_out_white == True:
        g.white_alpha -= g.fade_speed
        if g.white_alpha <= 0:
            g.white_alpha = 0
            g.fade_out_white = False

    image = g.white_haikei
    image.set_alpha(g.white_alpha)
    g.screen.blit(image, (0,0))

#
# RPG 背景の描画
#
def draw_rpg_haikei():
    if g.fade_in_haikei == True:
        g.alpha += g.fade_speed
        if g.alpha >= 255:
            g.alpha = 255
            g.fade_in_haikei = False
    if g.fade_out_haikei == True:
        g.bgm_level -= 0.5 / 20
        if g.bgm_level < 0:
            g.bgm_level = 0
        set_bgm_level(g.bgm_level)
        g.screen.fill((0, 0, 0))
        g.alpha -= g.fade_speed
        if g.alpha <= 0:
            g.alpha = 0
            g.fade_out_haikei = False

    g.rpg_haikei.set_alpha(g.alpha)
    g.screen.blit(g.rpg_haikei, (0,0))

#
# SF 背景の描画
#
def draw_sf_haikei():
    if g.fade_in_haikei == True:
        g.alpha += g.fade_speed
        if g.alpha >= 255:
            g.alpha= 255
            g.fade_in_haikei = False
    if g.fade_out_haikei == True:
        g.screen.fill((0, 0, 0))
        g.alpha -= g.fade_speed
        if g.alpha <= 0:
            g.alpha = 0
            g.fade_out_haikei = False

    g.sf_haikei.set_alpha(g.alpha)
    g.screen.blit(g.sf_haikei, (0,0))

#
# SF メニューの描画
#
def draw_sf_menu():
    draw_sf_start()
    draw_sf_online()
    draw_sf_option()
    draw_sf_exit()


#
# RPG選択ボタンの描画
#
def draw_rpg():
    rpg_pos = (230,100)
    g.screen.blit(g.rpg_image, rpg_pos)
    g.rpg_image_rect.topleft = rpg_pos

#
# SF選択ボタンの描画
#
def draw_sf():
    sf_pos = (230,280)
    g.screen.blit(g.sf_image, sf_pos)
    g.sf_image_rect.topleft = sf_pos

#
# カーソルの描画
#
def draw_cursor():
    g.screen.blit(g.cursor, (g.cursor_pos[0], g.cursor_pos[1] + (g.selected_item - 1) * 40))

#
# ねこの描画
#
def draw_neko():
    g.screen.blit(g.dot_neko, (200,200))

#
# 着地ねこの描画
#
def draw_landing_neko():
    g.screen.blit(g.landing_neko_costume[g.neko_costume_num], (200, g.neko_y))

#
# SF START メニューの描画
#
def draw_sf_start():
    if g.selected_item == 1:
        g.angle += 30
        angle_radians = math.radians(g.angle)
        g.screen.blit(adjust_brightness(g.sf_start_image, math.sin(angle_radians) * 50), (220,220))
    else:
        g.screen.blit(g.sf_start_small_image, (250,230))

#
# SF ONLINE メニューの描画
#
def draw_sf_online():
    if g.selected_item == 2:
        g.angle += 30
        angle_radians = math.radians(g.angle)
        g.screen.blit(adjust_brightness(g.sf_online_image, math.sin(angle_radians) * 50), (220,270))
    else:
        g.screen.blit(g.sf_online_small_image, (250,280))

#
# SF OPTION メニューの描画
#
def draw_sf_option():
    if g.selected_item == 3:
        g.angle += 30
        angle_radians = math.radians(g.angle)
        g.screen.blit(adjust_brightness(g.sf_option_image, math.sin(angle_radians) * 50), (220,320))
    else:
        g.screen.blit(g.sf_option_small_image, (250,330))

#
# SF EXIT メニューの描画
#
def draw_sf_exit():
    if g.selected_item == 4:
        g.angle += 30
        angle_radians = math.radians(g.angle)
        g.screen.blit(adjust_brightness(g.sf_exit_image, math.sin(angle_radians) * 50), (220,370))
    else:
        g.screen.blit(g.sf_exit_small_image, (250,380))

#
# RPG カーソル移動音再生
#
def play_cursor_move_rpg_snd():
    if g.sound_ok:
        g.cursor_move_rpg_snd.play()

#
# SF カーソル移動音再生
#
def play_cursor_move_sf_snd():
    if g.sound_ok:
        g.cursor_move_sf_snd.play()

#
# POP音再生
#
def play_pop_snd():
    if g.sound_ok:
        g.pop_snd.play()

#
# RPG Message音再生
#
def play_message_rpg_snd():
    if g.sound_ok:
        g.message_rpg_snd.play()

#
# RPG 開始音再生
#
def play_start_rpg_snd():
    if g.sound_ok:
        g.start_rpg_snd.play()

#
# SF 開始音再生
#
def play_start_sf_snd():
    if g.sound_ok:
        g.start_sf_snd.play()

#
# RPG BGM再生
#
def play_bgm_rpg():
    if g.sound_ok:
        g.bgm_rpg_snd.play(-1)

#
# SF BGM再生
#
def play_bgm_sf():
    if g.sound_ok:
        g.bgm_sf_snd.play(-1)

#
# BGMレベル設定
#
def set_bgm_level(level):
    if g.sound_ok:
        g.bgm_rpg_snd.set_volume(level)
        g.bgm_sf_snd.set_volume(level)

#
# BGM再生を止める
#
def stop_bgm():
    if g.sound_ok:
        g.bgm_rpg_snd.stop()
        g.bgm_sf_snd.stop()

#
# カーソルの移動
#
def move_cursor():
    keys = pygame.key.get_pressed()

    target_key = pygame.K_UP
    if keys[target_key]:
        if not g.key_states.get(target_key, False):
            g.key_states[target_key] = True
            if g.selected_item > 1:
                g.selected_item -= 1
                if g.mode == g.MODE_RPG:
                    play_cursor_move_rpg_snd()
                else:
                    play_cursor_move_sf_snd()
    else:
        g.key_states[target_key] = False

    target_key = pygame.K_DOWN
    if keys[target_key]:
        if not g.key_states.get(target_key, False):
            g.key_states[target_key] = True
            if g.selected_item < 4:
                g.selected_item += 1
                if g.mode == g.MODE_RPG:
                    play_cursor_move_rpg_snd()
                else:
                    play_cursor_move_sf_snd()
    else:
        g.key_states[target_key] = False

    target_key = pygame.K_SPACE
    if keys[target_key]:
        if not g.key_states.get(target_key, False):
            g.key_states[target_key] = True
            g.blink_interval = 50
            if g.mode == g.MODE_RPG:
                play_start_rpg_snd()
            else:
                play_start_sf_snd()
            return 1
    else:
        g.key_states[target_key] = False

    return 0

#
# カーソルの点滅処理
#
def blink_cursor():
    current_time = pygame.time.get_ticks()

    if current_time - g.last_blink_time > g.blink_interval:
        g.show_image = not g.show_image
        g.last_blink_time = current_time

    if g.show_image and not g.fade_out_haikei:
        draw_cursor()


#
# ねこの落下処理
#
def fall_neko():
    end = False
    if g.neko_y < 350:
        g.neko_y += g.neko_speed
        if g.neko_y < 350:
            g.neko_costume_num = 4
        else:
            if g.neko_costume_num == 2:
                g.neko_costume_num = 3
            else:
                g.neko_costume_num = 2
        g.neko_speed += 1
    elif g.neko_y > 350:
        g.neko_y = 350
        g.neko_costume_num = 5
        g.landing_start_time = pygame.time.get_ticks()

    if g.neko_y == 350:
        current_time = pygame.time.get_ticks()
        if current_time - g.landing_start_time > 300:
            end = True
        elif current_time - g.landing_start_time > 250:
            g.neko_costume_num = 8
        elif current_time - g.landing_start_time > 200:
            g.neko_costume_num = 7
        elif current_time - g.landing_start_time > 150:
            g.neko_costume_num = 6
        elif current_time - g.landing_start_time > 100:
            g.neko_costume_num = 5

    return end

#
# 明るさを調整する関数
#
def adjust_brightness(surface, brightness):
    adjusted_surface = surface.copy()

    if brightness > 0:
        # 明るくする: 白をブレンド
        overlay = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((brightness, brightness, brightness, 0))
        adjusted_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    elif brightness < 0:
        # 暗くする: 黒をブレンド
        overlay = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((-brightness, -brightness, -brightness, 0))
        adjusted_surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

    return adjusted_surface

#
# 吹き出しにテキストを描く
#  左右反転対応
#
def draw_hukidashi(x, y, text_char):
    text = g.font.render(text_char, True, BLACK)
    if x > WIDTH / 2:
        g.screen.blit(g.inv_hukidashi, (x - 140, y))
        text_rect = text.get_rect(topleft=(x - 140 + 10, y + 5))
    else:
        g.screen.blit(g.hukidashi, (x, y))
        text_rect = text.get_rect(topleft=(x + 10, y + 5))
    g.screen.blit(text, text_rect)

#
# 指定された時間(秒)待つ
#
def wait_time(times):
    StartTime = pygame.time.get_ticks()
    while True:
        pygame.time.delay(10)
        pygame.display.update()

        if (pygame.time.get_ticks() - StartTime) > times * 1000:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#
# マウスイベント処理
#
def mouse_event(event):
    mouse_pos = event.pos
    if g.mode == g.MODE_MAIN_TITLE:
        if g.rpg_image_rect.collidepoint(mouse_pos):
            g.mode = g.MODE_RPG
            play_pop_snd()
            wait_time(1)
        if g.sf_image_rect.collidepoint(mouse_pos):
            g.mode = g.MODE_SF
            play_pop_snd()
            wait_time(1)

#
# 画面更新とユーザー操作を監視
#
def update_and_eventchk():
    pygame.display.update()
    g.clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_event(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
