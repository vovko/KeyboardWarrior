import sys, pygame
from pygame import gfxdraw
import pdb
import os
import time
import random
import subprocess
import math

## Start keylogger
def root_path():
    return os.path.dirname(os.path.realpath(__file__))

# pdb.set_trace()
subprocess.call(["sudo", "{}/keylogger/start.sh".format(root_path())])


pygame.init()

WIDTH = 800
HEIGHT = 400

size = (WIDTH, HEIGHT)


RED = (255,0,0)
BLACK = (0, 0, 0)
red_half_visible = (255, 0, 0, 0)
GRAY=(125, 125, 125)
GREEN=(0,100,0)

# KEYBOARD KEYS
Q_KEY = 113
F_KEY = 102

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
# screen = pygame.display.set_mode(size)
pygame.display.set_caption("Keyboard Warrior")

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


def show_frame_rate(fps):
    padding = 2
    box_width = 60
    box_height = 20
    box_x = WIDTH-box_width-padding
    box_y = padding

    # print("fps:", fps)
    myfont = pygame.font.SysFont("monospace", 15)
    pygame.draw.rect(screen, GRAY, (box_x, box_y, box_width, box_height), 0)


    # render text
    label = myfont.render(str(int(fps)), 1, (255, 255, 255))
    screen.blit(label, (box_x, 0))


def read_changes_from_log():
    path_to_file = root_path() + '/keylogger/log/keys.log'
    return os.stat(path_to_file).st_mtime


def render_last_keyboard_input(start_timestamp):
    myfont = pygame.font.Font(root_path() + '/assets/bignoodletoo.ttf', 50)

    one_minute = 60
    one_hour = one_minute * 60

    seconds = (current_time() - start_timestamp)/1000
    hours = int(seconds / 3600)
    minutes = int(seconds / 60)
    leftover = round(seconds - (3600*hours) - (60*minutes), 3)

    # TODO: Refactor this using adequate date formatter
    # Current lazy implementation breaks after long period of time
    if hours > 0:
        hours_str = "{}h ".format(hours)
    else:
        hours_str = ""

    if minutes > 0:
        minutes_str = "{}m ".format(minutes)
    else:
        minutes_str = ""

    since_formatted = "{}{}{}".format(hours_str, minutes_str, leftover)


    time_passed = "Since last keyboard input: " + since_formatted

    label = myfont.render(time_passed, 1, (255,255,255))
    screen.blit(label, (10, 10))

def render_keyboard_input_counter(key_count):
    myfont = pygame.font.Font(root_path() + '/assets/bignoodletoo.ttf', 25)
    key_count_label = "Key count: {:,}".format(key_count)

    label = myfont.render(key_count_label, 1, (255,255,255))
    screen.blit(label, (10, 60))

def current_time():
    return round(time.time() * 1000)

pie_start = 0


def fill_arc(surface, center, radius, theta0, theta1, color, ndiv=360):
    x0, y0 = center

    dtheta = (theta1 - theta0) / ndiv
    angles = [theta0 + i*dtheta for i in range(ndiv + 1)]

    points = [(x0 + radius * math.cos(math.radians(theta)), y0 - radius * math.sin(math.radians(theta))) for theta in angles]

    for pair in points:
        # pygame.gfxdraw.filled_trigon(surface, x0, y0, int(pair[0]), int(pair[1]), int(pair[0]+1), int(pair[1]), color)
        pygame.gfxdraw.line(surface, x0, y0, int(pair[0]), int(pair[1]), RED)

def render_combo_timer(start_timestamp):
    seconds = (current_time() - start_timestamp)/1000
    max_width = 360
    step_size = max_width - (seconds)*100

    fill_arc( screen, (200,200), 100, 0, step_size, RED )

    if step_size < 1:
        return

    start_x = 10

    out_circle_x = 200
    out_circle_y = 200
    out_circle_r = 50

    # plane = pygame.Surface((out_circle_r*4, out_circle_r*3))
    # plane.fill(GRAY)


    # left = pygame.Surface((out_circle_r*2, out_circle_r*2), pygame.SRCALPHA)
    # pygame.gfxdraw.filled_circle(left, out_circle_r, out_circle_r, out_circle_r, RED)
    # plane.blit(left, (0, 0))

    # right = pygame.Surface((out_circle_r*2, out_circle_r*2), pygame.SRCALPHA)
    # pygame.gfxdraw.filled_circle(right, out_circle_r, out_circle_r, out_circle_r, GREEN)
    # plane.blit(right, (50, 0))

    combo_duration = 10


booms = []
last_change = 0
key_count = 0

timer_start = current_time()


while 1:
    time.sleep(0.01)
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == Q_KEY:
                sys.exit()

            # Fullscreen acts strange in Ubuntu
            # if event.key == F_KEY:
            #     pygame.display.toggle_fullscreen()


        if event.type == pygame.QUIT: sys.exit()

    clock.tick()
    screen.fill(BLACK)

    show_frame_rate(clock.get_fps())

    file_change = read_changes_from_log()

    if (file_change > last_change):
        key_count += 1
        booms.append(Boom(screen, (int(random.uniform(0, WIDTH)), int(random.uniform(0, HEIGHT)))))
        timer_start = current_time()

    render_last_keyboard_input(timer_start)
    render_keyboard_input_counter(key_count)
    render_combo_timer(timer_start)


    for i, boom in enumerate(booms):
        if boom.running == False:
            del booms[i]
            continue

        boom.render()

    last_change = file_change
    pygame.display.flip()
