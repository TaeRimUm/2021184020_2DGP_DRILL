from pico2d import *
import game_framework
import game_world
import gamestop

from grass import Grass
from boy import Boy, attack_d
from ball import Ball

boy = None
grass = None
balls = []


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            boy.handle_event(event)

        if event.key == SDLK_q:
            game_framework.push_state(gamestop)


# 초기화
def enter():
    global boy, grass
    boy = Boy()
    grass = Grass()


    game_world.add_object(grass, 0)
    game_world.add_object(boy, 1)

    global balls
    balls = [Ball() for i in range(10)]
    game_world.add_objects(balls, 1)

    # 충돌 대상 정보 등록
    game_world.add_collision_pairs(boy, balls, 'boy:ball')
                                    #'boy:ball' 이란 그룹의 이름으로 boy와 ball의 충돌하겠다라는걸 저장함.


# 종료
def exit():
    game_world.clear()

def update():
    # 원래 def update에서 바꾸면 내가 어떤 객체를 추가하든, 이 코드를 수정할 필요가 없음.
    # 게임월드를 만들어 거기에 객체를 넣고 빼므로써, 전체를 통째로 업데이트를 만들어 줌으로써,
    # 새로운 객체가 추가 되더라도 거기에 대한 코딩을 할 필요가 없음.
    for game_object in game_world.all_objects():
        game_object.update()

    # 만약에 게임 월드에 충돌체크를 해야 될 2개의 대상을 나한테 넣어줄 수 있는 기능이 있다면,
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b): #a하고 b가 충돌이 되면,
            print('COLLISION ', group)
            a.handle_collision(b, group) #큰놈이 와서 박았는지, 작은놈이 와서 박았는지. #어떤놈이 너한테 와서 충돌했는지 알려주기.
            b.handle_collision(a, group) #충돌처리를 하라고 명령.

    # # 충돌 체크.
    # # 볼들과 소년의 충돌
    # for ball in balls.copy():                            #!!copy는 복사본!!
    #     if collide(boy, ball):
    #         print('COLLISION boy:ball 소년과 볼의 충돌이다')
    #         balls.remove(ball) #리스트 자체를 건드려서 위험함. !!balls는 원본!!
    #         game_world.remove_object(ball) #볼들 죽이기 - 하지만 오류, ball에서는 죽였지만, balls는 못죽임.
    #                                         #balls는 충돌 체크할 볼만 관리. balls는 Null로 있음.
    # for ball in balls:
    #     if collide(grass, ball):
    #         ball.stop()




def draw_world():
    for game_object in game_world.all_objects():
        game_object.draw()

def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    pass

def resume():
    pass


def collide(a, b): #a하고 b라는 객체가 충돌하느냐?
    left_a, bottom_a, right_a, top_a = a.get_bb()  # a의 바운딩 박스로부터 가져옴
    left_b, bottom_b, right_b, top_b = b.get_bb()  # b의 바운딩 박스로부터 가져옴

    if left_a > right_b: return False  # 왼쪽에 닿으면    ##A의 왼쪽이, B의 오른쪽보다 크면
    if right_a < left_b: return False  # 오른쪽에 닿으면  ##A의 오른쪽이 B의 왼쪽보다 작으면
    if top_a < bottom_b: return False  # 위에 닿으면     ##A의 위쪽이 B의 아래쪽보다 작으면
    if bottom_a > top_a: return False  # 바닥에 닿으면   ##A의 아래쪽이 B의 위쪽보다 크면
    # 충돌하지 않는걸 걸러내는거
    return True


def test_self():
    import play_state

    pico2d.open_canvas()
    game_framework.run(play_state)
    pico2d.clear_canvas()

if __name__ == '__main__':
    test_self()
