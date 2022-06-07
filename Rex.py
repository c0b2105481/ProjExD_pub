import pygame as pg
import sys
from random import randint 
import pygame.mixer

BULLET_LIST = [1, 2, 3]         #障害物の確率
SCREEN = (0, 0, 600, 500)       #移動範囲（x, y) 
RUN = True                      #実行：True 停止:False
HP = 5                          #HPの設定

class Screen:
    def __init__(self, fn, wh, title): 
        #fn:背景画像のパス wh:幅高さのタプル title:画面タイトル
        pg.display.set_caption(title)
        self.width , self.height = wh     #ウィンドウサイズの引数
        self.disp = pg.display.set_mode((self.width, self.height)) #Surface
        self.rect= self.disp.get_rect() #Rect
        self.image = pg.image.load(fn) #Surfac
 

class Plane(pg.sprite.Sprite):            #キャラクタークラス
    def __init__(self, fn, r, xy): 
        # fn: 画像パス r:拡大率 xy:初期位置
        super().__init__()
        self.image = pg.image.load(fn)    #Surface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect= self.image.get_rect()  #Rect
        self.rect.center = xy             #キャラの座標を設定

    def update(self, screen):             #キャラの操作
        key_states = pg.key.get_pressed() # スペースキーが押されたら
        if key_states[pg.K_SPACE]:        #ジャンプ設定
            self.rect.move_ip(0, -1)      #スペースが押されたらmove_ipを(0, -1)
        else:                             #それ以外をmove_ip(0, +1)にする
            self.rect.move_ip(0, 1)
        self.rect.clamp_ip(SCREEN)        #キャラの移動範囲



class Bullet(pg.sprite.Sprite):                     #障害物クラス
    def __init__(self, fn, r, xy):
        #fn:画像パス r:拡大率 xy:位置
        super().__init__()
        self.image = pg.image.load(fn)              #surface
        self.image = pg.transform.rotozoom(self.image, 0, r)
        self.rect = self.image.get_rect()           #rect
        self.rect.center = xy                       #障害物の位置を設定
    
    def update(self, screen):
       self.rect.move_ip(-1, 0)                     #x-1の方向に動かし続ける


class Cloud(pg.sprite.Sprite):                                  #雲クラス
    def __init__(self, fn, r, xy): 
        #fn:画像パス r:拡大率 xy:位置
        super().__init__()
        self.image = pg.image.load(fn)                          #画像をロードsurface
        self.image = pg.transform.rotozoom(self.image, 0, r) 
        self.rect = self.image.get_rect()                       #Rect
        self.rect.center = xy                                   #位置設定

    def update(self, screen):
        self.rect.move_ip(-2, 0)                                #x-2の方向に動かし続ける


class Score:                                                   #Score classの定義
    def __init__(self, fontsize):                              #font size　の　引数を設定
        self.font = pg.font.Font(None, fontsize)               #Surface
        self.score = pg.time.get_ticks()//1000                 #スコアの計算　1秒につき1増えるようにする
        self.txt = self.font.render(str(f"Score:{self.score }"), True, (0, 0, 0)) #テキストの設定　（（テキスト）、Ture、（色RGB））


class Hp: #Hp class
    global HP #グローバル変数
    def __init__(self, fontsize):
        self.font = pg.font.Font(None, fontsize)
        self.txt = self.font.render(str(f"Life:{HP}"), True, (0, 0, 0))

def main():                                                       #main関数
    global BULLET_LIST, RUN, HP                                   #グローバル変数
    clock = pg.time.Clock()
    screen = Screen("dg/sky.jpg",(900,500),"避けろ！！こうかとん")  #背景画像、ウィンドウサイズ、タイトル
    screen.disp.blit(screen.image, (0, 0))                        #背景画像のはりつけ
    plane = pg.sprite.Group()                                     #飛行機の空のコンテナを作成
    plane.add(Plane("dg/plean3.png", 0.15, (200, 125)))           #飛行機を画面に追加
    bullet = pg.sprite.Group()                                    #障害物の空のコンテナを作成
    cloud = pg.sprite.Group()                                     #雲の空のコンテナを作成

    pygame.mixer.init(frequency = 44100)                #BGM設定
    pygame.mixer.music.load("ProjExD_pub/rex.mp3")#BGMファイル
    pygame.mixer.music.play(-1)                         #BGMをループ再生



    while RUN:
        screen.disp.blit(screen.image, (0, 0))                    #画像の貼り付け
        score = Score(30)                                         #Scoreクラスの呼出し
        screen.disp.blit(score.txt, (0, 0))                       #スコアの表示
        hp = Hp(30)
        screen.disp.blit(hp.txt, (0, 30))
        cloud.draw(screen.disp)                                   #雲の貼り付け
        cloud.update(screen)                                      #雲の更新
        plane.draw(screen.disp)                                   #飛行機の貼り付け
        bullet.draw(screen.disp)                                  #障害物の貼り付け
        plane.update(screen)                                      #飛行機の更新
        bullet.update(screen)                                     #障害物の更新
        if randint(0, 1500) == 1:                                 #もし１だったら雲の追加
            cloud.add(Cloud("dg/cloud4.jpg", 1, (randint(900, 1000), randint(0, 500))))
        if randint(0, 1000) in BULLET_LIST:                       #BULLET＿LISTのなかにあったら障害物を追加
            bullet.add(Bullet("dg/b1.png", 0.25, (randint(900, 1000), randint(0, 500))))
        if len(pg.sprite.groupcollide(bullet, plane, True, False)) != 0: #障害物と飛行機が当たったらHP-10する0になったら終了
            HP -= 1
            if HP == 0:
                RUN = False
  
        for event in pg.event.get():
            if event.type == pg.QUIT: return       # ✕ボタンでmain関数から戻る

        pg.display.update()  # 画面の更新
        clock.tick(500)


if __name__ == "__main__":
    pg.init() 
    main()
    pg.quit()
    sys.exit()
  
