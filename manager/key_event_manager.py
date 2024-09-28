import sys

import pygame


class KeyEventManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game

    def check_events(self, ai_game):
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ai_game.ship_manager.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ai_game.ship_manager.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ai_game.ship_manager.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ai_game.ship_manager.ship.moving_down = True
        if event.key == pygame.K_SPACE:
            self.ai_game.bullet_manager.fire_bullet()
        if event.key == pygame.K_RETURN:
            self.ai_game.button_manager.check_play_button()
        if event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ai_game.ship_manager.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ai_game.ship_manager.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ai_game.ship_manager.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ai_game.ship_manager.ship.moving_down = False
