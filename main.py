import sys
import pygame
import asyncio
from pygame.locals import *

# ゲームの状態を定義する定数
GAME_STATE_START_SCREEN = 0        # スタート画面
GAME_STATE_STAGE1_PLAYING = 1      # ステージ1プレイ中
GAME_STATE_STAGE1_CLEARED = 2      # ステージ1クリア後（NEXTボタン表示）
GAME_STATE_STAGE2_PLAYING = 3      # ステージ2プレイ中
GAME_STATE_STAGE2_CLEARED = 4      # ステージ2クリア後（NEXTボタン表示）
GAME_STATE_STAGE3_PLAYING = 5      # ステージ3プレイ中（回答1表示）
GAME_STATE_STAGE3_SHOW_MESSAGE_AND_A2 = 6 # ステージ3メッセージ表示中かつ回答2がクリック可能
GAME_STATE_GAME_OVER = 7           # ゲームオーバー画面（RESTARTボタン表示）

async def main():
    print('起動確認')  # 起動確認用
    pygame.init()  # Pygameの初期化

    # 画面サイズの定義
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 1280 x 720の大きさの画面を作る
    pygame.display.set_caption("脱出ゲーム")  # 画面上部に表示するタイトルを設定

    # ボタンのRect定義 (初期状態は全て非アクティブなRectで初期化)
    # これらのRectは、各ゲーム状態の描画ロジック内で適切な位置とサイズで再定義されます
    start_b = pygame.Rect(0, 0, 0, 0)
    next_b1 = pygame.Rect(0, 0, 0, 0)
    next_b2 = pygame.Rect(0, 0, 0, 0)
    restart_b = pygame.Rect(0, 0, 0, 0) # 終了ボタンを再スタートボタンに変更

    # 画像ファイルの読み込み (pygbagではimage/ディレクトリが自動的に含まれることを確認)
    try:
        stage1_image = pygame.image.load("image/stage1.jpg").convert_alpha()
        stage1_a_image = pygame.image.load("image/stage1_a.jpg").convert_alpha()
        stage2_image = pygame.image.load("image/stage2.jpg").convert_alpha()
        stage2_a_image = pygame.image.load("image/stage2_a.jpg").convert_alpha()
        stage3_image = pygame.image.load("image/stage3.jpg").convert_alpha()
        stage3_a1_image = pygame.image.load("image/stage3_a1.jpg").convert_alpha()
        stage3_com_image = pygame.image.load("image/stage3_com.jpg").convert_alpha()
        stage3_a2_image = pygame.image.load("image/stage3_a2.jpg").convert_alpha()
        key_image = pygame.image.load("image/key.png").convert_alpha()
    except pygame.error as e:
        print(f"画像の読み込みエラー: {e}")
        # エラーが発生した場合の代替処理や終了処理
        pygame.quit()
        sys.exit()

    # 正解画像の座標宣言 (初期化)
    # これらのRectも、各ゲーム状態の描画ロジック内で適切な位置とサイズで再定義されます
    s1_rect = pygame.Rect(0, 0, 0, 0)
    s2_rect = pygame.Rect(0, 0, 0, 0)
    s31_rect = pygame.Rect(0, 0, 0, 0)
    s32_rect = pygame.Rect(0, 0, 0, 0)

    # フォントの用意
    font_large = pygame.font.SysFont(None, 160) # RESTARTなどの大きなテキスト用
    font_medium = pygame.font.SysFont(None, 80) # メッセージ用の少し小さめのテキスト用
    
    # テキストの中身をレンダリング
    start_txt = font_large.render("START", True, (0,0,0))
    next_txt = font_large.render("NEXT", True, (0,0,0))
    restart_txt = font_large.render("RESTART", True, (0,0,0))
    
    # ALL CLEAR!! の文字色を黒に変更 (0,0,0)
    clear_message_line1 = font_medium.render("ALL CLEAR!!", True, (0,0,0)) 
    clear_message_line2 = font_medium.render("", True, (255,255,255)) # 空の文字列にする

    game_state = GAME_STATE_START_SCREEN # ゲームの初期状態を設定

    # ゲーム進行中の処理
    running = True
    while running:
        # イベント処理
        for event in pygame.event.get():
            # アプリ終了用のイベント (ブラウザのタブを閉じるなど)
            if event.type == QUIT:
                running = False
            
            # マウスクリック（ゲーム進行用のイベント）
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == GAME_STATE_START_SCREEN:
                    if start_b.collidepoint(event.pos):
                        game_state = GAME_STATE_STAGE1_PLAYING
                
                elif game_state == GAME_STATE_STAGE1_PLAYING:
                    if s1_rect.collidepoint(event.pos):
                        game_state = GAME_STATE_STAGE1_CLEARED
                
                elif game_state == GAME_STATE_STAGE1_CLEARED:
                    if next_b1.collidepoint(event.pos):
                        game_state = GAME_STATE_STAGE2_PLAYING

                elif game_state == GAME_STATE_STAGE2_PLAYING:
                    if s2_rect.collidepoint(event.pos):
                        game_state = GAME_STATE_STAGE2_CLEARED

                elif game_state == GAME_STATE_STAGE2_CLEARED:
                    if next_b2.collidepoint(event.pos):
                        game_state = GAME_STATE_STAGE3_PLAYING

                elif game_state == GAME_STATE_STAGE3_PLAYING:
                    if s31_rect.collidepoint(event.pos):
                        game_state = GAME_STATE_STAGE3_SHOW_MESSAGE_AND_A2 # メッセージ表示状態へ遷移

                elif game_state == GAME_STATE_STAGE3_SHOW_MESSAGE_AND_A2:
                    # メッセージ表示中にエアコンのコンセントがクリックされたらゲームオーバーへ
                    if s32_rect.collidepoint(event.pos):
                        game_state = GAME_STATE_GAME_OVER
                
                elif game_state == GAME_STATE_GAME_OVER:
                    if restart_b.collidepoint(event.pos):
                        game_state = GAME_STATE_START_SCREEN # ゲームオーバーからスタート画面に戻る

        # 画面描画
        # screen.fill((0,0,0)) # 毎フレーム画面を黒色でクリアする行は、各状態の描画ロジック内に移動

        # 各状態に応じた描画処理
        if game_state == GAME_STATE_START_SCREEN:
            screen.fill((0,0,0)) # START画面は毎回クリア
            # STARTボタンの描画
            start_b = pygame.Rect(400, 360, 440, 110) # STARTボタンをアクティブな位置に定義
            pygame.draw.rect(screen,(255, 255, 255),start_b)
            
            # STARTテキストをボタンの中央に表示
            start_text_width, start_text_height = start_txt.get_size()
            screen.blit(start_txt, (start_b.x + (start_b.width - start_text_width) // 2, start_b.y + (start_b.height - start_text_height) // 2))
            
            # 他のボタンやクリック領域は非アクティブ（当たり判定なし）にするため、Rectを(0,0,0,0)にリセット
            next_b1 = pygame.Rect(0,0,0,0)
            next_b2 = pygame.Rect(0,0,0,0)
            restart_b = pygame.Rect(0,0,0,0)
            s1_rect = pygame.Rect(0,0,0,0)
            s2_rect = pygame.Rect(0,0,0,0)
            s31_rect = pygame.Rect(0,0,0,0)
            s32_rect = pygame.Rect(0,0,0,0)

        elif game_state == GAME_STATE_STAGE1_PLAYING:
            screen.blit(stage1_image, (0, 0)) # 背景を描画
            s1_rect = pygame.Rect((880, 50), stage1_a_image.get_rect().size) # ステージ1の回答領域をアクティブに定義
            screen.blit(stage1_a_image, s1_rect)
            # 他のボタンやクリック領域は非アクティブに
            start_b = pygame.Rect(0,0,0,0)
            next_b1 = pygame.Rect(0,0,0,0)
            next_b2 = pygame.Rect(0,0,0,0)
            restart_b = pygame.Rect(0,0,0,0)
            s2_rect = pygame.Rect(0,0,0,0)
            s31_rect = pygame.Rect(0,0,0,0)
            s32_rect = pygame.Rect(0,0,0,0)

        elif game_state == GAME_STATE_STAGE1_CLEARED:
            # ステージ1クリア後の描画 (NEXTボタン表示)
            screen.blit(stage1_image, (0, 0)) # 背景を再描画
            screen.blit(stage1_a_image, (880, 50)) # 正解画像を再描画 (固定座標で指定)
            next_b1 = pygame.Rect(500, 500, 330, 110) # NEXTボタン1をアクティブな位置に定義
            pygame.draw.rect(screen,(255,255,255),next_b1)
            screen.blit(key_image, (550, 250))
            
            # NEXTテキストをボタンの中央に表示
            next_text_width, next_text_height = next_txt.get_size()
            screen.blit(next_txt, (next_b1.x + (next_b1.width - next_text_width) // 2, next_b1.y + (next_b1.height - next_text_height) // 2))
            
            # s1_rectは非アクティブに
            s1_rect = pygame.Rect(0,0,0,0)

        elif game_state == GAME_STATE_STAGE2_PLAYING:
            screen.blit(stage2_image, (0, 0)) # 背景を描画
            s2_rect = pygame.Rect((336, 177), stage2_a_image.get_rect().size) # ステージ2の回答領域をアクティブに定義
            screen.blit(stage2_a_image, s2_rect)
            # 他のボタンやクリック領域は非アクティブに
            start_b = pygame.Rect(0,0,0,0)
            next_b1 = pygame.Rect(0,0,0,0)
            next_b2 = pygame.Rect(0,0,0,0)
            restart_b = pygame.Rect(0,0,0,0)
            s1_rect = pygame.Rect(0,0,0,0)
            s31_rect = pygame.Rect(0,0,0,0)
            s32_rect = pygame.Rect(0,0,0,0)

        elif game_state == GAME_STATE_STAGE2_CLEARED:
            # ステージ2クリア後の描画 (NEXTボタン表示)
            screen.blit(stage2_image, (0, 0)) # 背景を再描画
            screen.blit(stage2_a_image, (336, 177)) # 正解画像を再描画 (固定座標で指定)
            next_b2 = pygame.Rect(500, 500, 330, 110) # NEXTボタン2をアクティブな位置に定義
            pygame.draw.rect(screen,(255,255,255),next_b2)
            screen.blit(key_image, (550, 250))
            
            # NEXTテキストをボタンの中央に表示
            next_text_width, next_text_height = next_txt.get_size()
            screen.blit(next_txt, (next_b2.x + (next_b2.width - next_text_width) // 2, next_b2.y + (next_b2.height - next_text_height) // 2))
            
            # s2_rectは非アクティブに
            s2_rect = pygame.Rect(0,0,0,0)

        elif game_state == GAME_STATE_STAGE3_PLAYING:
            screen.blit(stage3_image, (0, 0)) # 背景を描画
            s31_rect = pygame.Rect((30, 329), stage3_a1_image.get_rect().size) # ステージ3の回答領域1をアクティブに定義
            screen.blit(stage3_a1_image, s31_rect)
            # 他のボタンやクリック領域は非アクティブに
            start_b = pygame.Rect(0,0,0,0)
            next_b1 = pygame.Rect(0,0,0,0)
            next_b2 = pygame.Rect(0,0,0,0)
            restart_b = pygame.Rect(0,0,0,0)
            s1_rect = pygame.Rect(0,0,0,0)
            s2_rect = pygame.Rect(0,0,0,0)
            s32_rect = pygame.Rect(0,0,0,0)

        elif game_state == GAME_STATE_STAGE3_SHOW_MESSAGE_AND_A2:
            screen.blit(stage3_image, (0, 0)) # 背景を保持
            screen.blit(stage3_com_image, (30, 300)) # コメント画像を表示
            s32_rect = pygame.Rect((1262, 0), stage3_a2_image.get_rect().size) # ステージ3の回答領域2をアクティブに定義
            screen.blit(stage3_a2_image, s32_rect)
            # s31_rectは非アクティブに
            s31_rect = pygame.Rect(0,0,0,0)

        elif game_state == GAME_STATE_GAME_OVER:
            screen.blit(stage3_image, (0, 0)) # ステージ3の背景を保持

            # 鍵の画像を中央に表示
            key_image_width, key_image_height = key_image.get_size()
            key_x = (SCREEN_WIDTH - key_image_width) // 2
            key_y = 250
            screen.blit(key_image, (key_x, key_y))
            
            # 感謝のメッセージ（1行目）を鍵の上に中央揃えで表示
            clear_message_line1_width, clear_message_line1_height = clear_message_line1.get_size()
            clear_message_line1_x = (SCREEN_WIDTH - clear_message_line1_width) // 2
            clear_message_line1_y = key_y - clear_message_line1_height - 10 # 鍵の上に10pxの余白
            screen.blit(clear_message_line1, (clear_message_line1_x, clear_message_line1_y))

            # 感謝のメッセージ（2行目）を1行目の下に中央揃えで表示 (今回は空なので描画されない)
            clear_message_line2_width, clear_message_line2_height = clear_message_line2.get_size()
            clear_message_line2_x = (SCREEN_WIDTH - clear_message_line2_width) // 2
            clear_message_line2_y = clear_message_line1_y + clear_message_line1_height # 1行目のすぐ下
            screen.blit(clear_message_line2, (clear_message_line2_x, clear_message_line2_y))

            # RESTARTボタンの描画
            # テキストの幅に合わせてボタンの幅を調整し、中央揃えにする
            restart_text_width, restart_text_height = restart_txt.get_size()
            button_width = restart_text_width + 100 # テキストの幅に余白を追加
            button_height = 110
            restart_b = pygame.Rect(
                (SCREEN_WIDTH - button_width) // 2, # 中央揃えのX座標
                500, # Y座標は固定
                button_width,
                button_height
            )
            pygame.draw.rect(screen,(255,255,255),restart_b)
            
            # RESTARTテキストをボタンの中央に表示
            screen.blit(restart_txt, (restart_b.x + (restart_b.width - restart_text_width) // 2, restart_b.y + (restart_b.height - restart_text_height) // 2))

            # 他のボタンやクリック領域は非アクティブに
            start_b = pygame.Rect(0,0,0,0)
            next_b1 = pygame.Rect(0,0,0,0)
            next_b2 = pygame.Rect(0,0,0,0)
            s1_rect = pygame.Rect(0,0,0,0)
            s2_rect = pygame.Rect(0,0,0,0)
            s31_rect = pygame.Rect(0,0,0,0)
            s32_rect = pygame.Rect(0,0,0,0)

        pygame.display.update() # 毎フレーム最後に一度だけ画面を更新

        # 必須らしい。引数は0で固定
        await asyncio.sleep(0)

    # ゲームループが終了した場合の処理 (Webではブラウザタブは閉じない)
    pygame.quit()
    sys.exit()

# pygbagではasyncio.run()が自動的に呼ばれるため、重複を避ける
# if __name__ == "__main__": のブロックはpygbag環境では実行されないことが多い
# そのため、直接 asyncio.run(main()) のみを残します。
asyncio.run(main())
