import game_framework
from pico2d import *

import game_world
import server

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



# Boy Event
RD, LD, RU, LU, DD, DU, UPKEY_DOWN, DOWNKEY_DOWN, UPKEY_UP, DOWNKEY_UP = range(10)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_d): DD,
    (SDL_KEYUP, SDLK_d): DU,

    (SDL_KEYUP, SDLK_UP): UPKEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWNKEY_UP,
    (SDL_KEYDOWN, SDLK_UP): UPKEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWNKEY_DOWN,
}


# Boy States

class WalkingState:

    def enter(self, event):

        self.attack_dir = 0

        if event == RD:
            self.x_velocity += RUN_SPEED_PPS
        elif event == RU:
            self.x_velocity -= RUN_SPEED_PPS
        if event == LD:
            self.x_velocity -= RUN_SPEED_PPS
        elif event == LU:
            self.x_velocity += RUN_SPEED_PPS

        if event == UPKEY_DOWN:
            self.y_velocity += RUN_SPEED_PPS
        elif event == UPKEY_UP:
            self.y_velocity -= RUN_SPEED_PPS
        if event == DOWNKEY_DOWN:
            self.y_velocity -= RUN_SPEED_PPS
        elif event == DOWNKEY_UP:
            self.y_velocity += RUN_SPEED_PPS



    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.x_velocity * game_framework.frame_time
        self.y += self.y_velocity * game_framework.frame_time

        self.x = clamp(0, self.x, server.background.w - 1)
        self.y = clamp(0, self.y, server.background.h - 1)


    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom

        self.font.draw(sx - 40, sy + 40, '(%d, %d)' % (self.x, self.y), (255, 255, 0))

        if self.x_velocity > 0:                         #오른쪽으로 뛰기
            self.image.clip_draw(int(self.frame) * 100, 100, 100, 100, sx, sy)
            self.dir = 1
        elif self.x_velocity < 0:                       #왼쪽으로 뛰기
            self.image.clip_draw(int(self.frame) * 100, 0, 100, 100, sx, sy)
            self.dir = -1
        else:
            # if boy x_velocity == 0
            if self.y_velocity > 0 or self.y_velocity < 0:
                if self.dir == 1:
                    self.image.clip_draw(int(self.frame) * 100, 100, 100, 100, sx, sy)
                else:
                    self.image.clip_draw(int(self.frame) * 100, 0, 100, 100, sx, sy)
            else:
                # boy is idle
                if self.dir == 1:                               #오른쪽보고 대기
                    self.image.clip_draw(int(self.frame) * 100, 300, 100, 100, sx, sy)
                else:                                           #왼쪽보고 대기
                    self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, sx, sy)


class ATTACK:
    def enter(self, event):
        if event == DD:
            print('존나 때리기')
            self.attack_dir += 1
        elif event == DU:
            self.attack_dir -= 1
    def exit(self, event): #ATTACK이 끝날 때 마다 때리면 문제가 생김.
        print('그만 때리기')

    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self):
        sx, sy = self.x - server.background.window_left, self.y - server.background.window_bottom

        if self.attack_dir == 1 and self.dir == 1:
            self.ATTACK.clip_draw(self.frame * 200, 100, 200, 100, sx, sy)

        elif self.attack_dir == 1 and self.dir == -1:
            self.ATTACK.clip_draw(self.frame * 200, 0, 200, 100, sx, sy)



        # if self.attack_dir == 1 and self.face_dir == 1:
        #     self.ATTACK.clip_draw(self.frame * 200, 100, 200, 100, self.x, self.y)
        #
        # elif self.attack_dir == 1 and self.face_dir == -1:
        #     self.ATTACK.clip_draw(self.frame * 200, 0, 200, 100, self.x, self.y)

    def handle_collision(self, other, group):
        pass #충돌 되어도, 아무 반응없기.

    def update(self):
        self.cur_state.do(self)

        # if self.event_que:
        #     event = self.event_que.pop()
        #     self.cur_state.exit(self, event)
        #     try: #예외처리
        #         self.cur_state = next_state_table[self.cur_state][event]
        #         # SLEEP에서 S키를 눌렀을 때 정의가 없어서 오류가 발생함.
        #
        #     except KeyError: #이 줄을 실행하려 했는데, 문제가 발생했고 그 문제가 KeyError였다면
        #         # 아래 코드 실행 후 정상적으로 실행된다. 최소한 죽지는 않음.
        #
        #         # 어떤 상태에서? 어떤 이벤트 때문에 문제가 발생했는지??
        #         print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
        #     self.cur_state.enter(self, event)








next_state_table = {
    WalkingState: {RU: WalkingState, LU: WalkingState, RD: WalkingState, LD: WalkingState,
                UPKEY_UP: WalkingState, UPKEY_DOWN: WalkingState, DOWNKEY_UP: WalkingState, DOWNKEY_DOWN: WalkingState},
    ATTACK: {DD: WalkingState, DU: WalkingState},
}


class Boy:

    def __init__(self):
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('SayBar_1.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.ATTACK = load_image('attack_d.png')
        self.dir = 1
        self.x_velocity, self.y_velocity = 0, 0
        self.frame = 0
        self.event_que = []
        self.cur_state = WalkingState
        self.cur_state.enter(self, None)
        self.x, self.y = get_canvas_width() // 2, get_canvas_height() // 2


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)



    def draw(self):
        self.cur_state.draw(self)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

