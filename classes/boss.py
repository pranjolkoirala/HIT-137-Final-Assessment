import pygame
import random
from constant import SCREEN_WIDTH, SCREEN_HEIGHT
from classes.enemy import EnemyTank
class BossEnemy(EnemyTank):
    def __init__(self, level, hits_required):
        super().__init__( level)
        self.image.fill((0, 0, 255))  # Different color (blue) for the boss
        self.speed = 3 + level  # Boss speed
        self.health = hits_required  # Set health based on hits required
        self.image_normal = pygame.image.load('./images/boss.png').convert_alpha()
        self.image_weak = pygame.image.load('./images/boss.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_normal, (50, 50))  # Scale the normal image
        self.rect = self.image.get_rect()

    def update(self,obstacles):
        # Change direction randomly after a set time
        self.change_direction_timer += 1
        if self.change_direction_timer > random.randint(30, 90):  # Change direction every 30 to 90 frames
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.change_direction_timer = 0

        # Save the original position in case of collision
        original_rect = self.rect.copy()

        # Update position based on direction
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Check for collisions with obstacles
        if pygame.sprite.spritecollideany(self, obstacles):
            self.rect = original_rect  # Revert to the original position
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # Change to a new random direction

        # Prevent the enemy from moving out of the screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction = (-self.direction[0], self.direction[1])  # Reverse direction on x-axis
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])  # Reverse direction on y-axis
