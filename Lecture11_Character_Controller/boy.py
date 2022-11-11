from pico2d import *


#이벤트 정의 Right Down...Letf Up
#RD, LD, RU, LU = 0, 1, 2, 3
RD, LD, RU, LU, TIMER, AUTO_RUN,AU,AD = range(8)

key_event_table = { #맵핑
    (SDL_KEYDOWN, SDLK_RIGHT) : RD,
    (SDL_KEYDOWN, SDLK_LEFT) : LD,
    (SDL_KEYUP, SDLK_RIGHT) : RU,
    (SDL_KEYUP, SDLK_LEFT) : LU,
    (SDL_KEYDOWN, SDLK_a) : AD,
    (SDL_KEYUP, SDLK_a) : AU

}

#이벤트가 막 들어오는걸 해석할 큐가 필요함 -> 들어오는 작업을 놓치지 않고, 하나하나 꺼내서 실행하는게 큐다.
# "줄 서" 먼저 오는 사람(이벤트) 먼저 실행 in, out





#스테이트를 클래스를 이용해서 구현. 클래스의 함수를 그루핑하는 기능을 이용해서.
class IDLE: ##상태를 먼저 만듦.##
    #들어올 떄, 나갈 때 각각 함수로 구현
    @staticmethod #<== 이게 self안쓰도록 하는거.
    def enter(self, event): #enter(self)안쓰도록.
        print('ENTER IDLE')
        self.dir = 0 #정지상태니까 0
        self.timer = 1000

        #키가 눌렸을 떄, 떄였을 때 움직임 정의를 정리한거임.


    @staticmethod
    def exit(self):
        print('EXIT IDLE')

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8

        self.timer -= 1 #시간 감소
        if self.timer == 0: #시간이 다 되면,
            self.add_event(TIMER) #쳐 자기.


    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)

class RUN: ##이벤트를 만듦.##
    def enter(self, event): #왼쪽 눌렸을 때부터 오른쪽 때였을 떄 까지 많은 이벤트가 들어감 +event
        print('ENTER RUN')

        #어떤 이벤트 때문에, RUN으로 들어왔는지 파악을 하고, 그 이벤트에 따라사 실제 방향을 결정.
        if event == RD:
            self.dir += 1
        elif event == LD:
            self.dir -= 1
        elif event == RU:
            self.dir -= 1
        elif event == LU:
            self.dir += 1
        elif event == AD:
            self.a += 1
        elif event == AU:
            self.a -= 1

    def exit(self):
        print('EXIT RUN')

        #RUN 상태를 나갈 떄 ==> 움직임을 멈췄기 때문에, 왼쪽에서 멈췄으면 왼쪽보기가 가능함.
        #런 상태를 나갈 때, 현재 방향을 저장해 놓음.
        self.face_dir = self.dir


    def do(self):

        #달리게 만들기.
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        self.x = clamp(0, self.x, 800)

    def draw(self): #단순한 이름이라 self나 boy나 상관없음.
        print('DRAW RUN')
        if self.dir == -1:
            self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)


class SLEEP: ##상태를 먼저 만듦.##
    #들어올 떄, 나갈 때 각각 함수로 구현
    @staticmethod #<== 이게 self안쓰도록 하는거.
    def enter(self, event):
        print('ENTER SLEEP')
        self.frame = 0

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8

    @staticmethod
    def draw(self):
        print('DRAW SLEEP')
        if self.face_dir == -1:
            self.image.clip_composite_draw(self.frame * 100, 200, 100, 100,
                                           -3.141592/2, '', #회전각, 좌우반전. 누워있는거니까ㅇㅇ
                                           self.x + 25, self.y - 25, 100, 100)
        else:
            self.image.clip_compoaite_draw(self.frame * 100, 300, 100, 100,
                                 3.141592/2, '',
                                 self.x - 25, self.y - 25, 100, 100)


#상태 변환
next_state = {
    IDLE : { RU:RUN, LU:RUN, RD:RUN, LD:RUN, TIMER:SLEEP }, #두개가 동시에 눌러져 있을 때(왼, 오) 오른쪽을 때면 왼쪽으로 가도록.
    RUN : { RU:IDLE, LU:IDLE, LD:IDLE, RD:IDLE },
    SLEEP : { RU:RUN, LU:RUN, RD:RUN, LD:RUN },
    AUTO_RUN : { RU:RUN, LU:RUN, RD:RUN, LD:RUN, TIMER:SLEEP, RU:IDLE, LU:IDLE, LD:IDLE, RD:IDLE }
}

        #if event.type == SDL_KEYDOWN:
        #    match event.key:
        #        case pico2d.SDLK_LEFT:
        #            self.dir -= 1
        #        case pico2d.SDLK_RIGHT:
        #            self.dir += 1
        #elif event.type == SDL_KEYUP:
        #    match event.key:
        #        case pico2d.SDLK_LEFT:
        #            self.dir += 1
        #            self.face_dir = -1
        #        case pico2d.SDLK_RIGHT:
        #            self.dir -= 1
        #            self.face_dir = 1
        #pass
class Boy:
    def __init__(self):
        self.x, self.y = 800//2, 90
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('animation_sheet.png')

        self.timer = 100
        self.q = []
        #초기상태 설정과 entry action 수행
        self.cur_state = IDLE #맨 처음 상태는 IDLE임.
        self.cur_state.enter(self, None) #다른 이벤트가 없으니 None.

    def update(self):
        self.cur_state.do(self)

        if self.q:  # 만약 list q에 뭔가 들어있으면...
            event = self.q.pop()  # 이벤트 꺼내기
            self.cur_state.exit(self)  # 현재 상태 나가고
            self.cur_state = next_state[self.cur_state][event]  # 현재 상태(다음 상태) 계산
            self.cur_state.enter(self, event) #다음 상태의 enter 액션을 수행.

    def draw(self): #소년을 그려야 함.
        self.cur_state.draw(self) #draw(self)로 자기 자신을 넘겨줌.

    def add_event(self, event):
        self.q.insert(0, event)

    def handle_event(self, event):  # event 입력 이벤트
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


        #self.frame = (self.frame + 1) % 8
        #self.x += self.dir * 1
        #self.x = clamp(0, self.x, 800)

        #if self.dir == -1:
        #    self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        #elif self.dir == 1:
        #    self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)
        #else:
        #    if self.face_dir == 1:
        #        self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        #    else:
        #        self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
