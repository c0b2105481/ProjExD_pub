from glob import glob
import pygame as pg
import sys
from random import randint
import pygame.mixer

BULLET_LIST = [1, 2, 3]         # 障害物の確率
SCREEN = (0, 0, 600, 500)       # 移動範囲（x, y) 
RUN = True                      # 実行：True 停止:False
HP = 100                        # HPの設定
BULLET = 1000                   # 乱数の範囲上限        武田

class Screen:
    def __init__(self, fn, wh, title): 
        # fn:背景画像のパス wh:幅高さのタプル title:画面タイトル
        pg.display.set_caption(title)
        self.width , self.height = wh     # ウィンドウサイズの引数
        self.disp = pg.display.set_mode((self.width, self.height)) # Surface
        self.rect= self.disp.get_rect() # Rect
        self.image = pg.image.load(fn) # Surfac
 

class Plane(pg.sprite.Sprite):            # キャラクタークラス
    def __init__(self, fn, r, xy): 
        # fn: 画像パス r:拡大率 xy:初期位置
        super().__init__()
        self.image = pg.image.load(fn)    # Surface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect= self.image.get_rect()  # Rect
        self.rect.center = xy             # キャラの座標を設定

    def update(self):             # キャラの操作
        key_states = pg.key.get_pressed() # 押されたキーを取得し、key_statesに格納
        if key_states[pg.K_SPACE] or key_states[pg.K_UP]:        # ジャンプ設定
            self.rect.move_ip(0, -1)      # スペースキーか上矢印キーが押されたらmove_ipを(0, -1) 武田
        else:                             # それ以外をmove_ip(0, +1)にする
            self.rect.move_ip(0, 1)
        self.rect.clamp_ip(SCREEN)        # キャラの移動範囲


class Bullet(pg.sprite.Sprite):                     # 障害物クラス
    def __init__(self, fn, r, xy, vxy):
        # fn:画像パス r:拡大率 xy:位置
        super().__init__()
        self.image = pg.image.load(fn)              # surface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect = self.image.get_rect()           # rect
        self.rect.center = xy                       # 障害物の位置を設定
        self.vxy = vxy                              # Bulletの速度の変更 髙山
    
    def update(self):
        global BULLET
        self.rect.move_ip(self.vxy)                     # x-1の方向に動かし続ける           武田, 髙山
        key_states = pg.key.get_pressed()            # 押されたキーをkey_statesに格納    武田
        if key_states[pg.K_1]:                       # 1が押されたら                　　武田
            BULLET = 800                             # BULLETを800に変更            　　武田
        elif key_states[pg.K_2]:                     # 2が押されたら                　　武田
            BULLET = 500                             # BULLETを500に変更            　　武田
        elif key_states[pg.K_3]:                     # 3が押されたら                　　武田
            BULLET = 200                             # BULLETを200に変更            　　武田
        elif key_states[pg.K_d]:                     # dが押されたら                    武田
            BULLET = 1000                            # BULLETを初期値に戻す             武田
        

class Cloud(pg.sprite.Sprite):                                  # 雲クラス
    def __init__(self, fn, r, xy): 
        #fn:画像パス r:拡大率 xy:位置
        super().__init__()
        self.image = pg.image.load(fn)                          # 画像をロードsurface
        self.image = pg.transform.rotozoom(self.image, 0, r) 
        self.rect = self.image.get_rect()                       # Rect
        self.rect.center = xy                                   # 位置設定

    def update(self):
        self.rect.move_ip(-2, 0)                                # x-2の方向に動かし続ける


class Score:                                                   # Score classの定義
    def __init__(self, fontsize):                              # font size　の　引数を設定
        self.font = pg.font.Font(None, fontsize)               # Surface
        self.score = pg.time.get_ticks()//1000                 # スコアの計算　1秒につき1増えるようにする
        self.txt = self.font.render(str(f"Score:{self.score }"), True, (0, 0, 0)) # テキストの設定　（（テキスト）、Ture、（色RGB））


class Hp: #Hp class
    global HP #グローバル変数
    def __init__(self, fontsize):                                       
        self.font = pg.font.Font(None, fontsize)                            # HPの表示フォント、表示サイズの設定
        self.txt = self.font.render(str(f"HP:{HP}"), True, (0, 0, 0))       # HP文字列の描画

def main():                                                       # main関数
    global BULLET_LIST, RUN, HP                                   # グローバル変数
    clock = pg.time.Clock()
    screen = Screen("dg/sky.jpg",(900,500),"Crash Plane")  # 背景画像、ウィンドウサイズ、タイトル
    screen.disp.blit(screen.image, (0, 0))                        # 背景画像の貼り付け
    plane = pg.sprite.Group()                                     # 飛行機の空のコンテナを作成
    plane.add(Plane("dg/plean3.png", 0.15, (200, 125)))           # 飛行機を画面に追加
    bullet = pg.sprite.Group()                                    # 障害物の空のコンテナを作成
    cloud = pg.sprite.Group()                                     # 雲の空のコンテナを作成

    pygame.mixer.init(frequency = 44100)                #BGM設定　和田
    pygame.mixer.music.load("dg/rex.mp3")               #BGMファイル　和田
    pygame.mixer.music.play(-1)                         #BGMをループ再生


    while RUN:
        screen.disp.blit(screen.image, (0, 0))                    # 画像の貼り付け
        score = Score(30)                                         # Scoreクラスの呼出し
        screen.disp.blit(score.txt, (0, 0))                       # スコアの表示

        hp = Hp(30)                                               # フォントサイズ30でHPを表示
        screen.disp.blit(hp.txt, (0, 30))                         # HP表示の貼り付け
        cloud.draw(screen.disp)                                   # 雲の貼り付け
        cloud.update()                                            # 雲の更新
        plane.draw(screen.disp)                                   # 飛行機の貼り付け
        bullet.draw(screen.disp)                                  # 障害物の貼り付け
        plane.update()                                            # 飛行機の更新
        bullet.update()                                           # 障害物の更新
        if randint(0, 1500) == 1:                                 # 与えられた乱数がもし１だったら雲を追加
            cloud.add(Cloud("dg/cloud4.jpg", 1, (randint(900, 1000), randint(0, 500))))
        if randint(0, BULLET) in BULLET_LIST:                       # 与えられた乱数がBULLET＿LISTのなかにあったら障害物を追加      武田
            bullet.add(Bullet("dg/b1.png", 0.25, (900, randint(0, 500)), (randint(-7, -1), randint(-1, 1)))) #弾の速度、方向をランダムに設定　髙山
        if len(pg.sprite.groupcollide(bullet, plane, True, False)) != 0: # 障害物と飛行機が当たったらHPを20減らし、HPが0になったら終了
            HP -= 20
            if HP == 0:
                RUN = False
  
        for event in pg.event.get():
            if event.type == pg.QUIT: return       # ✕ボタンでmain関数から戻る

        pg.display.update()  # 画面の更新
        clock.tick(500)


if __name__ == "__main__":
    pg.init()               # pygameの初期化
    main()                  # main関数の実行
    pg.quit()               # pygameの終了
    sys.exit()              # プログラムの終了
  
  
