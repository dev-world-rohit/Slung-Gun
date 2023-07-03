import pygame
from data.scripts.collision_detection import collision_check
from data.scripts.animation_loader import load_animations


class Character(object):
    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.real_x = x
        self.real_y = y
        self.rect = pygame.Rect(self.x, self.y, self.x_size - 4, self.y_size - 2)
        self.movement = []
        self.x_movement = False
        self.y_movement = False
        self.flip = False
        self.y_momentum = 0
        self.speed = 5
        self.x_speed = 0
        self.y_speed = 0.4
        self.jump_count = 2
        self.gravity = 0.5
        self.phy_obj = collision_check(self.x, self.y, self.x_size - 5, self.y_size)
        self.animation_data = {}
        self.animation_frame = 0
        self.animation_state = 'idle'
        self.previous_animation_state = 'idle'
        self.animation = None
        self.dropping = True
        self.have_weapon = False

    # Updating the Position---------------------------------------#    
    def update_pos(self, scroll):
        self.x = self.rect.x - scroll[0]
        self.y = self.rect.y - scroll[1]

    # Loading the Animations-------------------------------------------------#
    def animations(self, path):
        self.animation_data = load_animations(path)
        self.current_animation()

    # Setting the Current Animation----------------------------------------#
    def current_animation(self):
        self.animation = self.animation_data[self.animation_state]

    def set_motion(self, scroll, delta_time, game_speed):
        self.movement = [0, 0]
        if self.x_movement:
            self.animation_state = 'run'
            if self.x_movement == 'left':
                self.movement[0] -= self.speed * delta_time * game_speed
            if self.x_movement == 'right':
                self.movement[0] += self.speed * delta_time * game_speed

        else:
            self.movement[0] = 0

        self.movement[1] += self.y_momentum
        self.y_momentum += self.gravity * delta_time * game_speed
        if self.y_momentum > 5:
            self.y_momentum = 5

    # Playing the Animation-----------------------------------------#
    def play_animation(self, display, scroll):
        if self.animation_state == self.previous_animation_state:
            if self.animation_frame == len(self.animation):
                self.animation_frame = 0
                
        else:
            self.animation_frame = 0
            self.previous_animation_state = self.animation_state
            self.current_animation()

        display.blit(pygame.transform.flip(self.animation[self.animation_frame], self.flip, False), (self.x - scroll[0], self.y - scroll[1] + 3))
        self.animation_frame += 1
        
    def display_rect(self, display, scroll):
        pygame.draw.rect(display, (255, 0, 0), (self.x - scroll[0], self.y - scroll[1], self.x_size, self.y_size))