from pico2d import *
import game_world
import game_framework
from boy import Boy
from grass import Grass
from ball import Ball
from zombie import Zombie
import random

boy = None


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy
    global balls

    # 객체들을 생성
    boy = Boy()
    grass = Grass()
    balls = [Ball(random.randint(100, 1600-100), 60, 0) for _ in range(30)]
    zombies = [Zombie() for i in range(4)]

    # 생성된 객체들을 game_world에 등록
    game_world.add_oject(boy)
    game_world.add_oject(grass, 0)
    game_world.add_objects(balls, 1)
    game_world.add_objects(zombies, 1)

    game_world.add_collision_pairs("boy:ball", boy, None)
    game_world.add_collision_pairs("zombies:ball", zombies, None)
    # 생성된 객체들의 충돌 관계를 등록
    for ball in balls:
        game_world.add_collision_pairs('boy:ball', None, ball)
        game_world.add_collision_pairs("zombies:ball", None, zombies)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()
    game_world.handle_collision()
     # .copy()를 사용하여 balls 리스트를 복사한 후 반복합니다. 이렇게 하면 반복 중에 balls 리스트에서 요소를 제거해도 반복이 안전하게 진행됩니다.
    #for ball in balls.copy(): # [:]  <- 이렇게 해도 됨   
     #     if game_world.colide(boy, ball):
     #          print('COLLISION BOY:BALL \n\n')
     #         game_world.remove_object(ball)
     #          boy.ball_count += 1
     #         balls.remove(ball)
              

def render():
    clear_canvas()
    game_world.render()
    update_canvas()




# 현재의 게임엔진들은 아래 설명하는 구조를 가지고 있음
# 충돌처리가 필요로 하는 두개의 객체 A,B를 먼저 일일이 등록하고,
# 나중에 등록된 페어 전체에 대해 충돌검사를 수행한 후, 충돌이 있으면 A,B에게
# 충돌 처리를 할 수 있도록 지시함.
# 충돌 처리해야할 대상들을 그룹화해서 처리


# 딕셔너리를 활용함
# Key값은 문자열, 내부 값은 리스트로 구성
# ex) "boy:ball"은 Key값, boy, ball 객체들은 리스트에 들어감

