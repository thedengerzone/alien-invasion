import random
import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from game_stats import GameStats
from settings import Settings
from ship import Ship
from button import Button
from scoreboard import ScoreBoard
from explosion import Explosion

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        self.bg_image = pygame.image.load('images/background2.png')
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((1024, 1024))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.game_active = False

        self.play_button = Button(self, "Play")
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        self.ship = Ship(self)
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """ Start the main loop for the game """
        while True:
            # Watch for keyboard and mouse events
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self.alien_bullets.update()
                self._fire_alien_bullet()
                self._update_bullets()
                self._update_aliens()
                self.explosions.update()

            self._update_screen()
            self.clock.tick(60)

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.blit(self.bg_image, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        self.ship.render()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)
        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()
        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _check_events(self):
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self, self.ship.rect.centerx, self.ship.rect.top, 'up')
            self.bullets.add(new_bullet)

    def _fire_alien_bullet(self):
        if len(self.alien_bullets) < self.settings.bullet_max:
            random_alien = random.choice(self.aliens.sprites())
            new_bullet = Bullet(self, random_alien.rect.centerx, random_alien.rect.bottom, 'down')
            self.alien_bullets.add(new_bullet)



    def _update_bullets(self):

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        self.check_bullet_ship_collisions()

    def _create_fleet(self):
        """Create the fleet of aliens"""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = new_alien.y
        self.aliens.add(new_alien)

    def _update_aliens(self):

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._create_explosion(self.ship.rect.center)
            self.ship_hit()

        self.check_fleet_edges()
        self.aliens.update()

        self.check_aliens_bottom()

    def _create_explosion(self, center):
        explosion = Explosion(center)
        self.explosions.add(explosion)

    def check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_bullet_alien_collisions(self):
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        for aliens in collisions.values():
            self.stats.score += self.settings.alien_points * len(aliens)
            self.explosions.add(Explosion(aliens[0].rect.center))

        self.sb.prep_score()
        self.sb.check_high_score()

    def check_bullet_ship_collisions(self):
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self.ship_hit()

    def ship_hit(self):

        self.explosions.add(Explosion(self.ship.rect.center))

        if self.stats.ships_left > 0:

            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get Rid of any remaining bullets and aliens
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Pause for a moment to show the explosion
            pygame.display.flip()
            pygame.time.delay(3000)  # Delay for 1 second (1000 milliseconds)

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()



        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()



    def check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
              self.ship_hit()
              break


if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
