from pico2d import *

def handle_events():
    # 좌우 움직이기!!!!
    global running
    global x, y, xdir, ydir #바깥쪽에 정의된 X
    global t
    global attack_1

    events = get_events() #1. 입력 이벤트 폴링
    for event in events:
        if event.type == SDL_QUIT: #2. 이벤트 종류 구분
            running = False
        elif event.type == SDL_KEYDOWN:

            if event.key == SDLK_RIGHT:  # 오른쪽 #3. 이벤트 실제 입력값 구하기
                xdir += 1  # 증가
                t = 1

            elif event.key == SDLK_LEFT:  # 왼쪽
                xdir -= 1  # 감소
                t = 0

            elif event.key == SDLK_UP:
                ydir += 1

            elif event.key == SDLK_DOWN:
                ydir -= 1

            elif event.key == SDLK_ESCAPE:
                running = False

            elif event.key == SDLK_d:
                attack_1 += 1
                t = 4


        elif event.type == SDL_KEYUP:

            if event.key == SDLK_RIGHT:
                xdir -= 1
                t = 3

            elif event.key == SDLK_LEFT:
                xdir += 1
                t = 2

            elif event.key == SDLK_UP:
                ydir -= 1

            elif event.key == SDLK_DOWN:
                ydir += 1

            elif event.key == SDLK_d:
                attack_1 -= 1
                t = 3




open_canvas()
grass = load_image('SayBab_Test_BackGround.png')
character = load_image('SayBar_1.png')

running = True
attack = True
x = 800 // 2 #800 // 2 전체 캔버스800에서 절반을 사용하겠다 는 의미
y = 600 // 2
xdir = 0
ydir = 0
attack_1 = 0
frame = 0
t = 3

while running:
    clear_canvas()
    grass.draw(430, 305)

    character.clip_draw(frame * 100, 100 * t, 100, 100, x, y)
    #if xdir == 0 and ydir == 0: #대기
        #character.clip_draw(frame * 100, 100 * 3, 100, 100, x, y)

    if attack_1 == 1 :  # 공격
        character.clip_draw(frame * 100, 500 * 1, 100, 100, x, y)


    if xdir != 0 and ydir != 0:
        character.clip_draw(frame * 100, 100 * 4, 100, 100, x, y)

    #좌우 움직임
    if xdir == 1 and ydir == 0: #오른쪽으로
        character.clip_draw(frame * 100, 100 * t, 100, 100, x, y)

    elif xdir == -1 and ydir == 0: #왼쪽으로
        character.clip_draw(frame * 100, 100 * t, 100, 100, x, y)


    #위아래 움직임
    elif xdir == 0 and ydir == 1: #위로
        character.clip_draw(frame * 100, 100 * t, 100, 100, x, y)

    elif xdir == 0 and ydir == -1: #아래로
        character.clip_draw(frame * 100, 100 * t, 100, 100, x, y)


    #대각선
    elif xdir == 1 and ydir == 1: #오른쪽으로 움직임, 위로 올라감(오른쪽 위 대각선)
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)

    elif xdir == 1 and ydir == -1: #오른쪽으로 움직임, 아래로 내려감(오른쪽 아래 대각선)
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)


    elif xdir == -1 and ydir == 1: #왼쪽으로 움직임, 위로 올라감(왼쪽 위 대각선)
        character.clip_draw(frame * 100, 0 * 1, 100, 100, x, y)

    elif xdir == -1 and ydir == -1: #왼쪽으로 움직임, 아래로 내려감(왼쪽 아래 대각선)
        character.clip_draw(frame * 100, 0 * 1, 100, 100, x, y)
        

    update_canvas()

    handle_events()
    frame = (frame + 1) % 8
    x += xdir * 10
    y += ydir * 10
    delay(0.05)


close_canvas()