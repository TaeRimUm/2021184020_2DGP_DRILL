#만들다 실패한거
import math
import os

os.chdir('C:/2021184020_2DGP_DRILL/2DGP_HomeWork_03')

from pico2d import*
open_canvas()

Map = load_image('Sonic_map.png')
character = load_image('Sonic_A.png')


def render_all(x, y,):
        clear_canvas_now()
        Map.draw_now(150,430)
        character.draw_now(x, y)
        delay(0.05)



x=0
frame=0

while (x<800):
    print("시작")
    clear_canvas()
    
    character.clip_draw(frame * 100, 0, 100,100, x, 90)
    update_canvas()
    frame = (frame + 1) % 8
    x += 5
    delay(0.05)
    get_events()



    def run_rectangle1():
        print("직진1")
        for x in range(50, 430, 10):
            render_all(x, 150)
    
    def run_circle():
        print("원")
        cx , cy, r = 500, 330, 180
        for deg in range(-90, 270+1, 5):
            x = cx + r * math.cos(deg / 360 * 2 * math.pi)
            y = cy + r * math.sin(deg / 360 * 2 * math.pi)
            render_all(x, y)
    pass



    def run_rectangle():
        print("직진2")

        for x in range(500, 750+1, 10):
            render_all(x, 150)
    pass


    while True:
        run_rectangle1()
        run_circle()
        run_rectangle()

    
    break




close_canvas()
