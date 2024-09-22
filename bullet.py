import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship or aliens"""

    def __init__(self, ai_game, x, y, direction):
        """Create a bullet object at the given position with the specified direction"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.direction = direction

        # Load the bullet image, scale it, and set its rect attribute
        self.image = pygame.image.load('images/bullet.png')
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y) if direction == 'up' else (x, y)

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up or down the screen"""
        # Update the exact position of the bullet
        if self.direction == 'up':
            self.y -= self.settings.bullet_speed
        else:
            self.y += self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.image, self.rect)