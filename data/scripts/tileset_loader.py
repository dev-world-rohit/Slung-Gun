import pygame
from data.scripts.clip import clip_surface
from data.scripts.image_functions import import_image

def load_tileset(path, size = [16, 16], offset = 0, colorkey = (0, 0, 0), alpha = 255, image_number = 0):
    image_data = []
    image_x = 0
    image = import_image(path, colorkey, alpha)
    if image_number == 0:
        image_number = image.get_width() // size[0]
    for img in range(0, image_number):
        image_data.append(clip_surface(image, image_x, 0, size[0], size[1], colorkey, alpha))
        image_x += size[0] + offset
    return image_data
