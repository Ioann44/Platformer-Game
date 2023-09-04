import pygame
pygame.init()

class Text:
    def __init__(self, gabarits, text, color):
        self.gabarits = int(gabarits)
        self.text = str(text)
        self.color = color
        self.font = pygame.font.Font(None, self.gabarits)
        self.surf = self.font.render(self.text, 1, self.color)

    def blit_center(self, surface, height):
        self.surface = surface
        self.surface.blit(self.surf, [self.surface.get_width()/2-\
                                 self.surf.get_width/2, height])

    def blit(self, surface, topleftx, toplefty):
        self.location = [topleftx, toplefty]
        self.surface = surface
        self.surface.blit(self.surf, self.location)

def blittext(surface, text, location=[0,0], size=40, color=(0,0,0)):
    surface.blit(pygame.font.Font(None,size).render(str(text),1,color), location)
