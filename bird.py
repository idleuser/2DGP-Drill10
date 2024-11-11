import random

from pico2d import get_time, load_image
from state_machine import *
import game_world
import game_framework

# 새 달리기 속도
PIXEL_PER_METER = (10.0 / 0.3)
FLY_SPEED_KMPH = 35.0
FY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = FLY_SPEED_MPS * PIXEL_PER_METER

#새 애니메이션 속도
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class Run:
    @staticmethod
    def enter(bird, e):
        bird.dir, bird.face_dir, bird.action = 1, 1, 2
        bird.frame = random.randint(0, 4)

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        if bird.x >= 1500:
            bird.dir = -1
        elif bird.x <= 20:
            bird.dir = 1

        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        bird.x += bird.dir * FLY_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(bird):
        if bird.dir > 0:
            bird.image.clip_draw(int(bird.frame) * 184, bird.action * 169, 184, 169, bird.x, bird.y, 100, 100)
        elif bird.dir < 0:
            bird.image.clip_composite_draw(int(bird.frame) * 184, bird.action * 169, 184, 169, 0, 'h', bird.x, bird.y, 100, 100)



class Bird:
    def __init__(self):
        self.x, self.y = random.randint(20, 1300), 390
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            {
                Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Run}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()