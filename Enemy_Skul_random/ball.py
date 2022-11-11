import random
#pip install pandas , pip install pillow
from pico2d import *
import game_world

class Ball:
    frame = 0
    image = None
    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x = clamp(0, self.x, 1600)

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('Enemy_Skul_1.png')
        self.x, self.y, self.fall_speed = random.randint(0, 1600), 90, 0


    def draw(self):
        #t = [200, 300]
        self.frame = (self.frame + 1) % 8
        #self.x = clamp(0, self.x, 1600)
        #self.image.draw(self.x, self.y) # 일단 200으로 넣자. #
        self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
        #self.image.clip_draw(self.frame * 100, (random.choice(t)), 100, 100, self.x, self.y)
                                                    # ㄴ> 이거 넣으면 도리도리 존내함. 200이랑 300 중 하나를 뽑아오는건 맞는데,
                                                    # ㄴ> def draw 전체가 계속 돌아가는거라 도리도리하는 거일 듯.
                                                    # ㄴ> 이거 한번만 돌아가게 하고 싶은데, 이건 교수님께 여쭤보자. 방법을 모르겠다.

        draw_rectangle(*self.get_bb())  # pico2d 가 제공하는 사각형 그리는거


    def update(self):
        self.x += self.fall_speed

    def get_bb(self): #박스의 왼쪽 좌표, 오른쪽 좌표 알려주기(4개의 값을 넘겨주기)
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, other, group):
        if group == 'boy:ball': #볼 입장에서 소년이 부딪히면
            game_world.remove_object(self) #근데 이렇게 삭제해도 game_world에는 안없어짐. 여전히 충돌됨. 그 리스트에서도 삭제를 해 줘야 함.
            #나랑 부딪혔을 때 정보가 필요하니까 other도 넘겨줌.