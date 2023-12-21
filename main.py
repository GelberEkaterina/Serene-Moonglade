import os
import sys
import pygame
from math import sqrt

if __name__ == '__main__':
    pygame.init()
    i = 0
    pygame.mixer.music.load(f"{os.getcwd()}\\Music\\fading_hope.ogg")
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    size = width, height = 1200, 800
    # Я писала следующую часть кода до изучения спрайтов
    display = pygame.display.set_mode([width, height])
    sprite = pygame.sprite.Sprite()
    mc = [pygame.image.load(f"{os.getcwd()}\\Sprites\\MC\\{j}{i}.png") for j in ['l', 'r', 'u', 'd'] for i in range(4)]
    menu_bg = [pygame.image.load(f"{os.getcwd()}\\Images\\Menu\\menu_bg{i}.png") for i in range(8)]
    story_btn = [pygame.image.load(f"{os.getcwd()}\\Images\\Menu\\story_btn{i}.png") for i in range(3)]
    x, y = 0, 0
    speed = 1
    direction = 3
    screen = pygame.display.set_mode(size)
    game = True
    gamemode = 1
    while game:
        if gamemode == -1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            display.blit(pygame.transform.scale(menu_bg[i // 30], (1200, 800)), (0, 0))
            display.blit(pygame.transform.scale(story_btn[0], (400, 200)), (150, 300))
            i += 1
            if i == 240:
                i = 0
            pygame.display.flip()
            clock.tick(60)
        if gamemode == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            speed = 0.75
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    speed *= sqrt(2) / 2
                else:
                    speed *= 1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    speed *= sqrt(2) / 2
                else:
                    speed *= 1
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                direction = 0
                x = x - speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                direction = 2
                y = y - speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                direction = 3
                y = y + speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                direction = 1
                x = x + speed
            if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                i = 0
            display.fill([125, 0, 255])
            display.blit(pygame.transform.scale(mc[direction * 4 + i // 15], (128, 128)), (x, y))
            i += 1
            if i == 60:
                i = 0
            pygame.display.flip()
            clock.tick(120)
pygame.quit()
