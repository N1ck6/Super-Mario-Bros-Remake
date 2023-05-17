import pygame as pg
from random import choice, randrange
from math import sin, cos, radians
import time


def read(num=-1):
    with open("data/settings.txt", mode="r") as f:
        data = f.readlines()
        if num == -1:
            return len(data)
        return data[num].strip('\n')


name = read(0)
musical = read(1)
better = read(2)
vol1 = float(read(3))
sound = read(4)
vol2 = float(read(5))
fullscreen = read(6)
records = read(7).split()
mode = read(8).split()
pg.init()
info = pg.display.Info()
m_width, m_height = info.current_w, info.current_h
[width, height] = [1000, 750] if fullscreen == "Off" else [m_width, m_height]
screen = pg.display.set_mode((width, height))
edin = height // 15
edin_col = width / edin


def skin(name, size=(edin, edin)):
    return pg.transform.scale(pg.image.load(f'data/images/{name}.png'), size).convert_alpha()


sounds = {'coin': pg.mixer.Sound('data/sounds/coin.ogg'), 'jump': pg.mixer.Sound('data/sounds/jump.ogg'),
          'death': pg.mixer.Sound('data/sounds/death.ogg'), 'kill': pg.mixer.Sound('data/sounds/kill.ogg'),
          'appears': pg.mixer.Sound('data/sounds/appear.ogg'), 'fireball': pg.mixer.Sound('data/sounds/fireball.ogg'),
          'kick': pg.mixer.Sound('data/sounds/kick.ogg'), 'switched': pg.mixer.Sound('data/sounds/switched.ogg'),
          'fire': pg.mixer.Sound('data/sounds/fire.ogg'), 'bump': pg.mixer.Sound('data/sounds/bump.ogg'),
          'flag': pg.mixer.Sound('data/sounds/flagpole.ogg'), 'bowser': pg.mixer.Sound('data/sounds/bowser.mp3'),
          'powerup': pg.mixer.Sound('data/sounds/powerup.ogg'), 'theme': pg.mixer.Sound('data/sounds/level.mp3'),
          'menu': pg.mixer.Sound('data/sounds/menu.mp3'), 'fall': pg.mixer.Sound('data/sounds/fall.ogg'),
          'hammer': pg.mixer.Sound('data/sounds/hammer.ogg'), 'boom': pg.mixer.Sound('data/sounds/boom.ogg'),
          'gameover': pg.mixer.Sound('data/sounds/gameover.ogg'), 'star': pg.mixer.Sound('data/sounds/star.mp3'),
          'end': pg.mixer.Sound('data/sounds/end.ogg'), 'smash': pg.mixer.Sound('data/sounds/smash.ogg'),
          'roar': pg.mixer.Sound('data/sounds/loud_roar.ogg')}

sounds1 = {'coin': pg.mixer.Sound('data/sounds1/coin.ogg'), 'jump': pg.mixer.Sound('data/sounds1/jump.ogg'),
           'death': pg.mixer.Sound('data/sounds1/death.ogg'), 'kill': pg.mixer.Sound('data/sounds1/kill.ogg'),
           'appears': pg.mixer.Sound('data/sounds1/appear.ogg'), 'fireball': pg.mixer.Sound('data/sounds1/fireball.ogg'),
           'kick': pg.mixer.Sound('data/sounds1/kick.ogg'), 'switched': pg.mixer.Sound('data/sounds1/switched.ogg'),
           'fire': pg.mixer.Sound('data/sounds1/fire.ogg'), 'bump': pg.mixer.Sound('data/sounds1/bump.ogg'),
           'flag': pg.mixer.Sound('data/sounds1/flagpole.ogg'), 'bowser': pg.mixer.Sound('data/sounds1/bowser.mp3'),
           'powerup': pg.mixer.Sound('data/sounds1/powerup.ogg'), 'theme1': pg.mixer.Sound('data/sounds1/level1.mp3'),
           'theme3': pg.mixer.Sound('data/sounds1/level3.mp3'), 'theme2': pg.mixer.Sound('data/sounds1/level2.mp3'),
           'theme4': pg.mixer.Sound('data/sounds1/level4.mp3'), 'menu': pg.mixer.Sound('data/sounds1/menu.mp3'),
           'hammer': pg.mixer.Sound('data/sounds1/hammer.ogg'), 'boom': pg.mixer.Sound('data/sounds1/boom.ogg'),
           'gameover': pg.mixer.Sound('data/sounds1/gameover.ogg'), 'star': pg.mixer.Sound('data/sounds1/star.mp3'),
           'end': pg.mixer.Sound('data/sounds1/end.ogg'), 'smash': pg.mixer.Sound('data/sounds1/smash.ogg'),
           'roar': pg.mixer.Sound('data/sounds1/loud_roar.ogg'), 'fall': pg.mixer.Sound('data/sounds1/fall.ogg')}


def play(name, loops, volume):
    if (musical == "On" and name in ["menu", "theme1", "theme2", "theme3", "theme4", "star", "end", "bowser"]) or\
       (sound == "On" and name not in ["menu", "theme1", "theme2", "theme3", "theme4", "star", "end", "bowser"]):
        if better == "On":
            sounds1[name].play(loops=loops)
            sounds1[name].set_volume(volume)
        else:
            if 'theme' in name:
                name = 'theme'
            sounds[name].play(loops=loops)
            sounds[name].set_volume(volume)


def stop(name):
    if better == "On":
        if name == "all":
            for i in sounds1:
                sounds1[i].stop()
        else:
            sounds1[name].stop()
    else:
        if 'theme' in name:
            name = 'theme'
        if name == "all":
            for i in sounds:
                sounds[i].stop()
        else:
            sounds[name].stop()


def write(num, string):
    data = []
    ra = read()
    for i in range(ra):
        data.append(read(i))
    with open("data/settings.txt", mode="w+") as f:
        for i in range(ra):
            f.write(str(string) + '\n') if i == num else f.write(data[i] + '\n')


lava = skin('castle/lava', (edin * 2, edin * 3))
pl_images = [skin('plants/plant', (edin, edin * 1.5)), skin('plants/plant2', (edin, edin * 1.5))]
p_images = [skin('another/particle3', (edin * 0.6, edin * 0.6)), skin('another/particle2', (edin * 0.6, edin * 0.6)),
            skin('another/particle', (edin * 0.6, edin * 0.6)), skin('another/particle4', (edin * 0.6, edin * 0.6))]
b_image = [skin('another/b_particle3', (edin * 0.6, edin * 0.6)), skin('another/b_particle2', (edin * 0.6, edin * 0.6)),
           skin('another/b_particle', (edin * 0.6, edin * 0.6)), skin('another/b_particle4', (edin * 0.6, edin * 0.6))]
dead_koopa = skin('koopa/dead_koopa', (edin, edin * 0.8))
fly_koopa = skin('koopa/sonic', (edin, edin * 0.8))
left_koopas = [skin('koopa/left/koopa', (edin * 0.8, edin)), skin('koopa/left/koopa2', (edin * 0.8, edin))]
right_koopas = [skin('koopa/right/koopa', (edin * 0.8, edin)), skin('koopa/right/koopa2', (edin * 0.8, edin))]
left_flying_koopas = [skin('koopa/left/flly', (edin * 0.8, edin)), skin('koopa/left/flly2', (edin * 0.8, edin))]
right_flying_koopas = [skin('koopa/right/flly', (edin * 0.8, edin)), skin('koopa/right/flly2', (edin * 0.8, edin))]
animate_koopa = skin('koopa/dead', (edin, edin * 0.8))
animate_flyingkoopa = skin('koopa/fly_dead', (edin, edin * 0.8))
dead_goombs = skin('goomba/dead_goomba', (edin, edin * 0.5))
running_goombas = [skin('goomba/goombs1'), skin('goomba/goombs2')]
fly_goomba = skin('goomba/fly_goomba', (edin, edin * 0.5))
sizeup = skin('sizeup')
speedup = [skin('star/star'), skin('star/star2'), skin('star/star3'), skin('star/star4')]
flower = [skin('flower/flower1'), skin('flower/flower2'), skin('flower/flower3'), skin('flower/flower4')]
images = [skin('coins/coin', (edin * 0.8, edin * 0.8)), skin('coins/coin2', (edin * 0.8, edin * 0.8)),
          skin('coins/coin3', (edin * 0.8, edin * 0.8)), skin('coins/coin4', (edin * 0.8, edin * 0.8)),
          skin('coins/coin5', (edin * 0.8, edin * 0.8)), skin('coins/coin6', (edin * 0.8, edin * 0.8)),
          skin('coins/coin7', (edin * 0.8, edin * 0.8)), skin('coins/coin8', (edin * 0.8, edin * 0.8))]
boom_balls = [skin('fireworks/boom1', (edin * 0.8, edin * 0.8)), skin('fireworks/boom2', (edin * 0.8, edin * 0.8)),
              skin('fireworks/boom3', (edin * 0.8, edin * 0.8))]
running_balls = [skin('fireball/ball1', (edin * 0.5, edin * 0.5)), skin('fireball/ball2', (edin * 0.5, edin * 0.5)),
                 skin('fireball/ball3', (edin * 0.5, edin * 0.5)), skin('fireball/ball4', (edin * 0.5, edin * 0.5))]
platform = skin('platform', (edin * 3, edin * 0.5))
left_idle = skin('mario/small/left/idle')
left_idle1 = skin('mario/big/left/idle', (edin, 1.6 * edin))
right_idle = skin('mario/small/right/idle')
right_idle1 = skin('mario/big/right/idle', (edin, 1.6 * edin))
left_jump = skin('mario/small/left/jump')
left_jump1 = skin('mario/big/left/jump', (edin, 1.6 * edin))
right_jump = skin('mario/small/right/jump')
right_jump1 = skin('mario/big/right/jump', (edin, 1.6 * edin))
left_running = [skin('mario/small/left/run'), skin('mario/small/left/run2'),
                skin('mario/small/left/run3'), skin('mario/small/left/run4')]
left_running1 = [skin('mario/big/left/run1', (edin, 1.6 * edin)), skin('mario/big/left/run2', (edin, 1.6 * edin)),
                 skin('mario/big/left/run3', (edin, 1.6 * edin)), skin('mario/big/left/run4', (edin, 1.6 * edin))]
right_running = [skin('mario/small/right/run'), skin('mario/small/right/run2'),
                 skin('mario/small/right/run3'), skin('mario/small/right/run4')]
right_running1 = [skin('mario/big/right/run1', (edin, 1.6 * edin)), skin('mario/big/right/run2', (edin, 1.6 * edin)),
                  skin('mario/big/right/run3', (edin, 1.6 * edin)), skin('mario/big/right/run4', (edin, 1.6 * edin))]
dead_image = skin('mario/small/dead')
loop_image = [skin('mario/small/loop1'), skin('mario/small/loop2')]
loop_image1 = [skin('mario/big/loop1', (edin, edin * 1.6)), skin('mario/big/loop2', (edin, edin * 1.6))]
r_shift = skin('mario/big/r_shift')
l_shift = skin('mario/big/l_shift')
left_idle_f = skin('mariofire/small/left/idle')
left_idle1_f = skin('mariofire/big/left/idle', (edin, 1.6 * edin))
right_idle_f = skin('mariofire/small/right/idle')
right_idle1_f = skin('mariofire/big/right/idle', (edin, 1.6 * edin))
left_jump_f = skin('mariofire/small/left/jump')
left_jump1_f = skin('mariofire/big/left/jump', (edin, 1.6 * edin))
right_jump_f = skin('mariofire/small/right/jump')
right_jump1_f = skin('mariofire/big/right/jump', (edin, 1.6 * edin))
left_running_f = [skin('mariofire/small/left/run'), skin('mariofire/small/left/run2'),
                  skin('mariofire/small/left/run3'), skin('mariofire/small/left/run4')]
left_running1_f = [skin('mariofire/big/left/run1', (edin, 1.6 * edin)), skin('mariofire/big/left/run2',
                                                                             (edin, 1.6 * edin)),
                   skin('mariofire/big/left/run3', (edin, 1.6 * edin)), skin('mariofire/big/left/run4',
                                                                             (edin, 1.6 * edin))]
right_running_f = [skin('mariofire/small/right/run'), skin('mariofire/small/right/run2'),
                   skin('mariofire/small/right/run3'), skin('mariofire/small/right/run4')]
right_running1_f = [skin('mariofire/big/right/run1', (edin, 1.6 * edin)), skin('mariofire/big/right/run2',
                                                                               (edin, 1.6 * edin)),
                    skin('mariofire/big/right/run3', (edin, 1.6 * edin)), skin('mariofire/big/right/run4',
                                                                               (edin, 1.6 * edin))]
dead_image_f = skin('mariofire/small/dead')
loop_image_f = [skin('mariofire/small/loop1'), skin('mariofire/small/loop2')]
loop_image1_f = [skin('mariofire/big/loop1', (edin, edin * 1.6)), skin('mariofire/big/loop2', (edin, edin * 1.6))]
r_shift_f = skin('mariofire/big/r_shift')
l_shift_f = skin('mariofire/big/l_shift')
random_animations = [skin('random'), skin('random'), skin('random2'), skin('random3'), skin('random2')]
left = [skin('bowser/left/left_bowser1', (96, 96)), skin('bowser/left/left_bowser2', (96, 96)),
        skin('bowser/left/left_bowser3', (96, 96)), skin('bowser/left/left_bowser4', (96, 96))]
left_images = [skin('bowser/leftfire1', (edin * 1.5, edin * 0.5)), skin('bowser/leftfire2', (edin * 1.5, edin * 0.5))]
bite_images = [skin('ball/ball', (edin * 0.8, edin * 0.8)), skin('ball/ball2', (edin * 0.8, edin * 0.8))]
axe_images = [skin('castle/axe/axe1'), skin('castle/axe/axe2'), skin('castle/axe/axe3')]
lhb_images = [skin('hammer_brother/left/left_run1', (edin, edin * 1.5)),
              skin('hammer_brother/left/left_run2', (edin, edin * 1.5))]
rhb_images = [skin('hammer_brother/right/right_run1', (edin, edin * 1.5)),
              skin('hammer_brother/right/right_run2', (edin, edin * 1.5))]
right_shoot = skin('hammer_brother/right/right_shoot', (edin, edin * 1.5))
left_shoot = skin('hammer_brother/left/left_shoot', (edin, edin * 1.5))
h_images = [skin('hammer/hammer1'), skin('hammer/hammer2'), skin('hammer/hammer3'), skin('hammer/hammer4')]
l_left = skin('latitu/left_idle', (edin, edin * 1.5))
l_right = skin('latitu/right_idle', (edin, edin * 1.5))
l_attack = skin('latitu/attack', (edin, edin * 1.5))
h_left_images = [skin('spiny/lrun1'), skin('spiny/lrun2')]
h_right_images = [skin('spiny/rrun1'), skin('spiny/rrun2')]
h_fall = [skin('spiny/fall1'), skin('spiny/fall2')]
cannon = skin('bullets/cannon', (edin, edin * 2))
bullet_left = skin('bullets/bullet_left', (edin, edin * 0.75))
bullet_right = skin('bullets/bullet_right', (edin, edin * 0.75))
bl = skin('b_locked', (edin * 2, edin * 2))
b_dead = skin('beetle/dead')
b_down = skin('beetle/down')
left_beetle = [skin('beetle/left1'), skin('beetle/left2')]
right_beetle = [skin('beetle/right1'), skin('beetle/right2')]
b1 = skin('b1', (edin * 2, edin * 2))
b2 = skin('b2', (edin * 2, edin * 2))
b3 = skin('b3', (edin * 2, edin * 2))
b4 = skin('b4', (edin * 2, edin * 2))
instead = skin('instead')
mar = skin('pl', (edin * 2, edin * 2))
cas = skin('castle/castle', (edin * 5.5, edin * 5.5))
change_b = skin('b_ch', (edin * 0.8, edin * 0.8))
on = skin('b_yes', (edin * 0.8, edin * 0.8))
off = skin('b_no', (edin * 0.8, edin * 0.8))
point = skin('point', (edin * 0.8, edin * 0.8))
quit_font = pg.font.Font('data/mario_font.ttf', 18)
text_surface = quit_font.render("QUITTING", True, (255, 255, 255))
quit_rect = text_surface.get_rect(topright=(width - 10, height - 10))
text_alpha = 30
start_time = 0
text_surface.set_alpha(text_alpha)
icon = pg.image.load('data/favicon.ico')
pg.display.set_icon(icon)
Game_over = False
current_level = 0
run = True
running = False
running2 = False
running_scene = False
White = (255, 255, 255)
seconds = 400
points_count = 0
fireworks_count = 4
font_path = 'data/mario_font.ttf'
font_size = int(edin / 5)
font_verysmall = pg.font.Font(font_path, font_size)
font_mediumsmall = pg.font.Font(font_path, int(font_size * 1.5))
font_small = pg.font.Font(font_path, font_size * 2)
font_medium = pg.font.Font(font_path, int(font_size * 2.2))
font_verylarge = pg.font.Font(font_path, font_size * 4)
Level = []
fps = 60
LOW_JUMP_MULTIPLIER, FALL_MULTIPLIER = 3, 1


def refresh():
    global name, musical, better, sound, vol1, vol2, records, mode
    name = read(0)
    musical = read(1)
    better = read(2)
    vol1 = float(read(3))
    sound = read(4)
    vol2 = float(read(5))
    records = read(7).split()
    mode = read(8).split()


class Button:
    def __init__(self, x, y, image):
        self.x = image.get_width()
        self.y = image.get_height()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.clicked = False
        self.clickable = True

    def __call__(self, *args):
        self.__init__(*args)

    def pressed(self, surface):
        if self.clickable:
            pressed = False
            if self.rect.collidepoint(pg.mouse.get_pos()):
                if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
            if pg.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                pressed = True
            surface.blit(self.image, (self.rect.x, self.rect.y))
            return pressed


class Point:
    def __init__(self, x, y, line):
        self.x = x
        self.y = y
        self.line = line
        self.width = height / 3
        self.height = 8
        self.rect = pg.Rect(x + 20, y, self.width - 40, self.height)
        if line == 3:
            self.point_value = vol1
        else:
            self.point_value = vol2
        self.point_width = 40
        self.point_height = 40
        self.point_x = self.x + round(self.point_value * (self.width - self.point_width))
        self.point_y = y - self.point_height // 2
        self.point_rect = pg.Rect(self.point_x, self.point_y - self.point_height / 2,
                                  self.point_width, self.point_height)
        self.dragging_rect = pg.Rect(x - edin, self.point_y - self.point_height / 2 - 10,
                                     self.width + edin * 2, self.height + self.point_height + 20)
        self.dragging = False

    def __call__(self, *args):
        self.__init__(*args)

    def update(self):
        if self.dragging:
            self.point_x = pg.mouse.get_pos()[0] - self.point_width / 2
            if self.point_x < self.x:
                self.point_x = self.x
            elif self.point_x > self.x + self.width - self.point_width:
                self.point_x = self.x + self.width - self.point_width
            self.point_value = round(100 * (self.point_x - self.x) / (self.width - self.point_width))
            self.point_x = self.x + round(self.point_value / 100 * (self.width - self.point_width))
            if self.point_value <= 0.1:
                self.point_value = 1
            write(self.line, self.point_value / 100)
            refresh()
        pg.draw.rect(screen, White, self.rect)
        screen.blit(point, (self.point_x, self.point_y - self.point_height / 2))

    def press(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.point_rect.collidepoint(pg.mouse.get_pos()) and not self.dragging:
                self.dragging = True
        elif (event.type == pg.MOUSEBUTTONUP and self.dragging) or \
             (not self.dragging_rect.collidepoint(pg.mouse.get_pos()) and self.dragging):
            self.dragging = False
            self.point_rect.x = self.point_x
            if self.point_value <= 0.1:
                self.point_value = 1


clock = pg.time.Clock()
player_group = pg.sprite.Group()
all_sprites = pg.sprite.Group()
block_sprites = pg.sprite.Group()
coin_sprites = pg.sprite.Group()
enemy_group = pg.sprite.Group()
cannons = pg.sprite.Group()
cannonballs = pg.sprite.Group()
pipe_sprites = pg.sprite.Group()
item_sprites = pg.sprite.Group()
goomba_sprites = pg.sprite.Group()
koopa_sprites = pg.sprite.Group()
decorations = pg.sprite.Group()
fireball_sprites = pg.sprite.Group()
castle = pg.sprite.Group()
flag = pg.sprite.Group()
Boss = pg.sprite.Group()
points = pg.sprite.Group()
mountain_and_clouds = pg.sprite.Group()
particles = pg.sprite.Group()
plants = pg.sprite.Group()
platforms = pg.sprite.Group()
bites = pg.sprite.Group()
bridge = pg.sprite.Group()
axe = pg.sprite.Group()
hammer_koopa = pg.sprite.Group()
Hammers = pg.sprite.Group()
hedgehogs = pg.sprite.Group()
latitu = pg.sprite.Group()
temp = pg.sprite.Group()
inviase = pg.sprite.Group()
extra_blocks = pg.sprite.Group()
firebar = pg.sprite.Group()


class Bullet(pg.sprite.Sprite):
    def __init__(self, all_sprites, cannons, x_pos, y_pos, direction):
        super().__init__(all_sprites, cannons)
        if direction == 'left':
            self.image = bullet_left
            self.speed = -5
        if direction == 'right':
            self.image = bullet_right
            self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.type = 'bullet'

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > width:
            self.kill()


class Cannon(pg.sprite.Sprite):
    def __init__(self, all_sprites, cannons, x_pos, y_pos):
        super().__init__(all_sprites, cannons)
        self.image = cannon
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.type = 'cannon'
        self.timer = 360
        self.direction = 'left'

    def update(self):
        if self.timer <= 0:
            play('boom', 0, vol2)
            if self.direction == 'left':
                Bullet(all_sprites, cannons, self.rect.left - self.rect.width, self.rect.top, self.direction)
            else:
                Bullet(all_sprites, cannons, self.rect.right, self.rect.top, self.direction)
            self.timer = 210
        self.timer -= 1
        if player.rect.left < self.rect.left:
            self.direction = 'left'
        else:
            self.direction = 'right'

    def animate(self):
        self.kill()


class Latitu(pg.sprite.Sprite):
    def __init__(self, all_sprites, latitu,  enemy_group, x_pos, y_pos):
        super().__init__(all_sprites, latitu, enemy_group)
        self.image = l_left
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.facing = 'left'
        self.back_speed = -6
        self.forward_speed = 6
        self.x_change = - 6
        self.hedge_timer = 270
        self.dead = False
        self.change_timer = 10
        self.need = True
        self.Animate = False
        self.was_Animate = False
        self.need_to_update = False
        self.killtime = 1000
        self.type = 'latitu'
        self.counter = 5

    def update(self):
        if not self.dead and self.need:
            if self.counter == 0:
                self.dead = True
            for sprite in flag:
                if self.rect.x + self.rect.width >= sprite.rect.x - 100:
                    self.need = False
            if self.rect.x + self.rect.width // 2 < player.rect.x + player.rect.width // 2:
                if self.change_timer <= 0:
                    self.x_change += 1
                    self.change_timer = 10
                if self.x_change == self.back_speed:
                    self.facing = 'right'
            if self.rect.x + self.rect.width // 2 >= player.rect.x + player.rect.width // 2:
                if self.change_timer <= 0:
                    self.x_change -= 1
                    self.change_timer = 10
                if self.x_change == self.forward_speed:
                    self.facing = 'left'
            if self.hedge_timer > 30:
                if self.facing == 'left':
                    self.image = l_left
                if self.facing == 'right':
                    self.image = l_right
            else:
                self.image = l_attack
            self.rect.x += self.x_change
            self.change_timer -= 1
            self.hedge_timer -= 1
            if self.hedge_timer == 0:
                self.hedge_timer = 270
                if self.facing == 'left':
                    Hedge_hog(all_sprites, hedgehogs, enemy_group, self.rect.x - edin // 2, self.rect.y, -2)
                if self.facing == 'right':
                    Hedge_hog(all_sprites, hedgehogs, enemy_group, self.rect.x + self.rect.width + edin // 2,
                              self.rect.y, 2)
                self.counter -= 1
            if self.x_change > self.forward_speed:
                self.x_change -= 1
            if self.x_change < self.back_speed:
                self.x_change += 1
        else:
            if self.counter == 0:
                self.rect.x -= 5
            elif self.dead:
                self.rect.y += 5
            elif not self.need:
                self.rect.x += self.back_speed

    def Dead(self):
        self.dead = True


class Part(pg.sprite.Sprite):
    def __init__(self, all_sprites, length, x, y):
        super().__init__(all_sprites, firebar)
        self.counter = 0
        self.size = edin / 2
        self.image = running_balls[int(self.counter)]
        self.rect = self.image.get_rect(center=(0, 0))
        self.angle = 0
        self.x = x
        self.y = y
        self.length = length
        self.counter = 0
        self.type = 'part'

    def __call__(self, *args):
        self.__init__(*args)

    def update(self):
        self.counter += 0.15
        if self.counter >= 4:
            self.counter = 0
        self.image = running_balls[int(self.counter)]
        self.rect = self.image.get_rect(center=(int(self.x + self.length * cos(radians(self.angle))),
                                                int(self.y + self.length * sin(radians(self.angle)))))
        self.angle += 1.5
        if self.angle > 360:
            self.angle = 0


class Hedge_hog(pg.sprite.Sprite):
    def __init__(self, all_sprites, hedge_hogs,  enemy_group, x_pos, y_pos, x):
        super().__init__(all_sprites, hedge_hogs, enemy_group)
        self.image = h_fall[0]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.on_ground = False
        self.speed = x
        self.x_change = self.speed
        self.y_change = -10
        self.gravity = 0.5
        self.counter = 0
        self.dead = False
        self.Animate = False
        self.was_Animate = False
        self.need_to_update = False
        self.killtime = 1000
        self.type = 'hedgehog'

    def update(self):
        if not self.dead:
            self.counter += 0.125
            if self.counter >= 2:
                self.counter = 0
            if not self.on_ground:
                self.image = h_fall[int(self.counter)]
            elif self.on_ground and self.x_change > 0:
                self.image = h_right_images[int(self.counter)]
            elif self.on_ground and self.x_change < 0:
                self.image = h_left_images[int(self.counter)]
            self.rect.x += self.x_change
            self.collide_x(block_sprites)
            self.collide_x(pipe_sprites)
            self.collide_x(inviase)
            if self.y_change != 0:
                self.on_ground = False
                self.x_change = 0
            else:
                if self.x_change == 0:
                    self.x_change = self.speed
            self.y_change += self.gravity
            self.rect.y += self.y_change
            self.collide_y(block_sprites)
            self.collide_y(pipe_sprites)
            self.collide_enemy(enemy_group)
            if self.rect.x + self.rect.width < -100:
                self.kill()
            if self.rect.x > width + 100:
                self.kill()

    def collide_y(self, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            self.on_ground = True
            self.y_change = 0
            self.rect.bottom = hits[0].rect.top

    def collide_x(self, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if self.x_change > 0:
                self.rect.right = hits[0].rect.left
            if self.x_change < 0:
                self.rect.left = hits[0].rect.right
            self.x_change = -self.x_change

    def collide_enemy(self, group):
        for sprite in group:
            if self.rect.x != sprite.rect.x:
                temp.add(sprite)
        hits = pg.sprite.spritecollide(self, temp, False)
        if hits:
            if self.x_change > 0:
                self.rect.right = hits[0].rect.left
            elif self.x_change < 0:
                self.rect.left = hits[0].rect.right
            self.x_change = -self.x_change
        temp.empty()

    def Dead(self):
        self.dead = True


class Hammer_Koopa(pg.sprite.Sprite):
    def __init__(self, all_sprites, Hammer_koopa, enemy_group, x_pos, y_pos):
        super().__init__(all_sprites, Hammer_koopa, enemy_group)
        self.image = lhb_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.facing = 'left'
        self.speed = 1
        self.x_change = - self.speed
        self.gravity = 0.5
        self.y_change = 0
        self.counter = 0
        self.steps = 100
        self.on_ground = False
        self.state = ''
        self.jump_timer = 180
        self.states = ['fall', 'jump']
        self.fall = 0
        self.hammer_counter = 120
        self.attaking = 0
        self.need_to_update = False
        self.dead = False
        self.Animate = False
        self.need_to_update = False
        self.was_Animate = False
        self.killtime = 1000
        self.type = 'hammer_koopa'

    def update(self):
        if not self.dead:
            self.counter += 0.125
            if self.counter >= 2:
                self.counter = 0
            if self.facing == 'left':
                if self.attaking <= 0:
                    self.image = lhb_images[int(self.counter)]
                else:
                    self.image = left_shoot
            if self.facing == 'right':
                if self.attaking <= 0:
                    self.image = rhb_images[int(self.counter)]
                else:
                    self.image = right_shoot
            self.rect.x += self.x_change
            self.steps -= 1
            self.rect.y += self.y_change
            self.y_change += self.gravity
            if self.y_change >= 0 and self.state == 'jump':
                self.state = ''
            if self.state == 'fall':
                self.fall += self.y_change
                if self.fall >= 150 or self.rect.y + self.rect.height >= height - edin * 2:
                    self.state = ''
                    self.fall = 0
            if self.steps == 0:
                self.steps = 100
                self.x_change = -self.x_change
            if self.rect.x + self.rect.width // 2 < player.rect.x + player.rect.width // 2:
                self.facing = 'right'
            if self.rect.x + self.rect.width // 2 >= player.rect.x + player.rect.width // 2:
                self.facing = 'left'
            if self.state != 'fall':
                self.check_collide_with_block('y')
            self.jump_timer -= 1
            if self.jump_timer <= 0:
                self.jump_timer = 180
                self.state = choice(self.states)
                if self.on_ground and self.state == 'jump':
                    self.y_change = -12
                elif self.state == 'fall':
                    self.on_ground = False
                    if self.rect.y + self.rect.height < height - edin * 2:
                        self.y_change = -5
            self.hammer_counter -= 1
            if self.hammer_counter <= 0:
                self.hammer_counter = 100
                play('hammer', 0, vol2)
                if self.facing == 'left':
                    Hammer(Hammers, all_sprites, self.rect.x - edin // 2, self.rect.y, -3)
                if self.facing == 'right':
                    Hammer(Hammers, all_sprites, self.rect.x + self.rect.width - edin // 2, self.rect.y, 3)
                self.attaking = 30
            if self.attaking > 0:
                self.attaking -= 1
        else:
            self.image = dead_koopa

    def Dead(self):
        self.dead = True

    def check_collide_with_block(self, direction):
        hits = pg.sprite.spritecollide(self, block_sprites, False)
        if hits:
            if direction == 'y':
                if self.y_change > 0:
                    self.on_ground = True
                    self.y_change = 0
                    if self.state == '':
                        self.rect.bottom = hits[0].rect.top


class Hammer(pg.sprite.Sprite):
    def __init__(self, Hammers, all_sprites,  x_pos, y_pos, speed):
        super().__init__(Hammers, all_sprites)
        self.image = h_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.counter = 0
        self.hitbox = pg.Rect((self.rect.x - self.rect.width // 2) // 2, (self.rect.y - self.rect.height // 2) // 2,
                              self.rect.width // 2, self.rect.height // 2)
        self.speed = speed
        self.y_change = -9
        self.gravity = 0.4
        self.type = ''

    def update(self):
        self.counter += 0.1
        if self.counter >= 4:
            self.counter = 0
        self.image = h_images[int(self.counter)]
        self.rect.x += self.speed
        self.rect.y += self.y_change
        if self.y_change <= 5:
            self.y_change += self.gravity
        self.hit_box()
        self.is_player_killed()

    def is_player_killed(self):
        if self.hitbox.colliderect(player.rect) and not player.untouchable:
            if player.form == 'big' and not player.star:
                player.untouchable = True
                player.form = 'small'
                self.fire = False
                player.rect.height = 50
            else:
                if not player.star:
                    player.dead = True

    def hit_box(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery


class Plant(pg.sprite.Sprite):
    def __init__(self, group, all_sprites, x, y):
        super().__init__(group, all_sprites)
        self.image = pl_images[0]
        self.rect = self.image.get_rect()
        self.rect.y = y - 25
        self.rect.x = x + self.rect.width // 2
        self.counter = 0
        self.top = self.rect.y
        self.y_change = -2
        self.timer = 0
        self.x = x
        self.y = y
        self.hitbox = pg.Rect(float(self.rect.x + 10), float(self.rect.y + 15), float(self.rect.width - 20),
                              float(self.rect.height - 20))
        self.type = ''

    def update(self):
        self.counter += 0.06
        if self.counter >= 2:
            self.counter = 0
        self.image = pl_images[int(self.counter)]
        if self.timer <= 0:
            if self.rect.y == self.top:
                self.y_change = -self.y_change
                self.timer = 120
            self.rect.y += self.y_change
            if self.rect.y >= height - self.rect.height:
                self.y_change = -self.y_change
        else:
            self.timer -= 1
        self.update_hit_box()
        self.check_collide()
        self.check_kill()

    def update_hit_box(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery + 5

    def check_collide(self):
        global points_count
        if self.hitbox.colliderect(player.rect) and not player.untouchable:
            if player.form == 'big' and not player.star:
                player.untouchable = True
                player.form = 'small'
                player.fire = False
                player.rect.height = 50
            else:
                if not player.star:
                    player.dead = True
                else:
                    self.kill()
                    play('kick', 0, vol2)
                    points_count += 100
                    Points(points, all_sprites, 100, self.hitbox.x + self.hitbox.width // 2, self.hitbox.y)

    def check_kill(self):
        global points_count
        for sprite in fireball_sprites:
            if self.hitbox.colliderect(sprite.rect):
                self.kill()
                points_count += 100
                Points(points, all_sprites, 100, sprite.rect.x + sprite.rect.width // 2, sprite.rect.y)
                play('kick', 0, vol2)


class Particles(pg.sprite.Sprite):
    def __init__(self, group, all_sprites, gravity, x, y, direction, counter, type):
        super().__init__(group, all_sprites)
        self.y_change = gravity
        self.x_change = direction
        self.gravity = 0.9
        self.timer = 1
        self.counter = counter
        self.type = type
        if type == 'brick':
            self.image = p_images[int(self.counter)]
        else:
            self.image = b_image[int(self.counter)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.counter += 0.125
        if self.counter >= 4:
            self.counter = 0
        if self.type == 'brick':
            self.image = p_images[int(self.counter)]
        else:
            self.image = b_image[int(self.counter)]
        self.y_change += self.gravity
        self.rect.y += self.y_change
        self.rect.x += self.x_change
        if self.rect.y >= height:
            self.kill()
        self.check_collide(enemy_group)
        self.check_collide(coin_sprites)
        if self.timer >= 0:
            self.timer -= 1

    def check_collide(self, group):
        global points_count
        hits = pg.sprite.spritecollide(self, group, False)
        if hits and self.timer > 0:
            if group == coin_sprites:
                if not hits[0].Animate:
                    play('coin', 0, vol2)
                    points_count += 200
            elif group == enemy_group:
                if not hits[0].Dead:
                    Points(points, all_sprites, 100, hits[0].rect.x + hits[0].rect.width // 2, hits[0].rect.y)
                    points_count += 100
                    play('kick', 0, vol2)
            hits[0].Dead = True
            hits[0].Animate = True


class Points(pg.sprite.Sprite):
    def __init__(self, group, all_sprites, count, x, y):
        super().__init__(group, all_sprites)
        self.image = font_mediumsmall.render(f'{count}', True, White)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.time = 30
        self.type = ''

    def update(self):
        self.rect.y -= 4
        self.time -= 1
        self.check_kill()

    def check_kill(self):
        if self.time <= 0:
            self.kill()


class Koopa(pg.sprite.Sprite):
    def __init__(self, enemy_group, koopa_sprites, all_sprites, x_pos, y_pos, type):
        super().__init__(enemy_group, koopa_sprites, all_sprites)
        self.x_change = -2
        if type == 'fly':
            self.y_change = 0
            self.state2 = True
        else:
            self.y_change = 0
        if type == 'fly':
            self.gravity = 0.1
        else:
            self.gravity = 0.5
        self.height = 50
        self.width = 40
        self.counter = 0
        self.Dead = False
        self.x = x_pos
        self.y = y_pos
        if type == 'koopa':
            self.image = left_koopas[0]
        elif type == 'fly':
            self.image = left_flying_koopas[0]
        else:
            self.image = left_beetle[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.on_ground = False
        self.type = type
        self.speed = 2
        self.allivetime = 600
        self.killtime = 1
        self.direction = 'left'
        self.sonic = False
        self.started = False
        self.Animate = False
        self.was_Animate = False
        self.need_to_update = False
        self.cooldown = 0
        self.state = ''
        self.timer = 20

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if not self.Dead:
            if not self.sonic and not self.Animate:
                self.counter += 0.09
                if self.counter >= 2:
                    self.counter = 0
                if self.direction == 'left':
                    if self.type == 'koopa':
                        self.image = left_koopas[int(self.counter)]
                    elif self.type == 'fly':
                        self.image = left_flying_koopas[int(self.counter)]
                    else:
                        self.image = left_beetle[int(self.counter)]
                else:
                    if self.type == 'koopa':
                        self.image = right_koopas[int(self.counter)]
                    elif self.type == 'fly':
                        self.image = right_flying_koopas[int(self.counter)]
                    else:
                        self.image = right_beetle[int(self.counter)]
        else:
            if not self.sonic and not self.Animate:
                self.dead()
                self.allivetime -= 1
        if self.sonic:
            self.collide_player()
        self.move()

    def move(self):
        if self.type != 'fly':
            self.y_change += self.gravity
            self.rect.y += self.y_change
        else:
            if not self.Dead:
                if not self.state2:
                    self.y_change += self.gravity
                else:
                    self.y_change -= self.gravity
                self.rect.y += int(self.y_change)
            else:
                self.rect.y += 7
                self.image = animate_flyingkoopa
        if self.type == 'fly' and not self.Dead:
            if self.y_change > 6 or self.y_change < -6:
                self.state2 = not self.state2
        if self.rect.y - self.rect.height >= height:
            self.kill()
        if not self.Animate:
            if self.type != 'fly':
                self.collide('y', block_sprites)
                self.collide('y', pipe_sprites)
            if not self.sonic:
                self.rect.x += self.x_change
                if self.type != 'fly':
                    self.collide('x', block_sprites)
                    self.collide('x', pipe_sprites)
                    self.collide('x', inviase)
                    self.collide_enemy('x')
            else:
                self.rect.x += self.x_change
                if self.type != 'fly':
                    self.collide('x', block_sprites)
                    self.collide('x', pipe_sprites)
                    self.collide_enemy('x')
        else:
            if not self.was_Animate:
                self.animate()

    def choose_direct(self):
        self.x_change = -self.x_change
        if self.x_change < 0:
            self.direction = 'left'
        else:
            self.direction = 'right'

    def change_direction(self):
        self.x_change = -self.x_change

    def rush(self):
        if not self.type == 'fly':
            if not self.sonic:
                if self.type == 'koopa':
                    self.image = fly_koopa
                elif self.type == 'beetle':
                    self.image = b_down
                self.speed = 8
                play('kill', 0, vol2)
                self.sonic = True
                if player.facing == 'right':
                    self.direction = 'right'
                    self.x_change = self.speed
                else:
                    self.direction = 'left'
                    self.x_change = -self.speed

    def collide(self, direction, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if direction == 'y':
                if self.y_change > 0:
                    self.on_ground = True
                    self.y_change = 0
                    self.rect.bottom = hits[0].rect.top
                elif self.y_change < 0:
                    self.y_change = 0
                    self.on_ground = False
                    self.rect.top = hits[0].rect.bottom
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                elif self.x_change < 0:
                    self.rect.left = hits[0].rect.right
                if not self.sonic:
                    self.choose_direct()
                else:
                    self.change_direction()
                    self.started = True

    def collide_enemy(self, direction):
        global points_count
        for sprite in enemy_group:
            if self.rect.x != sprite.rect.x:
                temp.add(sprite)
        hits = pg.sprite.spritecollide(self, temp, False)
        if hits and direction == 'x':
            if not self.sonic:
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                elif self.x_change < 0:
                    self.rect.left = hits[0].rect.right
                self.choose_direct()
            else:
                hits[0].need_to_update = True
                if not hits[0].was_Animate:
                    hits[0].Animate = True
                    play('kick', 0, vol2)
                    points_count += 150
                    Points(points, all_sprites, 150, hits[0].rect.x + hits[0].rect.width // 2, hits[0].rect.y)
        temp.empty()

    def collide_player(self):
        hits = pg.sprite.spritecollide(self, player_group, False)
        if hits and not self.Dead:
            if hits[0].y_change <= 0 and hits[0].rect.y - hits[0].rect.height <= self.rect.y and self.started:
                if player.form == 'big':
                    if not player.star:
                        player.untouchable = True
                        player.form = 'small'
                        player.fire = False
                        player.rect.height = 50
                    else:
                        self.animate()
                else:
                    if not player.untouchable and not player.star:
                        player.dead = True

    def alive(self):
        self.direction = 'right'
        self.Dead = False
        self.Animate = False
        self.x = self.rect.x
        self.y = self.rect.y
        if self.type == 'koopa':
            self.image = right_koopas[int(self.counter)]
        elif self.type == 'fly':
            self.image = right_flying_koopas[int(self.counter)]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.sonic = False
        self.x_change = self.speed

    def dead(self):
        self.Dead = True
        self.x = self.rect.x
        self.y = self.rect.y
        if self.type == 'koopa':
            self.image = dead_koopa
        elif self.type == 'beetle':
            self.image = b_down
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0
        self.need_to_update = True

    def animate(self):
        self.y_change = -edin / 10
        if self.type == 'koopa':
            self.image = animate_koopa
        elif self.type == 'fly':
            self.image = animate_flyingkoopa
        else:
            self.image = b_dead
        self.was_Animate = True
        self.Dead = True
        self.need_to_update = True


class Goomba(pg.sprite.Sprite):
    def __init__(self, goomba_sprites, all_sprites, x_pos, y_pos):
        super().__init__(enemy_group, goomba_sprites, all_sprites)
        self.speed = 2
        self.x_change = -self.speed
        self.y_change = 0
        self.gravity = 0.5
        self.Dead = False
        self.counter = 0
        self.x = x_pos
        self.y = y_pos
        self.image = running_goombas[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.on_ground = False
        self.killtime = 30
        self.allivetime = 1
        self.type = 'goomba'
        self.Animate = False
        self.was_Animate = False
        self.need_to_update = False

    def update(self):
        if not self.Dead:
            if not self.Animate:
                self.counter += 0.09
                if self.counter >= 2:
                    self.counter = 0
                self.image = running_goombas[int(self.counter)].convert_alpha()
        else:
            if not self.Animate:
                self.dead()
                self.killtime -= 1
        self.move()

    def move(self):
        self.y_change += self.gravity
        self.rect.y += self.y_change
        if self.rect.y - self.rect.height >= height:
            self.kill()
        if not self.Animate:
            self.collide('y', block_sprites)
            self.collide('y', pipe_sprites)
            self.rect.x += self.x_change
            self.collide('x', block_sprites)
            self.collide('x', pipe_sprites)
            self.collide('x', inviase)
            self.collide_enemy('x')
        else:
            if not self.was_Animate:
                self.animate()

    def choose_direct(self):
        self.x_change = - self.x_change

    def collide(self, direction, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if direction == 'y':
                self.on_ground = True
                self.y_change = 0
                self.rect.bottom = hits[0].rect.top
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                elif self.x_change < 0:
                    self.rect.left = hits[0].rect.right
                self.choose_direct()

    def collide_enemy(self, direction):
        for sprite in enemy_group:
            if self.rect.x != sprite.rect.x:
                temp.add(sprite)
        hits = pg.sprite.spritecollide(self, temp, False)
        if hits and direction == 'x':
            if self.x_change > 0:
                self.rect.right = hits[0].rect.left
            elif self.x_change < 0:
                self.rect.left = hits[0].rect.right
            self.choose_direct()
        temp.empty()

    def dead(self):
        self.Dead = True
        self.x = self.rect.x
        self.y = self.rect.y
        self.image = dead_goombs
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 0
        self.x_change = 0

    def animate(self):
        self.y_change = - 5
        self.image = fly_goomba
        self.was_Animate = True
        self.Dead = True

    def set_kill_time(self):
        self.killtime = 2
        pg.time.set_timer(pg.USEREVENT, 1000)


class Player(pg.sprite.Sprite):
    def __init__(self, player_group, x_pos, y_pos, mode):
        super().__init__(player_group)
        if mode[current_level * 2 - 2] == "big":
            self.form = 'big'
            self.image = right_idle1
        else:
            self.form = 'small'
            self.image = right_idle
        if mode[current_level * 2 - 1] == "True":
            self.fire = True
        else:
            self.fire = False
        self.star = False
        self.rect = self.image.get_rect()
        self.rect.x = self.x = x_pos
        self.rect.y = self.y = y_pos
        self.dead = False
        self.was_dead = False
        self.on_ground = False
        self.moving = False
        self.keyA = False
        self.keyS = False
        self.keyD = False
        self.keyCtrl = False
        self.keySpace = False
        self.isattack = False
        self.animate = False
        self.was_animate = False
        self.end = False
        self.untouchable = False
        self.speed = 4
        self.jumpspeed = -edin / 3.4
        self.gravity = edin / 100
        self.x_change = 0
        self.y_change = 0
        self.facing = 'right'
        self.speed_time = 0
        self.counter = 0
        self.attacking = 20
        self.cooldown = 100
        self.finalcoldown = 250
        self.axe = False
        self.bridge_sprite_kill = 60
        self.forbridge = []
        self.last = 0
        self.f_flag = False
        self.axe_timer = 200
        self.founded = False

    def get_rect(self):
        self.x = self.rect.x
        self.y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        if self.keyS:
            self.keyS = False
        if self.form == 'small':
            self.rect.y = self.y + edin
        else:
            self.rect.y = self.y

    def input(self):
        self.moving = True
        if self.keyS:
            self.x_change = 0
            self.moving = False
        elif self.keyA and not self.keyD:
            self.x_change = -self.speed
            self.facing = 'left'
        elif self.keyD and not self.keyA:
            self.x_change = self.speed
            self.facing = 'right'
        else:
            self.x_change = 0
            self.moving = False
        if not self.on_ground:
            self.moving = False
        if not self.isattack and self.keyCtrl and self.fire and not self.f_flag:
            self.f_flag = True
            Fireball(fireball_sprites, all_sprites, self.rect.x, self.rect.y, self.facing)
            play('fireball', 0, vol2)
            self.isattack = True

    def update(self):
        self.check_death()
        if self.axe:
            if not self.forbridge:
                for sprite in bridge:
                    self.forbridge.append(sprite.rect.x)
                if len(self.forbridge) >= 1:
                    self.max = max(self.forbridge)
            self.speed = 0
            for sprite in bridge:
                if self.bridge_sprite_kill <= 0:
                    if sprite.rect.x == self.max:
                        sprite.kill()
                        if len(self.forbridge) >= 1:
                            self.forbridge.pop()
                            if len(self.forbridge) >= 1:
                                self.max = max(self.forbridge)
                        self.bridge_sprite_kill = 40
                else:
                    self.bridge_sprite_kill -= 1
            self.axe_timer -= 1
            if self.axe_timer == 0:
                self.speed = 3
                self.x_change = player.speed
                self.moving = True
                self.animate = False
        if self.animate:
            self.was_animate = True
        if not self.dead:
            if not self.was_animate and not self.axe:
                self.input()
            else:
                if self.x_change == 0:
                    self.moving = False
                self.finalcoldown -= 1
                if self.finalcoldown == 0:
                    self.on_ground = True
                    self.keySpace = False
                if current_level == 4:
                    hits = pg.sprite.spritecollide(self, inviase, False)
                    if hits:
                        player.moving = False
                        self.x_change = 0
                        self.end = True
                else:
                    for sprite in castle:
                        hits = pg.sprite.spritecollide(self, castle, False)
                        if hits and sprite.rect.x + (
                                sprite.rect.width - edin) / 2 <= self.rect.x < sprite.rect.x + sprite.rect.width:
                            global fireworks_count
                            fireworks_count = 4
                            self.kill()
                            self.end = True
                            self.x_change = 0
            if not self.animate:
                if self.form == 'big':
                    if self.keyS:
                        if self.facing == 'right':
                            if self.fire:
                                self.image = r_shift_f
                            else:
                                self.image = r_shift
                        else:
                            if self.fire:
                                self.image = l_shift_f
                            else:
                                self.image = l_shift
                    elif not self.moving:
                        if not self.on_ground:
                            if self.facing == 'right':
                                if self.fire:
                                    self.image = right_jump1_f
                                else:
                                    self.image = right_jump1
                            else:
                                if self.fire:
                                    self.image = left_jump1_f
                                else:
                                    self.image = left_jump1
                        else:
                            if self.facing == 'right':
                                if self.fire:
                                    self.image = right_idle1_f
                                else:
                                    self.image = right_idle1
                            else:
                                if self.fire:
                                    self.image = left_idle1_f
                                else:
                                    self.image = left_idle1
                        self.counter = 0
                    else:
                        self.counter += 0.125
                        if self.counter >= 4:
                            self.counter = 0
                        if self.facing == 'right':
                            if self.fire:
                                self.image = right_running1_f[int(self.counter)]
                            else:
                                self.image = right_running1[int(self.counter)]
                        else:
                            if self.fire:
                                self.image = left_running1_f[int(self.counter)]
                            else:
                                self.image = left_running1[int(self.counter)]
                else:
                    if not self.moving:
                        if not self.on_ground:
                            if self.facing == 'right':
                                if self.fire:
                                    self.image = right_jump_f
                                else:
                                    self.image = right_jump
                            else:
                                if self.fire:
                                    self.image = left_jump_f
                                else:
                                    self.image = left_jump
                        else:
                            if self.facing == 'right':
                                if self.fire:
                                    self.image = right_idle_f
                                else:
                                    self.image = right_idle
                            else:
                                if self.fire:
                                    self.image = left_idle_f
                                else:
                                    self.image = left_idle
                        self.counter = 0
                    else:
                        self.counter += 0.125
                        if self.counter >= 4:
                            self.counter = 0
                        if self.facing == 'right':
                            if self.fire:
                                self.image = right_running_f[int(self.counter)]
                            else:
                                self.image = right_running[int(self.counter)]
                        else:
                            if self.fire:
                                self.image = left_running_f[int(self.counter)]
                            else:
                                self.image = left_running[int(self.counter)]
            else:
                self.counter += 0.1
                if self.counter >= 2:
                    self.counter = 0
                if self.fire:
                    if self.form == 'small':
                        self.image = loop_image_f[int(self.counter)]
                    else:
                        self.image = loop_image1_f[int(self.counter)]
                else:
                    if self.form == 'small':
                        self.image = loop_image[int(self.counter)]
                    else:
                        self.image = loop_image1[int(self.counter)]
                self.y_change = 5
            self.check_cam()
            self.cam()
            if not self.was_animate:
                self.check_collied('x', pipe_sprites)
                self.check_collied('x', block_sprites)
            self.enemy_kill('x')
            if self.keySpace:
                if not self.was_animate:
                    if self.on_ground:
                        self.on_ground = False
                        play('jump', 0, vol2)
                        self.y_change = self.jumpspeed
                        self.moving = False
            self.rect.y += self.y_change
            if not self.on_ground:
                if self.y_change < 0 and self.keySpace:
                    self.y_change += self.gravity
                elif self.y_change < 0 and not self.keySpace:
                    self.y_change += self.gravity * LOW_JUMP_MULTIPLIER
                else:
                    self.y_change += self.gravity * FALL_MULTIPLIER
            else:
                self.y_change += self.gravity * FALL_MULTIPLIER
            if self.y_change > 4:
                self.on_ground = False
            self.check_collied('y', pipe_sprites)
            self.check_collied('y', block_sprites)
            self.collide_platform()
            self.collide_coin()
            self.enemy_kill('y')
            self.collide_item()
            self.Was_Biten()
            self.Was_Firebarred()
            self.Axe()
            if not self.founded:
                self.found_bowser()
            self.collided(hedgehogs)
            self.collided(cannons)
            if self.isattack:
                self.attacking -= 1
            if self.attacking == 0:
                self.isattack = False
                self.attacking = 20
            if self.untouchable:
                self.cooldown -= 1
                if self.cooldown <= 0:
                    self.untouchable = False
                    self.cooldown = 100
        else:
            if not self.was_dead:
                if self.fire:
                    self.image = dead_image_f
                else:
                    self.image = dead_image
                self.y_change = -10
                self.was_dead = True
                game_over()
            else:
                self.rect.y += self.y_change
                if not self.animate:
                    self.y_change += self.gravity

    def found_bowser(self):
        for sprite in Boss:
            if sprite.rect.x <= width:
                for sprite2 in axe:
                    Block(block_sprites, block_sprites, all_sprites, sprite2.rect.x - 18 * edin, 5 * edin,
                          skin('bowser_brick'), 'b_brick')
                    Block(block_sprites, block_sprites, all_sprites, sprite2.rect.x - 18 * edin, 6 * edin,
                          skin('bowser_brick'), 'b_brick')
                    Block(block_sprites, block_sprites, all_sprites, sprite2.rect.x - 18 * edin, 7 * edin,
                          skin('bowser_brick'), 'b_brick')
                    Block(block_sprites, block_sprites, all_sprites, sprite2.rect.x - 18 * edin, 8 * edin,
                          skin('bowser_brick'), 'b_brick')
                    Block(block_sprites, block_sprites, all_sprites, sprite2.rect.x - 18 * edin, 9 * edin,
                          skin('bowser_brick'), 'b_brick')
                    stop('theme' + str(current_level))
                    play('boom', 0, vol2)
                    play('bowser', -1, vol1)
                    self.founded = True

    def collided(self, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if group == hedgehogs:
                if not hits[0].dead:
                    global points_count
                    if not self.untouchable:
                        if self.form == 'big' and not player.star:
                            self.untouchable = True
                            self.form = 'small'
                            self.fire = False
                            self.rect.height = 50
                        else:
                            if not self.star:
                                self.dead = True
                            else:
                                hits[0].kill()
                                play('kick', 0, vol2)
                                points_count += 100
                                Points(points, all_sprites, 100, hits[0].rect.x + hits[0].rect.width // 2,
                                       hits[0].rect.y)
            if group == cannons and hits[0].type == 'bullet':
                if not self.untouchable:
                    if self.form == 'big' and not player.star:
                        self.untouchable = True
                        self.form = 'small'
                        self.fire = False
                        self.rect.height = 50
                    else:
                        if not self.star:
                            self.dead = True

    def collide_platform(self):
        hits = pg.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.y_change > 0 and self.rect.y + self.rect.height <= hits[0].rect.y + hits[0].rect.height:
                self.on_ground = True
                self.y_change = 0
                self.rect.bottom = hits[0].rect.top

    def check_cam(self):
        if self.rect.x + 50 > width - edin * 8:
            self.rect.x = width - edin * 8 - 50
        elif self.rect.x < edin * 8:
            self.rect.x = edin * 9

    def cam(self):
        if self.rect.x + 50 + self.x_change > width - edin * 8 or self.rect.x + self.x_change < edin * 8:
            self.change_all_sprites_except_player()
        else:
            self.rect.x += self.x_change

    def change_all_sprites_except_player(self):
        for sprite in all_sprites:
            sprite.rect.x -= self.x_change
            if sprite.type == 'part':
                sprite.x -= self.x_change

    def check_collied(self, direction, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if direction == 'y':
                if self.y_change > 0:
                    self.on_ground = True
                    self.y_change = 0
                    self.rect.bottom = hits[0].rect.top
                elif self.y_change < 0:
                    self.on_ground = False
                    self.rect.top = hits[0].rect.bottom
                    self.y_change = 0
                    if hits[0].type != 'platform' and self.form == 'small':
                        hits[0].animate()
                        play('bump', 0, vol2)
                    if self.form == 'big' and (('brick' in hits[0].type and current_level != 4) or
                                               (current_level == 4 and hits[0].type == 'brick')):
                        Particles(particles, all_sprites, -10, hits[0].rect.x, hits[0].rect.y, -5, 0, hits[0].type)
                        Particles(particles, all_sprites, -10, hits[0].rect.x + 50, hits[0].rect.y, 5, 1, hits[0].type)
                        Particles(particles, all_sprites, 0, hits[0].rect.x + 50, hits[0].rect.y + 50, 5, 2,
                                  hits[0].type)
                        Particles(particles, all_sprites, 0, hits[0].rect.x, hits[0].rect.y + 50, -5, 3, hits[0].type)
                        hits[0].kill()
                        play('smash', 0, 1)
                    elif hits[0].type == 'random':
                        hits[0].animate()
                        play('bump', 0, vol2)
                        hits[0].update()
                        if hits[0].event_finish and not hits[0].is_busy:
                            if hits[0].item_type == 'coin':
                                Coin(item_sprites, all_sprites, hits[0].rect.x, hits[0].rect.y)
                                hits[0].counter_coin -= 1
                                if hits[0].counter_coin == 0:
                                    hits[0].is_busy = True
                                    hits[0].image = instead
                            else:
                                if hits[0].item_type is not None:
                                    Item(item_sprites, all_sprites, hits[0].rect.x, hits[0].rect.y,
                                         hits[0].item_type, True)
                                hits[0].is_busy = True
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                elif self.x_change < 0:
                    self.rect.left = hits[0].rect.right

    def collide_coin(self):
        global points_count
        hits = pg.sprite.spritecollide(self, coin_sprites, False)
        if hits and not hits[0].Animate:
            play('coin', 0, vol2)
            hits[0].counter = 0
            hits[0].Animate = True
            points_count += 1000

    def Axe(self):
        hits = pg.sprite.spritecollide(self, axe, False)
        if hits and not self.axe:
            stop('bowser')
            play('end', 0, vol2)
            self.axe = True
            self.x_change = 0
            self.moving = False
            hits[0].kill()

    def Was_Biten(self):
        hits = pg.sprite.spritecollide(self, bites, False)
        if hits and self.form != 'big' and not self.untouchable and not self.star:
            self.dead = True
        elif hits and self.form == 'big' and not self.star:
            self.untouchable = True
            self.form = 'small'
            player.rect.height = 50
            self.fire = False

    def Was_Firebarred(self):
        hits = pg.sprite.spritecollide(self, firebar, False)
        if hits and self.form != 'big' and not self.untouchable and not self.star:
            self.dead = True
        elif hits and self.form == 'big' and not self.star:
            self.untouchable = True
            self.form = 'small'
            player.rect.height = 50
            self.fire = False

    def check_death(self):
        if self.rect.y + 50 >= height:
            self.dead = True

    def enemy_kill(self, direction):
        global points_count
        hits = pg.sprite.spritecollide(self, enemy_group, False)
        if hits:
            if direction == 'y':
                if self.y_change > 0:
                    if not hits[0].Dead and not self.dead:
                        if self.star:
                            hits[0].Animate = True
                            hits[0].Dead = True
                            play('kick', 0, vol2)
                            point = Points(points, all_sprites, 100, hits[0].rect.x + hits[0].rect.width // 2,
                                           hits[0].rect.y)
                            points_count += 100
                        elif not self.untouchable:
                            hits[0].Dead = True
                            play('kill', 0, vol2)
                            points_count += 100
                            Points(points, all_sprites, 100, hits[0].rect.x + hits[0].rect.width // 2,
                                   hits[0].rect.y)
                            self.y_change = -8
                    elif hits[0].Dead and (hits[0].type == 'koopa' or hits[0].type == 'beetle') and not self.on_ground:
                        if hits[0].state == '':
                            hits[0].rush()
                    elif hits[0].type == 'fly':

                        if not hits[0].Dead:
                            play('kick', 0, vol2)
                            Points(points, all_sprites, 100, hits[0].rect.x + hits[0].rect.width // 2,
                                   hits[0].rect.y)

                        hits[0].Animate = True
                        hits[0].Dead = True
                        hits[0].animate()
                else:
                    if not hits[0].Dead and not self.star and not self.untouchable:
                        self.dead = True
            if direction == 'x':
                if not hits[0].Dead:
                    if self.star:
                        hits[0].Animate = True
                        hits[0].Dead = True
                        play('kick', 0, vol2)
                        Points(points, all_sprites, 100, hits[0].rect.x + hits[0].rect.width // 2,
                               hits[0].rect.y)
                        points_count += 100
                    elif self.form == 'big' and not self.star:
                        self.untouchable = True
                        self.form = 'small'
                        self.fire = False
                        player.rect.height = 50
                    else:
                        if not self.untouchable:
                            hits[0].Dead = False
                            self.dead = True

    def collide_item(self):
        global points_count
        hits = pg.sprite.spritecollide(self, item_sprites, False)
        if hits:
            if hits[0].type == 'coin':
                pass
            elif not hits[0].izanimate:
                hits[0].kill()
                play('powerup', 0, vol2)
                hits[0].new_event()
                point = Points(points, all_sprites, 1000, hits[0].rect.x + hits[0].rect.width // 2, hits[0].rect.y)
                points_count += 1000


class Item(pg.sprite.Sprite):
    def __init__(self, item_sprites, all_sprites, x_pos, y_pos, type, animate):
        super().__init__(item_sprites, all_sprites)
        self.x = x_pos
        self.y = y_pos
        self.type = type
        self.width = edin - 10
        self.height = edin - 10
        if self.type == 'size':
            self.image = sizeup
            play('appears', 0, vol2)
        elif self.type == 'speed':
            self.image = speedup[0]
            play('appears', 0, vol2)
        elif self.type == 'balls':
            self.image = flower[0]
            play('appears', 0, vol2)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.y_change = 0
        self.gravity = 0.25
        self.direction = ' right'
        self.x_change = 3
        self.animate = animate
        self.counter = 45
        self.animation_counter = 0
        if self.animate:
            self.y_change = - 1
            self.izanimate = True
            self.animate = False
        else:
            self.izanimate = False

    def update(self):
        if self.izanimate:
            if self.counter >= 0:
                self.rect.y += self.y_change
                self.counter -= 1
            else:
                self.izanimate = False
        else:
            if self.type != 'balls' and not self.izanimate:
                self.move()
                self.check_collide('y', block_sprites)
                self.check_collide('y', pipe_sprites)
                self.check_collide('x', block_sprites)
                self.check_collide('x', pipe_sprites)
            if self.type == 'balls':
                self.animation_counter += 0.125
                if self.animation_counter >= 4:
                    self.animation_counter = 0
                self.image = flower[int(self.animation_counter)]
            elif self.type == 'speed':
                self.animation_counter += 0.125
                if self.animation_counter >= 4:
                    self.animation_counter = 0
                self.image = speedup[int(self.animation_counter)]

    def move(self):
        self.rect.y += 9
        self.rect.x += self.x_change

    def check_collide(self, direction, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if direction == 'y':
                if self.rect.y < hits[0].rect.y:
                    self.rect.bottom = hits[0].rect.top
            elif direction == 'x':
                if self.rect.x < hits[0].rect.x:
                    self.rect.right = hits[0].rect.left
                else:
                    self.rect.left = hits[0].rect.right
                self.x_change = - self.x_change

    def new_event(self):
        player.time = 10
        if self.type == 'speed':
            if not player.star:
                stop('theme' + str(current_level))
                play('star', 0, vol1)
            player.speed = 5
            player.jumpspeed = -edin / 3.2
            pg.time.set_timer(pg.USEREVENT, 1000)
            player.speed_time = 10
            player.star = True
        elif self.type == 'size':
            player.form = 'big'
            player.counter = 0
            if player.facing == 'right':
                player.image = right_jump1
            else:
                player.image = left_jump1
            player.get_rect()
            pg.time.set_timer(pg.USEREVENT, 1000)
        elif self.type == 'balls':
            player.fire = True


class Block(pg.sprite.Sprite):
    def __init__(self, real_sprites, block_sprites, all_sprites, x_pos, y_pos, image, type):
        super().__init__(real_sprites, block_sprites, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x_pos
        self.y = y_pos
        self.rect.x = self.x
        self.rect.y = self.y
        self.gravity = 0.5
        self.jump = -3
        self.y_change = 0
        self.move = False
        self.type = type
        self.events = ['size', 'balls', 'speed', 'coin', 'coin', 'coin']
        self.event_finish = False
        self.counter_coin = randrange(3, 5)
        self.is_busy = False
        self.item_type = ''
        self.counter = 0

    def update(self):
        if self.move:
            if self.type == 'random':
                self.new_event()
            if self.type == 'brick' or self.type == 'random':
                if self.y_change < 3:
                    self.y_change += self.gravity
                    self.rect.y += self.y_change
                else:
                    self.move = False
            hits = pg.sprite.spritecollide(self, enemy_group, False)
            if hits:
                if not hits[0].Dead:
                    global points_count
                    point = Points(points, all_sprites, 100, hits[0].rect.x + hits[0].rect.width // 2,
                                   hits[0].rect.y)
                    points_count += 300
                    play('kick', 0, vol2)
                    hits[0].Dead = True
                    hits[0].Animate = True
        else:
            self.omg()

    def animate(self):
        self.y_change = self.jump
        self.move = True

    def omg(self):
        self.rect.y = self.y
        if self.type == 'random' and (not self.event_finish or (self.item_type == 'coin' and self.counter_coin != 0)):
            self.counter += 0.1
            if self.counter >= 5:
                self.counter = 0
            self.image = random_animations[int(self.counter)]

    def new_event(self):
        if not self.event_finish:
            a = choice(self.events)
            self.event = ['']
            self.item_type = a
            self.event_finish = True
            if a != 'coin':
                self.image = instead


class Pipes(pg.sprite.Sprite):
    def __init__(self, real_sprites, all_sprites, x_pos, y_pos, image):
        super().__init__(real_sprites, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x_pos
        self.y = y_pos
        self.rect.x = self.x
        self.rect.y = self.y
        self.type = 'pipe'


class Axe(pg.sprite.Sprite):
    def __init__(self, axe, all_sprites, x_pos, y_pos):
        super().__init__(axe, all_sprites)
        self.counter = 0
        self.image = axe_images[int(self.counter)]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.y_change = -12
        self.gravity = 0.5
        self.type = ''

    def update(self):
        self.counter += 0.125
        if self.counter >= 3:
            self.counter = 0
        self.image = axe_images[int(self.counter)]


class Coin(pg.sprite.Sprite):
    def __init__(self, coin_sprites, all_sprites, x_pos, y_pos):
        super().__init__(coin_sprites, all_sprites)
        self.counter = 0
        self.image = images[int(self.counter)]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.y_change = -12
        self.Animate = False
        self.gravity = 0.5
        self.type = 'coin'

    def update(self):
        if not self.Animate:
            self.counter += 0.125
        else:
            self.counter += 1
        if self.counter >= 8:
            self.counter = 0
        self.image = images[int(self.counter)]
        self.check_collide()
        self.animate()

    def check_collide(self):
        global points_count
        hits = pg.sprite.spritecollide(self, block_sprites, False)
        if hits:
            if not self.Animate:
                play('coin', 0, vol2)
                points_count += 1000
            self.Animate = True

    def animate(self):
        if self.Animate:
            self.rect.y += self.y_change
            self.y_change += self.gravity
        if self.rect.y >= height:
            self.kill()


class Decorations(pg.sprite.Sprite):
    def __init__(self, decorarions, all_sprites, x_pos, y_pos, image):
        super().__init__(decorarions, all_sprites)
        self.x = x_pos
        self.y = y_pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.type = ''


class Castle(pg.sprite.Sprite):
    def __init__(self, castle, all_sprites, x_pos, y_pos, image):
        super().__init__(castle, all_sprites)
        self.x = x_pos
        self.y = y_pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.counter = 45
        self.type = ''

    def update(self):
        global fireworks_count
        if player.end and fireworks_count != 0:
            self.counter -= 1
            if self.counter <= 0:
                fireworks_count -= 0.5
                Fireworks(fireball_sprites, all_sprites,
                          randrange(self.rect.x, self.rect.x + self.rect.width),
                          randrange(100, self.rect.y))
                play('boom', 0, vol2)
                self.counter = 45


class Flag1(pg.sprite.Sprite):
    def __init__(self, flag, all_sprites, x_pos, y_pos, image):
        super().__init__(flag, all_sprites)
        self.x = x_pos
        self.y = y_pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.type = 'flag1'

    def update(self):
        self.check_collide()

    def check_collide(self):
        hits = pg.sprite.spritecollide(self, player_group, False)
        if hits:
            player.rect.x += 10
            for sprite in flag:
                if not player.animate:
                    player.animate = True
                    player.x_change = 0
                    player.y_change = 0
                if sprite.type == 'flag2':
                    if not sprite.animate:
                        sprite.animate = True
                        stop('star')
                        stop('theme' + str(current_level))
                        play('flag', 0, vol2)


class Flag2(pg.sprite.Sprite):
    def __init__(self, flag, all_sprites, x_pos, y_pos, image):
        super().__init__(flag, all_sprites)
        self.x = x_pos
        self.y = y_pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.type = 'flag2'
        self.animate = False
        self.y_change = 5
        self.f = False

    def update(self):
        if self.animate:
            if self.rect.y <= height - 200:
                self.rect.y += self.y_change
            else:
                if not self.f:
                    global points_count
                    point = Points(points, all_sprites, 1000, player.rect.x + player.rect.width, self.rect.y - 250)
                    points_count += 1000
                    self.f = True
                    play('end', 0, vol2)
                if player.animate:
                    player.speed = 3
                    player.x_change = player.speed
                    player.moving = True
                    player.animate = False


class Fireworks(pg.sprite.Sprite):
    def __init__(self, fireballs, all_sprites, x_pos, y_pos):
        super().__init__(fireballs, all_sprites)
        self.image = boom_balls[0]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.counter = 0
        self.type = ''

    def update(self):
        self.counter += 0.125
        if self.counter >= 3:
            self.kill()
        self.image = boom_balls[int(self.counter) - 1]


class Winner_Flag(pg.sprite.Sprite):
    def __init__(self, flag, all_sprites, x_pos, y_pos, image):
        super().__init__(flag, all_sprites)
        self.x = x_pos
        self.y = y_pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.type = 'flag3'
        self.animate = False
        self.y_change = -1

    def update(self):
        if self.animate:
            if self.rect.y >= height - edin * 8:
                self.rect.y += self.y_change
        else:
            if player.end:
                self.animate = True


class Fireball(pg.sprite.Sprite):
    def __init__(self, fireball_sprites, all_sprites, x_pos, y_pos, direction):
        super().__init__(fireball_sprites, all_sprites)
        self.x = x_pos
        self.y = y_pos
        self.counter = 0
        self.image = running_balls[int(self.counter)]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 12
        self.y_change = 0
        self.gravity = 1
        self.direction = direction
        self.boom = False
        if self.direction == 'right':
            self.x_change = self.speed
        else:
            self.x_change = -self.speed
        self.type = ''

    def update(self):
        if self.rect.right < 0 or self.rect.left > width:
            self.boom = True
            self.kill()
        if not self.boom:
            if self.y_change <= 10:
                self.y_change += self.gravity
            self.rect.y += self.y_change
            self.check_collide('y', block_sprites)
            self.check_collide('y', pipe_sprites)
            self.collide_boss()
            self.counter += 0.15
            if self.counter >= 4:
                self.counter = 0
            self.image = running_balls[int(self.counter)]
            self.rect.x += self.x_change
            self.check_collide('x', block_sprites)
            self.check_collide('x', pipe_sprites)
            self.collide_enemy(enemy_group)
            self.collide_enemy(hammer_koopa)
            self.collide_enemy(hedgehogs)
            self.collide_enemy(latitu)
            self.collide_boss()
        else:
            self.counter += 0.125
            if self.counter >= 3:
                self.kill()
                self.counter = 0
            self.image = boom_balls[int(self.counter)]

    def check_collide(self, direction, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if direction == 'y':
                self.y_change = -10
                self.rect.bottom = hits[0].rect.top
            elif direction == 'x':
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                else:
                    self.rect.left = hits[0].rect.right
                self.boom = True
                play('bump', 0, vol2)
                self.counter = 0

    def collide_enemy(self, group):
        global points_count
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            if group == enemy_group:
                self.counter = 0
                if not hits[0].Animate and hits[0].type != 'beetle':
                    hits[0].Animate = True
                    hits[0].need_to_update = True
                    play('kick', 0, vol2)
                    points_count += 150
                    Points(points, all_sprites, 150, hits[0].rect.x + hits[0].rect.width // 2, hits[0].rect.y)
                    self.boom = True
                elif hits[0].type == 'beetle':
                    self.boom = True
                    play('bump', 0, vol2)
                elif hits[0].type == 'fly':
                    self.boom = True
                    if not hits[0].Dead:
                        play('kick', 0, vol2)
                        Points(points, all_sprites, 100, hits[0].rect.x + hits[0].rect.width // 2,
                               hits[0].rect.y)

                    hits[0].Animate = True
                    hits[0].Dead = True
                    hits[0].animate()
            if group == hammer_koopa or group == hedgehogs or group == latitu:
                if not hits[0].dead:
                    self.counter = 0
                    points_count += 150
                    Points(points, all_sprites, 150, hits[0].rect.x + hits[0].rect.width // 2, hits[0].rect.y)
                    hits[0].dead = True

    def collide_boss(self):
        hits = pg.sprite.spritecollide(self, Boss, False)
        if hits:
            if not self.boom:
                hits[0].hp -= 1
            self.boom = True
            self.counter = 0
            play('kick', 0, vol2)


class Invisable_Block(pg.sprite.Sprite):
    def __init__(self, block_sprites, all_sprites, x_pos, y_pos):
        super().__init__(block_sprites, all_sprites)
        self.image = pg.Surface((edin, edin))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.type = ''


class BowserFire(pg.sprite.Sprite):
    def __init__(self, fireball_sprites, all_sprites, x_pos, y_pos):
        super().__init__(fireball_sprites, all_sprites)
        self.image = left_images[0]
        self.x_change = -3
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.counter = 0
        self.sec = 0
        self.type = ''

    def update(self):
        self.counter += 0.125
        self.sec += 0.1
        if self.counter >= 2:
            self.counter = 0
        self.image = left_images[int(self.counter)]
        self.rect.x += self.x_change
        self.collide(block_sprites)
        self.collide(player_group)
        if self.sec > 22:
            self.kill()

    def collide(self, group):
        hits = pg.sprite.spritecollide(self, group, False)
        if hits:
            self.kill()
            if group == player_group:
                if player.form != 'big' and not player.untouchable and not player.star:
                    player.dead = True
                    game_over()
                elif hits and player.form == 'big' and not player.star:
                    player.untouchable = True
                    player.form = 'small'
                    player.rect.height = 50
                    player.fire = False


class Bowser(pg.sprite.Sprite):
    def __init__(self, Boss, all_sprites, x_pos, y_pos):
        super().__init__(Boss, all_sprites)
        self.image = left[0]
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.counter = 0
        self.y_change = 0
        self.jumpspeed = -edin / 3.8
        self.speed = 2
        self.x_change = -self.speed
        self.gravity = 0.5
        self.on_ground = False
        self.cooldown = 340
        self.jump_cooldown = 300
        self.dead = False
        self.hp = 5
        self.firetimer = 100
        self.steps = 70
        self.stepsold = self.steps
        self.attack_hammer_timer = 30
        self.attack_count = 5
        self.type = ''

    def update(self):
        if 0 <= self.rect.x <= width:
            self.check_collide('y')
            if not player.axe:
                self.rect.x += self.x_change
            self.check_collide('x')
            self.counter += 0.1
            if self.counter >= 4:
                self.counter = 0
            self.image = left[int(self.counter)]
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.cooldown = 0
                if self.attack_hammer_timer <= 0 and self.attack_count >= 0:
                    Hammer(Hammers, all_sprites, self.rect.x - edin // 2, self.rect.y, -3)
                    play('hammer', 0, vol2)
                    self.attack_hammer_timer = 30
                    self.attack_count -= 1
                if self.attack_count == 5 and self.attack_hammer_timer == 30:
                    play('roar', 0, vol2)
                self.firetimer = 100
                self.attack_hammer_timer -= 1
                if self.attack_count == 0:
                    self.cooldown = 340
                    self.attack_count = 5
            self.jump_cooldown -= 1
            self.firetimer -= 1
            if self.firetimer <= 40 and self.jump_cooldown <= 0:
                self.jump_cooldown = 300
                if self.on_ground:
                    self.jump()
            if self.firetimer <= 0:
                BowserFire(fireball_sprites, all_sprites, self.rect.x, self.rect.y)
                self.firetimer = 100
                play('fire', 0, vol2)
            self.collide_player()
            if self.hp == 0:
                self.dead = True
                self.kill()
            self.steps -= 1
            if self.steps == 0:
                self.x_change = -self.x_change
                self.steps = self.stepsold
            self.y_change += self.gravity
            self.rect.y += self.y_change
            if self.rect.y >= edin * 13:
                play('fall', 0, vol2)
                self.kill()

    def jump(self):
        self.y_change = self.jumpspeed
        self.on_ground = False

    def check_collide(self, direction):
        hits = pg.sprite.spritecollide(self, block_sprites, False)
        if hits:
            if direction == 'y':
                if self.y_change > 0:
                    self.rect.bottom = hits[0].rect.top
                    self.y_change = 0
                    self.on_ground = True
                elif self.y_change < 0:
                    self.rect.top = hits[0].rect.bottom
            if direction == 'x':
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                    self.x_change = -self.speed
                elif self.x_change < 0:
                    self.rect.left = hits[0].rect.right
                    self.x_change = self.speed

    def collide_player(self):
        hits = pg.sprite.spritecollide(self, player_group, False)
        if hits:
            hits[0].dead = True


class Platform(pg.sprite.Sprite):
    def __init__(self, platforms, all_sprites, x_pos, y_pos):
        super().__init__(platforms,  all_sprites)
        self.image = platform
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.type = 'platform'


class Lava(pg.sprite.Sprite):
    def __init__(self, bites, all_sprites, x_pos, y_pos, lava1=False):
        super().__init__(bites,  all_sprites)
        self.lava1 = lava1
        self.image = bite_images[0]
        self.rect = self.image.get_rect()
        if self.lava1:
            self.image = lava
            self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.state = "up"
        self.y_change = -18
        self.gravity = 0.4
        self.type = ''

    def update(self):
        if not self.lava1:
            if self.state == 'up':
                self.image = bite_images[0]
            elif self.state == 'down':
                self.image = bite_images[1]
            self.rect.y += self.y_change
            self.y_change += self.gravity
            if self.rect.y >= height:
                self.y_change = -18
            if self.y_change < 0:
                self.state = 'up'
            elif self.y_change >= 0:
                self.state = 'down'


def new_game(level):
    global player, Level
    all_sprites.empty()
    player_group.empty()
    block_sprites.empty()
    decorations.empty()
    enemy_group.empty()
    item_sprites.empty()
    mountain_and_clouds.empty()
    pipe_sprites.empty()
    koopa_sprites.empty()
    goomba_sprites.empty()
    particles.empty()
    points.empty()
    flag.empty()
    castle.empty()
    fireball_sprites.empty()
    Boss.empty()
    coin_sprites.empty()
    plants.empty()
    platforms.empty()
    temp.empty()
    bites.empty()
    bridge.empty()
    axe.empty()
    Hammers.empty()
    hammer_koopa.empty()
    hedgehogs.empty()
    latitu.empty()
    cannons.empty()
    extra_blocks.empty()
    firebar.empty()
    refresh()
    if current_level == 4:
        player = Player(player_group, edin * 7, height / 2, mode)
    else:
        player = Player(player_group, edin * 7, height - edin * 3, mode)
    for i, j in enumerate(level):
        for a, b in enumerate(j):
            if b == '#':
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin, skin('ground'), '')
            elif b == 'b':
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin, skin('brick'), 'brick')
            elif b == 'w':
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin,
                      skin('bowser_brick'), 'b_brick')
            elif b == 'W':
                Lava(bites, all_sprites, int(a) * edin, int(i) * edin)
            elif b == 's':
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin, skin('stone'), '')
            elif b == 'r':
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin, skin('random'), 'random')
            elif b == 'u':
                Pipes(pipe_sprites, all_sprites, int(a) * edin, int(i) * edin,
                      skin('pipes/pipeup', (edin * 2, edin * 2)))
            elif b == 'p':
                Pipes(pipe_sprites, all_sprites, int(a) * edin, int(i) * edin, skin('pipes/pipe', (edin * 2, edin)))
            elif b == 'c':
                Coin(coin_sprites, all_sprites, int(a) * edin + 5, int(i) * edin + 5)
            elif b == 'g':
                Goomba(goomba_sprites, all_sprites, int(a) * edin, int(i) * edin)
            elif b == 'k':
                Koopa(enemy_group, koopa_sprites, all_sprites, int(a) * edin, int(i) * edin, 'koopa')
            elif b == 'n':
                Koopa(enemy_group, koopa_sprites, all_sprites, int(a) * edin, int(i) * edin, 'fly')
            elif b == 'O':
                Koopa(enemy_group, koopa_sprites, all_sprites, int(a) * edin, int(i) * edin, 'beetle')
            elif b == '!':
                Decorations(mountain_and_clouds, all_sprites, int(a) * edin, int(i) * edin + edin // 2,
                            skin('another/small_mountain', (edin * 3, edin * 1.5)))
            elif b == '@':
                Decorations(mountain_and_clouds, all_sprites, int(a) * edin, int(i) * edin + edin // 2,
                            skin('another/big_mountain', (edin * 5, edin * 2.5)))
            elif b == 'o':
                Decorations(mountain_and_clouds, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/one_cloud', (edin * 2, edin * 1.5)))
            elif b == '0':
                Decorations(mountain_and_clouds, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/two_clouds', (edin * 3, edin * 1.5)))
            elif b == 'i':
                Decorations(mountain_and_clouds, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/three_clouds', (edin * 4, edin * 1.5)))
            elif b == '1':
                Decorations(decorations, all_sprites, int(a) * edin, int(i) * edin, skin('another/single_fense'))
            elif b == '2':
                Decorations(decorations, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/double_fense', (edin * 2, edin)))
            elif b == 'w':
                Decorations(decorations, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/high_tree', (edin * 2, edin * 4)))
            elif b == 'L':
                Decorations(decorations, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/low_tree', (edin, edin * 2)))
            elif b == 't':
                Decorations(decorations, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/bush', (edin * 2, edin)))
            elif b == 'v':
                Decorations(decorations, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/bush2', (edin * 3, edin)))
            elif b == 'T':
                Decorations(decorations, all_sprites, int(a) * edin, int(i) * edin,
                            skin('another/bush3', (edin * 4, edin)))
            elif b == 'K':
                Castle(castle, all_sprites, int(a) * edin, int(i) * edin, skin('castle/castle', (edin * 5, edin * 5)))
                Winner_Flag(flag, all_sprites, int(a + 2) * edin, int(i + 1) * edin, skin('winner_flag'))
            elif b == 'Z':
                Castle(castle, all_sprites, int(a) * edin, int(i) * edin,
                       skin('castle/castle_big', (edin * 8, edin * 8)))
            elif b == 'e':
                Invisable_Block(block_sprites, all_sprites, int(a) * edin, int(i) * edin)
            elif b == 'F':
                Invisable_Block(inviase, all_sprites, int(a) * edin, int(i) * edin)
            elif b == 'j':
                Pipes(pipe_sprites, all_sprites, int(a) * edin, int(i - 1) * edin,
                      skin('pipes/left', (edin * 4, edin * 2)))
                Invisable_Block(inviase, all_sprites, int(a) * edin, int(i) * edin)
            elif b == 'f':
                Flag1(flag, all_sprites, int(a) * edin + 12, (int(i) + 0.5) * edin,
                      skin('flag1', (edin * 0.5, edin * 10.5)))
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin * 11, skin('stone'), '')
                Flag2(flag, all_sprites, int(a) * edin - edin / 2, (int(i) + 1) * edin, skin('flag2'))
            elif b == 'B':
                Bowser(Boss, all_sprites, int(a) * edin, int(i) * edin)
            elif b == 'P':
                Plant(plants, all_sprites, int(a) * edin, int(i) * edin)
            elif b == 'C':
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin,
                      skin('mushrooms/lily_centre'), '')
                Decorations(decorations, all_sprites, int(a) * edin, int(i + 1) * edin,
                            skin('mushrooms/lily_base', (edin, edin * 12)))
            elif b == 'l':
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin,
                      skin('mushrooms/lily_left'), '')
            elif b == 'R':
                Block(block_sprites, block_sprites, all_sprites, int(a) * edin, int(i) * edin,
                      skin('mushrooms/lily_right'), '')
            elif b == '*':
                Block(bridge, block_sprites, all_sprites, int(a) * edin, int(i) * edin,
                      skin('castle/bridge'), '')
            elif b == '(':
                Lava(bites, all_sprites, int(a) * edin, int(i) * edin, True)
            elif b == 'A':
                Axe(axe, all_sprites, int(a) * edin, int(i) * edin)
            elif b == '7':
                Decorations(decorations, all_sprites, int(a) * edin, int(i) * edin - 0.5 * edin,
                            skin('castle/princess', (edin, edin * 1.5)))
            elif b == 'h':
                Hammer_Koopa(all_sprites, hammer_koopa, enemy_group, int(a) * edin, int(i) * edin - 0.5 * edin)
            elif b == '&':
                Latitu(all_sprites, latitu, enemy_group, int(a) * edin, int(i) * edin - 0.5 * edin)
            elif b == 'x':
                Cannon(cannons, block_sprites, int(a) * edin, int(i) * edin - edin)
            elif b == '-':
                Platform(all_sprites, platforms, int(a) * edin, int(i) * edin - edin)
            elif b == '3':
                Block(bridge, block_sprites, all_sprites, int(a) * edin, int(i) * edin,
                      skin('castle/bar_base'), '')
                length = edin * 3
                size = edin / 2
                Part(all_sprites, length, int(a) * edin + edin / 2, int(i) * edin + edin / 2)
                Part(all_sprites, length - size, int(a) * edin + edin / 2, int(i) * edin + edin / 2)
                Part(all_sprites, length - size * 2, int(a) * edin + edin / 2, int(i) * edin + edin / 2)
                Part(all_sprites, length - size * 3, int(a) * edin + edin / 2, int(i) * edin + edin / 2)
                Part(all_sprites, length - size * 4, int(a) * edin + edin / 2, int(i) * edin + edin / 2)
                Part(all_sprites, length - size * 5, int(a) * edin + edin / 2, int(i) * edin + edin / 2)


def game_over():
    global Game_over
    stop('all')
    play('death', 0, vol2)
    Game_over = True


def end():
    global points_count, running2, running, mode, records
    temp = 240
    stop('all')
    while running2:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running2 = False
                break
        temp -= 1
        if temp == 0:
            if len(records) < current_level:
                records.append(str(points_count))
            else:
                if points_count > int(records[current_level - 1]):
                    records[current_level - 1] = str(points_count)
            write(7, " ".join(records))
            if current_level != 4:
                mode[(current_level + 1) * 2 - 2] = str(player.form)
                mode[(current_level + 1) * 2 - 1] = str(player.fire)
                write(8, " ".join(mode))
            refresh()
            running2 = False
            break
        screen.fill((0, 0, 0))
        one = pg.transform.scale(font_verylarge.render("LEVEL COMPLETED", True, White), (height / 1.5, height / 10))
        two = pg.transform.scale(font_verylarge.render("LEVEL COMPLETED", True, (0, 0, 0)), (height / 1.5, height / 10))
        screen.blit(two, (two.get_rect(center=(width / 2 + 5, height / 2 + 5))))
        screen.blit(one, (one.get_rect(center=(width / 2, height / 2))))
        pg.display.update()
        clock.tick(fps)
    New_Game()


def pre_start():
    global Level, Game_over, running, fireworks_count, points_count
    stop('menu')
    Game_over = False
    Level = []
    with open(f'data/level{current_level}.txt', 'r') as f:
        for i in f.readlines():
            Level.append(i)
    points_count = 0
    scene_time = 100
    fireworks_count = 4
    run = True
    a = font_medium.render(f'1-{current_level}', True, White)
    if len(records) < current_level:
        record = font_medium.render(f'Record:0', True, White)
    else:
        record = font_medium.render(f'Record:{records[current_level - 1]}', True, White)
    while run:
        screen.fill((0, 0, 0))
        screen.blit(font_verylarge.render('GOOD LUCK', True, White), ((width - 360) / 2, height / 2))
        screen.blit(font_medium.render(name, True, White), (20, 20))
        screen.blit(record, ((width - record.get_width()) / 2, 20))
        screen.blit(font_medium.render('WORLD', True, White), (width - 130, 20))
        screen.blit(font_medium.render(f'1-{current_level}', True, White), (width - 110, 45))
        scene_time -= 1
        if scene_time == 0:
            run = False
            running = True
            new_game(Level)
            main()
            break
        pg.display.update()
        clock.tick(fps)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
    stop("all")
    play("menu", -1, vol1)


def New_Game():
    global Game_over, seconds, points_count, current_level, Level, run, running, screen, running2, name
    pg.display.set_caption('Super Mario Bros.')
    stop("menu")
    play("menu", -1, vol1)
    Game_over = False
    running2 = False
    points_count = 0
    seconds = 400
    decorations.empty()
    mountain_and_clouds.empty()
    block_sprites.empty()
    play_b = Button(width / 2, edin * 8, font_medium.render("Play", True, White))
    sett_b = Button(width / 2, edin * 9, font_medium.render("Settings", True, White))
    exit_b = Button(width / 2, edin * 10, font_medium.render("Exit", True, White))
    nick = font_medium.render(name, True, White)
    if len(records) != 4:
        world = font_medium.render(f'WORLD 1-{str(len(records))}', True, White)
    else:
        world = font_medium.render(f'GAME COMPLETED!', True, White)
    while run:
        screen.fill('#5c94fc')
        screen.blit(skin('bg_ground', (100 * edin, edin * 2)), (0, height - edin * 2))
        screen.blit(skin('name', (height * 0.8, height / 3)), (width / 2 - height * 0.4, height * 0.15))
        screen.blit(mar, (width / 8 - mar.get_width() / 2, height - mar.get_height() - 2 * edin))
        screen.blit(nick, (20, 20))
        screen.blit(world, (width - 20 - world.get_width(), 20))
        if play_b.pressed(screen):
            levels()
            refresh()
            if len(records) != 4:
                world = font_medium.render(f'WORLD 1-{str(len(records))}', True, White)
            else:
                world = font_medium.render(f'GAME COMPLETED!', True, White)
        if sett_b.pressed(screen):
            settings()
            refresh()
            nick = font_medium.render(name, True, White)
            if len(records) != 4:
                world = font_medium.render(f'WORLD 1-{str(len(records))}', True, White)
            else:
                world = font_medium.render(f'GAME COMPLETED!', True, White)
        if exit_b.pressed(screen):
            run = False
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()


def levels():
    global current_level
    locked = 'This level is Locked!'
    not_pl = 'Click to play!'
    curr = font_small.render('Choose level', True, White)
    pos = width / 8
    x = pos
    option = font_small.render('', True, White)
    one_b = Button(pos, height - edin, b1)
    two_b = Button(pos * 3, height - edin, b2)
    three_b = Button(pos * 5, height - edin, b3)
    final_b = Button(pos * 7, height - edin, b4)
    exit = font_medium.render("Exit", True, White)
    exit_b = Button(20 + exit.get_width() / 2, 20 + exit.get_height() / 2, exit)
    lev = len(records)
    op1 = lev + 1
    if len == 1:
        if op1 < 2:
            two_b = Button(pos * 5, height - edin, bl)
        three_b = Button(pos * 5, height - edin, bl)
        final_b = Button(pos * 7, height - edin, bl)
    if lev < 2:
        if op1 < 3:
            three_b = Button(pos * 5, height - edin, bl)
        final_b = Button(pos * 7, height - edin, bl)
    elif lev < 3:
        if op1 < 4:
            final_b = Button(pos * 7, height - edin, bl)
    run = True
    while run:
        screen.fill('#5c94fc')
        screen.blit(skin('bg_ground', (100 * edin, edin * 2)), (0, height - edin * 2))
        screen.blit(skin('nameless', (height * 0.8, height / 3)), (width / 2 - height * 0.4, height * 0.15))
        screen.blit(cas, (width - cas.get_width() / 2 - edin * 2.5, height - cas.get_height() - 2 * edin))
        screen.blit(mar, (x - mar.get_width() / 2, height - mar.get_height() - 2 * edin))
        screen.blit(curr, ((width - curr.get_width()) / 2, edin * 4))
        screen.blit(option, ((width - option.get_width()) / 2, edin * 5))
        if pg.mouse.get_pos()[0] <= pos + edin * 1.5 and pg.mouse.get_pos()[1] >= height - edin * 2:
            if op1 == 1:
                option1 = not_pl
            else:
                option1 = f"Completed! Record:{records[0]}"
            option = font_small.render(option1, True, White)
            curr = font_small.render('Level 1', True, White)
            x = pos
        elif pos * 3 - edin <= pg.mouse.get_pos()[0] <= pos * 3 + edin and pg.mouse.get_pos()[1] >= height - edin * 2:
            if op1 == 1:
                option1 = locked
            elif op1 == 2:
                option1 = not_pl
            else:
                option1 = f"Completed! Record: {records[1]}"
            option = font_small.render(option1, True, White)
            curr = font_small.render('Level 2', True, White)
            x = pos * 3
        elif pos * 5 - edin <= pg.mouse.get_pos()[0] <= pos * 5 + edin and pg.mouse.get_pos()[1] >= height - edin * 2:
            if op1 <= 2:
                option1 = locked
            elif op1 == 3:
                option1 = not_pl
            else:
                option1 = f"Completed! Record: {records[2]}"
            option = font_small.render(option1, True, White)
            curr = font_small.render('Level 3', True, White)
            x = pos * 5
        elif pos * 7 - edin <= pg.mouse.get_pos()[0] and pg.mouse.get_pos()[1] >= height - edin * 2:
            if op1 <= 3:
                option1 = locked
            elif op1 == 4:
                option1 = not_pl
            else:
                option1 = f"Completed! Record: {records[3]}"
            option = font_small.render(option1, True, White)
            curr = font_small.render('Level 4', True, White)
            x = pos * 7
        else:
            if pg.mouse.get_pos()[1] >= height - edin * 2:
                option = font_small.render('', True, White)
                curr = font_small.render('Choose level', True, White)
                x = pg.mouse.get_pos()[0]
        if one_b.pressed(screen):
            current_level = 1
            pre_start()
            refresh()
        if two_b.pressed(screen):
            current_level = 2
            if op1 >= current_level:
                pre_start()
                refresh()
        if three_b.pressed(screen):
            current_level = 3
            if op1 >= current_level:
                pre_start()
                refresh()
        if final_b.pressed(screen):
            current_level = 4
            if op1 >= current_level:
                pre_start()
                refresh()
        if exit_b.pressed(screen):
            run = False
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            run = False


def settings():
    global name, musical, better, sound, vol1, vol2, fullscreen, width, height, edin, screen
    x = width / 2 - height / 3
    y = height / 10
    h = on.get_height() / 4
    exit = font_medium.render("Exit", True, White)
    reset = font_small.render("Reset", True, White)
    double_check = False
    exit_b = Button(20 + exit.get_width() / 2, 20 + exit.get_height() / 2, exit)
    cancel = font_medium.render('Press anywhere to cancel', True, White)
    ch_b = Button(width - x, y * 1.4 + h, change_b)
    if musical == 'Off':
        musical_b = Button(width - x, y * 2.1 + h, off)
    else:
        musical_b = Button(width - x, y * 2.1 + h, on)
    if better == 'Off':
        better_b = Button(width - x, y * 2.8 + h, off)
    else:
        better_b = Button(width - x, y * 2.8 + h, on)
    if sound == 'Off':
        sound_b = Button(width - x, y * 5.1 + h, off)
    else:
        sound_b = Button(width - x, y * 5.1 + h, on)
    if fullscreen == 'Off':
        fullscreen_b = Button(width - x, y * 7.4 + h, off)
    else:
        fullscreen_b = Button(width - x, y * 7.4 + h, on)
    reset_b = Button(20 + reset.get_width() / 2, height - edin * 2.3, reset)
    text = name
    nick = font_medium.render(name, True, White)
    rect = nick.get_rect(topleft=(x, y * 1.4))
    cursor = pg.Rect(rect.topright, (3, rect.height))
    one = Point(width / 2 + y / 2, y * 4.5, 3)
    two = Point(width / 2 + y / 2, y * 6.8, 5)
    run = True
    pr = False
    refresh()
    while run:
        screen.fill('#5c94fc')
        screen.blit(skin('nameless', (height * 0.8, height / 1.4)), (width / 2 - height * 0.4, height * 0.1))
        screen.blit(skin('bg_ground', (100 * edin, edin * 2)), (0, height - edin * 2))
        screen.blit(nick, (x, y * 1.4))
        screen.blit(font_medium.render('Music', True, White), (x, y * 2.1))
        screen.blit(font_medium.render('Improved sounds', True, White), (x, y * 2.8))
        screen.blit(font_medium.render('Volume', True, White), (x, y * 3.5))
        screen.blit(font_medium.render('Sounds', True, White), (x, y * 5.1))
        screen.blit(font_medium.render('Volume', True, White), (x, y * 5.8))
        screen.blit(font_medium.render('Fullscreen', True, White), (x, y * 7.4))
        one.update()
        two.update()
        if (width != m_width and fullscreen == "On") or (width == m_width and fullscreen == "Off"):
            screen.blit(font_mediumsmall.render("You need to restart the game to change some settings", True, White),
                        (10, height - edin * 0.5))
        if pr:
            screen.blit(cancel, (width - cancel.get_width() - 10, 10))
            if time.time() % 1 > 0.5:
                pg.draw.rect(screen, White, cursor)
        if pg.mouse.get_pressed()[0] == 1 and pr and not ch_b.rect.collidepoint(pg.mouse.get_pos()):
            if sound == "On":
                play("switched", 0, vol2)
            pr = False
            ch_b = Button(width - x, y * 1.4 + h, change_b)
            text = name
            nick = font_medium.render(text, True, White)
            rect.size = nick.get_size()
            cursor.topleft = rect.topright
        if ch_b.pressed(screen):
            if sound == "On":
                play("switched", 0, vol2)
            if pr:
                ch_b = Button(width - x, y * 1.4 + h, change_b)
                pr = False
                rect.size = nick.get_size()
                cursor.topleft = rect.topright
                write(0, text)
            else:
                ch_b = Button(width - x, y * 1.4 + h, on)
                pr = True
        if reset_b.pressed(screen):
            if not double_check:
                reset = font_small.render("Press again to reset data", True, (255, 0, 0))
                reset_b = Button(20 + reset.get_width() / 2, height - edin * 2.3, reset)
                double_check = True
            else:
                write(0, 'Mario')
                write(7, '100')
                write(8, 'small False small False small False small False')
                refresh()
                run = False
        if musical_b.pressed(screen):
            if sound == "On":
                play("switched", 0, vol2)
            musical = "On" if musical == "Off" else "Off"
            write(1, musical)
            refresh()
            if musical == "On":
                musical_b = Button(width - x, y * 2.1 + h, on)
                play('menu', -1, vol1)
            else:
                musical_b = Button(width - x, y * 2.1 + h, off)
                stop('menu')
        if better_b.pressed(screen):
            if sound == "On":
                play("switched", 0, vol2)
            if better == "Off":
                better_b = Button(width - x, y * 2.8 + h, on)
            else:
                better_b = Button(width - x, y * 2.8 + h, off)
            stop("menu")
            better = "On" if better == "Off" else "Off"
            write(2, better)
            refresh()
            play("menu", -1, vol1)
        if sound_b.pressed(screen):
            if sound == "On":
                play("switched", 0, vol2)
            if sound == "Off":
                sound_b = Button(width - x, y * 5.1 + h, on)
            else:
                sound_b = Button(width - x, y * 5.1 + h, off)
            sound = "On" if sound == "Off" else "Off"
            write(4, sound)
            refresh()
        if fullscreen_b.pressed(screen):
            if sound == "On":
                play("switched", 0, vol2)
            if fullscreen == "Off":
                fullscreen_b = Button(width - x, y * 7.4 + h, on)
            else:
                fullscreen_b = Button(width - x, y * 7.4 + h, off)
            fullscreen = "On" if fullscreen == "Off" else "Off"
            write(6, fullscreen)
        if exit_b.pressed(screen):
            run = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            one.press(event)
            two.press(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if not pr:
                        run = False
                    else:
                        pr = False
                elif event.key == pg.K_BACKSPACE and pr:
                    if len(text) > 0:
                        text = text[:-1]
                        nick = font_medium.render(text, True, White)
                elif len(text) < 20 and pr:
                    text += event.unicode
                    nick = font_medium.render(text, True, White)
        if pr:
            rect.size = nick.get_size()
            cursor.topleft = rect.topright
        pg.display.update()


def main():
    global player, curr, text_surface
    temp = 240
    global running, seconds, running2, running_scene, Level
    play('theme' + str(current_level), -1, vol1)
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN:
                if e.key == 100:
                    player.keyD = True
                elif e.key == 97:
                    player.keyA = True
                elif e.key == 115:
                    if player.form == 'big' and player.on_ground and not player.keySpace:
                        player.rect.height = edin
                        player.rect.y += edin
                        player.keyS = True
                elif e.key == 1073742048:
                    player.keyCtrl = True
                elif e.key == 32:
                    if not player.keyS:
                        player.keySpace = True
                elif e.key == 27:
                    start_time = time.time()
                    text_surface = quit_font.render("QUITTING", True, White)
            elif e.type == pg.KEYUP:
                if e.key == 100:
                    player.keyD = False
                elif e.key == 97:
                    player.keyA = False
                elif e.key == 115:
                    if player.form == 'big' and player.keyS:
                        player.rect.height = 1.6 * edin
                        player.rect.y -= edin * 0.6
                        player.keyS = False
                elif e.key == 119:
                    player.keyW = False
                elif e.key == 1073742048:
                    player.keyCtrl = False
                    player.f_flag = False
                elif e.key == 32:
                    player.keySpace = False

            elif e.type == pg.USEREVENT:
                if not Game_over:
                    if player.star:
                        player.speed_time -= 1
                    if player.speed_time == 0 and player.star:
                        stop('star')
                        player.speed = 4
                        player.jumpspeed = -edin / 3.4
                        player.speed_time = 0
                        player.star = False
                        if not player.animate:
                            play('theme' + str(current_level), -1, vol1)
        if current_level == 2 or current_level == 4:
            screen.fill((0, 0, 0))
        else:
            screen.fill('#5c94fc')
        mountain_and_clouds.draw(screen)
        player.update()
        if Game_over:
            temp -= 1
            if temp <= 0:
                running = False
                running_scene = True
                break
        if player.end and seconds > 0:
            seconds -= 1
            if current_level == 4:
                end1 = pg.transform.scale(font_verylarge.render("YOU HAVE RESCUED THE PRINCESS", True, White),
                                          (height / 1.5, height / 10))
                end2 = pg.transform.scale(font_verylarge.render("THANK YOU, BRAVE TRAVELLER!", True, White),
                                          (height / 1.5, height / 10))
                screen.blit(end1, (end1.get_rect(center=(width / 2, height / 3))))
                screen.blit(end2, (end2.get_rect(center=(width / 2, height / 2))))
        if seconds <= 0:
            running = False
            running2 = True
            end()
            break
        for sprite in block_sprites:
            sprite.update()
            if sprite.rect.x <= width and sprite.rect.x + sprite.rect.width >= 0:
                extra_blocks.add(sprite)
        for sprite in coin_sprites:
            sprite.update()
        for sprite in enemy_group:
            if sprite.need_to_update:
                if sprite.killtime > 0 and sprite.rect.y <= height:
                    sprite.update()
                    sprite.need_to_update = True
                    if sprite.type == 'koopa' and sprite.allivetime < 0:
                        if not sprite.sonic:
                            sprite.allivetime = 600
                            if sprite.Dead:
                                sprite.alive()
                else:
                    sprite.kill()
            else:
                if sprite.rect.x + sprite.rect.width >= 0 and sprite.rect.x <= width:
                    sprite.need_to_update = True
        for sprite in item_sprites:
            sprite.update()
        for sprite in flag:
            sprite.update()
        for sprite in plants:
            sprite.update()
        for sprite in Boss:
            sprite.update()
        for sprite in castle:
            sprite.update()
        for sprite in platforms:
            sprite.update()
        for sprite in bites:
            sprite.update()
        for sprite in Hammers:
            sprite.update()
        for sprite in cannons:
            sprite.update()
        for sprite in firebar:
            sprite.update()
        cannons.draw(screen)
        decorations.draw(screen)
        platforms.draw(screen)
        cannonballs.draw(screen)
        flag.draw(screen)
        castle.draw(screen)
        plants.draw(screen)
        Boss.draw(screen)
        pipe_sprites.draw(screen)
        item_sprites.draw(screen)
        extra_blocks.draw(screen)
        firebar.draw(screen)
        extra_blocks.empty()
        coin_sprites.draw(screen)
        enemy_group.draw(screen)
        Hammers.draw(screen)
        pipe_sprites.draw(screen)
        cannons.draw(screen)
        for sprite in axe:
            sprite.update()
        axe.draw(screen)
        for sprite in fireball_sprites:
            sprite.update()
        bites.draw(screen)
        fireball_sprites.draw(screen)
        if player.untouchable:
            ticks = pg.time.get_ticks()
            if ticks % 2 == 0:
                player_group.draw(screen)
        else:
            player_group.draw(screen)
        for sprite in points:
            sprite.update()
        for sprite in particles:
            sprite.update()
        particles.draw(screen)
        points.draw(screen)
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            try:
                text_surface.set_alpha(min(round((time.time() - start_time), 2) * 100, 250))
                screen.blit(text_surface, (width - edin - 150, 10))
                if time.time() - start_time > 1.8:
                    text_surface = quit_font.render("QUITTING...", True, White)
                elif time.time() - start_time > 1.2:
                    text_surface = quit_font.render("QUITTING..", True, White)
                elif time.time() - start_time > 0.6:
                    text_surface = quit_font.render("QUITTING.", True, White)
                if time.time() > start_time + 2:
                    running = False
            except UnboundLocalError:
                start_time = time.time()
        one = font_medium.render(f'points: {points_count}', True, White)
        two = font_medium.render(f'points: {points_count}', True, (0, 0, 0))
        screen.blit(two, (two.get_rect(topleft=(13, 13))))
        screen.blit(one, (one.get_rect(topleft=(10, 10))))
        if Game_over:
            one = pg.transform.scale(font_verylarge.render("GAME OVER", True, White), (height / 1.5, height / 10))
            two = pg.transform.scale(font_verylarge.render("GAME OVER", True, (0, 0, 0)), (height / 1.5, height / 10))
            screen.blit(two, (two.get_rect(center=(width / 2 + 4, height / 2 + 4))))
            screen.blit(one, (one.get_rect(center=(width / 2, height / 2))))
        pg.display.update()
        clock.tick(fps)
    stop("all")
    play("menu", -1, vol1)


New_Game()
