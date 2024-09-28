import random

import pygame


class PowerupManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.powerups = pygame.sprite.Group()

    def update_powerup(self):
        powerup_type = random.choice([1, 4])
        if powerup_type == 1:
            self.ai_game.settings.update_ship_speed()
        elif powerup_type == 2:
            self.ai_game.settings.update_bullet_speed()
        elif powerup_type == 3:
            self.ai_game.settings.update_fire_rate()