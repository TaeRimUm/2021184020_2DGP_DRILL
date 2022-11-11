import random
from pico2d import *
import game_world

class Ball:
    image = None

    def __init__(self):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.fall_speed = random.randint(0, 1600), 70, 0

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())  # pico2d 가 제공하는 사각형 그리는거

    def update(self):
        self.x += self.fall_speed

    def get_bb(self): #박스의 왼쪽 좌표, 오른쪽 좌표 알려주기(4개의 값을 넘겨주기)
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, other, group):
        if group == 'boy:ball': #볼 입장에서 소년이 부딪히면
            game_world.remove_object(self) #근데 이렇게 삭제해도 game_world에는 안없어짐. 여전히 충돌됨. 그 리스트에서도 삭제를 해 줘야 함.
            #나랑 부딪혔을 때 정보가 필요하니까 other도 넘겨줌.