import pygame, random

class Aircraft():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.real_x = x
        self.real_y = y
        self.image = image
        self.size_x = image.get_width()
        self.size_y = image.get_height()
        self.arrival = False
        self.x_speed = -2
        self.y_speed = 0
        self.arrival_scroll = False
        self.time_count = 0
        self.time_of_arrival = 100
        self.time_array = [15, 45, 80]
        self.drop_points = []
        self.drop_points_selected = []
        self.choose_drop_points = False
        self.decay_rate = 0.2
        self.enemy_drop_point = []

    def start_aircraft(self, display, scroll, delta_time, game_speed, last_time):
        if not self.arrival and self.time_count < 3:
            if self.time_array[self.time_count] == last_time:
                self.arrival = True
                self.choose_drop_points = True

        if self.arrival:
            
            if -200 < self.x < 1400:
                self.arrival_scroll = True

            if self.choose_drop_points:
                self.drop_points_selected = self.selecting_drop_points()
                self.choose_drop_points = False

            self.move_aicraft()
            if self.x <= -700:
                self.arrival = False
                self.time_count += 1
                self.x = self.real_x
                self.y = self.real_y
            if self.x < -200:
                self.arrival_scroll = False
                
            display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))
            
    def move_aicraft(self):
        self.x += self.x_speed

    def selecting_drop_points(self):
        enemy_count = (self.time_count + 1) * 2 + 5
        enemies_pos = []        
        for a in range(1, enemy_count):
            p = random.choice(self.drop_points)
            enemies_pos.append(p)
        return enemies_pos

