world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI

def add_oject(o, depth=1):
    world[depth].append(o)

def add_objects(ol, depth=1):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

def update():
    for layer in world:
        for o in layer[:]:
            o.update()

def render():
    for layer in world:
        for o in layer[:]:
            o.draw()

def colide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True



def clear():
    for layer in world:
        layer.clear()

collision_pairs = {}

def add_collision_pairs(group, a, b):

    if group not in collision_pairs: # 처음 등록되는 그룹이면 그룹을 생성함
        collision_pairs[group] = [[], []]

    # group에 0번째 인덱스에는 a 객체들을, 1번째 인덱스에는 b 객체들을 저장
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collision():
    # items를 사용하여 key, value를 동시에 가져옴
    for group, pairs in collision_pairs.items():  
        for a in pairs[0]: # a 객체들을 반복
            for b in pairs[1]: # b 객체들을 반복
                if colide(a, b): # 충돌이 발생하면
                    a.handle_collision(group, b) # group을 넘겨 충돌상황과 함께 a에게 충돌처리를 지시
                    b.handle_collision(group, a) # group을 넘겨 충돌상황과 함께 b에게 충돌처리를 지시



def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
        
    raise ValueError('Trying destroy non existing object')