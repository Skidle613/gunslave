import os
import random
import time

import pygame
import ctypes

import sqlite3

user32 = ctypes.windll.user32
pygame.init()
size = w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
walls_list = []
score = 0
v = 150
fps = 60
selected_room = None
portal = False
rooms = [[None]]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
rooms_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
mobs_sprite = pygame.sprite.Group()
health_shield = pygame.sprite.Group()

player_health = [[], []]


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


def start_screen():
    pygame.init()
    title_text = "GUNSLAVE"
    intro_text = ["НАЖМИТЕ ESC для выхода из игры",
                  "НАЖМИТЕ F для открытия окна улучшения персонажа",
                  "НАЖМИТЕ SPACE для начала игры"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 120)
    title_rendered = title_font.render(title_text, 1, pygame.Color((220, 168, 43)))
    title_rect = title_rendered.get_rect()
    title_rect.x = w // 2 - title_rect.width // 2
    title_rect.top = 100
    screen.blit(title_rendered, title_rect)
    text_coord = 820
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color((152, 50, 231)))
        intro_rect = string_rendered.get_rect()
        text_coord += 40
        intro_rect.top = text_coord
        intro_rect.x = w // 2 - 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    main_game()
                if event.key == pygame.K_f:
                    upgrade_player()
        pygame.display.flip()
        clock.tick(fps)


def upgrade_player():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    hl = cur.execute("""SELECT health FROM player_stats WHERE id = 1""").fetchone()[0]
    hl_up = cur.execute("""SELECT health_upgrade_score FROM player_stats WHERE id = 1""").fetchone()[0]
    sh = cur.execute("""SELECT shield FROM player_stats WHERE id = 1""").fetchone()[0]
    sh_up = cur.execute("""SELECT shield_upgrade_score FROM player_stats WHERE id = 1""").fetchone()[0]
    at = cur.execute("""SELECT attack FROM player_stats WHERE id = 1""").fetchone()[0]
    at_up = cur.execute("""SELECT attack_upgrade_score FROM player_stats WHERE id = 1""").fetchone()[0]
    score = cur.execute("""SELECT score FROM player_stats WHERE id = 1""").fetchone()[0]
    intro_text = [("Текущее кол-во очков", str(score), ""),
                  ("ЗДОРОВЬЕ", str(hl), "ПРОКАЧАТЬ - 1"),
                  ("НАДО ОЧКОВ ДЛЯ ПРОКАЧКИ", str(hl_up), ""),
                  ("ЗАЩИТА", str(sh), "ПРОКАЧАТЬ - 2"),
                  ("НАДО ОЧКОВ ДЛЯ ПРОКАЧКИ", str(sh_up), ""),
                  ("АТАКА", str(at), "ПРОКАЧАТЬ - 3"),
                  ("НАДО ОЧКОВ ДЛЯ ПРОКАЧКИ", str(at_up), "")]
    fon = pygame.transform.scale(load_image('fon.jpg'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 300
    for line, line2, line3 in intro_text:
        string_rendered = font.render(line, 1, pygame.Color((255, 207, 171)))
        string_rendered2 = font.render(line2, 1, pygame.Color((255, 207, 171)))
        string_rendered3 = font.render(line3, 1, pygame.Color((255, 207, 171)))
        intro_rect = string_rendered.get_rect()
        intro_rect2 = string_rendered2.get_rect()
        intro_rect3 = string_rendered3.get_rect()
        text_coord += 40
        intro_rect.top = text_coord
        intro_rect2.top = text_coord
        intro_rect3.top = text_coord
        intro_rect.x = 200
        intro_rect2.x = 1000
        intro_rect3.x = 1400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        screen.blit(string_rendered2, intro_rect2)
        screen.blit(string_rendered3, intro_rect3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    start_screen()
                if event.key == pygame.K_1:
                    if score >= hl_up and hl < 20:
                        cur.execute(f"""UPDATE player_stats SET health = {hl + 1} WHERE id = 1""")
                        cur.execute(f"""UPDATE player_stats SET health_upgrade_score = {hl_up + 1000} WHERE id = 1""")
                        cur.execute(f"""UPDATE player_stats SET score = {score - hl_up} WHERE id = 1""")
                        con.commit()
                        upgrade_player()
                elif event.key == pygame.K_2:
                    if score >= sh_up and sh < 20:
                        cur.execute(f"""UPDATE player_stats SET shield = {sh + 1} WHERE id = 1""")
                        cur.execute(f"""UPDATE player_stats SET shield_upgrade_score = {sh_up + 1000} WHERE id = 1""")
                        cur.execute(f"""UPDATE player_stats SET score = {score - sh_up} WHERE id = 1""")
                        con.commit()
                        upgrade_player()
                elif event.key == pygame.K_3:
                    if score >= at_up and at < 5:
                        cur.execute(f"""UPDATE player_stats SET attack = {at + 1} WHERE id = 1""")
                        cur.execute(f"""UPDATE player_stats SET attack_upgrade_score = {at_up + 1000} WHERE id = 1""")
                        cur.execute(f"""UPDATE player_stats SET score = {score - at_up} WHERE id = 1""")
                        con.commit()
                        upgrade_player()
        pygame.display.flip()
        clock.tick(fps)


def end_game(score):
    global walls_list, selected_room, rooms, all_sprites, walls, \
        rooms_sprite, player_sprite, mobs_sprite, \
        health_shield, \
        player, player_health
    walls_list = []
    selected_room = None
    rooms = [[None]]
    intro_text = ["Вы закончили игру", "Ваш счет: ", str(score), 'Нажмите любую клавишу чтобы продолжить']
    fon = pygame.transform.scale(load_image('fon.jpg'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color((152, 50, 231)))
        intro_rect = string_rendered.get_rect()
        text_coord += 40
        intro_rect.top = text_coord
        intro_rect.x = w // 2 - 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    rooms_sprite = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    mobs_sprite = pygame.sprite.Group()
    health_shield = pygame.sprite.Group()

    player = Player()

    player_health = [[], []]
    for i in range(player.health):
        heart = pygame.sprite.Sprite(health_shield)
        heart.image = pygame.transform.scale(load_image('heart.png'), (20, 20))
        heart.rect = heart.image.get_rect()
        heart.rect.x = 20 + 20 * i
        heart.rect.y = 20
        player_health[0].append(heart)
    for i in range(player.shield):
        shield = pygame.sprite.Sprite(health_shield)
        shield.image = pygame.transform.scale(load_image('shield.png'), (20, 20))
        shield.rect = shield.image.get_rect()
        shield.rect.x = 20 + 20 * i
        shield.rect.y = 60
        player_health[1].append(shield)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
        pygame.display.flip()
        clock.tick(fps)


class Player(pygame.sprite.Sprite):
    player_image = load_image('player_1.png')

    def __init__(self, gun=1):
        global v, fps
        super().__init__(player_sprite)
        self.add(all_sprites)
        self.image = pygame.transform.scale(Player.player_image, (130, 161))
        self.rect = self.image.get_rect()
        self.rect.x = w // 2 - self.rect.width // 2
        self.rect.y = h // 2 - self.rect.height // 2
        self.gun = gun
        self.index = 0
        self.count1 = 0
        self.count2 = 0
        self.mb_x = w // 2 - self.rect.width // 2
        self.mb_y = h // 2 - self.rect.height // 2
        self.orientation = 1
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.attacck = self.cur.execute("""SELECT attack FROM player_stats WHERE id = 1""").fetchone()[0]
        self.max_health = self.cur.execute("""SELECT health FROM player_stats WHERE id = 1""").fetchone()[0]
        self.health = self.max_health
        self.max_shield = self.cur.execute("""SELECT shield FROM player_stats WHERE id = 1""").fetchone()[0]
        self.shield = self.max_shield
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
            if self.health != 0:
                self.shield += 1
            if self.shield > self.max_shield:
                self.shield = self.max_shield
            self.count2 = 0
        self.count2 += 1
        global player_health
        for sprite in player_health[0]:
            sprite.rect.x = -400
        for sprite in player_health[1]:
            sprite.rect.x = -400
        for i in range(self.health):
            player_health[0][i].rect.x = 20 + 20 * i
        for i in range(self.shield):
            player_health[1][i].rect.x = 20 + 20 * i

    def update(self, event):
        global selected_room
        if event[pygame.K_w]:
            self.mb_y -= v / fps
            self.rect.y = self.mb_y
            if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, mobs_sprite):
                if pygame.sprite.spritecollideany(self, walls):
                    portal = True
                self.mb_y += v / fps
                self.rect.y = self.mb_y
        if event[pygame.K_d]:
            self.mb_x += v / fps
            self.rect.x = self.mb_x
            if self.orientation == 0:
                self.orientation = 1
                self.image = pygame.transform.flip(self.image, True, False)
            if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, mobs_sprite):
                if pygame.sprite.spritecollideany(self, walls):
                    portal = True
                self.mb_x -= v / fps
                self.rect.x = self.mb_x
        if event[pygame.K_s]:
            self.mb_y += v / fps
            self.rect.y = self.mb_y
            if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, mobs_sprite):
                if pygame.sprite.spritecollideany(self, walls):
                    portal = True
                self.mb_y -= v / fps
                self.rect.y = self.mb_y
        if event[pygame.K_a]:
            self.mb_x -= v / fps
            self.rect.x = self.mb_x
            if self.orientation == 1:
                self.orientation = 0
                self.image = pygame.transform.flip(self.image, True, False)
            if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, mobs_sprite):
                if pygame.sprite.spritecollideany(self, walls):
                    portal = True
                self.mb_x += v / fps
                self.rect.x = self.mb_x

        if self.rect.x < -self.rect.width:
            try:
                assert selected_room.j != 0
                select_room(rooms[selected_room.i][selected_room.j - 1])
                self.mb_x += w + self.rect.width
                self.rect.x = self.mb_x
                for sprite in mobs_sprite:
                    sprite.mb_x += w
                    sprite.rect.x = sprite.mb_x
            except Exception:
                self.mb_x += v / fps
                self.rect.x = self.mb_x
        if self.rect.x > w:
            try:
                select_room(rooms[selected_room.i][selected_room.j + 1])
                self.mb_x -= w + self.rect.width
                self.rect.x = self.mb_x
                for sprite in mobs_sprite:
                    sprite.mb_x -= w
                    sprite.rect.x = sprite.mb_x
            except Exception:
                self.mb_x -= v / fps
                self.rect.x = self.mb_x
        if self.rect.y < -self.rect.height:
            try:
                assert selected_room.i != 0
                select_room(rooms[selected_room.i - 1][selected_room.j])
                self.mb_y += h + self.rect.height
                self.rect.y = self.mb_y
                for sprite in mobs_sprite:
                    sprite.mb_y += h
                    sprite.rect.y = sprite.mb_y
            except Exception:
                self.mb_y += v / fps
                self.rect.y = self.mb_y
        if self.rect.y > h:
            try:
                select_room(rooms[selected_room.i + 1][selected_room.j])
                self.mb_y -= h + self.rect.height
                self.rect.y = self.mb_y
                for sprite in mobs_sprite:
                    sprite.mb_y -= h
                    sprite.rect.y = sprite.mb_y
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

    def attack(self, coords):
        if self.gun == 1:
            self.mb_x -= 10 * v / fps
            self.rect.x = self.mb_x
            if pygame.sprite.spritecollideany(self, mobs_sprite):
                pygame.sprite.spritecollideany(self, mobs_sprite).health -= 1
            self.mb_x += 10 * v / fps
            self.rect.x = self.mb_x

            self.mb_x += 10 * v / fps
            self.rect.x = self.mb_x
            if pygame.sprite.spritecollideany(self, mobs_sprite):
                pygame.sprite.spritecollideany(self, mobs_sprite).health -= 1
            self.mb_x -= 10 * v / fps
            self.rect.x = self.mb_x

            self.mb_y -= 10 * v / fps
            self.rect.y = self.mb_y
            if pygame.sprite.spritecollideany(self, mobs_sprite):
                pygame.sprite.spritecollideany(self, mobs_sprite).health -= 1
            self.mb_y += 10 * v / fps
            self.rect.y = self.mb_y

            self.mb_y += 10 * v / fps
            self.rect.y = self.mb_y
            if pygame.sprite.spritecollideany(self, mobs_sprite):
                pygame.sprite.spritecollideany(self, mobs_sprite).health -= 1
            self.mb_y -= 10 * v / fps
            self.rect.y = self.mb_y
        else:
            for sprite in mobs_sprite:
                if sprite.rect.collidepoint(coords):
                    sprite.health -= 1

player = Player(2)


class Room(pygame.sprite.Sprite):
    def __init__(self, type, player, i=0, j=0):
        super().__init__(rooms_sprite)
        self.add(all_sprites)
        self.i = i
        self.j = j
        if type == 'g':
            image = load_image('green_floor.png')
        elif type == 'l':
            image = load_image('lava_floor.png')
        elif type == 'i':
            image = load_image('ice_floor.png')
        try:
            rooms[i][j] = self
        except Exception:
            if i >= len(rooms):
                for _ in range(i - len(rooms) + 1):
                    rooms.append([None for m in range(len(rooms[0]))])
            if j >= len(rooms[0]):
                for elem in rooms:
                    for _ in range(j - len(rooms[-1]) + 1):
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
        self.health = 10
        self.player = player
        self.v = 100
        self.orientation = 1
        self.image = pygame.transform.scale(load_image(image), (60, 80))
        self.rect = self.image.get_rect()
        self.tick = fps - 1
        while True:
            self.rect.x = random.randrange(w - self.rect.width)
            self.rect.y = random.randrange(h - self.rect.height)
            if pygame.sprite.spritecollideany(self, walls) is None and pygame.sprite.spritecollideany(self,
                                                                                                      player_sprite) is None and len(
                pygame.sprite.spritecollide(self, mobs_sprite, False)) == 1:
                break
        self.mb_x = self.rect.x
        self.mb_y = self.rect.y

    def update(self):
        global score
        if self.health <= 0:
            score += 10
            self.kill()
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
            if self.orientation == 1:
                self.orientation = 0
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            if self.orientation == 0:
                self.orientation = 1
                self.image = pygame.transform.flip(self.image, True, False)
        if y < 0:
            v_y = -v_y
        self.mb_x += v_x
        self.mb_y += v_y
        self.rect.x = self.mb_x
        self.rect.y = self.mb_y
        if pygame.sprite.spritecollideany(self, player_sprite):
            if pygame.sprite.spritecollideany(self, player_sprite):
                if self.tick == fps:
                    if self.player.shield != 0:
                        self.player.shield -= 1
                    else:
                        self.player.health -= 1
                        if self.player.health <= 0:
                            self.player.kill()
                            end_game(score)
                    self.tick = 0
            self.mb_x -= v_x
            self.mb_y -= v_y
            self.rect.x = self.mb_x
            self.rect.y = self.mb_y
        self.tick += 1
        if self.tick > fps:
            self.tick = fps
        if self.health == 7:
            self.image = pygame.transform.scale(load_image('mob2.png'), (60, 80))
            if self.orientation == 0:
                self.image = pygame.transform.flip(self.image, True, False)
        if self.health == 5:
            self.image = pygame.transform.scale(load_image('mob3.png'), (60, 80))
            if self.orientation == 0:
                self.image = pygame.transform.flip(self.image, True, False)
        if self.health == 2:
            self.image = pygame.transform.scale(load_image('mob4.png'), (60, 80))
            if self.orientation == 0:
                self.image = pygame.transform.flip(self.image, True, False)


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


def main_game():
    # floor 1
    global score, rooms, portal
    score = 0
    been = []
    rooms = [[None]]
    room_main = Room('g', player, 0, 0)
    room7 = Room('g', player, 1, 0)
    way = random.choice([0, 2])
    room2 = Room('g', player, 1, 1)
    room3 = Room('g', player, way, 1)
    room4 = Room('g', player, way, 2)
    room5 = Room('g', player, way, 3)
    room6 = Room('g', player, 1, 3)
    room_finish = Room('g', player, 1, 4)
    wall = Wall(player, [w // 2 - 100, h // 2 - 150, 200, 300], room_finish)
    select_room(room_main)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.attack(event.pos)
        if selected_room != room_main and selected_room != room_finish:
            if selected_room not in been:
                been.append(selected_room)
                mob = Monster(player, 'mob1.png')
                mob2 = Monster(player, 'mob1.png')
                mob3 = Monster(player, 'mob1.png')
                mob4 = Monster(player, 'mob1.png')
                mob5 = Monster(player, 'mob1.png')
        if not portal:
            for i in range(len(rooms)):
                for j in range(len(rooms[i])):
                    if rooms[i][j] is not None:
                        pygame.draw.rect(screen, (200, 200, 200), (w - 400 + i * 20, 200 + j * 20, 10, 10))
                    if rooms[i][j] == selected_room:
                        pygame.draw.rect(screen, (255, 255, 255), (w - 400 + i * 20, 200 + j * 20, 10, 10))

            player.life()
            player.update(pygame.key.get_pressed())
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            player_sprite.draw(screen)
            mobs_sprite.draw(screen)
            health_shield.draw(screen)
            mobs_sprite.update()
            pygame.display.flip()
            clock.tick(fps)
        else:
            screen.fill((255, 255, 255))
            time.sleep(1)
            running = False
            portal = False

    been = []
    rooms = [[]]
    room_main = Room('g', player, 2, 0)
    way = random.choice([1, 3])
    room2 = Room('i', player, 2, 1)
    room3 = Room('i', player, way, 1)
    room4 = Room('i', player, way, 2)
    room5 = Room('i', player, way, 3)
    room6 = Room('i', player, 2, 3)
    room7 = Room('i', player, 4 - way, 3)
    room8 = Room('i', player, 4 - way, 2)
    if way == 1:
        room_finish = Room('g', player, 4, 2)
    else:
        room_finish = Room('g', player, 0, 2)
    wall = Wall(player, [w // 2 - 100, h // 2 - 150, 200, 300], room_finish)

    select_room(room_main)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.attack(event.pos)
        if selected_room != room_main and selected_room != room_finish:
            if selected_room not in been:
                been.append(selected_room)
                mob = Monster(player, 'mob1.png')
                mob2 = Monster(player, 'mob1.png')
                mob3 = Monster(player, 'mob1.png')
                mob4 = Monster(player, 'mob1.png')
                mob5 = Monster(player, 'mob1.png')
                mob6 = Monster(player, 'mob1.png')
                mob7 = Monster(player, 'mob1.png')
        if not portal:
            for i in range(len(rooms)):
                for j in range(len(rooms[i])):
                    if rooms[i][j] is not None:
                        pygame.draw.rect(screen, (200, 200, 200), (w - 400 + i * 20, 200 + j * 20, 10, 10))
                    if rooms[i][j] == selected_room:
                        pygame.draw.rect(screen, (255, 255, 255), (w - 400 + i * 20, 200 + j * 20, 10, 10))
            player.life()
            player.update(pygame.key.get_pressed())
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            player_sprite.draw(screen)
            mobs_sprite.draw(screen)
            health_shield.draw(screen)
            mobs_sprite.update()
            pygame.display.flip()
            clock.tick(fps)
        else:
            running = False
            portal = False


    been = []
    rooms = [[]]
    room_main = Room('g', player, 2, 0)
    way = random.choice([1, 3])
    room2 = Room('l', player, 2, 1)
    room3 = Room('l', player, way, 1)
    room4 = Room('l', player, way, 2)
    room5 = Room('l', player, way, 3)
    room6 = Room('l', player, 2, 3)
    room7 = Room('l', player, 4 - way, 3)
    room8 = Room('l', player, 4 - way, 2)
    room9 = Room('l', player, 2, 4)
    room10 = Room('l', player, 2, 5)
    room11 = Room('l', player, 1, 5)
    if way == 1:
        room_finish = Room('g', player, 4, 2)
    else:
        room_finish = Room('g', player, 0, 2)
    wall = Wall(player, [w // 2 - 100, h // 2 - 150, 200, 300], room_finish)

    select_room(room_main)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.attack(event.pos)
        if selected_room != room_main and selected_room != room_finish:
            if selected_room not in been:
                been.append(selected_room)
                mob = Monster(player, 'mob1.png')
                mob2 = Monster(player, 'mob1.png')
                mob3 = Monster(player, 'mob1.png')
                mob4 = Monster(player, 'mob1.png')
                mob5 = Monster(player, 'mob1.png')
                mob6 = Monster(player, 'mob1.png')
                mob7 = Monster(player, 'mob1.png')
                mob8 = Monster(player, 'mob1.png')
                mob9 = Monster(player, 'mob1.png')
        if not portal:
            for i in range(len(rooms)):
                for j in range(len(rooms[i])):
                    if rooms[i][j] is not None:
                        pygame.draw.rect(screen, (200, 200, 200), (w - 400 + i * 20, 200 + j * 20, 10, 10))
                    if rooms[i][j] == selected_room:
                        pygame.draw.rect(screen, (255, 255, 255), (w - 400 + i * 20, 200 + j * 20, 10, 10))
            player.life()
            player.update(pygame.key.get_pressed())
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            player_sprite.draw(screen)
            mobs_sprite.draw(screen)
            health_shield.draw(screen)
            mobs_sprite.update()
            pygame.display.flip()
            clock.tick(fps)
        else:
            running = False
            portal = False
            end_game(score)


for i in range(player.health):
    heart = pygame.sprite.Sprite(health_shield)
    heart.image = pygame.transform.scale(load_image('heart.png'), (20, 20))
    heart.rect = heart.image.get_rect()
    heart.rect.x = 20 + 20 * i
    heart.rect.y = 20
    player_health[0].append(heart)
for i in range(player.shield):
    shield = pygame.sprite.Sprite(health_shield)
    shield.image = pygame.transform.scale(load_image('shield.png'), (20, 20))
    shield.rect = shield.image.get_rect()
    shield.rect.x = 20 + 20 * i
    shield.rect.y = 60
    player_health[1].append(shield)

# room = Room('g', player, 0, 1)
# room2 = Room('i', player, 0, 2)


# mob = Monster(player, 'mob1.png')
# mob2 = Monster(player, 'mob1.png')
# mob3 = Monster(player, 'mob1.png')
# mob4 = Monster(player, 'mob1.png')
# mob5 = Monster(player, 'mob1.png')

start_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         player.attack(event.pos)
    # player.life()
    # player.update(pygame.key.get_pressed())
    # screen.fill((0, 0, 0))
    # all_sprites.draw(screen)
    # player_sprite.draw(screen)
    # mobs_sprite.draw(screen)
    # health_shield.draw(screen)
    # mobs_sprite.update()
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
