# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
import sys

# 画面サイズの設定
SCR_RECT = Rect(0, 0, 800, 600)

"""
Class スプライトの作成
UPdateを使用することで移動することができる
Drawを使う場合は、screenを引数で持って行く
"""
class MyPlayer(pygame.sprite.Sprite):
    # コンストラクタ
    # Filenameはファイル名
    # x,yはファイルの座標位置
    # vx,vyは動く移動量
    # shotnumは現在発射されている数
    # moveflgは押されているkeyの取得
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        self.shotnum = 0
        self.moveflg = 0
        
    # Updateを呼び出すことで画像の移動が可能
    def update(self):
        # 移動量の計算
        if self.moveflg != 0:
            # X軸の移動量の計算
            if self.moveflg % 4 % 3 == 1:
                self.vx = 10
            elif self.moveflg % 4 % 3 == 2:
                self.vx = -10
            else:
                self.vx = 0

        # Y軸の移動量の計算
            if self.moveflg / 4 == 3:
                self.vy = 0
            elif self.moveflg / 4 >= 2:
                self.vy = 10
            elif self.moveflg / 4 >= 1:
                self.vy = -10
            else:
                self.vy = 0
        else:
            self.vx = 0
            self.vy = 0

        self.rect.move_ip(self.vx, self.vy)

        # 壁にぶつかったら移動量０
        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
            self.vx = 0
        if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
            self.vy = 0
        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)
    
    # 画像を描画する。要：screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Key操作によって移動量の変更
    def movestart(self, xyflg):
        # xyflg 0~3 0 = 右 | 1 = 左 | 2 = 上 | 3 = 下 |
        if xyflg == 0:
            self.moveflg += 1
        elif xyflg == 1:
            self.moveflg += 2
        elif xyflg == 2:
            self.moveflg += 4
        elif xyflg == 3:
            self.moveflg += 8

    def movestop(self, xyflg):
        # xyflg | 0~3 | 0 = 右 | 1 = 左 | 2 = 上 | 3 = 下 |
        if xyflg == 0:
            self.moveflg -= 1
        elif xyflg == 1:
            self.moveflg -= 2
        elif xyflg == 2:
            self.moveflg -= 4
        elif xyflg == 3:
            self.moveflg -= 8

    def shot(self):
        MyShot(self.rect.center)

class MyShot(pygame.sprite.Sprite):
    # プレイヤーが発射するショット

    def __init__(self, pos):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
        self.vx = 20
    
    def update(self):
        self.rect.move_ip(self.vx, 0)  # 右へ移動
        if self.rect.right > SCR_RECT.width:  # 右端端に達したら除去
            self.kill()

def main():
    # 初期セットアップ
    pygame.init() # 初期化
    screen = pygame.display.set_mode(SCR_RECT.size) # ウィンドウの設置
    pygame.display.set_caption("GA Gaming") # ウィンドウの上の方に出てくるアレの指定

    # スプライトグループを作成
    all = pygame.sprite.RenderUpdates()
    shots = pygame.sprite.Group() # ミサイルグループ
    MyPlayer.containers = all
    MyShot.containers = all, shots

    # キャラの読み込み
    player = MyPlayer("img/player.png", 50, 300, 0, 0)
    MyShot.image = load_image("shot.png")

    # 背景の描画
    bg = pygame.Surface(SCR_RECT.size)
    bg.fill((0, 20, 0)) # 画面の背景色
    screen.blit(bg, (0, 0)) # 背景色の指定。RGBだと思う
    pygame.display.update()

    # flamelateの設定
    clock = pygame.time.Clock()

    while(True):
        # フレームレート(30fps)
        clock.tick(30)

        # 計算フェーズ
        for event in pygame.event.get(): # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN: # KEYが押されたときの処理
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                # 矢印キーに応じて移動処理
                if event.key == K_RIGHT:
                    player.movestart(0)
                elif event.key == K_LEFT:
                    player.movestart(1)
                elif event.key == K_UP:
                    player.movestart(2)
                elif event.key == K_DOWN:
                    player.movestart(3)

                # 弾の発射
                if event.key == K_SPACE:
                    player.shot()

            if event.type == KEYUP: # KEYが離されたの処理
                # 矢印キーに応じて移動処理
                if event.key == K_RIGHT:
                    player.movestop(0)
                elif event.key == K_LEFT:
                    player.movestop(1)
                elif event.key == K_UP:
                    player.movestop(2)
                elif event.key == K_DOWN:
                    player.movestop(3)
        all.update()

        # 描画フェーズ
        all.clear(screen, bg)

        # スプライトを更新
        dirty_rects = all.draw(screen)

        # updateにdirty rectを渡すとその部分だけ更新するので効率よい
        # 画面更新
        pygame.display.update(dirty_rects)

def load_image(filename, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("img", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image

if __name__ == "__main__":
    main()
