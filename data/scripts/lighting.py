import pygame
from data.scripts.image_functions import import_image, scale_image

class Lighting():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.img = import_image('circle.png').convert_alpha()
        self.size = size
        if size != [0, 0]:
            self.img = scale_image(self.img, self.size)
        else:
            pass
    def effect(self, display, scroll, color):
        filter = pygame.surface.Surface(display.get_size()) # create surface same size as window
        filter.fill(pygame.color.Color(color)) # Black will give dark unlit areas, Grey will give you a fog
        filter.blit(self.img, (self.x - scroll[0], self.y - scroll[1])) # blit light to the filter surface -400 is to center effect
        display.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)