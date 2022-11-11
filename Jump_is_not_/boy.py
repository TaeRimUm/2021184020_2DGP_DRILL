import pico2d
from pico2d import *
import game_world
import play_state #ball 객체확보
from ball import Ball #볼 클래스인 Ball를 확보.
#from attack_d import Attack_d

# #점프키 구현에서 쓰이는 속도와 질량 기본 값#
# VELOCITY = 7
# MASS = 2
#
# #게임화면 크기#
# WINDOW_WIDTH = 800
# WINDOW_HIGHT = 500

#1 : 이벤트 정의
RD, LD, RU, LU, TIMER, S, DD, DU, SPACE = range(9)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'S', 'DD', 'DU', 'SPACE']

key_event_table = {
    # (SDL_KEYDOWN, SDLK_s): S, ##얘는 검사라 공 못던져!!##
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_d): DD,
    (SDL_KEYUP, SDLK_d): DU,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}

#2 : 상태의 정의
class IDLE:
    @staticmethod
    def enter(self, event):
        print('IDLE 엔터')
        self.dir = 0
        self.attack_dir = 0
        self.space_dir = 0

        self.timer = 1000

    @staticmethod
    def exit(self, event): #IDLE이 끝날 때 마다 파이어볼하면 문제가 생김.
        print('IDLE 나가기')

        ##얘는 검사라 공 못던져!!##
        # if event == S: #그래서 S가 눌린 exit일 때 파이어볼을 함.
        #     self.fire_ball()
        # elif event == DD:
        #     print('DD키를 입력함.')
        #     self.attack_d()
        ##얘는 검사라 공 못던져!!##

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
        print('RUN 입력')
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1


    def exit(self, event): #RUN이 끝날 때 마다 파이어볼하면 문제가 생김.
        print('RUN 나가기')
        self.face_dir = self.dir

        ##얘는 검사라 공 못던져!!##
        # if event == S: #그래서 RUN일 상태에서 스페이스를 눌러서, exit일 때 파이어볼을 함.
        #     self.fire_ball() #달려가면서 공발사할 수 있도록.
        ##얘는 검사라 공 못던져!!##


    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)


class attack_d:
    def enter(self, event):
        if event == DD:
            print('attack_d 입력')
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


# class JUMP:
#     def enter(self, event):
#         if event == SPACE:
#             self.space_dir += 1
#


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
    IDLE:  {RU: RUN,  LU: RUN,  RD: RUN,  LD: RUN, TIMER: SLEEP, DD: attack_d, DU: attack_d}, #S: IDLE
    RUN:   {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE}, #S: RUN
    SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN}, #S: IDLE
    attack_d: {DD: IDLE, DU: IDLE},
    # JUMP: {SPACE: IDLE, SPACE: RUN, SPACE: SLEEP}
}




class Boy:

    def __init__(self):
        self.x, self.y = 800 // 2, 90 #90 -> 50 으로 바꾸면 먼저 그린게 먼저 가려짐. 소년->잔디 순으로 그렸기 때문이다.
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('SayBar_1.png')

        self.attack_d = load_image('attack_d.png')

        self.timer = 100

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    #     #점프#
    #     self.jump_image = load_image('SayBar_1.png')
    #     self.rect = ""
    #     self.x = ''
    #     self.isJump = 0
    #     self.v = VELOCITY #속도
    #     self.m = MASS #질량
    #
    # def jump(self, j): #점프 상태를 체크하는 메서드
    #     self.isJump = j



    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try: #예외처리
                self.cur_state = next_state[self.cur_state][event]
                #SLEEP에서 S키를 눌렀을 때 정의가 없어서 오류가 발생함.

            except KeyError: #이 줄을 실행하려 했는데, 문제가 발생했고 그 문제가 KeyError였다면
                # 아래 코드 실행 후 정상적으로 실행된다. 최소한 죽지는 않음.

                # 어떤 상태에서? 어떤 이벤트 때문에 문제가 발생했는지??
                print(f'Error: State {self.cur_state.__name__}  Event {event_name[event]}')
            self.cur_state.enter(self, event)
            
    #     #점프 구현# - 점프일 경우 y 좌표를 변경해주는 메서드
    #     if self.isJump > 0: #isJump 값이 0보다 큰지 확인
    #         # isJump 값이 2일 경우 속도를 리셋.
    #         # 점프 한 상태에서 다시 점프를 위한 값.
    #         # 이 코드를 주석처리하면 이중점프를 못함.
    #         if self.isJump == 2:
    #             self.v = VELOCITY
    #
    #         # 역학공식 계산 (F). F = 0.5 * mass * velocity^2
    #         if self.v > 0: # 속도가 0보다 클 때는 위로 올라감.
    #             F = (0.5 * self.m * (self.v * self.v))
    #         else: # 속도가 0보다 작을 때는 아래로 내려감.
    #             F = -(0.5 * self.m * (self.v * self.v))
    #
    #         # 좌표 수정 : 위로 올라가기 위해서는 y좌표를 줄여줌.
    #         #self.y -= round(F)
    #
    #         # 속도 줄여줌
    #         self.v -= 1
    #
    #         # 바닥에 닿았을 때, 변수 리셋
    #         if self.x.bottom > WINDOW_HIGHT:
    #             self.x.bottom = WINDOW_HIGHT
    #             self.isJump = 0
    #             self.v = VELOCITY
    #     # 점프 구현# - 점프일 경우 y 좌표를 변경해주는 메서드
    #
    # # 점프 구현# - 스페이스바를 눌렀을 때, 점프 상태를 변경시켜주는 코드를 게임 루프안에 추가.
    #     while get_events():
    #         # 키가 눌린 상태 체크
    #         keys = pico2d.key.get_pressed()
    #         # 스페이스키가 눌려있고, isJump가 2라면 1로 변경한다.
    #         # 이 작업을 해주지 않으면 스페이스가 눌려있는 상태면 플레이어가 계속 위로 올라가게 됨.
    #         if (keys[pico2d.SDLK_SPACE]):
    #             if self.isJump == 2:
    #                 self.jump(1)
    #
    #         for event in pico2d.event.get():
    #             if event.type == pico2d.SDL_QUIT:
    #                 event = False
    #                 pico2d.quit()
    #                 sys.exit()
    #
    #             # 스페이스키를 눌렀을 때,
    #             # 0이면 바닥인 상태 : 1로 변경
    #             # 1이면 점프를 한 상태 : 2로 변경,
    #             #점프 한 위치에서 다시 점프를 하게 된다. = 낭만 넘치는 이중점프.
    #             if event.key == pico2d.SDLK_SPACE:
    #                 if event.isJump == 0:
    #                     event.jump(1)
    #                 elif event.isJump == 1:
    #                     event.jump(2)


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

    ##얘는 검사라 공 못던져!!##
    # def fire_ball(self):
    #     print('FIRE BALL')
    #     #생성
    #     ball = Ball(self.x, self.y, self.face_dir*3) #self.face_dir = 바라보는 뱡항
    #     game_world.add_object(ball, 1)
    ##얘는 검사라 공 못던져!!##

    # def attack_d(self):
    #     attack_d = Attack_d(self.x, self.y, self.face_dir*3)
    #     attack_d.do()
    #     attack_d.draw()



