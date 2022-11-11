from pico2d import *
import game_framework

from grass import Grass #grass 분리됨. 여기에 있는 grass가 오류가 걸리지 않음.
from boy import Boy

boy = None
grass = None

#class grass: 어쩌고 ==> grass.py

#class boy: 어쩌고 ==> boy.py

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            boy.handle_event(event)

# 초기화
def enter():
    global boy, grass
    boy = Boy()
    grass = Grass()

# 종료
def exit():
    global boy, grass
    del boy
    del grass

def update():
    boy.update()

def draw_world():
    grass.draw()
    boy.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass




def test_self():
    import play_state

    pico2d.open_canvas()
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
