from pico2d import *
import game_framework
import play_state
import time

running = True
Saybab_x = None
frame = 0
x = 0

def enter():
    global gamestop
    gamestop = load_image('gamestop.png')
    pass

def exit():
    global gamestop
    del gamestop
    # fill here
    pass

def update():

    pass

def do(self):
    self.frame = (self.frame + 1) % 8


def draw():
    frame = 0
    x = 0
    # Saybab_x = load_image('Saybab_X.gif')
    gamestop = load_image('gamestop.png')

    clear_canvas()
    play_state.draw_world() #잘 실행하다가, I키를 누르면 멈추고 공화면이 뜬다. 하지만 배경은 없어짐으로 이를 해결하기 위한 코드

    #이거 왜 무한반복하지#
    print('일시정지')
    gamestop.draw(800, 300)
    # Saybab_x.draw(400, 300)
    #self.Saybab_x.draw(self.frame * 200, 2100, 200, 100, self.x, self.y)
    # while (x<800):
    #     gamestop.draw(400, 300)
    #     #Saybab_x.clip_draw(frame * 100, 0, 4200, 500, 2100, 200)
    #     update_canvas()
    #     frame = (frame + 1) % 6
    #     x += 1
    update_canvas()



##움짤 실행 됐을 때, 타이머 시작 -> 몇초 뒤에 화면에서 나가기.##
##일단 Esc키로 나가자.##
def handle_events():
    #global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN: #and event.key == SDLK_ESCAPE:
            # game_framework.change_state(logo_state)
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    print('일시정지 끝남')
                    game_framework.pop_state()