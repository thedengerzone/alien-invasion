# manager/ship_manager.py
import pygame

from sprites.ship import Ship


class ShipManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.ship = Ship(ai_game)  # Initialize the ship instance once
        self.respawn_timer = None

    def update(self):
        self.ship.update()  # Update the same ship instance

    def render(self):
        self.ship.render()  # Render the same ship instance

    def ship_hit(self):
        self._create_explosion(self.ship.rect.center)
        if self.ai_game.stats.ships_left > 0:
            self.ai_game.stats.ships_left -= 1
            self.ai_game.scoreboard_manager.scoreboard.decrement_ships()
            self.ai_game.scoreboard_manager.scoreboard.prep_ships()
            self.ai_game.bullet_manager.bullets.empty()
            self.ai_game.bullet_manager.alien_bullets.empty()
            self.ai_game.meteor_manager.meteors.empty()
            self._respawn_ship()
        else:
            self.ai_game.game_active = False
            pygame.mouse.set_visible(True)

    def _respawn_ship(self):
        self.respawn_timer = None
        self.ship.center_ship()

    def _create_explosion(self, center):
        self.ai_game.explosion_manager.create_explosion(center)