import os
import pygame
import ctypes

user32 = ctypes.windll.user32
pygame.init()
size = w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
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
        self.count = 0
        self.mb_x = w // 2
        self.mb_y = h // 2
        self.orientation = 1
        self.players = ['player_1.png', 'player_2.png', 'player_3.png', 'player_4.png', 'player_5.png', 'player_6.png',
                        'player_7.png', 'player_8.png']

    def life(self):
        if self.count == 8:
            self.index = (self.index + 1) % 8
            if self.orientation == 1:
                self.image = pygame.transform.scale(load_image(self.players[self.index]), (130, 161))
            else:
                self.image = self.image = pygame.transform.flip(
                    pygame.transform.scale(load_image(self.players[self.index]), (130, 161)), True, False)
            self.count = 0
        self.count += 1

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
    selected_room = rooom
    for a in range(len(rooms)):
        for b in range(len(rooms[a])):
            if rooms[a][b]:
                if rooms[a][b] == rooom:
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


arrow_sprite = pygame.sprite.Group()
arrow = pygame.sprite.Sprite(arrow_sprite)
arrow.add(all_sprites)
arrow_image = load_image('arrow.png')
arrow.image = arrow_image
arrow.rect = arrow.image.get_rect()

player_sprite = pygame.sprite.Group()
player = Player()

rooms_sprite = pygame.sprite.Group()
room = Room('g', player, 0, 1)
room2 = Room('i', player, 0, 2)

select_room(room)

wall = Wall(player, (0, 0, w, 50), room)
wall_2 = Wall(player, (0, h - 50, w, 50), room)

pygame.mouse.set_visible(False)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            arrow.image = pygame.transform.scale(arrow_image, (40, 37))
        if event.type == pygame.MOUSEBUTTONUP:
            arrow.image = arrow_image
    player.life()
    player.update(pygame.key.get_pressed())
    if pygame.mouse.get_focused():
        arrow.rect.x = pygame.mouse.get_pos()[0]
        arrow.rect.y = pygame.mouse.get_pos()[1]
    else:
        arrow.rect.x, arrow.rect.y = -200, -200
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    player_sprite.draw(screen)
    arrow_sprite.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
