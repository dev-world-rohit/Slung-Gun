from operator import length_hint
import pygame, random

#from data.scripts.image_functions import blit_centre

# Grass---------------------------------------------------------------------------#
def crating_grass_data(grass_data, grass_pos, density_of_grass = [6, 10]):
    final_grass_data = []
    for pos in grass_pos:
        grass_number = random.randint(density_of_grass[0], density_of_grass[1])
        grass_img_group = 'grass1' #random.choice(('grass1'))
        grass_images = grass_data[grass_img_group]
        for grass in range(0, grass_number):
            if grass_img_group != 'grass3':
                grass_img = random.choice(grass_images)
            else:
                grass_img = grass_images
            pos_x, pos_y = random.randint(pos[0], pos[0] + 13), pos[1]
            final_grass_data.append([Grass(pos_x, pos_y, grass_img)])
            
    return final_grass_data

def normalize(angle, max_angle):
    change_angle = False
    if angle > max_angle:
        angle -=  0.5
    if angle < max_angle:
        angle += 0.5
    if angle == max_angle:
        change_angle = True

    return angle, change_angle

class Grass():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.rotate_side = random.choice(('left', 'right'))
        self.max_angle = random.randint(-50, 50)
        self.max_reach = False
        self.angle = 0

    def display_img(self, display, scroll, player):       
        pos_x, pos_y = self.x - scroll[0] + 5, self.y - scroll[1] + 20

        if -800 < pos_x - player.x - scroll[0] < 800 or -400 < pos_y - player.y - scroll[1] < 400:
            self.angle, self.max_reach = normalize(self.angle, self.max_angle)
            if self.max_reach:
                if self.max_angle < 0:
                    self.max_angle = random.randint(0, 50)
                if self.max_angle > 0:
                    self.max_angle = random.randint(-50, 0)
                if self.max_angle == 0:
                    self.max_angle = random.randint(-50, 50)

            #self.angle = 150
            img = pygame.transform.rotate(self.img, self.angle)
            
            img_x = int(img.get_width() / 2)
            img_y = int(img.get_height() /2)

            display.blit(img, (pos_x - img_x, pos_y - img_y))
        else:
            pass

class Shooting_Star():
    def __inti__(self, x, y):
        self.x = x
        self.y = y
        self.lenght = random.randint(100, 300)
        
    def display_star(self, display, scroll):
        pass
