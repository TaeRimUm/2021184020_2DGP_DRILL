from pico2d import *
import game_framework
import play_state

running = True
image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('add_delete_boy.png')
    pass

def exit():
    global image
    del image
    # fill here
    pass

def update():

    pass

def draw():
    clear_canvas()
    play_state.draw_world() #잘 실행하다가, I키를 누르면 멈추고 공화면이 뜬다. 하지만 배경은 없어짐으로 이를 해결하기 위한 코드
    image.draw(400,300)
    update_canvas()
    # fill here
    pass

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
                    game_framework.pop_state()
                case pico2d.SDLK_0:
                    play_state.boy.item = None
                    game_framework.pop_state()
                case pico2d.SDLK_PLUS:
                    play_state.boy.item = 'PLUS'
                    game_framework.pop_state()
                case pico2d.SDLK_MINUS:
                    play_state.boy.item = 'MINUS'
                    game_framework.pop_state()




