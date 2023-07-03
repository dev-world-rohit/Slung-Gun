# Importing Stuff------------------------------------------------------#
import pygame
import time
import random
import math
import pygame.mixer
from pygame.locals import *

from data.scripts.extra_functions import import_file
from data.scripts.image_functions import *
from data.scripts.text import font
from data.scripts.character import Character

from data.scripts.collision_detection import collision_check
from data.scripts.tileset_loader import load_tileset
from data.scripts.map_loader import load_map
from data.scripts.environment import crating_grass_data, Grass, Shooting_Star
from data.scripts.weapons import Gun, Bullet, initiate_level_tiles
from data.scripts.aircraft import Aircraft
from data.scripts.particles import *
from data.scripts.lighting import Lighting

# Setting Up the Window-------------------------------------#
pygame.init()

screen_size = (16 * 35 * 2, 16 * 22 * 2)
screen = pygame.display.set_mode(screen_size, 0, 32)

pygame.display.set_caption('Slung Gun')

display_ratio = 1.7
display_size = (screen_size[0] // display_ratio,
                screen_size[1] // display_ratio)
display = pygame.Surface(display_size)


# Images------------------------------------------------------#

player_img = import_image("player.png", (0, 0, 0))

enemy_bullet = import_image('weapons/bullet_enemy.png', (0, 0, 0))
player_bullet = import_image('weapons/bullet_player.png', (0, 0, 0))

ship = import_image('space_ship_final.png', (255, 255, 255))
ship = pygame.transform.flip(ship, False, False)

stars = import_image('background/stars.png')
moon_front = import_image('background/moon_front.png', (0, 0, 0))
moon_middle = import_image('background/moon_middle.png', (0, 0, 0), 120)
moon_back = import_image('background/moon_back.png', (0, 0, 0), 50)
dark = import_image('background/dark.png', (255, 255, 255), 100)
dark = pygame.transform.scale(dark, screen_size)

cursor = import_image('cursor.png', (0, 0, 0))

parachute = import_image('parachute.png', (0, 0, 0))

button_back_1 = import_image("button_back.png", (0, 0, 0))

# Clouds---------------------------#
cloud_0 = import_image('clouds/cloud_0.png', (255, 255, 255))
cloud_3 = import_image('clouds/cloud_1.png', (255, 255, 255))
cloud_2 = import_image('clouds/cloud_2.png', (255, 255, 255))
cloud_1 = import_image('clouds/cloud_3.png', (255, 255, 255))

clouds = [cloud_0, cloud_1, cloud_2, cloud_3]

clouds_pos = []
cloud_count = 15

for cloud in range(0, cloud_count):
    cloud = random.choice(clouds)
    clouds_pos.append([cloud, [random.randint(-100, 800),
                      random.randint(-50, 100)], clouds.index(cloud) + 2])

# Tilesets-------------------------#
tileset_data = {}

tileset_data['grass_1'] = load_tileset(
    'tilesets/grass_1.png', [16, 16], 1, (0, 0, 0), 255, 0)
tileset_data['grass_2'] = load_tileset(
    'tilesets/grass_2.png', [16, 16], 1, (0, 0, 0), 255, 0)
tileset_data['water'] = load_tileset(
    'tilesets/water.png', [16, 20], 1, (0, 0, 0), 150, 0)
tileset_data['grass_3'] = load_tileset(
    'tilesets/grass_3.png', [16, 20], 1, (0, 0, 0), 255, 0)
tileset_data['drop_point'] = load_tileset(
    'tilesets/drop_point.png', [16, 16], 1, (0, 0, 0), 255, 0)

tileset_names = []

for tile in tileset_data:
    tileset_names.append(tile)
non_collision_list = ['water', 'grass_3', 'drop_point']

grass_data = {}

grass_data['grass1'] = load_tileset(
    'tilesets/grass1.png', [6, 40], 1, (0, 0, 0), 255)

# Text---------------------------------------------------------#
text_1 = font('large_font.png', (255, 255, 255), 1)
text_2 = font('small_font.png', (255, 0, 0), 2)
text_3 = font('large_font.png', (0, 0, 255), 5)
text_4 = font('large_font.png', (255, 255, 255), 5)

# Particles--------------------------------------------------------#
load_particle_images('data/images/particles/')
particles = []

# Sounds------------------------------------------------------#


def load_sound(file_name):
    return pygame.mixer.Sound("data/sounds/" + file_name)


def play_sound(sound):
    pygame.mixer.Sound.play(sound)


player_shoot = load_sound("player_shoot")
enemy_shoot = load_sound("enemy_shoot")
player_bullet_explosion = load_sound("player_bullet_explosion")
enemy_bullet_explosion = load_sound("enemy_bullet_explosion")
main_music = pygame.mixer.music.load("data/sounds/main.mp3")

pygame.mixer.music.play(-1)


# Map--------------------------------------------------------#
level = 1
level_1, collision_tiles, gates, grass_pos, enemy_drop_points = load_map(
    'data/levels/level_' + str(level) + '.json', tileset_data, non_collision_list)
initiate_level_tiles(level)

# Grass-------------------------------------------------------#
final_grass_data = crating_grass_data(grass_data, grass_pos, [2, 4])

# Scrolling the background------------------------------------------#


def scroll_back(true_scroll, obj, delta_time, x=256, y=200):
    true_scroll[0] += ((obj.x - true_scroll[0] - x) / 10) * delta_time
    true_scroll[1] += ((obj.y - true_scroll[1] - y) / 10) * delta_time
    return true_scroll


def main_game():

    pygame.mouse.set_visible(False)

    # Clock--------------------------------------------------------#
    clock = pygame.time.Clock()
    delta_time = 0
    last_time = 0
    frame_rate = 60
    counting_time = 0

    # Variable----------------------------------------------------#
    # Player---------------------#
    player = Character(80, int((display_size[1] - player_img.get_height(
    )) // 2) - 100, player_img.get_width(), player_img.get_height())
    player.animations('player')

    gun_1 = Gun(player.rect.centerx, player.rect.centery +
                30, 'weapons/gun.png')
    bullets = []

    aircraft = Aircraft(1700, -150, ship)
    aircraft.drop_points = enemy_drop_points
    game_speed = 1

    enemies = []
    enemy_positions = []
    enemy_bullets = []
    # gun_2 = Gun(0, 0, 'weapons/gun.png')

    bullet_explosion = []
    # platforms = [pygame.Rect(100, 200, 10, 300), pygame.Rect(10, 250, 200, 30)]
    a = "Hello my nsme is"
    true_scroll = [0, 0]
    scroll = [0, 0]
    moon_x, moon_y = 80, -50
    moon = Lighting(moon_x, moon_y, moon_front.get_size())

    array_for_eney_drop_pos = []
    # Main Game Loop-------------------------------------------#
    run_game = True
    while run_game:

        mouse_pos = pygame.mouse.get_pos()
        mx, my = mouse_pos[0] // display_ratio, mouse_pos[1] // display_ratio
        cursor_x, cursor_y = mx, my

        if cursor_x > player.x - scroll[0]:
            player.flip = False
        else:
            player.flip = True

        # Scroling Back-----------------------------------------------------------#
        scroll_moon_x, scroll_moon_y = moon_x - \
            scroll[0] // 20, moon_y - scroll[1] // 20

        if aircraft.arrival_scroll != True:
            true_scroll = scroll_back(true_scroll, player, delta_time)
        else:
            true_scroll = scroll_back(
                true_scroll, aircraft, delta_time, 300, 0)

        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # Delta Time-----------------------------------------------------#
        delta_time = pygame.time.get_ticks() - last_time
        last_time = pygame.time.get_ticks()
        delta_time = delta_time * frame_rate / 1000

        # Backgrounds-----------------------------------------------------#
        display.fill((0, 0, 0))
        display.blit(stars, (0, 0))
        display.blit(moon_back, (scroll_moon_x, scroll_moon_y))
        display.blit(moon_middle, (scroll_moon_x, scroll_moon_y))
        display.blit(moon_front, (scroll_moon_x, scroll_moon_y))

        # Clouds Display-----------------------------#
        for cloud in clouds_pos:
            display.blit(cloud[0], (cloud[1][0] - (scroll[0] //
                                                   cloud[2]), (cloud[1][1] - (scroll[1] // cloud[2]))))

        # Grass-------------------------------------------------------#
        for grass in final_grass_data:
            grass[0].display_img(display, scroll, player)

        # Player Stuff-----------------------------------#
        if not aircraft.arrival_scroll:
            player.set_motion(scroll, delta_time, game_speed)
            # Bullet display----------------------------#
            for bullet in bullets:
                if bullet.fire:
                    state = bullet.fire_weapon(display, scroll)

                    for e, gun in enemies:
                        if e.x < bullet.x < e.x + 25 and e.y < bullet.y < e.y + 30:
                            enemies.remove([e, gun])
                            state = False
                            bullet.explosion = True
                    if not state:
                        if bullet.explosion:
                            for d in range(0, 40):
                                particles.append(Particle([bullet.x + random.randint(-3, 3), bullet.y + random.randint(0, 3)], 'p', [
                                    random.randint(-2, 2), 5], 0.2, 0, random.choice([(255, 0, 0), (255, 255, 0)]), True))
                                particles.append(Particle([bullet.x + random.randint(-10, 6), bullet.y + random.randint(0, 20)], 'p', [
                                    random.randint(-2, 2), 0], 0.2, 0, random.choice([(255, 0, 0), (255, 255, 0)]), True))
                            bullet.explosion = False
                        bullets.remove(bullet)
                if gun_1.fire_state == False:
                    gun_1.check_fire_state(pygame.time.get_ticks())

        player.rect, collision_list = player.phy_obj.move(
            player.movement, collision_tiles, [])

        player.update_pos([0, 0])

        if collision_list['bottom']:
            player.y_momentum = 0
            player.jump_count = 2
            player.y_movement = False

        player.play_animation(display, scroll)

        if player.y >= 700:
            run_game = False

        # Weapons -------------------------------------------------#
        gun_1.display_weapons(display, [
            player.rect.center[0] - scroll[0], player.rect.center[1] - scroll[1]], [mx, my])

        # Background Tile Display----------------------------#
        for tile in level_1['background']:
            display.blit(
                tile[0], (tile[1][0] - scroll[0], tile[1][1] - scroll[1]))

        # Enemy----------------------------------------------------#
        if enemies != []:
            for enemy, gun_2 in enemies:
                if enemy.x > player.x:
                    enemy.flip = True
                else:
                    enemy.flip = False
                if not enemy.dropping:
                    enemy.gravity = 0.3
                enemy.set_motion(scroll, delta_time, game_speed)

                enemy.rect, collision_list = enemy.phy_obj.move(
                    enemy.movement, collision_tiles, [])

                enemy.update_pos([0, 0])

                if collision_list['bottom']:
                    enemy.dropping = False
                    enemy.y_momentum = 0
                    enemy.jump_count = 2
                    enemy.y_movement = False
                    enemy.animation_state = 'idle'
                    enemy_positions.append([enemy.x, enemy.y, 25, 30])

                # Bullet display----------------------------#
                for bullet in enemy_bullets:
                    if bullet.fire:
                        state = bullet.fire_weapon(display, scroll)

                        if not state:
                            if bullet.explosion:
                                for d in range(0, 40):
                                    particles.append(Particle([bullet.x + random.randint(-3, 3), bullet.y + random.randint(0, 3)], 'p', [
                                        random.randint(-2, 2), 5], 0.2, 0, random.choice([(0, 0, 255), (255, 255, 255)]), True))
                                particles.append(Particle([bullet.x + random.randint(-10, 6), bullet.y + random.randint(0, 20)], 'p', [
                                    random.randint(-2, 2), 0], 0.2, 0, random.choice([(0, 0, 255), (255, 255, 255)]), True))
                                bullet.explosion = False
                            enemy_bullets.remove(bullet)

                if enemy.animation_state == 'idle':
                    if gun_2.fire_state == False:
                        gun_2.fire_state = gun_2.check_fire_state(
                            pygame.time.get_ticks())

                    if gun_2.fire_state:
                        angle = gun_2.angle
                        enemy_bullets.append(Bullet(
                            True, enemy.rect.center[0], enemy.rect.center[1], angle, enemy_bullet, 0.9))
                        gun_2.fire_state = False
                        play_sound(enemy_shoot)

                if enemy.animation_state == 'drop':
                    if enemy.y - enemy.real_y > 60:
                        display.blit(
                            parachute, (enemy.x - scroll[0] - 25, enemy.y - scroll[1] - 75))
                enemy.play_animation(display, scroll)
                gun_2.display_weapons(display, [enemy.rect.center[0] - scroll[0], enemy.rect.center[1] - scroll[1]], [
                    player.rect.center[0] - scroll[0], player.rect.center[1] - scroll[1]])

        # Foreground Layer Display-------------------------------#
        for tile in level_1['foreground']:
            display.blit(
                tile[0], (tile[1][0] - scroll[0], tile[1][1] - scroll[1]))

        # Particles ---------------------------------------------- #
        # for a in range(1, 3):
        #         particles.append(Particle([player.x, player.y], 'p', [0.5, 0.2], 0.3, random.randint(0, 10), random.choice([(255, 0, 0), (255, 255, 0)])))

        for i, particle in sorted(enumerate(particles), reverse=True):
            alive = particle.update(1)
            if not alive:
                particles.pop(i)
            else:
                particle.draw(display, scroll)

        # Display Tile Disaply-------------------------------#
                # Display tiles contain the grass and water
        for tile in level_1['display']:
            display.blit(
                tile[0], (tile[1][0] - scroll[0], tile[1][1] - scroll[1]))

        # Key Binding----------------------------------------------#
        # Assiging the keys to the players for its proper functioning
        for event in pygame.event.get():
            if event.type == QUIT:
                run_game = False

            if event.type == KEYDOWN:
                if event.key == K_a:
                    player.x_movement = 'left'
                if event.key == K_d:
                    player.x_movement = 'right'
                if event.key == K_SPACE:
                    if player.jump_count > 0:
                        player.y_momentum = -7
                        player.jump_count -= 1
                if event.key == K_z:
                    array_for_eney_drop_pos.append([aircraft.x, aircraft.y])

            if event.type == KEYUP:
                if event.key == K_a:
                    player.animation_state = 'idle'
                    player.x_movement = False
                if event.key == K_d:
                    player.x_movement = False
                    player.animation_state = 'idle'

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gun_1.fire_state = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    x = player.rect.centerx
                    y = player.rect.centery
                    bullets.append(
                        Bullet(True, x, y, gun_1.angle, player_bullet, 5))
                    gun_1.fire_state = False
                    play_sound(player_shoot)

        # Aircraft Stuff-----------------------------------------------------------#
        # Dispay the warning for airplane coming
        # Passing of aircraft
        # Points at which it drops the enemies
        # Frequency of coming
        if aircraft.time_count < 3:
            if 0 < aircraft.time_array[aircraft.time_count] - last_time // 1000 < 5:
                text_2.display_fonts(display, "Enemies are coming!", [250, 10])
            else:
                pass
            aircraft.start_aircraft(
                display, scroll, delta_time, game_speed, last_time // 1000)
            if aircraft.arrival:
                for a in aircraft.drop_points_selected:
                    if 0 <= aircraft.x - a[0] <= 2:
                        gun_2 = Gun(0, 0, 'weapons/gun.png')
                        e = Character(aircraft.x + 30, aircraft.y + 15, 27, 31)
                        e.animations('enemy_1')
                        e.gravity = 0.04
                        e.animation_state = 'drop'
                        enemies.append([e, gun_2])
                        aircraft.drop_points_selected.remove(a)

            if aircraft.arrival:
                for a in range(1, 3):
                    particles.append(Particle([aircraft.x + 150, aircraft.y + 65], 'p', [
                        0.2, 0.1], aircraft.decay_rate, random.randint(0, 20) / 5, random.choice([(255, 0, 0), (255, 255, 0)])))
                    particles.append(Particle([aircraft.x + 150, aircraft.y + 68], 'p', [
                        0.2, 0.1], aircraft.decay_rate, random.randint(0, 20) / 5, random.choice([(255, 0, 0), (255, 255, 0)])))
                    particles.append(Particle([aircraft.x + 150, aircraft.y + 71], 'p', [
                        0.2, 0.1], aircraft.decay_rate, random.randint(0, 20) / 5, random.choice([(255, 0, 0), (255, 255, 0)])))
                    particles.append(Particle([aircraft.x + 150, aircraft.y + 74], 'p', [
                        0.2, 0.1], aircraft.decay_rate, random.randint(0, 20) / 5, random.choice([(255, 0, 0), (255, 255, 0)])))

        # moon.effect(display, scroll, 'White')
        display.blit(cursor, (cursor_x, cursor_y))
        screen.blit(pygame.transform.scale(display, screen_size), (0, 0))
        pygame.display.flip()
        clock.tick(frame_rate)
        
main_game()