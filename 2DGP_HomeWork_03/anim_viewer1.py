#소닉이 정자세로 앞으로 쭉 가는거
import math
import os

os.chdir('C:/2021184020_2DGP_DRILL/2DGP_HomeWork_03')

from pico2d import*
open_canvas()


clear_canvas()
Map = load_image('Sonic_mapB.png')
character = load_image('Sonic_B.png')
update_canvas()
delay(0.01)

x = 0
while (x<800):
    clear_canvas()
    Map.draw_now(600,300)
    character.draw(x, 350)
    x = x+2
    update_canvas()
    delay(0.01)
    get_events()


  
close_canvas()
