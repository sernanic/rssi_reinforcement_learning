import pygame
pygame.init()
colors = pygame.color.THECOLORS
class RSSI(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((100,100))
        self.image.fill(colors['blue'])
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.value = 0