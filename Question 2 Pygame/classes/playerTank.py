import pygame
from constant import SCREEN_WIDTH, SCREEN_HEIGHT


class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load tank images
        self.image_right = pygame.image.load('./images/tank_right.png').convert_alpha()
        self.image_left = pygame.image.load('./images/tank_left.png').convert_alpha()
        self.image_up = pygame.image.load('./images/tank_up.png').convert_alpha()
        self.image_down = pygame.image.load('./images/tank_down.png').convert_alpha()

        # Scale images to appropriate size
        self.image_right = pygame.transform.scale(self.image_right, (50, 40))
        self.image_left = pygame.transform.scale(self.image_left, (50, 40))
        self.image_up = pygame.transform.scale(self.image_up, (50, 40))
        self.image_down = pygame.transform.scale(self.image_down, (50, 40))

        self.image = self.image_right  # Set the initial image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.health = 100
        self.lives = 3
        self.direction = (1, 0)  # Initially facing right


    def update_player_movement(self,obstacles):
        keys = pygame.key.get_pressed()
        original_rect = self.rect.copy()  # Save the original position
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = (-1, 0)  # Facing left
            self.image = self.image_left
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = (1, 0)  # Facing right
            self.image = self.image_right
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = (0, -1)  # Facing up
            self.image = self.image_up
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = (0, 1)  # Facing down
            self.image = self.image_down

        # Check for collisions with obstacles
        if pygame.sprite.spritecollideany(self, obstacles):
            self.rect = original_rect  # Revert to the original position if there’s a collision

    # In the PlayerTank class, replace the `update` method with the following:
    def update(self,obstacles):
        self.update_player_movement(obstacles)
        # Prevent the tank from moving out of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
