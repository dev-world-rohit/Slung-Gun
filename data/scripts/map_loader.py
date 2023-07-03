import pygame, random
from data.scripts.extra_functions import import_file
from data.scripts.image_functions import swap_color

def load_map(path, tileset_data, non_collision_list):
    random_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    data = eval(import_file(path))
    map_data = {}
    collision_platforms = []
    gates_pos = []
    grass_pos = []
    enemy_drop_points = []
    for layer in data:
        real_layer = []
        layer_data = data[layer]
        if layer != 'drop_points':
            for tile in layer_data:
                size = [tileset_data[tile[0][0]][tile[0][1]].get_width(), tileset_data[tile[0][0]][tile[0][1]].get_height()]
                if tile[0][0] != 'grass_3':
                    real_layer.append([swap_color(tileset_data[tile[0][0]][tile[0][1]], (255, 255, 255), random.choice(random_colors), (0, 0, 0)), tile[1]])
                if tile[0][0] in non_collision_list:
                    gates_pos.append([tile[1][0], tile[1][1]])
                    if tile[0][0] in 'grass_3':
                        grass_pos.append([tile[1][0], tile[1][1]])
                        continue
                else:
                    collision_platforms.append(pygame.Rect(tile[1][0], tile[1][1], size[0] - 4, size[1]))
            map_data[layer] = real_layer
        else:
            for tile in layer_data:
                enemy_drop_points.append(tile[1])
    return map_data, collision_platforms, gates_pos, grass_pos, enemy_drop_points
