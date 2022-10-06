from pico2d import *

def handle_events():
    # fill here
    # 좌우 움직이기!!!!
    global running
    global x #바깥쪽에 정의된 X이다!
    global y #일단 추가
    global xdir
    global ydir
    global stop_RIGHT
    global stop_LEFT
    global stop_UP
    global stop_DOWN

    events = get_events() #1. 입력 이벤트 폴링
    for event in events:
        if event.type == SDL_QUIT: #2. 이벤트 종류 구분
            running = False
        elif event.type == SDL_KEYDOWN:

            # 아래 Tab키로 띄어쓰기 중요함
            if event.key == SDLK_RIGHT:  # 오른쪽 #3. 이벤트 실제 입력값 구하기
                xdir += 1  # 증가

            elif event.key == SDLK_LEFT:  # 왼쪽
                xdir -= 1  # 감소

            elif event.key == SDLK_UP:
                ydir += 1

            elif event.key == SDLK_DOWN:
                ydir -= 1

            
            elif event.key == SDLK_ESCAPE:
                running = False


        elif event.type == SDL_KEYUP:

            if event.key == SDLK_RIGHT:
                xdir -= 1


            elif event.key == SDLK_LEFT:
                xdir += 1


            elif event.key == SDLK_UP:
                ydir -= 1


            elif event.key == SDLK_DOWN:
                ydir += 1





open_canvas()
grass = load_image('SayBab_Test_BackGround.png')
character = load_image('SayBar.png')

running = True
x = 800 // 2 #이게 뭔 값이였지# #800 // 2 전체 캔버스800에서 절반을 사용하겠다 는 의미
xdir = 0
ydir = 0
y = 600 // 2 #얘는 내가 왜 넣었지.

frame = 0

while running:
    clear_canvas()
    grass.draw(450, 305)

    if xdir == 0 and ydir == 0: #대기
        character.clip_draw(frame * 100, 300 * 1, 100, 100, x, y)

    #좌우 움직임
    elif xdir == 1 and ydir == 0: #오른쪽으로
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)

    elif xdir == -1 and ydir == 0: #왼쪽으로
        character.clip_draw(frame * 100, 0 * 1, 100, 100, x, y)

    #위아래 움직임
    elif xdir == 0 and ydir == 1: #위로
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    elif xdir == 0 and ydir == -1: #아래로
        character.clip_draw(frame * 100, 0 * 1, 100, 100, x, y)


    #대각선
    elif xdir == 1 and ydir == 1: #오른쪽으로 움직임, 위로 올라감(오른쪽 위 대각선)
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)

    elif xdir == 1 and ydir == -1: #오른쪽으로 움직임, 아래로 내려감(오른쪽 아래 대각선)
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)


    elif xdir == -1 and ydir == 1: #왼쪽으로 움직임, 위로 올라감(왼쪽 위 대각선)
        character.clip_draw(frame * 100, 0 * 1, 100, 100, x, y)

    elif xdir == -1 and ydir == -1:  #왼쪽으로 움직임, 아래로 내려감(왼쪽 아래 대각선)
        character.clip_draw(frame * 100, 0 * 1, 100, 100, x, y)




    # 여기서 빈 공간 이미지 하나 더 만들어서, 빈 이미지 출력하면, 그럴싸 해보이지 않을까?


    if xdir == -1:
        character.clip_draw(frame * 100, 0 * 1, 100, 100, x, y)
                                                       #x, y) 로 수정하면 대각선으로 움직임.
                                                       #90, x)로 수정하면 좌, 우 키눌렀는데 위, 아래로 움직임.
    elif xdir == 1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)


    if ydir == 1 and xdir == 1:
        character.clip_draw(frame * 100, 0 * 1, 100, 100, x, y)

    elif ydir == -1 and xdir == -1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)



    update_canvas()

    handle_events()
    frame = (frame + 1) % 8
    x += xdir * 10
    y += ydir * 10
    delay(0.05)


close_canvas()