import pygame, anim, os

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'Boss')

class BigBossClass(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        pre_names = 'pre_legb,footb,legb,handb,pre_handb,armb,connect,pre_leg,body,head,foot,leg,hand,pre_hand,arm'
        pre_names = pre_names.split(',')
        names = []
        self.parts = []
        for i in pre_names:
            names.append(os.path.join(image_path, '%s%s' %(i,'.png')))
            self.parts.append(pygame.image.load(names[-1]))
        self.rect = pygame.Rect(loc[0],loc[1],70,300)
        
        self.anims = {}
        self.anims['walk'] = anim.walk
        self.anims['hk'] = anim.hand_blow
        self.anims['lk'] = anim.leg_blow
        self.anims['hr'] = anim.hand_reset
        self.anims['lr'] = anim.leg_reset
        self.anims['jump'] = anim.jump
        self.action = ['start']
        self.anim_lst = 0
        self.anim_num = 0
        self.max_num = 1

        self.x_vel, self.y_vel = [0,0]
        self.jump_power = 17
        self.walk_power = 10
        self.hp = 1000   #
        self.gravity = 1
        self.jump_pixels = self.jump_power**2/2./self.gravity
        self.i = 0
        self.onGround = [0,0,0,0]
        self.duration = 'right'
        self.sprite_group = pygame.sprite.Group(self)
        self.damage_h = 75
        self.damage_l = 150

    def move_x(self):
        self.rect.left += self.x_vel

    def move_y(self):
        for d in self.onGround:
            if not d:
                self.y_vel -= self.gravity
                break
        self.rect.top -= self.y_vel

    def collide_x(self, platforms):
        for p in platforms:
            if pygame.sprite.spritecollide(p, self.sprite_group, False):
                if self.x_vel > 0:
                    if p.rect.right > self.rect.right > p.rect.left:
                        self.rect.right = p.rect.left
                if self.x_vel < 0:
                    if p.rect.right > self.rect.left > p.rect.left:
                        self.rect.left = p.rect.right

    def collide_y(self, platforms):
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
                        self.onGround = [1,1,1,1]
                        self.y_vel = 0

    def collide_packs(self):
        for p in packs:
            if pygame.sprite.spritecollide(p, hero, False):
                if p.gun == 'gun':
                    self.gun = GunClass()
                elif p.gun == 'akm':
                    self.gun = AkmClass()
                everybody.remove(p)
                packs.remove(p)
                
    def anim(self, screen):
        for i in range(len(self.parts)):
            if self.duration == 'right':
                screen.blit(pygame.transform.rotate(self.parts[i],\
                            self.anim_lst[self.anim_num][i][0]),\
                            [(self.anim_lst[self.anim_num][i][1][0]*2+self.rect.left),\
                             (self.anim_lst[self.anim_num][i][1][1]*2+self.rect.top)])
            else:
                img = pygame.transform.rotate(self.parts[i], self.anim_lst[self.anim_num][i][0])
                screen.blit(pygame.transform.flip(img,True,False),\
                            [self.rect.right-self.anim_lst[self.anim_num][i][1][0]*2-img.get_width(),\
                             self.anim_lst[self.anim_num][i][1][1]*2+self.rect.top])

    def update(self, aim, platforms, screen):
        self.i += 1
        if self.i == 4:
            self.i = 0
        self.aim = aim

        ampx = self.rect.center[0]-aim.rect.center[0]
        ampy = self.rect.center[1]-aim.rect.center[1]

        if ampx > 0:                                   #aiming target
            self.x_vel = -self.walk_power
        else:
            self.x_vel = self.walk_power
        if self.aim.rect.right > self.rect.left and self.aim.rect.left < self.rect.right:
            self.x_vel = 0
        if self.aim.rect.bottom > self.rect.top - self.jump_pixels:
            if self.aim.rect.bottom < self.rect.top and len(self.action)<3:
                if 1 in self.onGround and not 'jump' in self.action:
                    self.action.append('jump')

        if len(self.action)<2:
            if -70<=ampx<=70 and -80<=ampy<=180: self.action.extend(['hk','hr'])
            elif -100<=ampx<=100 and -180<=ampy<=60: self.action.extend(['lk','lr'])
##        print self.action
##        self.action = ['lr','lr','lr','lr','lr','lr','lr']
               
        self.anim_num += 1
        if self.max_num == self.anim_num:
            self.anim_num = 0
            if self.action[0] == 'hk' and -70<=ampx<=70 and -80<=ampy<=180:
                aim.hp -= self.damage_h
                aim.y_vel = -20
            elif self.action[0] == 'lk' and -100<=ampx<=100 and -180<=ampy<=60:
                aim.hp -= self.damage_l
                aim.y_vel = 20
                if self.duration == 'right': aim.x_vel = 30
                else: aim.x_vel = -30
            elif self.action[0] == 'jump': self.y_vel = self.jump_power
            del self.action[0]
            if not self.action: self.action.append('walk')
            self.anim_lst = self.anims[self.action[0]]
            self.max_num = len(self.anim_lst)

        self.move_x()
        self.collide_x(platforms)
        self.move_y()
        self.collide_y(platforms)
##        self.collide_packs()
            
        if self.x_vel > 0:
            self.duration = 'right'
        elif self.x_vel < 0:
            self.duration = 'left'

        self.anim(screen)
##        self.health.blit(self.hp,screen)
