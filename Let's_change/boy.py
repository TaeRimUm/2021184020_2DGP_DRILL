from pico2d import *
import game_world

import play_state #ball 객체확보
from ball import Ball #볼 클래스인 Ball를 확보.


#1 : 이벤트 정의
RD, LD, RU, LU, TIMER, SPACE, DD, DU = range(8)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'SPACE', 'DD', 'DU']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_d): DD,
    (SDL_KEYUP, SDLK_d): DU
}


#2 : 상태의 정의
class IDLE:
    @staticmethod
    def enter(self, event):
        print('ENTER IDLE')
        self.dir = 0
        self.attack_dir = 0
        self.timer = 1000

    @staticmethod
    def exit(self, event): #IDLE이 끝날 때 마다 파이어볼하면 문제가 생김.
        print('EXIT IDLE')

        if event == SPACE: #그래서 스페이스가 눌린 exit일 때 파이어볼을 함.
            self.fire_ball()

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)


    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)


class RUN:

    def enter(self, event):
        print('ENTER RUN')
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1

    def exit(self, event): #RUN이 끝날 때 마다 파이어볼하면 문제가 생김.
        print('EXIT RUN')
        self.face_dir = self.dir

        if event == SPACE: #그래서 RUN일 상태에서 스페이스를 눌러서, exit일 때 파이어볼을 함.
            self.fire_ball()

    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir #, self.attack_dir
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)


#D키를 누르면 EXIT IDLE, ENTER IDLE 눌렀다 때도 EXIT IDLE, ENTER IDLE 가 출력 됨.

#        if event == SPACE: #그래서 스페이스가 눌린 exit일 때 파이어볼을 함.
#            self.fire_ball()
#       이거 처럼 if event == DD: 를 사용해서 attack_d.py를 만들어야 하나?
#       아니면 def attack_d를 사용해야 하나?
#       공격 모션은 하나의 상태로 만들어야 하기 때문에 Class를 써야 하는데 싯팔 진짜

class Attack_d:

    def enter(self, event):
        print('attack_d')
        if event == DD:
            self.attack_dir += 1
        elif event == DU:
            self.attack_dir -= 1

    def exit(self, event): #RUN이 끝날 때 마다 attack_d하면 문제가 생김.
        print('attack_d_exit')
        self.face_dir = self.attack_dir

    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.attack_dir
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.attack_dir == 1:
            self.attack_d.clip_draw(self.frame * 100, 0, 200, 100, self.x, self.y)

        elif self.attack_dir == -1:
            pass



class SLEEP:

    def enter(self, event):
        print('ENTER SLEEP')
        self.frame = 0

    def exit(self, event):
        pass

    def do(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(self.frame * 100, 200, 100, 100,
                                          -3.141592 / 2, '', self.x + 25, self.y - 25, 100, 100)
        else:
            self.image.clip_composite_draw(self.frame * 100, 300, 100, 100,
                                          3.141592 / 2, '', self.x - 25, self.y - 25, 100, 100)


#3. 상태 변환 구현

next_state = {
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, TIMER: SLEEP, SPACE: IDLE, DD: IDLE, DU: IDLE},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, SPACE: RUN},
    SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, SPACE: IDLE}
}




class Boy:

    def __init__(self):
        self.x, self.y = 800 // 2, 90 #90 -> 50 으로 바꾸면 먼저 그린게 먼저 가려짐. 소년->잔디 순으로 그렸기 때문이다.
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('SayBar_1.png')

        self.attack_d = 0
        self.attack_d = load_image('attack_d.png')

        self.timer = 100

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try: #예외처리
                self.cur_state = next_state[self.cur_state][event]
                #SLEEP에서 SPACE를 눌렀을 때 정의가 없어서 오류가 발생함.

            except KeyError: #이 줄을 실행하려 했는데, 문제가 발생했고 그 문제가 KeyError였다면
                # 아래 코드 실행 후 정상적으로 실행된다. 최소한 죽지는 않음.

                # 어떤 상태에서? 어떤 이벤트 때문에 문제가 발생했는지??
                print(f'Error: State {self.cur_state.__name__}  Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        debug_print('PPPP')
        debug_print(f'Face Dir: {self.face_dir}, Dir: {self.dir}')

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def fire_ball(self):
        print('FIRE BALL')
        #생성
        ball = Ball(self.x, self.y, self.face_dir*3) #self.face_dir = 바라보는 뱡항
        game_world.add_object(ball, 1)

