import pygame

from game_stats import GameStats
from manager.alien_manager import AlienManager
from manager.bullet_manager import BulletManager
from manager.button_manager import ButtonManager
from manager.key_event_manager import KeyEventManager
from manager.meteor_manager import MeteorManager
from manager.powerup_manager import PowerupManager
from manager.sprite_manager import SpriteUpdateManager
from manager.explosion_manager import ExplosionManager
from manager.ship_manager import ShipManager
from manager.scoreboard_manager import ScoreBoardManager
from settings import Settings


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1024, 1024))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.bullet_manager = BulletManager(self)
        self.alien_manager = AlienManager(self)
        self.meteor_manager = MeteorManager(self)
        self.powerup_manager = PowerupManager(self)
        self.explosion_manager = ExplosionManager(self)
        self.ship_manager = ShipManager(self)
        self.button_manager = ButtonManager(self)
        self.scoreboard_manager = ScoreBoardManager(self)
        self.event_manager = KeyEventManager(self)
        self.sprite_manager = SpriteUpdateManager(self)

        self.game_active = False

        self.alien_manager.create_fleet()

    def run_game(self):
        while True:
            self.event_manager.check_events(self)

            if self.game_active:
                self.sprite_manager.update()
                self.bullet_manager.fire_alien_bullet()
                self.bullet_manager.update_bullets()
                self.alien_manager.update_aliens()
                self.meteor_manager.spawn_meteors()
                self.meteor_manager.update_meteors()

            self.sprite_manager.update_screen(self.screen, self.game_active)
            self.clock.tick(60)

if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()