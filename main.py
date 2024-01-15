import os
import sys
import pygame
from math import sqrt


class AnimatedMenu(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, a, b):
        super().__init__(menu)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.size = (a, b)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.scale(self.frames[self.cur_frame], self.size)


class AnimatedChar(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, a, b):
        super().__init__(char)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.size = (a, b)
        self.direction = direction

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, x_m, y_m, an=0):
        if an == 0:
            self.cur_frame = (self.cur_frame + 1) % 4 + direction * 4
        elif an == 1:
            self.cur_frame = direction * 4
        self.image = pygame.transform.scale(self.frames[self.cur_frame], self.size)
        self.rect.x = x_m
        self.rect.y = y_m


speed = 0
direction = 0
menu = pygame.sprite.Group()
char = pygame.sprite.Group()
music_on = pygame.mixer.music
menu_background = AnimatedMenu(pygame.image.load(f"{os.getcwd()}\\Sprites\\Menu Background.png"), 4, 2, 0, 0, 1200,
                               800)
mc = AnimatedChar(pygame.image.load(f"{os.getcwd()}\\Sprites\\MC.png"), 4, 4, 0, 0, 128, 128)


def start_screen():
    global i
    global start
    global gamemode
    i += 1
    if i == 15:
        menu_background.update()
        i = 0
    menu.draw(screen)
    if 150 < pygame.mouse.get_pos()[0] < 550 and 300 < pygame.mouse.get_pos()[1] < 500:
        display.blit(pygame.transform.scale(story_btn[1], (400, 200)), (150, 300))
    else:
        display.blit(pygame.transform.scale(story_btn[0], (400, 200)), (150, 300))
    if 650 < pygame.mouse.get_pos()[0] < 1050 and 300 < pygame.mouse.get_pos()[1] < 500:
        display.blit(pygame.transform.scale(free_mode_btn[1], (400, 200)), (650, 300))
    else:
        display.blit(pygame.transform.scale(free_mode_btn[0], (400, 200)), (650, 300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            if 150 < pygame.mouse.get_pos()[0] < 550 and 300 < pygame.mouse.get_pos()[1] < 500:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start = False
                    gamemode = 0
                    return
    pygame.display.flip()
    clock.tick(120)


if __name__ == '__main__':
    pygame.init()
    i = 0
    music_on.load(f"{os.getcwd()}\\Music\\fading_hope.ogg")
    # MUS!!! music_on.play(-1)
    clock = pygame.time.Clock()
    size = width, height = 1200, 800
    display = pygame.display.set_mode([width, height])
    story_btn = [pygame.image.load(f"{os.getcwd()}\\Sprites\\Buttons\\story_btn{i}.png") for i in range(2)]
    free_mode_btn = [pygame.image.load(f"{os.getcwd()}\\Sprites\\Buttons\\free_mode_btn{i}.png") for i in range(2)]
    x, y = 0, 0
    direction = 0
    screen = pygame.display.set_mode(size)
    start = True

    while start:
        start_screen()
    music_on.load(f"{os.getcwd()}\\Music\\ambivalence.ogg")
    # MUS!!! music_on.play(-1)
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        speed = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
                speed *= sqrt(2) / 2
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
                speed *= sqrt(2) / 2
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = 3
            x -= speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = 2
            y -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = 0
            y += speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = 1
            x += speed
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]) or (
                keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
            char.update(x, y, 1)
            i = 0
        else:
            if i % 15 == 0:
                char.update(x, y)
            else:
                char.update(x, y, 2)
        if i == 30:
            i = 0
        display.fill([125, 0, 255])
        char.draw(screen)
        i += 1
        pygame.display.flip()
        clock.tick(120)
pygame.quit()
