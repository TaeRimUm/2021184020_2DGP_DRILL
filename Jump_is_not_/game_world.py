# layer 0: 백스라운드 옵젝
# layer 1: 포그라운드 옵젝
objects = [[], [], [], []]

def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o) # 리스트로부터 삭제
    #공이 화면 밖으로 나가면 없어짐. 하지만 메모리에서 날리지는 않음.
    #월드에서 지운거지, 메모리에서 지운건 아니기 때문.
            del o # 실제로 메모리 삭제
            return
    raise ValueError('Trying destory non existing object')

def all_objects():
    for layer in objects:
        for o in layer:
            yield o

def clear():
    for o in all_objects():
        del o
    for layer in objects:
        layer.clear()

