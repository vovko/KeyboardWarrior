import sys, pygame
from pygame import gfxdraw
import pdb
import os
import time
import random

pygame.init()

WIDTH = 400
HEIGHT = 200

size = (WIDTH, HEIGHT)


RED = (255,0,0)
black = (0, 0, 0)
red_half_visible = (255, 0, 0, 0)
grey=(125, 125, 125)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

class Boom:
    last_time = 0
    position = None
    # self.radius = 10
    frames = 0
    running = True

    max_radius = 0

    color = RED

    def __init__(self, screen, position):
        self.radius = 10
        self.position = position
        self.last_time = self.current_time()
        self.max_radius = int(random.uniform(40, 80))

    def render(self):
        if (self.running == False):
            return None

        if ( self.current_time() >  self.last_time + 5):
            self.next_frame()
            self.last_time = self.current_time()

        # pygame.draw.circle(screen, self.color, , self.radius)
        # pygame.gfxdraw.filled_circle(screen, self.position[0], self.position[1], self.radius, self.color)
        pygame.gfxdraw.aacircle(screen, self.position[0], self.position[1], self.radius, self.color)
        pygame.gfxdraw.filled_circle(screen, self.position[0], self.position[1], self.radius, self.color)


    def current_time(self):
        return round(time.time() * 1000)

    def next_frame(self):
        if(self.radius > self.max_radius-20):
            self.color = (255,255,255)

        if(self.radius > self.max_radius):
            self.running = False

        self.radius += 5

def root_path():
    return os.path.dirname(os.path.realpath(__file__))

def show_frame_rate(fps):
    padding = 2
    box_width = 60
    box_height = 20
    box_x = WIDTH-box_width-padding
    box_y = padding

    # print("fps:", fps)
    myfont = pygame.font.SysFont("monospace", 15)
    pygame.draw.rect(screen, grey, (box_x, box_y, box_width, box_height), 0)


    # render text
    label = myfont.render(str(int(fps)), 1, (255, 255, 255))
    screen.blit(label, (box_x, 0))


def read_changes_from_log():
    path_to_file = root_path() + '/keylogger/log/keys.log'
    return os.stat(path_to_file).st_mtime

def show_read_change(timestamp):
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render(str(int(timestamp)), 1, (255,255,255))
    screen.blit(label, (100, 100))


booms = []
last_change = 0

while 1:
    time.sleep(0.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    clock.tick()
    screen.fill(black)

    show_frame_rate(clock.get_fps())

    file_change = read_changes_from_log()
    show_read_change(file_change)


    if (file_change > last_change):
        booms.append(Boom(screen, (int(random.uniform(0, WIDTH)), int(random.uniform(0, HEIGHT)))))

    for i, boom in enumerate(booms):
        if boom.running == False:
            del booms[i]
            continue

        boom.render()

    last_change = file_change
    pygame.display.flip()
