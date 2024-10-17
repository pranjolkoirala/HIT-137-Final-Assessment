import pygame
import random
from constant import SCREEN_WIDTH, SCREEN_HEIGHT,OBSTACLE_COORDINATES

# Hitting Enemy Sound
hit_enemy = pygame.mixer.Sound('./question_pygame/audio/enemy_hit.mp3') 
hit_enemy.set_volume(0.3)  # Adjust the volume as needed

class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        # Load enemy tank images
        self.image_normal = pygame.image.load('./question_pygame/images/enemy.png').convert_alpha()
        self.image_weak = pygame.image.load('./question_pygame/images/enemy_weak.png').convert_alpha()
        x,y = get_valid_enemy_position(OBSTACLE_COORDINATES,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.image = pygame.transform.scale(self.image_normal, (50, 30))  # Scale the normal image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 3 + level  # Increase speed based on level
        self.health = 1 if level == 1 else 2  # 1 hit to kill in level 1, 2 hits in level 2

        # Random initial movement direction
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # right, left, down, up
        self.change_direction_timer = 0  # Timer to change direction

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

    def hit(self):
        """Decrease health and return True if enemy is killed."""
        self.health -= 1
        if self.health <= 0:
            hit_enemy.play()
            self.kill()  # Remove enemy if health is 0
            return True  # Indicate that the enemy was killed
        else:
            # Change to the weak enemy image when hit once
            self.image = pygame.transform.scale(self.image_weak, (50, 30))  # Scale the weak image
            return False  # Indicate that the enemy is still alive



def get_valid_enemy_position(obstacle_coords, screen_width, screen_height, buffer_distance=50, enemy_size=(50, 30)):
    """
    Generate a valid coordinate for the enemy tank that does not overlap with obstacles.

    Parameters:
    - obstacle_coords: A list of tuples representing obstacle positions (x, y).
    - screen_width: The width of the screen.
    - screen_height: The height of the screen.
    - buffer_distance: The minimum distance the enemy must spawn away from obstacles and edges.
    - enemy_size: A tuple representing the size of the enemy tank (width, height).

    Returns:
    - (x, y): A tuple representing the valid coordinate for the enemy tank.
    """
    enemy_width, enemy_height = enemy_size

    while True:
        # Randomly generate x and y coordinates
        x = random.randint(buffer_distance, screen_width - buffer_distance - enemy_width)
        y = random.randint(buffer_distance, screen_height - buffer_distance - enemy_height)

        # Check if the new enemy coordinates overlap with any obstacles
        overlap = False
        for obs_x, obs_y in obstacle_coords:
            # Check for collision based on size of the enemy tank
            if (x < obs_x + enemy_width and x + enemy_width > obs_x and
                y < obs_y + enemy_height and y + enemy_height > obs_y):
                overlap = True
                break
        
        if not overlap:
            return x, y
