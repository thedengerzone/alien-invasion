import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = [pygame.image.load(f'images/explosions/ex{i}.png') for i in range(1, 7)]
        self.images = [pygame.transform.scale(image, (75, 75)) for image in self.images]
        self.image = self.images[0]  # Set the initial image
        self.rect = self.image.get_rect(center=center)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # Time in milliseconds between frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame]