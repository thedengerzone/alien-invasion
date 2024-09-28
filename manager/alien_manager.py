import pygame
from random import random
from sprites.alien import Alien
from sprites.powerups import Powerups

class AlienManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.aliens = pygame.sprite.Group()

    def create_fleet(self):
        alien = Alien(self.ai_game)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        while current_y < (self.ai_game.settings.screen_height - 8 * alien_height):
            while current_x < (self.ai_game.settings.screen_width - 2 * alien_width):
                self.create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def create_alien(self, x_position, y_position):
        new_alien = Alien(self.ai_game)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = new_alien.y
        self.aliens.add(new_alien)

    def update_aliens(self):
        if pygame.sprite.spritecollideany(self.ai_game.ship_manager.ship, self.aliens):
            self.ai_game.explosion_manager.create_explosion(self.ai_game.ship_manager.ship.rect.center)
            self.ai_game.ship_manager.ship_hit()

        self.check_fleet_edges()
        self.aliens.update()
        self.check_aliens_bottom()

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.ai_game.settings.fleet_drop_speed
        self.ai_game.settings.fleet_direction *= -1

    def check_aliens_bottom(self):
        screen_rect = self.ai_game.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ai_game.ship_manager.ship_hit()
                break

    def check_bullet_alien_collisions(self):
        if not self.aliens:
            self.ai_game.bullet_manager.bullets.empty()
            self.create_fleet()
            self.ai_game.settings.increase_difficulty()
            self.ai_game.stats.level += 1
            self.ai_game.sb.prep_level()

        collisions = pygame.sprite.groupcollide(self.ai_game.bullet_manager.bullets, self.aliens, True, True)
        for aliens in collisions.values():
            self.ai_game.stats.score += self.ai_game.settings.alien_points * len(aliens)
            self.ai_game.explosion_manager.create_explosion(aliens[0].rect.center)
            if random() < 0.1:
                powerup = Powerups(self.ai_game, aliens[0].rect.centerx, aliens[0].rect.centery)
                self.ai_game.sprite_manager.powerups.add(powerup)
        self.ai_game.sb.prep_score()
        self.ai_game.sb.check_high_score()