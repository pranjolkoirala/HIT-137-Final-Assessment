import pygame
from constant import SCREEN_WIDTH, SCREEN_HEIGHT

# Shooting Sound
shooting_sound = pygame.mixer.Sound('./question_pygame/audio/gun_sound.mp3')
shooting_sound.set_volume(0.3)  # Adjust the volume as needed


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 0))  # Yellow color for the projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction  # direction should be a tuple like (1, 0) for right
        shooting_sound.play()


    def update(self,obstacles):
        # Move projectile
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Check for collision with obstacles
        if pygame.sprite.spritecollideany(self, obstacles):
            self.kill()  # Destroy projectile on hit

        # Remove projectile if it goes off screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.kill()
