import pygame
##class HealthClass():
##    def __init__(self,loc):
##        self.surf = pygame.surface.Surface([200,70])
##        self.stages = {}
##        self.stages['good'] = pygame.image.load('screen/normal_pulse.png')
##        self.location = loc
##        self.x = 0
##
##    def blit(self,health,screen):
##        self.surf.fill([255,255,255])
##        self.surf.set_colorkey([255,255,255])
##        if health >= 70:
##            self.hp = 'good'
##        elif health >= 40:
##            self.hp = 'normal'
##        elif self.hp > 0:
##            self.hp = 'bad'
##        else:
##            self.hp = 'dead'
##        self.surf.blit(self.stages[self.hp], [self.x,0])
##        screen.blit(self.surf, self.location)
##        
##        self.x -= 2
##        if self.x == -300:
##            self.x = 0

class HealthClass():
    def __init__(self,loc):
        self.location = loc
        self.surf = pygame.surface.Surface([268,54])
        self.surf.set_colorkey((0,0,0))
        self.bar = pygame.image.load('screen/pulsebarb.png')
        self.hp = pygame.image.load('screen/healthline.png')
        self.x = 16

    def blit(self,health,screen):
        self.surf.fill((0,0,0))
        self.surf.blit(self.hp, [268*(health-100)*0.01, 0])
        screen.blit(self.bar, self.location)
        screen.blit(self.surf, [self.location[0]+self.x,self.location[1]+13])

class AssistantClass():
    def __init__(self):
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.colorKey = (2,0,0)
    
    def loadImage(self, name, convert = True):
        image = pygame.image.load(os.path.join(self.path, name))
        if convert: return image.convert()
        else: return image
