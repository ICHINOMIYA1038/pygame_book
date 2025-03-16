#
# <ミドル２コース Python課題 2月号 ゲームタイトル作成>
#

# partsファイル(パーツファイル)をインポート
from parts import *
from shooting import *

#
# メインタイトル
#
def main_title():
    g.bgm_level = 0.5
    set_bgm_level(g.bgm_level)
    while g.mode == g.MODE_MAIN_TITLE:
        draw_main_haikei()
        draw_rpg()
        draw_sf()
        update_and_eventchk()

#
# RPGタイトル
#
def rpg_title():
    if g.mode == g.MODE_RPG:
        g.alpha = 0
        g.fade_in_haikei = True
        g.selected_item = 1
        g.blink_interval = 500
        start_time = None
        play_bgm_rpg()
        move_done = False
        while g.mode == g.MODE_RPG:
            draw_rpg_haikei()
            if move_done == False and move_cursor() == 1:
                move_done = True
                start_time = pygame.time.get_ticks()
            if start_time is not None and pygame.time.get_ticks() - start_time >= 500:
                g.fade_out_haikei = True
            if start_time is not None and pygame.time.get_ticks() - start_time >= 1500:
                g.mode = g.MODE_RPG_START
            blink_cursor()
            update_and_eventchk()

#
# RPG決定
#
def rpg_start():
    stop_bgm()
    if g.mode == g.MODE_RPG_START:
        g.last_update_time = pygame.time.get_ticks()
        g.text_index = 0
        g.display_text = ""
        match g.selected_item:
            case 1:
                serihu = "ぼうけんのはじまりだ！"
            case 2:
                serihu = "ぼうけんのきろくをよみこむよ"
            case 3:
                serihu = "せっていをかえるよ"
            case 4:
                serihu = "またあそんでね！"
            case _:
                serihu = ""
        while g.mode == g.MODE_RPG_START:
            draw_main_haikei()
            draw_neko()
            serihu_end = update_text(serihu)
            draw_hukidashi(260, 160, g.display_text)
            if serihu_end:
                break
            update_and_eventchk()
        wait_time(len(serihu)/4)
        g.mode = g.MODE_MAIN_TITLE

#
# テキスト表示するタイミングを返す処理
#
def text_timer():
    current_time = pygame.time.get_ticks()
    if current_time - g.last_update_time > g.char_interval:
        g.last_update_time = current_time
        return True
    else:
        return False

#
# テキストの更新
#
def update_text(full_text):
    #✅プログラミングチャレンジ2
    #g.display_text = full_text
    if text_timer():
        play_message_rpg_snd()
        g.display_text += full_text[g.text_index]
        g.text_index += 1

    return len(g.display_text) >= len(full_text)

#
# SF タイトル
#
def sf_title():
    if g.mode == g.MODE_SF:
        play_bgm_sf()
        g.fade_in_haikei = True
        g.alpha = 0
        g.selected_item = 1

        while g.mode == g.MODE_SF:
            if move_cursor() == 1:
                break
            draw_sf_haikei()
            draw_sf_menu()
            update_and_eventchk()

        # 発光処理
        g.white_alpha = 255
        g.fade_in_white = False
        g.fade_out_white = True
        while g.mode == g.MODE_SF:
            for _ in range(10):
                draw_sf_haikei()
                draw_sf_menu()
                draw_shine()
                update_and_eventchk()
            break

        # 背景が消える
        g.alpha = 255
        g.fade_speed = 10
        g.fade_in_haikei = False
        g.fade_out_haikei = True
        while g.mode == g.MODE_SF:
            for _ in range(26):
                g.bgm_level -= 0.5 / 20
                if g.bgm_level < 0:
                    g.bgm_level = 0
                set_bgm_level(g.bgm_level)

                draw_sf_haikei()
                update_and_eventchk()
            g.mode = g.MODE_SF_START
#
# SF 決定
#
def sf_start():
    stop_bgm()
    if g.mode == g.MODE_SF_START:
        wait_time(0.5)
        g.neko_y = 0
        g.neko_speed = 50
        serihu = ""
        while g.mode == g.MODE_SF_START:
            g.screen.fill((0, 0, 0))
            draw_landing_neko()
            if fall_neko():
                break
            update_and_eventchk()

        menu = ":"
        serihu = ""
        match g.selected_item:
            case 1:
                menu = "START:"
                setumei = " ゲーム開始！"
            case 2:
                menu = "ONLINE:"
                setumei = " オンラインで遊ぶ"
            case 3:
                menu = "OPTION:"
                setumei = " 設定変更"
            case 4:
                menu = "EXIT:"
                setumei = " またあそんでね"

        # ねこがセリフを話す処理
        g.last_update_time = pygame.time.get_ticks()
        g.text_index = 0
        g.display_text = ""
        end = True
        while g.mode == g.MODE_SF_START:
            #✅プログラミングチャレンジ3
            serihu = menu + setumei
            end = update_text(serihu)
            draw_hukidashi(260, 300, g.display_text)
            if end:
                break
            update_and_eventchk()

        wait_time(len(serihu)/4)

        #✅プログラミングチャレンジ4
        g.last_update_time = pygame.time.get_ticks()
        g.text_index = 0
        g.display_text = ""
        end = True
        while g.mode == g.MODE_SF_START:
            end = update_text("この世界を救うのはキミだけニャ！")
            draw_hukidashi(260, 300, g.display_text)
            if end:
                break
            update_and_eventchk()
        wait_time(len(serihu)/4)

        pygame.quit()
        shooting()

#
# 開始
#
def start():
    #初期化（しょきか）
    parts_init()

    while True:
        main_title()

        rpg_title()
        rpg_start()

        sf_title()
        sf_start()

#
# 🔰ここからメインプログラムを開始しています
#
start()
