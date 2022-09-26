from pico2d import *

import os
os.chdir('C:/2021184020_2DGP_DRILL/2D_game_Work')

open_canvas()
grass = load_image('grass.png')
character = load_image('run_animation.png')

x = 0

# 여기를 채우세요.
frame = 0

#for x in range(0, 800, 5): while 대신넣기
while (x<800):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 0, 100,100, x, 90)
    update_canvas()
    frame = (frame + 1) % 8
    x += 5
    delay(0.05)
    get_events()

close_canvas()

#Sprite Sheet 검색하면 많~~이 나옴#
