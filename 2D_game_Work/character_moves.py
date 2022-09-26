from pico2d import *

import os
os.chdir('C:/2021184020_2DGP_DRILL/2D_game_Work')

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

#채우기 - 백버퍼를 이용해서 부드러운 애니메이션 넣기

x = 0
while (x<800):
    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, 90)
    x = x+2
    update_canvas()
    delay(0.01)
    get_events()

close_canvas()
