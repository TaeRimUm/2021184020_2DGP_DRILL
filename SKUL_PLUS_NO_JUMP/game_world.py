
# layer 0: Background Objects
# layer 1: Foreground Objects
objects = [[], [], [], []]

# collision imformation
# key는 'boy:balls' string
# value는 [ [boy], [ball1, ball2, ball3] ]라는 리스트
                 #이러한 스트링과 리스트를 담고 있는 딕셔너리
collision_group = dict()

def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            # 충돌드룹에서도 지워야 한다.
            remove_collision_object(o)
            del o
            return
    raise ValueError('Trying destroy non existing object')


def all_objects():
    for layer in objects:
        for o in layer:
            yield o


def clear():
    for o in all_objects():
        del o
    for layer in objects:
        layer.clear()


def add_collision_pairs(a, b, group):
    if group not in collision_group: # 그룹 이름이 현재의 컬리젼 이내에 존재하지 않으면,
        print('Add new group ', group) # 새로운 그룹을 등록함
        collision_group[group] = [ [], [] ]  # 빈 리스트 초기화(만들기) # list of list : list pair
                                   #a  #b
    if a:
        if type(b) is list: #a가 리스트라면,
            collision_group[group][1] += b # 리스트니까, 리스트 더하기
        else:
            collision_group[group][1].append(b) # 단일 오브젠트이면 추가
    if b:
        if type(a) is list:
            collision_group[group][0] += a #b가 있으면 2번째 그룹에 넣기. # 리스트니까, 리스트 더하기
        else:
            collision_group[group][0].append(a) # 단일 오브젠트이면 추가


def all_collision_pairs(): ##컬리션 정보에 있는걸 다 꺼내서, 비교할 대상들을 페어로 넘겨줌. 그룹 정보를 추가해서.##
    for group, pairs in collision_group.items():  # key(group이름), value(pairs리스트)를 다 가져옴.
        for a in pairs[0]: #pairs[0]에 들어있는 a
            for b in pairs[1]: #pairs[1]에 들어있는 b //양쪽 리스트에 들어있는걸 서로 뽑아옴.
                yield a, b, group


def remove_collision_object(o): #22~23행 : 리스트에서 지울 때 하나하나 검사하는거.
    for pairs in collision_group.values(): # key는 필요 없음.
        if o in pairs[0]: #o가 첫번째그룹(a)에 있으면
            pairs[0].remove(o)
        if o in pairs[1]: #o가 두번째그룹(b)에 있으면
            pairs[1].remove(o)
#컬리션 정보에서 오브젝트를 삭제하는 것.


