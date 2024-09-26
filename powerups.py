import pygame
from pygame.sprite import Sprite


class Powerups(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/powerups/powerup.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.velocity = 1