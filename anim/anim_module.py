import pygame, math, pickle

rad = 57.2958
def cos(ang):
    cos = math.cos(ang/rad)
    return cos
def sin(ang):
    sin = math.sin(ang/rad)
    return sin
def acos(lenght):
    acos = math.acos(lenght)*rad
    acos = [int(acos),int((360-acos)%360)]
    return acos
def asin(lenght):
    asin = math.asin(lenght)*rad
    asin = [int(asin),int((540-asin)%360)]
    return asin
def get_ang(acos,asin):
    if acos[0] in asin or -acos[0] in asin:
        ang = acos[0]
    else:
        ang = acos[1]
    return ang

class AnimClass():
    def __init__(self, name_image):
        self.image = pygame.image.load(name_image)
##        self.image = pygame.transform.scale2x(pygame.transform.scale2x(self.image))
        self.image = pygame.transform.scale2x(self.image)
        self.nimage = self.image
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [0,0]

        self.target = None
        self.son = None
        self.sons = []
        self.mhook = [0,0,0]
        
        self.hook = [0,0,0,0]
        self.hooks = []
        
        self.angles = 0
        self.lenght = self.rect.width/2.

    def add_mhook(self, mouse_loc):
        self.mhook[2] = mouse_loc[0]-self.rect.center[0]
    def add_hook(self, mouse_loc):
        self.a = mouse_loc[0]-self.rect.center[0]
        self.b = mouse_loc[1]-self.rect.center[1]
        self.hook[2] = (self.a**2+self.b**2)**0.5
        
        self.hook[3] = get_ang(acos(self.a/self.hook[2]),\
                             asin(self.b/self.hook[2]))
        if self.a<0 or (self.a>0 and self.b>0):
            self.hook[3] = 360 - self.hook[3]

    def get_mhook(self):
        self.mhook = [cos(self.angles)*self.mhook[2],\
                       sin(self.angles)*self.mhook[2],self.mhook[2]]
    def get_hook(self):
        self.hook = [self.rect.center[0]+cos((self.angles+self.hook[3])%360)*self.hook[2],\
                     self.rect.center[1]-sin((self.angles+self.hook[3])%360)*self.hook[2],\
                     self.hook[2],self.hook[3]]
        if self.hooks:
            for i in range(len(self.hooks)):
                self.hooks[i] = [self.rect.center[0]+cos((self.angles+self.hooks[i][3])%360)*self.hooks[i][2],\
                     self.rect.center[1]-sin((self.angles+self.hooks[i][3])%360)*self.hooks[i][2],\
                     self.hooks[i][2],self.hooks[i][3]]

    def tp_to_mhook(self):
        if self.target:
            self.rect.center = [self.target[0]-self.mhook[0],\
                               self.target[1]+self.mhook[1]]

    def rotate(self, angles):
        self.angles = (self.angles + angles) % 360
        self.nimage = pygame.transform.rotate(self.image, self.angles)
        self.rect = self.nimage.get_rect()

    def collide(self, mouse_loc):
        if self.rect.left < mouse_loc[0] < self.rect.right and\
           self.rect.top < mouse_loc[1] < self.rect.bottom:
            return True
        else:
            return False

    def update_son(self):
        if self.son:
            self.son.target = self.hook[:2]
        if self.sons:
            for i in range(len(self.sons)):
                self.sons[i].target = self.hooks[i][:2]

    def update(self):
        self.rotate(0)
        self.get_mhook()
        self.tp_to_mhook()
        self.get_hook()
        self.update_son()

class PanelClass():
    def __init__(self):
        from anim_setup import gab
        self.image = pygame.image.load('panel.png')
        self.points = []
        self.rectpoints = []
        self.rectmsg = []
        self.point_num = 0
        self.buttons = []
        self.msg = []
        for i in [13,76,138]:
            self.buttons.append(pygame.Rect(i+gab[0]-200,12,48,48))

    def collide_buttons(self, mouse_loc, num):
        if self.buttons[num].left < mouse_loc[0] < self.buttons[num].right and\
           self.buttons[num].top < mouse_loc[1] < self.buttons[num].bottom:
            return True
        else:
            return False

    def add(self):
        self.helper = []
        for i in self.lst:
            self.helper.append([i.angles, i.rect.topleft])
        self.points.append([self.helper])
        try:
            self.points[-1].append(int(input('time of animation: ')))
        except:
            self.points[-1].append(200) ##****ENTER_TIME****

    def delete(self):
        try:
            del self.points[self.point_num]
            del self.rectpoints[self.point_num]
        except: print('haven`t points')

    def gener_angles(self):
        self.save_file = []
        self.msg = []
        self.rectmsg = []
        for i in range(len(self.points)):
            if i < len(self.points)-1:
                frames = self.points[i+1][1]/33.
                for n in range(0,1000,int(1./frames*1000)):
                    k = n/1000.
                    parts = []
                    for part in range(len(self.points[i][0])):
                        ang = self.points[i+1][0][part][0] - self.points[i][0][part][0]
                        if ang > 180:
                            ang = -(360-ang)
                        elif ang < -180:
                            ang = 360 + ang
                        parts.append(ang/frames)
                    self.msg.append(parts)
                    self.rectmsg.append([(self.rectpoints[i+1][0] - self.rectpoints[i][0])/frames,\
                                        (self.rectpoints[i+1][1] - self.rectpoints[i][1])/frames])

    def save(self):
        # name = raw_input('name of file: ')
        # name = 't.txt'
        # fl = open(name, 'w')
        # fl.write(self.save_file)
        # pickle.dump(self.save_file, fl)
        # fl.close()
        print(self.save_file)
        print
        print
        print
  
    def update(self):
        try:
            self.point_num = self.point_num % len(self.points)
            return True
        except:
            return False
