import pygame
from sprites.button import Button
from sprites.game_stats import GameStats
from sprites.scoreboard import ScoreBoard
from sprites.powerups import Powerups
from manager.explosion_manager import ExplosionManager
from random import random

class SpriteUpdateManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.ship = ai_game.ship_manager.ship
        self.aliens = ai_game.alien_manager.aliens
        self.bullets = ai_game.bullet_manager.bullets
        self.alien_bullets = ai_game.bullet_manager.alien_bullets
        self.meteors = ai_game.meteor_manager.meteors
        self.powerups = ai_game.powerup_manager.powerups
        self.play_button = Button(ai_game, "Play")
        self.stats = GameStats(ai_game)
        self.sb = ScoreBoard(ai_game)
        self.bg_image = pygame.image.load('images/background/background2.png')
        self.explosions = ai_game.explosion_manager.explosions

    def update(self):
        self.ship.update()
        self.bullets.update()
        self.alien_bullets.update()
        self.meteors.update()
        self.powerups.update()
        self.aliens.update()
        self.explosions.update()
        self.sb.update()

    def update_screen(self, screen, game_active):
        screen.blit(self.bg_image, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(screen)
        self.meteors.draw(screen)
        self.explosions.draw(screen)
        self.powerups.draw(screen)
        self.sb.show_score()
        self.ship.render()
        if not game_active:
            self.play_button.draw_button()
        pygame.display.flip()
