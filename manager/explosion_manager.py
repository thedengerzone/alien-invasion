import pygame
from sprites.explosion import Explosion

class ExplosionManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.explosions = pygame.sprite.Group()

    def create_explosion(self, center):
        explosion = Explosion(center)
        self.explosions.add(explosion)

    def draw_explosions(self, screen):
        self.explosions.draw(screen)