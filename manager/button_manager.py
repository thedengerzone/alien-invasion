# manager/button_manager.py
import pygame
from sprites.button import Button

class ButtonManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.play_button = Button(ai_game, "Play")

    def draw_buttons(self):
        if not self.ai_game.game_active:
            self.play_button.draw_button()

    def check_play_button(self):
        if not self.ai_game.game_active:
            self.ai_game.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            self.ai_game.stats.reset_stats()
            self.ai_game.scoreboard_manager.scoreboard.prep_score()
            self.ai_game.scoreboard_manager.scoreboard.prep_level()
            self.ai_game.scoreboard_manager.scoreboard.prep_ships()
            self.ai_game.game_active = True

            self.ai_game.sprite_manager.aliens.empty()
            self.ai_game.bullet_manager.bullets.empty()

            self.ai_game.alien_manager.create_fleet()
            self.ai_game.ship_manager.ship.center_ship()