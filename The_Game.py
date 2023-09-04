import pygame, random, anm
from interface import *
from Boss import *
from text import *  # blittext(surface, text, location=[0,0], size=40, color=(0,0,0))


class DogClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("men/body.png")
        self.parts = [
            [pygame.image.load("men/arm.png"), pygame.image.load("men/hand.png")],
            [
                pygame.image.load("men/b_leg.png"),
                pygame.image.load("men/b_foot.png"),
                pygame.image.load("men/leg.png"),
                pygame.image.load("men/foot.png"),
            ],
        ]
        self.anims = {
            "top_stay": anm.top_stay,
            "top_shoot": anm.top_shoot,
            "top_reload": anm.top_reload,
            "bottom_stay": anm.bottom_stay,
            "bottom_walk": anm.bottom_walk,
            "bottom_jump": anm.bottom_jump
        }

        self.anim_lst = [0, 0]
        self.anim_num = [0, 0]
        self.action = ["start", "start"]
        self.max_num = [1, 1]

        self.rect = self.image.get_rect()
        self.location = self.rect.left, self.rect.top = location
        self.rect.width = 48
        self.rect.height = 84
        self.x_vel, self.y_vel = [0, 0]
        self.jump_power = 27
        self.walk_power = 15
        self.power_brake = 5
        self.full_hp = 300  #
        self.hp = self.full_hp
        self.health = HealthClass([50, 50])
        self.gravity = 1
        self.i = 0
        self.onGround = [0, 0, 0, 0]
        self.duration = "right"
        self.win = False

        #    self.gun = GunClass()
        #    self.gun = CattyClass()
        self.gun = AkmClass()

    def move_x(self):
        self.rect.left += self.x_vel

    def move_y(self):
        for d in self.onGround:
            if not d:
                self.y_vel -= self.gravity
                break
        self.rect.top -= self.y_vel

    def collide_x(self):
        for p in platforms:
            if pygame.sprite.spritecollide(p, hero, False):
                if self.x_vel > 0:
                    if p.rect.right > self.rect.right > p.rect.left:
                        self.rect.right = p.rect.left
                if self.x_vel < 0:
                    if p.rect.right > self.rect.left > p.rect.left:
                        self.rect.left = p.rect.right

    def collide_y(self):
        self.onGround[self.i] = 0
        for p in platforms:
            if pygame.sprite.spritecollide(p, hero, False):
                if self.y_vel > 0:
                    if p.rect.bottom > self.rect.top > p.rect.top:
                        self.rect.top = p.rect.bottom
                        self.y_vel = 0
                if self.y_vel < 0:
                    if p.rect.bottom > self.rect.bottom > p.rect.top:
                        self.rect.bottom = p.rect.top
                        self.onGround = [1, 1, 1, 1]
                        self.y_vel = 0

    def collide_packs(self):
        for p in packs:
            if pygame.sprite.spritecollide(p, hero, False):
                if p.gun == "gun":
                    self.gun = GunClass()
                elif p.gun == "akm":
                    self.gun = AkmClass()
                elif p.gun == "hart":
                    self.hp = self.full_hp
                elif p.gun == "cup":
                    self.gun.image = self.gun.left = self.gun.right = p.image
                    self.gun.ammo = self.gun.max_ammo = 0
                    self.win = True
                everybody.remove(p)
                packs.remove(p)

    def anim(self):
        global screen
        if self.duration == "right":
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(
                pygame.transform.flip(self.image, True, False),
                [self.rect.right - self.image.get_width(), self.rect.top],
            )

        for j in [1, 0]:
            for i in range(len(self.parts[j])):
                if self.duration == "right":
                    screen.blit(
                        pygame.transform.rotate(
                            self.parts[j][i], self.anim_lst[j][self.anim_num[j]][i][0]
                        ),
                        [
                            self.anim_lst[j][self.anim_num[j]][i][1][0]
                            + self.rect.left,
                            self.anim_lst[j][self.anim_num[j]][i][1][1] + self.rect.top,
                        ],
                    )
                else:
                    img = pygame.transform.rotate(
                        self.parts[j][i], self.anim_lst[j][self.anim_num[j]][i][0]
                    )
                    screen.blit(
                        pygame.transform.flip(img, True, False),
                        [
                            self.rect.right
                            - self.anim_lst[j][self.anim_num[j]][i][1][0]
                            - img.get_width(),
                            self.anim_lst[j][self.anim_num[j]][i][1][1] + self.rect.top,
                        ],
                    )

    def update(self):
        global screen

        self.i += 1
        if self.i == 4:
            self.i = 0
        self.anim_num[0] += 1
        if self.max_num[0] == self.anim_num[0]:
            self.anim_num[0] = 0
            if self.action[0] == "top_reload":
                self.gun.ammo = self.gun.max_ammo
                self.action[0] = "start"
        self.anim_num[1] += 1
        if self.max_num[1] == self.anim_num[1]:
            self.anim_num[1] = 0
            if self.action[1] == "bottom_jump":
                self.action[1] = "start"

        self.move_x()
        self.collide_x()
        self.move_y()
        self.collide_y()
        self.collide_packs()
        if self.gun.duration == "right":
            self.gun.rect.center = [self.rect.center[0] + 15, self.rect.center[1] - 10]
        else:
            self.gun.rect.center = [self.rect.center[0] - 15, self.rect.center[1] - 10]
        self.gun.update()

        if self.x_vel > 0:
            self.gun.duration = "right"
            self.duration = "right"
            actb = "bottom_walk"
        elif self.x_vel < 0:
            self.gun.duration = "left"
            self.duration = "left"
            actb = "bottom_walk"
        else:
            actb = "bottom_stay"

        if self.gun.shooting:
            actt = "top_shoot"
        else:
            actt = "top_stay"

        if self.action[0] != actt and self.action[0] != "top_reload":
            self.action[0] = actt
            self.anim_num[0] = 0
            self.anim_lst[0] = self.anims[self.action[0]]
            self.max_num[0] = len(self.anim_lst[0])
        if self.action[1] != actb and self.action[1] != "bottom_jump":
            self.action[1] = actb
            self.anim_num[1] = 0
            self.anim_lst[1] = self.anims[self.action[1]]
            self.max_num[1] = len(self.anim_lst[1])

        self.anim()
        hp_per = self.hp * 100.0 / self.full_hp
        self.health.blit(hp_per, screen)


class MonsterClass(DogClass):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        #    self.right = [pygame.image.load('Monsters\mr_r_1.png'),pygame.image.load('Monsters\mr_r_2.png')]
        #    self.left = [pygame.image.load('Monsters\mr_l_1.png'),pygame.image.load('Monsters\mr_l_2.png')]
        self.image = pygame.image.load("Monster.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.x_vel, self.y_vel = [0, 0]
        self.jump_power = 30
        self.walk_power = 20
        self.gravity = 1.25
        self.jump_pixels = 385
        self.onGround = [0, 0, 0, 0]
        self.hp = 100
        self.i = 0
        self.aim = ""
        self.sprite_group = pygame.sprite.Group(self)
        self.damage = 10
        self.chill = 0
        self.CD = 15

    def collide_x(self):
        for p in platforms:
            if pygame.sprite.spritecollide(p, self.sprite_group, False):
                if self.x_vel > 0:
                    if p.rect.right > self.rect.right > p.rect.left:
                        self.rect.right = p.rect.left
                if self.x_vel < 0:
                    if p.rect.right > self.rect.left > p.rect.left:
                        self.rect.left = p.rect.right
                for d in self.onGround:
                    if d:
                        self.y_vel = self.jump_power
                        break

    def collide_y(self):
        self.onGround[self.i] = 0
        for p in platforms:
            if pygame.sprite.spritecollide(p, self.sprite_group, False):
                if self.y_vel > 0:
                    if p.rect.bottom > self.rect.top > p.rect.top:
                        self.rect.top = p.rect.bottom
                        self.y_vel = 0
                if self.y_vel < 0:
                    if p.rect.bottom > self.rect.bottom > p.rect.top:
                        self.rect.bottom = p.rect.top
                        self.onGround = [1, 1, 1, 1]
                        self.y_vel = 0

    def anim(self):
        pass

    #    global anim_num
    #    if self.x_vel > 0:
    #        self.image = self.right[anim_num]
    #    else:
    #        self.image = self.left[anim_num]

    def attack(self, aim):
        aim.hp -= self.damage
        self.chill = self.CD
        self.attacking = True

    def update(self, aim):
        self.aim = aim
        self.i += 1
        if self.i == 4:
            self.i = 0

        if self.aim.rect.center[0] < self.rect.center[0]:
            self.x_vel = -self.walk_power
        else:
            self.x_vel = self.walk_power
        if (
            self.aim.rect.right > self.rect.left
            and self.aim.rect.left < self.rect.right
        ):
            self.x_vel = 0
        if self.aim.rect.bottom > self.rect.top - self.jump_pixels:
            if self.aim.rect.bottom < self.rect.top:
                for d in self.onGround:
                    if d:
                        self.y_vel = self.jump_power
                        break

        self.move_x()
        self.collide_x()
        self.move_y()
        self.collide_y()
        if pygame.sprite.spritecollide(aim, self.sprite_group, False):
            if not self.chill:
                self.attack(aim)
        if self.chill:
            self.chill -= 1
        else:
            self.attacking = False
        self.anim()


class BabyClass(MonsterClass):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("crazy_baby/1.png")
        self.images = [self.image, pygame.image.load("crazy_baby/2.png")]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.x_vel, self.y_vel = [0, 0]
        self.gravity = 1.25
        self.jump_pixels = 160
        self.onGround = [0, 0, 0, 0]
        self.i = 0
        self.aim = ""
        self.anim_number = 0
        self.anim_n = 0
        self.old_num = 0
        self.sprite_group = pygame.sprite.Group(self)
        self.attacking = False

        self.jump_power = 20  #
        self.walk_power = 7  #
        self.hp = 200  #
        self.damage = 10  #
        self.chill = 0  #
        self.CD = 15  #

    def anim(self):
        global anim_num
        if anim_num != self.old_num:
            self.old_num = anim_num
            self.anim_number += 1
            if self.anim_number == 4:
                self.anim_number = 0
        if self.anim_number < 2:
            self.anim_n = 0
        else:
            self.anim_n = 1
        self.image = self.images[self.anim_n]


class DHeroClass(BabyClass):
    def __init__(self, location):
        BabyClass.__init__(self, location)
        self.image = pygame.image.load("crazy_baby/dasyashero.png")
        self.images = [self.image, pygame.image.load("crazy_baby/dasyashero2.png")]
        self.jump_power = 10  #
        self.walk_power = 4  #
        self.hp = 500  #
        self.damage = 50  #
        self.chill = 0  #
        self.CD = 15  #


class FlyerClass(MonsterClass):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.right = [
            pygame.image.load("Monsters\\urbo_r_1.png"),
            pygame.image.load("Monsters\\urbo_r_2.png"),
        ]
        self.left = [
            pygame.image.load("Monsters\\urbo_l_1.png"),
            pygame.image.load("Monsters\\urbo_l_2.png"),
        ]
        self.image = self.right[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.x_vel, self.y_vel = [0, 0]
        self.jump_power = 7
        self.walk_power = 7
        self.gravity = 1.25
        self.onGround = [0, 0, 0, 0]
        self.attacking = False
        self.hp = 60  #
        self.damage = 1  #
        self.chill = 0  #
        self.CD = 5  #
        self.i = 0
        self.aim = ""
        self.sprite_group = pygame.sprite.Group(self)
        self.duration = "right"
        self.smoke_colors = [
            (255, 230, 230),
            (200, 170, 170),
            (130, 90, 90),
            (200, 100, 100),
            (200, 200, 100),
        ]

    def anim(self):
        global anim_num
        if self.x_vel > 0:
            self.duration = "right"
        elif self.x_vel < 0:
            self.duration = "left"
        if self.duration == "right":
            self.image = self.right[anim_num]
            for i in range(self.particles):
                pygame.draw.rect(
                    screen,
                    random.choice(self.smoke_colors),
                    [
                        self.rect.left + random.randint(-20, 20),
                        self.rect.bottom + random.randint(-10, 40),
                        4,
                        4,
                    ],
                    0,
                )
        else:
            self.image = self.left[anim_num]
            for i in range(self.particles):
                pygame.draw.rect(
                    screen,
                    random.choice(self.smoke_colors),
                    [
                        self.rect.right + random.randint(-20, 20),
                        self.rect.bottom + random.randint(-10, 40),
                        4,
                        4,
                    ],
                    0,
                )

    def update(self, aim):
        self.aim = aim
        self.i += 1
        if self.i == 4:
            self.i = 0

        if self.aim.rect.center[0] < self.rect.center[0]:
            self.x_vel = -self.walk_power
        else:
            self.x_vel = self.walk_power
        if (
            self.aim.rect.right > self.rect.left
            and self.aim.rect.left < self.rect.right
        ):
            self.x_vel = 0
        if self.aim.rect.bottom < self.rect.top:
            self.y_vel += self.jump_power
            self.particles = 7
            if self.y_vel > 10:
                self.y_vel = 10
        else:
            self.particles = 3
            if self.y_vel < -10:
                self.y_vel += self.jump_power

        self.move_x()
        self.collide_x()
        self.move_y()
        self.collide_y()
        if pygame.sprite.spritecollide(aim, self.sprite_group, False):
            if not self.chill:
                self.attack(aim)
        if self.chill:
            self.chill -= 1
        else:
            self.attacking = False
        self.anim()


class GunClass(pygame.sprite.Sprite):
    def __init__(self):
        global screen
        pygame.sprite.Sprite.__init__(self)
        self.image = self.right = pygame.image.load("Guns/Gun_r.png")
        self.left = pygame.image.load("Guns/Gun_l.png")
        self.rect = self.image.get_rect()
        self.used_ammo = BulletClass
        self.duration = "right"

        self.max_ammo = 30
        self.ammo = 30
        self.delay = 10
        self.bullet_speed = 20

        self.delay_num = 0
        self.fire_delay = 4
        self.fire_delay_num = 0
        self.shooting = False
        self.shooted_bullets = []

    def update(self):
        if self.delay_num:
            self.delay_num -= 1
        if self.shooting:
            if self.ammo:
                if not self.delay_num:
                    self.ammo -= 1
                    if self.duration == "right":
                        self.shooted_bullets.append(
                            self.used_ammo(
                                self.duration,
                                self.bullet_speed,
                                (
                                    self.rect.right,
                                    self.rect.top + 0.25 * self.rect.height,
                                ),
                            )
                        )
                    else:
                        self.shooted_bullets.append(
                            self.used_ammo(
                                self.duration,
                                self.bullet_speed,
                                (
                                    self.rect.left,
                                    self.rect.top + 0.25 * self.rect.height,
                                ),
                            )
                        )
                    self.delay_num = self.delay
                    self.fire_delay_num = 9
            else:
                self.shooting = False

        for bullet in self.shooted_bullets:
            bullet.move()
            for pltf in platforms:
                if pygame.sprite.spritecollide(pltf, bullet.sprite_group, False):
                    self.shooted_bullets.remove(bullet)
                    break
            for monster in monsters:
                if pygame.sprite.spritecollide(monster, bullet.sprite_group, False):
                    self.shooted_bullets.remove(bullet)

                    monster.hp -= bullet.damage
                    #    monsters.remove(monster)
                    break
            # **********************************************************************************
            for monster in evo_monsters:
                if pygame.sprite.spritecollide(monster, bullet.sprite_group, False):
                    if bullet in self.shooted_bullets:
                        self.shooted_bullets.remove(bullet)

                    monster.hp -= bullet.damage
                    ##                    monsters.remove(monster)
                    break
            screen.blit(bullet.image, bullet.rect.topleft)
        if self.duration == "right":
            self.image = self.right
            if self.fire_delay_num > self.fire_delay:
                screen.blit(
                    fire_r[anim_num],
                    [self.rect.right, self.rect.top + 0.25 * self.rect.height - 16],
                )
            elif self.fire_delay_num:
                screen.blit(
                    fire_r[2],
                    [self.rect.right, self.rect.top + 0.25 * self.rect.height - 16],
                )
        else:
            self.image = self.left
            if self.fire_delay_num > self.fire_delay:
                screen.blit(
                    fire_l[anim_num],
                    [self.rect.left - 40, self.rect.top + 0.25 * self.rect.height - 16],
                )
            elif self.fire_delay_num:
                screen.blit(
                    fire_l[2],
                    [self.rect.left - 40, self.rect.top + 0.25 * self.rect.height - 16],
                )
        if self.fire_delay_num:
            self.fire_delay_num -= 1
        screen.blit(self.image, self.rect.topleft)


##class CattyClass(GunClass):
##    def __init__(self):
##        GunClass.__init__(self)
##        self.image = self.right = pygame.image.load('Guns/Catty_rifle_r.png')
##        self.left = pygame.image.load('Guns/Catty_rifle_l.png')
##        self.rect = self.image.get_rect()
##        self.used_ammo = CattyBulletClass
##        self.ammo = 10
##        self.delay = 30
##        self.bullet_speed = 10


class AkmClass(GunClass):
    def __init__(self):
        GunClass.__init__(self)
        self.image = self.right = pygame.image.load("Guns/akm_r.png")
        self.left = pygame.image.load("Guns/akm_l.png")
        self.rect = self.image.get_rect()
        self.used_ammo = BulletClass
        self.ammo = 30
        self.delay = 3
        self.bullet_speed = 40


class BulletClass(pygame.sprite.Sprite):
    def __init__(self, duration, speed, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Guns/Bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.sprite_group = pygame.sprite.Group(self)
        self.damage = 20
        if duration == "right":
            self.speed = speed
        else:
            self.speed = -speed

    def move(self):
        self.rect.left += self.speed


##class CattyBulletClass(BulletClass):
##    def __init__(self, duration, speed, location):
##        BulletClass.__init__(self, duration, speed, location)
##        self.image = pygame.image.load('Guns/Catty_bullet.png')


class AmmoPunchClass(pygame.sprite.Sprite):
    def __init__(self, location, gun):
        pygame.sprite.Sprite.__init__(self)

        ##        self.surf = pygame.surface.Surface([48,48])
        ##        self.surf.set_colorkey((0,0,0))
        ##        pygame.draw.rect(self.surf,[150,25,25],[0,0,48,48],5)
        ##        self.image = self.surf.convert()
        self.image = pygame.image.load("Guns/GunAmmoPunch.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.gun = gun

    def blit(self):
        global screen
        screen.blit(self.image, self.rect.topleft)


class HartClass(AmmoPunchClass):
    def __init__(self, location):
        AmmoPunchClass.__init__(self, location, "hart")
        self.image = pygame.image.load("Animation/hart.png")


class CupClass(AmmoPunchClass):
    def __init__(self, location):
        AmmoPunchClass.__init__(self, location, "cup")
        self.image = pygame.image.load("Animation/cup.png")


fire_r = [
    pygame.image.load("Animation/fire_r_1.png"),
    pygame.image.load("Animation/fire_r_2.png"),
    pygame.image.load("Animation/fire_r_3.png"),
]
fire_l = [
    pygame.image.load("Animation/fire_l_1.png"),
    pygame.image.load("Animation/fire_l_2.png"),
    pygame.image.load("Animation/fire_l_3.png"),
]


class ShotClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shooting = False
        self.cloud = [
            pygame.image.load("Animation/cloud_1.png"),
            pygame.image.load("Animation/cloud_2.png"),
        ]
        self.shot = [
            pygame.image.load("Animation/shot_1.png"),
            pygame.image.load("Animation/shot_2.png"),
        ]
        self.fired = [
            pygame.image.load("Animation/fired_1.png"),
            pygame.image.load("Animation/fired_2.png"),
        ]
        self.image = self.cloud[0]
        self.rect = self.image.get_rect()


class PaddleClass(pygame.sprite.Sprite):
    def __init__(self, location, image):
        pygame.sprite.Sprite.__init__(self)

        ##        self.surf = pygame.surface.Surface([48,48])
        ##        self.surf.set_colorkey((0,0,0))
        ##        pygame.draw.rect(self.surf,[150,25,25],[0,0,48,48],5)
        ##        self.image = self.surf.convert()

        self.image = image

        self.rect = self.image.get_rect()
        self.location = self.rect.left, self.rect.top = location


class Camera:
    def __init__(self):
        global gabarits, everybody, max_x, max_y
        self.rect = pygame.Rect(0, 0, gabarits[0], gabarits[1])
        self.gamerect = pygame.Rect(0, 0, max_x, max_y)
        self.amplitude = [0, 0]

    def fix(self):
        if self.gamerect.left > 0:
            for i in everybody:
                i.rect.left -= self.gamerect.left
            self.gamerect.left = 0
        elif self.gamerect.right < self.rect.right:
            for i in everybody:
                i.rect.right -= self.gamerect.right - self.rect.right
            self.gamerect.right = self.rect.right

        if self.gamerect.top > 0:
            for i in everybody:
                i.rect.top -= self.gamerect.top
            self.gamerect.top = 0
        elif self.gamerect.bottom < self.rect.bottom:
            for i in everybody:
                i.rect.bottom -= self.gamerect.bottom - self.rect.bottom
            self.gamerect.bottom = self.rect.bottom

    def move(self):
        self.amplitude[0] = dog.rect.center[0] - self.rect.center[0]
        self.amplitude[1] = dog.rect.center[1] - self.rect.center[1]

        self.gamerect.left -= self.amplitude[0]
        self.gamerect.top -= self.amplitude[1]

        for items in everybody:
            items.rect.left -= self.amplitude[0]
            items.rect.top -= self.amplitude[1]

    def update(self):
        self.move()
        self.fix()


##*************************************************************
##*************************************************************
##*************************************************************


def load_level():
    global max_x, max_y, everybody, monsters, evo_monsters, platforms, loco, tile_set

    lvl = open("level.txt", "r")
    level = lvl.readlines()
    lvl.close()
    tile_set_image = pygame.image.load("forest_tiles.png")
    ##    tile_set_image = pygame.image.load('Test.jpg')
    tile_set = [[], [], []]
    surf = pygame.surface.Surface([48, 48])
    surf.set_colorkey((0, 0, 0))

    a = 0
    for y in [0, 48, 96]:
        for x in [0, 48, 96]:
            surf.fill((0, 0, 0))
            surf.blit(tile_set_image, [-y, -x])
            tile_set[a].append(surf.convert())
        a += 1

    platforms = []
    loco = [96, 96]
    y = 0
    max_x = 0
    max_y = 0
    for p in range(len(level)):
        x = 0
        for i in range(len(level[p])):
            if level[p][i] == "o":
                a, b = 0, 0
                ##*************************************************************
                if p == 0:
                    if level[p + 1][i] == "o":
                        a = 1
                    else:
                        a = 2
                elif p == len(level) - 1:
                    if level[p - 1][i] == "o":
                        a = 1
                    else:
                        a = 0
                else:
                    if level[p - 1][i] == "o" and level[p + 1][i] == "o":
                        a = 1
                    elif level[p - 1][i] == "o":
                        a = 2
                    else:
                        a = 0
                ##*************************************************************
                if i == 0:
                    if level[p][i + 1] == "o":
                        b = 1
                    else:
                        b = 2
                elif i == len(level[p]) - 2:
                    if level[p][i - 1] == "o":
                        b = 1
                    else:
                        b = 0
                else:
                    if level[p][i - 1] == "o" and level[p][i + 1] == "o":
                        b = 1
                    elif level[p][i - 1] == "o":
                        b = 2
                    else:
                        b = 0
                ##*************************************************************
                pddl = PaddleClass([x, y], tile_set[b][a])
                platforms.append(pddl)
                everybody.append(pddl)
            if level[p][i] == "x":
                loco = [x, y]
            elif level[p][i] == "a":
                packs.append(AmmoPunchClass([x, y], "gun"))
            elif level[p][i] == "h":
                packs.append(HartClass([x, y]))
            elif level[p][i] == "c":
                packs.append(CupClass([x, y]))
            elif level[p][i] == "g":
                monsters.append(BabyClass([x, y]))
            elif level[p][i] == "d":
                monsters.append(DHeroClass([x, y]))
            elif level[p][i] == "f":
                monsters.append(FlyerClass([x, y]))
            elif level[p][i] == "b":
                evo_monsters.append(BigBossClass([x, y]))
            x += 48
        y += 48
    max_x = x - 48
    max_y = y


def main():
    global anim_num, platforms, monsters, evo_monsters, everybody, gabarits, hero, dog
    global screen, packs
    pygame.init()
    gabarits = [864, 672]
    screen = pygame.display.set_mode(gabarits)
    screen_image = pygame.image.load("side.png")
    fone = pygame.image.load("try.png")
    screen_rect = pygame.Rect(0, 0, gabarits[0], gabarits[1])
    clock = pygame.time.Clock()

    n = 0
    anim_num = 0

    packs = []
    everybody = []

    platforms = []
    monsters = []
    evo_monsters = []
    boxes = []
    y = 0
    max_x = 0
    max_y = 0

    load_level()
    dog = DogClass(loco)
    hero = pygame.sprite.Group(dog)
    everybody.append(dog)
    for i in evo_monsters:
        everybody.append(i)
    for i in packs:
        everybody.append(i)
    for i in monsters:
        everybody.append(i)

    cam = Camera()

    running = True
    while running:
        clock.tick(30)
        # print clock.get_fps()
        screen.blit(screen_image, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if dog.x_vel < 0:
                        dog.x_vel = 0
                    # if 0 > dog.x_vel > -dog.power_brake: dog.x_vel = 0
                    # else: dog.x_vel += dog.power_brake
                elif event.key == pygame.K_RIGHT:
                    if dog.x_vel > 0:
                        dog.x_vel = 0
                    # if 0 < dog.x_vel < dog.power_brake: dog.x_vel = 0
                    # else: dog.x_vel -= dog.power_brake
                elif event.key == pygame.K_SPACE:
                    dog.gun.shooting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dog.x_vel = -dog.walk_power
                    # if dog.x_vel > -dog.walk_power: dog.x_vel -= dog.power_brake
                elif event.key == pygame.K_RIGHT:
                    dog.x_vel = dog.walk_power
                    # if dog.x_vel < dog.walk_power: dog.x_vel += dog.power_brake
                elif event.key == pygame.K_UP:
                    if 1 in dog.onGround:
                        dog.y_vel = dog.jump_power
                        dog.action[1] = "bottom_jump"
                        dog.anim_num[1] = 0
                        dog.anim_lst[1] = dog.anims["bottom_jump"]
                        dog.max_num[1] = len(dog.anim_lst[1])
                elif event.key == pygame.K_r:
                    if not dog.action[0] == "top_reload":
                        dog.gun.shooting = False
                        dog.action[0] = "top_reload"
                        dog.anim_num[0] = 0
                        dog.anim_lst[0] = dog.anims["top_reload"]
                        dog.max_num[0] = len(dog.anim_lst[0])
                elif event.key == pygame.K_SPACE:
                    if not dog.action[0] == "top_reload":
                        dog.gun.shooting = True

        n += 1
        if n == 10:
            n = 0

        anim_num = int(n >= 5)

        for p in platforms:
            if -100 < p.rect.left < 1000 and -100 < p.rect.top < 1000:
                screen.blit(p.image, p.rect.topleft)

        for p in packs:
            p.blit()

        dog.update()

        for monster in monsters:
            if monster.hp <= 0:
                monsters.remove(monster)
                continue
            if -100 < monster.rect.left < 1000 and -100 < monster.rect.top < 1000:
                monster.update(dog)
                screen.blit(monster.image, monster.rect.topleft)
        for monster in evo_monsters:
            if monster.hp <= 0:
                evo_monsters.remove(monster)
                continue
            if -300 < monster.rect.left < 1300 and monster.rect.top < 1300:
                monster.update(dog, platforms, screen)

        cam.update()
        # screen.blit(fone, (0,0))
        if dog.win:
            blittext(screen, "You WIN!!!!", [60, 300], 200, (255, 255, 255))
        pygame.display.flip()

        # screen.fill([155,155,155])
        # for i in range(3):
        #     for j in range(3):
        #         screen.blit(tile_set[i][j], [i*50,j*50])
        # pygame.display.flip()
        # pygame.time.delay(3000)
        if dog.hp <= 0 and not dog.win:
            running = False
    if dog.hp <= 0:
        main()

    pygame.quit()


main()
