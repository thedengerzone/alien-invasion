import pygame


class Meteor(pygame.sprite.Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.images = [pygame.image.load(f'images/meteors/met{i}.png') for i in range(1, 5)]
        self.images = [pygame.transform.scale(image, (50, 50)) for image in self.images]
        self.image = self.images[0]  # Set the initial image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60  # Time in milliseconds between frames
        self.direction = x

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.velocity = self.settings.meteor_speed


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


        if self.direction == 0:
            # Update position
            self.rect.y += self.velocity
            self.rect.x += self.velocity
        else:
            self.rect.y += self.velocity
            self.rect.x -= self.velocity

    def draw_meteor(self):
        self.screen.blit(self.image, self.rect)
