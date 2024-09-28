import random

import pygame
from sprites.bullet import Bullet
from sprites.powerups import Powerups

class BulletManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

    def fire_bullet(self):
        if len(self.bullets) < self.ai_game.settings.bullets_allowed:
            new_bullet = Bullet(self.ai_game, self.ai_game.ship_manager.ship.rect.centerx, self.ai_game.ship_manager.ship.rect.top, 'up')
            self.bullets.add(new_bullet)

    def fire_alien_bullet(self):
        if len(self.alien_bullets) < self.ai_game.settings.bullet_max:
            random_alien = random.choice(self.ai_game.alien_manager.aliens.sprites())
            new_bullet = Bullet(self.ai_game, random_alien.rect.centerx, random_alien.rect.bottom, 'down')
            self.alien_bullets.add(new_bullet)

    def update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()
        self.check_bullet_meteor_collisions()
        self.check_ship_powerup_collisions()
        self.check_bullet_ship_collisions()

        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.ai_game.settings.screen_height:
                self.alien_bullets.remove(bullet)

        self.check_bullet_ship_collisions()


    def check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.ai_game.alien_manager.aliens, True, True)
        if not self.ai_game.alien_manager.aliens:
            self.bullets.empty()
            self.ai_game.alien_manager.create_fleet()
            self.ai_game.settings.increase_difficulty()
            self.ai_game.stats.level += 1
            self.ai_game.scoreboard_manager.scoreboard.prep_level()

        for aliens in collisions.values():
            self.ai_game.stats.score += self.ai_game.settings.alien_points * len(aliens)
            self.ai_game.explosion_manager.create_explosion(aliens[0].rect.center)
            if random.random() < 0.1:
                powerup = Powerups(self.ai_game, aliens[0].rect.centerx, aliens[0].rect.centery)
                self.ai_game.sprite_manager.powerups.add(powerup)
        self.ai_game.scoreboard_manager.scoreboard.prep_score()
        self.ai_game.scoreboard_manager.scoreboard.check_high_score()

    def check_bullet_meteor_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.ai_game.meteor_manager.meteors, True, True)
        for meteors in collisions.values():
            self.ai_game.explosion_manager.create_explosion(meteors[0].rect.center)
        self.ai_game.scoreboard_manager.scoreboard.prep_score()
        self.ai_game.scoreboard_manager.scoreboard.check_high_score()

    def check_ship_powerup_collisions(self):
        collision = pygame.sprite.spritecollideany(self.ai_game.ship_manager.ship, self.ai_game.sprite_manager.powerups)
        if collision:
            self.ai_game.sprite_manager.powerups.remove(collision)
            self.ai_game.powerup_manager.update_powerup()

    def check_bullet_ship_collisions(self):
        if pygame.sprite.spritecollideany(self.ai_game.ship_manager.ship, self.alien_bullets):
            self.ai_game.explosion_manager.create_explosion(self.ai_game.ship_manager.ship.rect.center)
            self.ai_game.ship_manager.ship_hit()