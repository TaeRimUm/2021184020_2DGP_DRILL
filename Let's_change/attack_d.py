from pico2d import *
import game_world

class Attack_d:
    image = None

    def __int__(self, x = 400, y = 300):
        if Attack_d.image == None:
            Attack_d.image = load_image('attack_d.png')
        self.x, self.y, = x, y

    def draw(self):
        self.image.draw(self.x, self.y)
