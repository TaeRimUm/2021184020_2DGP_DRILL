import math

import os
os.chdir('C:/2021184020_2DGP_DRILL/2D_game_Work')

from pico2d import *
open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

#어? 싸이클이랑 렉탱글이랑 비슷한게 있네? 그럼 함수로 해야지#
def render_all(x, y,):
        clear_canvas_now()
        grass.draw_now(400, 30)
        character.draw_now(x, y) #(400, 90)
        delay(0.05) #돌아가는 빠르기#



def run_circle():
    print("싸이클~")
    cx , cy, r = 400, 300, 200
    #캔버스에서 원점은 0, 0 왼쪽 맨 아래니까 돌릴 원의 위치를 400, 300으로 옮겨줌#

   # for deg in range(-90, 270+1, 5):
     #   x = cx + r * math.cos(deg / 360 * 2 * math.pi)
     #   y = cy + r * math.sin(deg / 360 * 2 * math.pi)
     #   render_all(x, y)
  #  pass



def run_rectangle():
    print("렉탱글~~")

    # -> 사각형으로 돌기(바텀라인) - 아래 라인으로 움직임 Bottom line
    for x in range(50, 750+1, 10):
        render_all(x, 90)

    # ㅅ 아래에서 위로
    for y in range(90, 550+1, 10):
        render_all(750, y)

    # <- 탑라인 top line
    for x in range(750, 50, -10):
        render_all(x, 550)

    # V 왼쪽에서 오른쪽 아래
    for y in range(550, 90-1, -10):
        render_all(50, y)
        
    pass


while True:
    run_circle()
    run_rectangle()

    
    break
    #break

close_canvas()
