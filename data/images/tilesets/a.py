import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))

clock = pygame.time.Clock()

img = pygame.image.load('water.png').convert()
img = pygame.transform.scale(img , (128, 128 * 2))
img.set_colorkey((0, 0, 0))
img.set_alpha(200)

while True:

    screen.fill((255, 0, 255))
    screen.blit(img, (100, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()
    clock.tick(30)
