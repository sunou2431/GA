# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

# 画面サイズの設定
SCR_RECT = Rect(0, 0, 800, 600)

"""
Class スプライトの作成
UPdateを使用することで移動することができる
Drawを使う場合は、screenを引数で持って行く
"""
class MySprite(pygame.sprite.Sprite):
    # コンストラクタ
    # Filenameはファイル名
    # x,yはファイルの座標位置
    # vx,vyは動く移動量
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        
    # Updateを呼び出すことで画像の移動が可能
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        # 壁にぶつかったら跳ね返る
        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
            self.vy = -self.vy
        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)
    
    # 画像を描画する。要：screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Key操作によって移動量の変更
    def movestart(self, xyflg):
        # xyflg 0~3 0 = 右 | 1 = 左 | 2 = 上 | 3 = 下 |
        if xyflg == 0:
            self.vx = 1
        elif xyflg == 1:
            self.vx = -1
        elif xyflg == 2:
            self.vy = -1
        elif xyflg == 3:
            self.vy = 1

    def movestop(self, xyflg):
        # xyflg | 0~3 | 0 = 右 | 1 = 左 | 2 = 上 | 3 = 下 |
        if xyflg <= 1:
            self.vx = 0
        elif xyflg <= 3:
            self.vy = 0

def main():
    # 初期セットアップ
    pygame.init() # 初期化
    screen = pygame.display.set_mode(SCR_RECT.size) # ウィンドウの設置
    pygame.display.set_caption("GA Gaming") # ウィンドウの上の方に出てくるアレの指定

    # 自操作キャラの読み込み
    player = MySprite("img/player.png", 50, 300, 0, 0)

    while(True):
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

        player.update() # 自キャラの移動処理

        # 描画フェーズ
        screen.fill((255, 63, 10,)) # 背景色の指定。RGBだと思う
        player.draw(screen) # 自操作キャラの描画
        pygame.display.update() # 画面更新

if __name__ == "__main__":
    main()
