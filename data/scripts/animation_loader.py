import pygame
from data.scripts.image_functions import *
from data.scripts.extra_functions import import_file

def load_animations(name):
    path = 'data/images/animations/' + name + '/' + name + '.txt' 
    data = import_file(path)
    data = data.split('\n')

    animation_data = {}

    for info in data:
        ani_name = info.split(':')[0]
        ani_data = info.split(':')[1]

        ani_path = 'animations/' + name + '/' + ani_name
        animation = []
        for num in range(0, len(ani_data)):
            frames = ani_data[num]
            img = import_image(ani_path + '/' + ani_name + '_' + str(num) + '.png', (0, 0, 0))

            for frame in range(0, int(frames)):
                animation.append(img)
        animation_data[ani_name] = animation

    return animation_data
            
