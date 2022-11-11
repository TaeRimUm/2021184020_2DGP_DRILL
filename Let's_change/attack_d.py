from pico2d import *
import game_world

class Attack_d:
    def __init__(self, x, y, v):
        print('attack_d.py로 이동함')
        Attack_d.image = load_image('attack_d.png')
        self.x, self.y, self.face_dir = x, y, v

    ####################################
    ##여기서 self.attack_dir가 뭔지 모름.##
    ####################################



    def do(self):
        print('do로 옴')
        # self.frame = (self.frame + 1) % 8
        # self.x += self.attack_dir
        # self.x = clamp(0, self.x, 800)

    def draw(self):
        print('공격하는 애니메이션 출력함')

        # if self.attack_dir == 1:
        #     self.Attack_d.clip_draw(self.frame * 100, 0, 200, 100, self.x, self.y)
        # elif self.attack_dir == -1:
        #     self.image.clip_draw(self.frame*100, self.dir, 100, 100, 100, self.x, self.y)

    #def update(self):
    #    self.x += self.velocity

        #Attack_d.__init__() takes 0 positional arguments but 4 were given
        #Attack_d.__init__() takes 1 positional argument but 4 were given