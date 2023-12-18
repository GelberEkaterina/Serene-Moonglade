import os
import sys
import pygame

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 800
    mc = [pygame.image.load(f"{os.getcwd()}\\Sprites\\MC\\{j}{i}.png") for j in ['l', 'r', 'u', 'd'] for i in range(4)]
    x, y = 0, 0
    speed = 1
    direction = 3
    screen = pygame.display.set_mode(size)
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
