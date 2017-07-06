from modules.common_constants import *
import time
import random
import pygame

class Boom:
    last_time = 0
    position = None
    # self.radius = 10
    frames = 0
    running = True

    max_radius = 0

    color = RED

    def __init__(self, screen, position):
        self.screen = screen
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
        pygame.gfxdraw.aacircle(self.screen, self.position[0], self.position[1], self.radius, self.color)
        pygame.gfxdraw.filled_circle(self.screen, self.position[0], self.position[1], self.radius, self.color)


    def current_time(self):
        return round(time.time() * 1000)

    def next_frame(self):
        if(self.radius > self.max_radius-20):
            self.color = (255,255,255)

        if(self.radius > self.max_radius):
            self.running = False

        self.radius += 5
