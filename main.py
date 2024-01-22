import os
import sys
import pygame
from math import sqrt
import pygame.mixer
import pygame.freetype
import random


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class AnimatedMenu(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, a, b):
        global x, y
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
    def __init__(self, sheet, columns, rows, a, b):
        super().__init__(char)
        global x_m, y_m
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.x, self.rect.y = 600 - a // 2, 400 - b // 2
        self.size = (a, b)
        self.direction = direction
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, an=0):
        if an == 0:
            self.cur_frame = (self.cur_frame + 1) % 4 + direction * 4
        elif an == 1:
            self.cur_frame = direction * 4
        self.image = pygame.transform.scale(self.frames[self.cur_frame], self.size)
        self.collide_walls()

    def collide_walls(self):
        global x_m, y_m
        global move, speed, room_id, music_on, game
        for spr in obstacle_sprites:
            hits = pygame.sprite.collide_mask(self, spr)
            if hits:
                if move[0] == 1:
                    self.rect.x += speed
                if move[3] == 1:
                    self.rect.x -= speed
                if move[1] == 1:
                    self.rect.y += speed
                if move[2] == 1:
                    self.rect.y -= speed
        for spr in event_sprites:
            ev = pygame.sprite.collide_mask(self, spr)
            if ev:
                if spr.event == 'room_1':
                    timestamp = music_on.get_pos() / 1000
                    music_on.load(f"{os.getcwd()}\\Data\\Music\\ambivalence_glitch.ogg")
                    music_on.play(-1)
                    music_on.set_pos(timestamp)
                    room_id = 1
                    self.rect.x, self.rect.y = 600 - self.rect.width // 2, 400 - self.rect.height // 2
                if spr.event == 'battle':
                    game = False
                    battle_mode('battle')


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, a, b):
        super().__init__(all_sprites, battle)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(450, 32)
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
        i = random.randint(1, 30)
        if i % 10 == 0:
            self.cur_frame = i // 10
        else:
            self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], self.size)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - x_m, tile_height * pos_y - y_m)


class TileObstacle(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(obstacle_sprites, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - x_m, tile_height * pos_y - y_m)
        self.mask = pygame.mask.from_surface(self.image)


class TileEvent(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, event_type):
        super().__init__(event_sprites, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - x_m, tile_height * pos_y - y_m)
        self.mask = pygame.mask.from_surface(self.image)
        self.event = event_type


class Battle_UI(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, thing):
        super().__init__(battle_UI, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(0, 0)
        self.size = (1200, 800)
        self.thing = thing

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.thing == 'layout':
            if 16 < pygame.mouse.get_pos()[0] < 576 and 448 < pygame.mouse.get_pos()[1] < 592:
                self.cur_frame = 1
            elif 608 < pygame.mouse.get_pos()[0] < 1168 and 448 < pygame.mouse.get_pos()[1] < 592:
                self.cur_frame = 2
            elif 16 < pygame.mouse.get_pos()[0] < 576 and 624 < pygame.mouse.get_pos()[1] < 768:
                self.cur_frame = 3
            elif 608 < pygame.mouse.get_pos()[0] < 1168 and 624 < pygame.mouse.get_pos()[1] < 768:
                self.cur_frame = 4
            else:
                self.cur_frame = 0
        if self.thing == 'live':
            self.cur_frame = 3 - current_lifes
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (1200, 800))
        if self.thing == 'counter':
            self.cur_frame = counter_q
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (1200, 800))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '|':
                TileObstacle('stone_right', x, y)
            elif level[y][x] == '_':
                TileObstacle('stone_down', x, y)
            elif level[y][x] == '+':
                TileObstacle('big_corner', x, y)
            elif level[y][x] == '-':
                TileObstacle('small_corner', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                new_player = mc
            elif level[y][x] == '!':
                TileEvent('grass', x, y, 'room_1')
            elif level[y][x] == '?':
                TileObstacle('wall', x, y)
            elif level[y][x] == '%':
                Tile('floor', x, y)
            elif level[y][x] == '=':
                Tile('null', x, y)
            elif level[y][x] == ',':
                TileEvent('null', x, y, 'battle')
    return new_player, x, y


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
            elif 650 < pygame.mouse.get_pos()[0] < 1050 and 300 < pygame.mouse.get_pos()[1] < 500:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start = False
                    gamemode = 1
                    return
    pygame.display.flip()
    clock.tick(120)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


n = 64
x, y = 0, 0
x_m, y_m = n * 3.875, n * 3
gamemode = 0
speed = 0
direction = 0
pygame.mixer.init()
all_sprites = pygame.sprite.Group()
menu = pygame.sprite.Group()
char = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
event_sprites = pygame.sprite.Group()
battle = pygame.sprite.Group()
battle_UI = pygame.sprite.Group()
music_on = pygame.mixer.music
menu_background = AnimatedMenu(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Menu Background.png"), 4, 2, 1200, 800)
mc = AnimatedChar(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\MC.png"), 4, 4, 36, 84)
enemy = Enemy(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Exam\\Enemy.png"), 4, 1, 185, 368)
story_btn = [pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Buttons\\story_btn{i}.png") for i in range(2)]
free_mode_btn = [pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Buttons\\free_mode_btn{i}.png") for i in range(2)]
sky = pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Game BG Sky.png")
forest = pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Game BG Forest.png")
glitch = pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Game BG SkyGlitch.png")
camera = Camera()
tile_images = {
    'null': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\null.png"), (n, n)),
    'grass': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\grass.png"), (n, n)),
    'stone_right': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\stone_right.png"),
                                          (n, n)),
    'stone_down': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\stone_down.png"),
                                         (n, n)),
    'big_corner': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\corner_big.png"),
                                         (n, n)),
    'small_corner': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\corner_small.png"),
                                           (n, n)),
    'wall': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\glitch_wall.png"),
                                   (n, n)),
    'floor': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\glitch_floor.png"),
                                    (n, n)),
}
tile_width = tile_height = n
move = [0, 0, 0, 0]
i = 0
clock = pygame.time.Clock()
size = width, height = 1200, 800
display = pygame.display.set_mode([width, height])
room_id = 0
screen = pygame.display.set_mode(size)
start_lvl = load_level(f"{os.getcwd()}\\Data\\Maps\\0.txt")
second_lvl = load_level(f"{os.getcwd()}\\Data\\Maps\\1.txt")
layout = Battle_UI(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Exam\\Quiz_Layout.png"), 5, 1, 'layout')
life = Battle_UI(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Exam\\Lifes.png"), 3, 1, 'live')
counter = Battle_UI(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Exam\\Q_Counter.png"), 5, 2, 'counter')
current_lifes = 3
counter_q = 0


def battle_mode(quiz_type):
    global current_lifes, mouse
    current_lifes = 3
    if quiz_type == 'test':
        music_on.load(f"{os.getcwd()}\\Data\\Music\\test_of_wits.ogg")
        music_on.play(-1)
        game = True
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            mouse = pygame.mouse.get_pos()
            layout.update()
            life.update()
            counter.update()
            display.blit(pygame.transform.scale(sky, (1200, 800)), (0, 0))
            battle_UI.draw(screen)
            pygame.display.flip()
            clock.tick(30)
    if quiz_type == 'battle':
        music_on.load(f"{os.getcwd()}\\Data\\Music\\error_file_corrupted.ogg")
        music_on.play(-1)
        game = True
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            mouse = pygame.mouse.get_pos()
            layout.update()
            life.update()
            counter.update()
            enemy.update()
            display.blit(pygame.transform.scale(glitch, (1200, 800)), (0, 0))
            battle_UI.draw(screen)
            battle.draw(screen)
            pygame.display.flip()
            clock.tick(30)


def exam():
    game = True
    while game:
        battle_mode('test')


def story_mode():
    global direction, i, speed, move, mc, game
    music_on.load(f"{os.getcwd()}\\Data\\Music\\ambivalence.ogg")
    music_on.play(-1, 0)
    game = True
    char.update(1)
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        speed = 2.5
        if keys[pygame.K_LEFT]:
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                speed *= sqrt(2) / 2
        elif keys[pygame.K_RIGHT]:
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                speed *= sqrt(2) / 2
        move = [0, 0, 0, 0]
        if keys[pygame.K_LEFT]:
            direction = 3
            mc.rect.x -= speed
            move[0] = 1
        if keys[pygame.K_UP]:
            direction = 2
            mc.rect.y -= speed
            move[1] = 1
        if keys[pygame.K_DOWN]:
            direction = 0
            mc.rect.y += speed
            move[2] = 1
        if keys[pygame.K_RIGHT]:
            direction = 1
            mc.rect.x += speed
            move[3] = 1
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            char.update(1)
            i = 0
        else:
            if i % 3 == 1:
                char.update()
            else:
                char.update(2)
        if i == 15:
            i = 0
        for sprite in tiles_group:
            sprite.kill()
        for sprite in obstacle_sprites:
            sprite.kill()
        for sprite in event_sprites:
            sprite.kill()
        if room_id == 0:
            display.blit(pygame.transform.scale(sky, (1200, 800)), (0, 0))
            mc, level_x, level_y = generate_level(start_lvl)
        elif room_id == 2:
            display.blit(pygame.transform.scale(forest, (1200, 800)), (0, 0))
        elif room_id == 1:
            display.blit(pygame.transform.scale(glitch, (1200, 800)), (0, 0))
            mc, level_x, level_y = generate_level(second_lvl)
        camera.update(mc)
        for sprite in tiles_group:
            camera.apply(sprite)
        for sprite in obstacle_sprites:
            camera.apply(sprite)
        for sprite in event_sprites:
            camera.apply(sprite)
        i += 1
        tiles_group.draw(screen)
        obstacle_sprites.draw(screen)
        event_sprites.draw(screen)
        char.draw(screen)
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    music_on.load(f"{os.getcwd()}\\Data\\Music\\fading_hope.ogg")
    music_on.play(-1)
    start = True
    while start:
        start_screen()
    while gamemode == 0:
        story_mode()
    while gamemode == 1:
        exam()

pygame.quit()
