import sys, pygame
import pdb
import os
pygame.init()

WIDTH = 400
HEIGHT = 200

size = (WIDTH, HEIGHT)

black = (0, 0, 0)
red = (255,0,0)
red_half_visible = (255, 0, 0, 0)
grey=(125, 125, 125)

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


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
    path_to_file = '/home/vovko/PycharmProjects/KeyboardWarrior/keylogger/log/keys.log'
    timestamp = os.stat(path_to_file).st_mtime
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render(str(int(timestamp)), 1, (255,255,255))
    screen.blit(label, (100, 100))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    clock.tick()
    screen.fill(black)

    show_frame_rate(clock.get_fps())

    last_change = read_changes_from_log()

    print(last_change)

    pygame.display.update()