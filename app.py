import sys
import pygame
import pdb
import os
import time
import random
import subprocess
import math

from pygame import gfxdraw

from modules.pie import Pie
from modules.common_constants import *
from modules.boom import Boom

## Start keylogger
subprocess.call(["sudo", "{}/keylogger/start.sh".format(root_path())])

pygame.init()

WIDTH = 600
HEIGHT = 400

size = (WIDTH, HEIGHT)

red_half_visible = (255, 0, 0, 0)

COMBO_KEY_THRESHOLD = 200
COMBO_TIME_THRESHOLD = 5.0 #seconds

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
# screen = pygame.display.set_mode(size)
pygame.display.set_caption("Keyboard Warrior")

clock = pygame.time.Clock()

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


# TODO: params should be sourface, position, font-size
def render_combo_counter(key_count):
    myfont = pygame.font.Font(root_path() + '/assets/bignoodletoo.ttf', 110)
    key_count_str = "{:,}".format(key_count)

    key_count_label = myfont.render(key_count_str, 1, (255,255,255))

    key_count_label_position = (
        screen.get_width() / 2 - key_count_label.get_width() / 2,
        screen.get_height() / 2 - key_count_label.get_height() / 2
    )

    screen.blit(key_count_label, key_count_label_position)

    combo_label_font = pygame.font.Font(root_path() + '/assets/bignoodletoo.ttf', 50)
    combo_label = combo_label_font.render("COMBO!", 1, (255, 255, 255))

    combo_label_position = (
        screen.get_width() / 2 - combo_label.get_width() / 2,
        screen.get_height() / 2 - combo_label.get_height() / 2 + 120
    )

    screen.blit(combo_label, combo_label_position)


def current_time():
    return round(time.time() * 1000)



def render_combo_progress(start_timestamp, max_time = COMBO_TIME_THRESHOLD):
    seconds = (current_time() - start_timestamp)/1000

    value = (100 * seconds)/max_time
    reverse_value = 100 - value

    pie = Pie(100, reverse_value, WHITE, BLACK).to_surface() # radius, value, color, key_color

    # pie = filled_pie(100, reverse_value, WHITE)
    pie.set_colorkey(BLACK)

    pie_position = (
        screen.get_width()/2 - pie.get_width() / 2,
        screen.get_height()/2 - pie.get_height() / 2
    )

    screen.blit(pie, pie_position)



    # Grave yard of pygame examples, remove later
    #
    # pie_surface = pygame.Surface((100, 100)).convert()
    # # pie_surface.set_colorkey(GREEN)
    # pie_surface.fill(BLACK)
    # pygame.draw.ellipse(pie_surface, GREEN, pygame.Rect((0,0), (100, 100)))
    #
    # # screen.blit(self.background, (0, 0))
    # screen.blit(pie_surface, (150, 150))


    # plane = pygame.Surface((out_circle_r*4, out_circle_r*3))
    # plane.fill(GRAY)

    # left = pygame.Surface((out_circle_r*2, out_circle_r*2), pygame.SRCALPHA)
    # pygame.gfxdraw.filled_circle(left, out_circle_r, out_circle_r, out_circle_r, RED)
    # plane.blit(left, (0, 0))

    # right = pygame.Surface((out_circle_r*2, out_circle_r*2), pygame.SRCALPHA)
    # pygame.gfxdraw.filled_circle(right, out_circle_r, out_circle_r, out_circle_r, GREEN)
    # plane.blit(right, (50, 0))




booms = []
last_change = 0
key_count = 0


combo_key_count = 0
combo_start = current_time()

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
    screen.fill(GRAY)

    show_frame_rate(clock.get_fps())

    file_change = read_changes_from_log()

    # ABSOLUTE KEY PRESS, THIS IS MAIN BRAIN
    if (file_change > last_change):
        key_count += 1
        booms.append(Boom(screen, (int(random.uniform(0, WIDTH)), int(random.uniform(0, HEIGHT)))))
        timer_start = current_time()
        combo_key_count += 1

    # TODO: same time_diff is calculated in render method, refactor this
    time_diff = (current_time() - timer_start) / 1000
    if combo_key_count > COMBO_KEY_THRESHOLD and time_diff <= COMBO_TIME_THRESHOLD:
        # Tracking keys for combo
        # combo_key_count += 1
        # if combo_key_count
        render_combo_counter(combo_key_count)
        render_combo_progress(timer_start)


    if time_diff > COMBO_TIME_THRESHOLD:
        combo_key_count = 0

    render_last_keyboard_input(timer_start)
    render_keyboard_input_counter(key_count)

    for i, boom in enumerate(booms):
        if boom.running == False:
            del booms[i]
            continue

        boom.render()

    last_change = file_change
    pygame.display.flip()
