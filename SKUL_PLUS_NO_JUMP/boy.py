from pico2d import *
import game_world
from ball import Ball

#1 : 이벤트 정의
RD, LD, RU, LU, TIMER, SPACE, DD, DU = range(8)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'SPACE', 'DD', 'DU']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_d): DD,
    (SDL_KEYUP, SDLK_d): DU,
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
    def exit(self, event):
        print('EXIT IDLE')


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

    def exit(self, event):
        print('RUN 나가기')
        self.face_dir = self.dir


    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        self.x = clamp(0, self.x, 1600)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)


class attack_d:

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try: #예외처리
                self.cur_state = next_state[self.cur_state][event]
                # SLEEP에서 S키를 눌렀을 때 정의가 없어서 오류가 발생함.

            except KeyError: #이 줄을 실행하려 했는데, 문제가 발생했고 그 문제가 KeyError였다면
                # 아래 코드 실행 후 정상적으로 실행된다. 최소한 죽지는 않음.

                # 어떤 상태에서? 어떤 이벤트 때문에 문제가 발생했는지??
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)


    def enter(self, event):
        if event == DD:
            print('존나 때리기')
            self.attack_dir += 1
        elif event == DU:
            self.attack_dir -= 1

    def exit(self, event): #attack_d이 끝날 때 마다 때리면 문제가 생김.
        print('그만 때리기')
        #self.face_dir == self.attack_dir

    def do(self):
        self.frame = (self.frame + 1) % 8
        #self.face_dir == self.attack_dir
        #self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.attack_dir == 1 and self.face_dir == 1:
            self.attack_d.clip_draw(self.frame * 200, 100, 200, 100, self.x, self.y)

        elif self.attack_dir == 1 and self.face_dir == -1:
            self.attack_d.clip_draw(self.frame * 200, 0, 200, 100, self.x, self.y)

        elif self.attack_dir == -1:
            self.image.clip_draw(self.frame*100, self.face_dir, 100, 100, 100, self.x, self.y)

        draw_rectangle(*self.get_bb())

    def handle_collision(self, other, group):
        pass #충돌 되어도, 아무 반응없기.


    # def get_bb(self): #박스의 왼쪽 좌표, 오른쪽 좌표 알려주기(4개의 값을 넘겨주기)
    #     if self.attack_dir == 1 and self.face_dir == 1:
    #         return self.x - 15, self.y - 30, self.x + 100, self.y + 30
    #     elif self.attack_dir == 1 and self.face_dir == -1:
    #         return self.x - 100, self.y - 30, self.x + 100, d.y + 30





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
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, TIMER: SLEEP, DD: attack_d, DU: attack_d},
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE},
    SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN},
    attack_d: {DD: IDLE, DU: IDLE},
}




class Boy:

    def __init__(self):
        self.x, self.y = 100, 80
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('SayBar_1.png')
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
                # SLEEP에서 S키를 눌렀을 때 정의가 없어서 오류가 발생함.

            except KeyError: #이 줄을 실행하려 했는데, 문제가 발생했고 그 문제가 KeyError였다면
                # 아래 코드 실행 후 정상적으로 실행된다. 최소한 죽지는 않음.

                # 어떤 상태에서? 어떤 이벤트 때문에 문제가 발생했는지??
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        # self.font.draw(self.x - 60, self.y + 50, ##시발 이게 왜 들어있는거야 내가 또 뭔 잘못했나 존내 머리굴렸는데 시부앙!#
        #                '(Time: %3.2f)' % get_time(), (255, 255, 0))

        debug_print('PPPP')
        debug_print(f'Face Dir: {self.face_dir}, Dir: {self.dir}')

        draw_rectangle(*self.get_bb())  # pico2d 가 제공하는 사각형 그리는거

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb(self): #박스의 왼쪽 좌표, 오른쪽 좌표 알려주기(4개의 값을 넘겨주기)
        return self.x - 15, self.y - 30, self.x + 15, self.y + 30


    def handle_collision(self, other, group):
        pass #그냥 가만히 있기.

    def fire_ball(self):
        print('FIRE BALL')
        ball = Ball(self.x, self.y, self.face_dir*2)
        game_world.add_object(ball, 1)