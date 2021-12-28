import os
import random

import pygame
import ctypes

user32 = ctypes.windll.user32
pygame.init()
size = w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
walls_list = []
v = 150
fps = 60
selected_room = None
rooms = [[]]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('Images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite):
    player_image = load_image('player_1.png')

    def __init__(self):
        global v, fps
        super().__init__(player_sprite)
        self.add(all_sprites)
        self.image = pygame.transform.scale(Player.player_image, (130, 161))
        self.rect = self.image.get_rect()
        self.rect.x = w // 2
        self.rect.y = h // 2
        self.index = 0
        self.count1 = 0
        self.count2 = 0
        self.mb_x = w // 2
        self.mb_y = h // 2
        self.orientation = 1
        self.health = 5
        self.shield = 5
        self.players = ['player_1.png', 'player_2.png', 'player_3.png', 'player_4.png', 'player_5.png', 'player_6.png',
                        'player_7.png', 'player_8.png']

    def life(self):
        if self.count1 == 8:
            self.index = (self.index + 1) % 8
            if self.orientation == 1:
                self.image = pygame.transform.scale(load_image(self.players[self.index]), (130, 161))
            else:
                self.image = self.image = pygame.transform.flip(
                    pygame.transform.scale(load_image(self.players[self.index]), (130, 161)), True, False)
            self.count1 = 0
        self.count1 += 1
        if self.count2 == fps * 2:
            self.shield += 1
            if self.shield > 5:
                self.shield = 5
            self.count2 = 0
        self.count2 += 1

    def update(self, event):
        global selected_room
        if event[pygame.K_w]:
            self.mb_y -= v / fps
            self.rect.y = self.mb_y
            if pygame.sprite.spritecollideany(self, walls):
                self.mb_y += v / fps
                self.rect.y = self.mb_y
        if event[pygame.K_d]:
            self.mb_x += v / fps
            self.rect.x = self.mb_x
            if self.orientation == 0:
                self.orientation = 1
                self.image = pygame.transform.flip(self.image, True, False)
            if pygame.sprite.spritecollideany(self, walls):
                self.mb_x -= v / fps
                self.rect.x = self.mb_x
        if event[pygame.K_s]:
            self.mb_y += v / fps
            self.rect.y = self.mb_y
            if pygame.sprite.spritecollideany(self, walls):
                self.mb_y -= v / fps
                self.rect.y = self.mb_y
        if event[pygame.K_a]:
            self.mb_x -= v / fps
            self.rect.x = self.mb_x
            if self.orientation == 1:
                self.orientation = 0
                self.image = pygame.transform.flip(self.image, True, False)
            if pygame.sprite.spritecollideany(self, walls):
                self.mb_x += v / fps
                self.rect.x = self.mb_x
        if self.rect.x < -self.rect.width:
            try:
                assert selected_room.j != 0
                select_room(rooms[selected_room.i][selected_room.j - 1])
                self.mb_x += w + self.rect.width
                self.rect.x = self.mb_x
            except Exception:
                self.mb_x += v / fps
                self.rect.x = self.mb_x
        if self.rect.x > w:
            try:
                select_room(rooms[selected_room.i][selected_room.j + 1])
                self.mb_x -= w + self.rect.width
                self.rect.x = self.mb_x
            except Exception:
                self.mb_x -= v / fps
                self.rect.x = self.mb_x
        if self.rect.y < -self.rect.height:
            try:
                assert selected_room.i != 0
                select_room(rooms[selected_room.i - 1][selected_room.j])
                self.mb_y += h + self.rect.height
                self.rect.y = self.mb_y
            except Exception:
                self.mb_y += v / fps
                self.rect.y = self.mb_y
        if self.rect.y > h:
            try:
                select_room(rooms[selected_room.i + 1][selected_room.j])
                self.mb_y -= h + self.rect.height
                self.rect.y = self.mb_y
            except Exception:
                self.mb_y -= v / fps
                self.rect.y = self.mb_y
        if self.rect.x <= 0:
            try:
                assert selected_room.j != 0
                a = rooms[selected_room.i][selected_room.j - 1]
                if a is None:
                    self.mb_x += v / fps
                    self.rect.x = self.mb_x
            except:
                self.mb_x += v / fps
                self.rect.x = self.mb_x
        if self.rect.x >= w - self.rect.width:
            try:
                a = rooms[selected_room.i][selected_room.j + 1]
                if a is None:
                    self.mb_x -= v / fps
                    self.rect.x = self.mb_x
            except:
                self.mb_x -= v / fps
                self.rect.x = self.mb_x
        if self.rect.y <= 0:
            try:
                assert selected_room.i != 0
                a = rooms[selected_room.i - 1][selected_room.j]
                if a is None:
                    self.mb_y += v / fps
                    self.rect.y = self.mb_y
            except:
                self.mb_y += v / fps
                self.rect.y = self.mb_y
        if self.rect.y >= h - self.rect.height:
            try:
                a = rooms[selected_room.i + 1][selected_room.j]
                if a is None:
                    self.mb_y -= v / fps
                    self.rect.y = self.mb_y
            except:
                self.mb_y -= v / fps
                self.rect.y = self.mb_y


class Room(pygame.sprite.Sprite):
    def __init__(self, type, player, i=0, j=0):
        super().__init__(rooms_sprite)
        self.add(all_sprites)
        self.i = i
        self.j = j
        if type == 'g':
            image = load_image('green_floor.png')
        elif type == 'l':
            pass
        elif type == 'i':
            image = load_image('ice_floor.png')
        try:
            rooms[i][j] = self
        except Exception:
            if i >= len(rooms):
                for _ in range(i - len(rooms) + 1):
                    rooms.append([None * len(rooms[0])])
            if j >= len(rooms[0]):
                for elem in rooms:
                    for _ in range(j - len(rooms[0]) + 1):
                        elem.append(None)
            rooms[i][j] = self
        self.image = pygame.transform.scale(image, (1960, 1080))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.player = player


class Monster(pygame.sprite.Sprite):
    def __init__(self, player, image):
        super().__init__(mobs_sprite)
        self.health = 3
        self.player = player
        self.v = 100
        self.image = pygame.transform.scale(load_image(image), (60, 80))
        self.rect = self.image.get_rect()
        self.tick = fps - 1
        while True:
            self.rect.x = random.randrange(w - self.rect.width)
            self.rect.y = random.randrange(h - self.rect.height)
            print(pygame.sprite.spritecollideany(self, walls))
            print(pygame.sprite.spritecollideany(self, player_sprite))
            print(pygame.sprite.spritecollide(self, mobs_sprite, False))
            if pygame.sprite.spritecollideany(self, walls) is None and pygame.sprite.spritecollideany(self,
                                                                                                      player_sprite) is None and len(
                pygame.sprite.spritecollide(self, mobs_sprite, False)) == 1:
                break
        self.mb_x = self.rect.x
        self.mb_y = self.rect.y

    def update(self):
        x = self.player.rect.x + self.player.rect.width // 2 - self.rect.x - self.rect.width // 2
        y = self.player.rect.y + self.player.rect.height // 2 - self.rect.y - self.rect.height // 2
        v_x = 0
        v_y = 0
        if x != 0:
            v_x = (self.v / fps) * (abs(x) / (abs(x) + abs(y)))
        if y != 0:
            v_y = (self.v / fps) * (abs(y) / (abs(x) + abs(y)))
        if x < 0:
            v_x = -v_x
        if y < 0:
            v_y = -v_y
        if x == 0 and y == 0:
            if self.tick == fps:
                if self.player.shield != 0:
                    self.player.shield -= 1
                else:
                    self.player.health -= 1
                self.tick = 0
        self.mb_x += v_x
        self.mb_y += v_y
        self.rect.x = self.mb_x
        self.rect.y = self.mb_y
        self.tick += 1
        if self.tick > fps:
            self.tick = fps


class Wall(pygame.sprite.Sprite):
    def __init__(self, player, coords, room):
        super().__init__(walls)
        self.add(all_sprites)
        walls_list.append(self)
        self.room = room
        self.image = pygame.transform.scale(load_image('wall.png'), (coords[2], coords[3]))
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.x, self.y = coords[0], coords[1]
        self.player = player


def select_room(rooom):
    global selected_room
    if rooom is None:
        a = 4
        a += '4'
    for a in range(len(rooms)):
        for b in range(len(rooms[a])):
            if rooms[a][b]:
                if rooms[a][b] == rooom:
                    selected_room = rooom
                    rooms[a][b].rect.x = 0
                    rooms[a][b].rect.y = 0
                    for elem in walls_list:
                        if elem.room == rooom:
                            elem.rect.x = elem.x
                            elem.rect.y = elem.y
                else:
                    rooms[a][b].rect.x = -10000
                    rooms[a][b].rect.x = -10000
                    for elem in walls_list:
                        if elem.room == rooms[a][b]:
                            elem.rect.x = -10000
                            elem.rect.y = -10000


all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
rooms_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
mobs_sprite = pygame.sprite.Group()

player = Player()

room = Room('g', player, 0, 1)
room2 = Room('i', player, 0, 2)

mob = Monster(player, 'mob1.png')
mob2 = Monster(player, 'mob1.png')
mob3 = Monster(player, 'mob1.png')
mob4 = Monster(player, 'mob1.png')
mob5 = Monster(player, 'mob1.png')

select_room(room)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.life()
    player.update(pygame.key.get_pressed())
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    player_sprite.draw(screen)
    mobs_sprite.draw(screen)
    mobs_sprite.update()
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
