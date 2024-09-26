import pygame
from pygame.sprite import Sprite

class Powerups(Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.images = [pygame.image.load(f'images/powerup/powerup{i}.png') for i in range(1, 3)]
        self.images = [pygame.transform.scale(image, (30, 30)) for image in self.images]
        self.image = self.images[0]  # Set the initial image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 120  # Time in milliseconds between frames

        self.screen = ai_game.screen
        self.settings = ai_game.settings

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.image = self.images[0]
                self.frame = 0
            else:
                self.image = self.images[self.frame]

        # Update position
        self.rect.y += self.settings.meteor_speed

        # Remove the powerup if it moves off the screen
        if self.rect.top > self.screen.get_height():
            self.kill()