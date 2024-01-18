import os
import sys
import pygame
from math import sqrt


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

    def update(self, an=0):
        if an == 0:
            self.cur_frame = (self.cur_frame + 1) % 4 + direction * 4
        elif an == 1:
            self.cur_frame = direction * 4
        self.image = pygame.transform.scale(self.frames[self.cur_frame], self.size)
        self.rect.x = x_m
        self.rect.y = y_m
        self.collide_walls()

    def collide_walls(self):
        global x_m, y_m
        hits = pygame.sprite.spritecollide(self, obstacle_sprites, False)
        if hits:
            if x_m - self.rect.x > 0:
                self.rect.x = hits[0].rect.left - self.rect.width
                x_m = self.rect.x
                print("left")
            elif x_m - self.rect.x < 0:
                self.rect.x = hits[0].rect.right
                x_m = self.rect.x
            if y_m - self.rect.y < 0:
                self.rect.y = hits[0].rect.top
                y_m = self.rect.y
            elif y_m - self.rect.y > 0:
                self.rect.y = hits[0].rect.bottom
                y_m = self.rect.y


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


x, y = 0, 0
x_m, y_m = 735, 475
speed = 0
direction = 0
all_sprites = pygame.sprite.Group()
menu = pygame.sprite.Group()
char = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
free = [1, 1, 1, 1]
music_on = pygame.mixer.music
menu_background = AnimatedMenu(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Menu Background.png"), 4, 2, 1200, 800)
mc = AnimatedChar(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\MC.png"), 4, 4, 128, 128)
story_btn = [pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Buttons\\story_btn{i}.png") for i in range(2)]
free_mode_btn = [pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Buttons\\free_mode_btn{i}.png") for i in range(2)]
sky = pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Game BG Sky.png")
forest = pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Game BG Forest.png")
glitch = pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Game BG SkyGlitch.png")
camera = Camera()

tile_images = {
    'null': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\null.png"), (64, 64)),
    'grass': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\grass.png"), (64, 64)),
    'stone': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\stone.png"), (64, 64)),
    'wall': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\glitch_wall.png"),
                                   (64, 64)),
    'floor': pygame.transform.scale(pygame.image.load(f"{os.getcwd()}\\Data\\Sprites\\Tiles\\glitch_floor.png"),
                                    (64, 64)),
}
tile_width = tile_height = 64


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class TileObstacle(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(obstacle_sprites, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                TileObstacle('stone', x, y)
            elif level[y][x] == '@':
                Tile('grass', x, y)
                new_player = mc
            elif level[y][x] == '!':
                Tile('grass', x, y)
            elif level[y][x] == '?':
                TileObstacle('wall', x, y)
            elif level[y][x] == '%':
                Tile('floor', x, y)
            elif level[y][x] == '-':
                Tile('null', x, y)
            elif level[y][x] == ',':
                Tile('null', x, y)
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
    pygame.display.flip()
    clock.tick(120)


if __name__ == '__main__':
    pygame.init()
    i = 0
    music_on.load(f"{os.getcwd()}\\Data\\Music\\fading_hope.ogg")
    # MUS!!! music_on.play(-1)
    clock = pygame.time.Clock()
    size = width, height = 1200, 800
    display = pygame.display.set_mode([width, height])
    direction = 0
    room_id = 0
    screen = pygame.display.set_mode(size)
    start_lvl = load_level(f"{os.getcwd()}\\Data\\Maps\\0.txt")
    second_lvl = load_level(f"{os.getcwd()}\\Data\\Maps\\1.txt")
    start = True

    while start:
        start_screen()
    music_on.load(f"{os.getcwd()}\\Data\\Music\\ambivalence.ogg")
    # MUS!!! music_on.play(-1)
    game = True
    char.update(1)
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
                speed *= sqrt(2) / 2
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]:
                speed *= sqrt(2) / 2
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = 3
            x_m -= speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = 2
            y_m -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = 0
            y_m += speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = 1
            x_m += speed
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]) or (
                keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
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
        for sprite in char:
            camera.apply(sprite)
        i += 1
        tiles_group.draw(screen)
        obstacle_sprites.draw(screen)
        char.draw(screen)
        pygame.display.flip()
        clock.tick(30)
pygame.quit()
