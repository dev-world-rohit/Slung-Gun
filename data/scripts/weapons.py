from webbrowser import get
import pygame, math

from data.scripts.image_functions import *
from data.scripts.extra_functions import get_angle, get_distance, import_file

def initiate_level_tiles(level):
    global level_1_collision_tiles
    level_1_collision_tiles = eval(import_file('data/levels/level_' + str(level) + '.txt'))
    back = level_1_collision_tiles['foreground']
    dis = level_1_collision_tiles['display']
    fore = level_1_collision_tiles['background']
    level_1_collision_tiles = back + dis + fore

class Gun():
    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.img = import_image(img_path)
        self.fire_state = True
        self.angle = 40
        self.reload_time = 0
        self.last_time = pygame.time.get_ticks()
        # self.flip_x = False
        # self.flip_y = False

    def display_weapons(self, surface, pos, mouse_pos):
        self.x = pos[0]
        self.y = pos[1]
        self.angle = -math.degrees(math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x))
        img = pygame.transform.rotate(self.img, self.angle)
        surface.blit(img, (self.x - int(img.get_width() / 2), self.y - int(img.get_height() / 2)))

        
    def check_fire_state(self, new_time):
        if (new_time - self.last_time) // 1000 > self.reload_time:
            self.last_time = pygame.time.get_ticks()
            return True
        else:
            return False


class Bullet():
    def __init__(self, fire, x, y, angle, bullet_img, speed_ratio):
        self.x = x
        self.y = y
        self.time = pygame.time.get_ticks()
        self.original_angle = angle
        self.angle = -angle * math.pi / 180
        self.speed_ratio = speed_ratio
        self.x_speed = math.cos(self.angle) * self.speed_ratio       #math.pow(math.pow(math.cos(self.angle), 2), 0.5)
        self.y_speed = math.sin(self.angle) * self.speed_ratio        #math.pow(math.pow(math.sin(self.angle), 2), 0.5)
        self.real_x_speed = self.x_speed
        self.real_y_speed = self.y_speed
        self.original_x = x
        self.original_y = y
        self.img = bullet_img
        self.fire = fire  
        self.explosion = False

    def fire_weapon(self, display, scroll):

        self.x += self.real_x_speed
        self.y += self.real_y_speed

        if [(self.x // 16) * 16, (self.y // 16) * 16] in level_1_collision_tiles:
            self.explosion = True
            return False
        display.blit(rotate_image(self.img, self.original_angle), (self.x - scroll[0], self.y - scroll[1]))

        if pygame.time.get_ticks() - self.time  > 3000:
            return False
        else:
            return True