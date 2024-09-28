import random

import pygame

from sprites.metors import Meteor


class MeteorManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.meteors = pygame.sprite.Group()

    def spawn_meteors(self):
        if len(self.meteors) < self.ai_game.settings.meteor_max:
            meteor = Meteor(self.ai_game, random.choice([0, self.ai_game.settings.screen_width]),
                            random.randint(0, int(self.ai_game.settings.screen_height / 2)))
            self.meteors.add(meteor)

    def update_meteors(self):
        check_for_meteor_collision = pygame.sprite.spritecollideany(self.ai_game.ship_manager.ship, self.meteors)

        if check_for_meteor_collision:
            self.ai_game.ship_manager.ship_hit()

        for meteor in self.meteors.copy():
            if meteor.rect.top >= self.ai_game.settings.screen_height:
                self.meteors.remove(meteor)