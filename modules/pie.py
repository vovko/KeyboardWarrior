import pdb
import pygame
import math

from modules.common_constants import *

class Pie:
    MAX_VALUE = 100

    START_ANGLE = 90
    MAX_ANGLE = 360

    radius = None
    value = None
    color = None
    key_color = None

    surface = None

    def __init__(self, radius, value, color, key_color):
        self.radius = radius
        self.value = value
        self.color = color
        self.key_color = key_color

        self.__width = self.radius * 2
        self.__height = self.radius * 2

        self.surface = self.create_surface()

    def create_surface(self):
        surface = pygame.Surface((self.__width, self.__height)).convert()
        surface.fill(self.key_color)

        return surface

    def __centre_pos(self):
        return (self.__width/2, self.__height/2)

    def to_surface(self):
        self.draw_pie()
        return self.surface

    def draw_pie(self):
        value_angle = self.START_ANGLE + (self.value * self.MAX_ANGLE / self.MAX_VALUE)
        segments = int(self.value) * 5

        # CREATE A FILLED ARC
        self.fill_arc(self.surface, self.__centre_pos(), self.radius, self.START_ANGLE, value_angle, self.color, segments)

        # CREATE OUTTER HOLE
        # out of Surface filled with self.key_color
        # filled circle with RED color, clipped off out_hole as colorkey to make a hole inside of surface
        out_hole = pygame.Surface((self.__width, self.__height)).convert()
        out_hole.fill(self.key_color)

        pygame.gfxdraw.filled_circle(out_hole, int(self.__centre_pos()[0]), int(self.__centre_pos()[1]), int(self.radius-2), RED)
        # pygame.gfxdraw.aacircle(out_hole, radius, radius, 90, WHITE)
        out_hole.set_colorkey(RED)

        self.surface.blit(out_hole, (0, 0))

        # Fill inside of a pie with self.key_color circle
        pygame.gfxdraw.filled_circle(self.surface, self.radius, self.radius, 80, self.key_color)

        return self.surface

    # Potentially refactor into custom Pygame.gfx.filled_arc
    def fill_arc(self, surface, centre, radius, theta0, theta1, color, ndiv=5):

        if ndiv < 1:
            return False

        x0, y0 = centre

        dtheta = (theta1 - theta0) / ndiv
        # print(dtheta)
        angles = [theta0 - i * dtheta for i in range(ndiv + 1)]

        points = [(x0 + radius * math.cos(math.radians(theta)), y0 - radius * math.sin(math.radians(theta))) for theta
                  in angles]
        for pair in points:
            pygame.draw.line(surface, color, (x0, y0), (int(pair[0]), int(pair[1])), 3)
