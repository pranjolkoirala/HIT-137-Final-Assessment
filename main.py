import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Battle Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load tank images
        self.image_right = pygame.image.load('./images/tank_right.png').convert_alpha()
        self.image_left = pygame.image.load('./images/tank_left.png').convert_alpha()
        self.image_up = pygame.image.load('./images/tank_up.png').convert_alpha()
        self.image_down = pygame.image.load('./images/tank_down.png').convert_alpha()

        # Scale images to appropriate size
        self.image_right = pygame.transform.scale(self.image_right, (50, 30))
        self.image_left = pygame.transform.scale(self.image_left, (50, 30))
        self.image_up = pygame.transform.scale(self.image_up, (50, 30))
        self.image_down = pygame.transform.scale(self.image_down, (50, 30))

        self.image = self.image_right  # Set the initial image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.health = 100
        self.lives = 3
        self.direction = (1, 0)  # Initially facing right


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = (-1, 0)  # Facing left
            self.image = self.image_left  # Set image to left-facing tank
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = (1, 0)  # Facing right
            self.image = self.image_right  # Set image to right-facing tank
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = (0, -1)  # Facing up
            self.image = self.image_up  # Set image to up-facing tank
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = (0, 1)  # Facing down
            self.image = self.image_down  # Set image to down-facing tank

        # Prevent the tank from moving out of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
      


class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        super().__init__()
        # Load enemy tank images
        self.image_normal = pygame.image.load('./images/enemy.png').convert_alpha()
        self.image_weak = pygame.image.load('./images/enemy_weak.png').convert_alpha()
        
        self.image = pygame.transform.scale(self.image_normal, (50, 30))  # Scale the normal image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 3 + level  # Increase speed based on level
        self.health = 1 if level == 1 else 2  # 1 hit to kill in level 1, 2 hits in level 2

        # Random initial movement direction
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # right, left, down, up
        self.change_direction_timer = 0  # Timer to change direction

    def update(self):
        # Change direction randomly after a set time
        self.change_direction_timer += 1
        if self.change_direction_timer > random.randint(30, 90):  # Change direction every 30 to 90 frames
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            self.change_direction_timer = 0

        # Update position based on direction
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Prevent the enemy from moving out of the screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction = (-self.direction[0], self.direction[1])  # Reverse direction on x-axis
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction = (self.direction[0], -self.direction[1])  # Reverse direction on y-axis

    def hit(self):
        """Decrease health and return True if enemy is killed."""
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Remove enemy if health is 0
            return True  # Indicate that the enemy was killed
        else:
            # Change to the weak enemy image when hit once
            self.image = pygame.transform.scale(self.image_weak, (50, 30))  # Scale the weak image
            return False  # Indicate that the enemy is still alive




class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 0))  # Yellow color for the projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.direction = direction  # direction should be a tuple like (1, 0) for right

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Remove projectile if it goes off screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


def game_loop():
    # Initialize variables for level management
    enemies_killed = 0    
    player = PlayerTank(100, SCREEN_HEIGHT - 50)
    player_group = pygame.sprite.Group(player)

    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    boss = None

    for _ in range(5):
        enemy = EnemyTank(random.randint(100, 700), random.randint(50, SCREEN_HEIGHT - 50), 1)
        enemies.add(enemy)

    score = 0
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over and event.key == pygame.K_SPACE:
                    # Create a projectile that fires in the direction the tank is facing
                    projectile = Projectile(player.rect.centerx, player.rect.centery, player.direction)
                    projectiles.add(projectile)

        

        if not game_over:
            # Update game objects
            player_group.update()
            projectiles.update()
            enemies.update()



        # Draw everything
        screen.fill(BLACK)  # Clear screen with black color
        player_group.draw(screen)
        projectiles.draw(screen)
        enemies.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display game over message
        if game_over:
            game_over_text = font.render('Game Over! Press R to Restart', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Limit frame rate

    pygame.quit()


game_loop()

