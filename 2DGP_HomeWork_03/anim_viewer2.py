#소닉이 열심히 달리는거 + 배경 뒤로 가는거 해보려다 실패한거
import math
import os

os.chdir('C:/2021184020_2DGP_DRILL/2DGP_HomeWork_03')

from pico2d import*
open_canvas()

clear_canvas()
Map = load_image('Back.png')
character = load_image('Sonic_A.png')


def render_all(x, y,):
        clear_canvas_now()
        character.draw_now(x, y)
        delay(0.05)



x=200
frame=0

while (x<800):
    clear_canvas()
    Map.draw_now(600,300)
    character.clip_draw(frame * 100, 0, 100,100, x, 90)
    update_canvas()
    frame = (frame + 1) % 8
    delay(0.05)
    get_events()






close_canvas()
