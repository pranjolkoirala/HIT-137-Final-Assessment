import pygame
import random

# Initialize Pygame
pygame.init()


from classes.playerTank import PlayerTank
from classes.obstacle import Obstacle
from classes.projectile import Projectile
from classes.enemy import EnemyTank
from classes.boss import BossEnemy
from constant import SCREEN_WIDTH, SCREEN_HEIGHT,FPS,WHITE,OBSTACLE_COORDINATES,ENEMIES_IN_LEVEL_1,ENEMIES_IN_LEVEL_2,ENEMIES_IN_LEVEL_3,BOSS_HEALTH



#Background music
pygame.mixer.music.load('./audio/background_music.mp3')  
pygame.mixer.music.set_volume(0.2) # Set volume to 20% of its full level
pygame.mixer.music.play(-1)  # Loop the music indefinitely


obstacles = pygame.sprite.Group()



# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Battle Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()



def game_loop():

    #Text to show when game is over
    GAME_OVER_TEXT = "Game Over! Press R to Restart"
    # Initialize variables for level management
    level = 1
    enemies_per_level_1 = ENEMIES_IN_LEVEL_1  # Number of enemies for Level 1
    enemies_per_level_2 = ENEMIES_IN_LEVEL_2 # Number of enemies for Level 2
    enemies_per_level_3 = ENEMIES_IN_LEVEL_3 # Number of enemies for Level 3
    boss_hits_required = BOSS_HEALTH  # Number of hits required to kill the boss
    total_enemies = enemies_per_level_1  # Start with Level 1 enemy count
    

    # Background Image
    background_image = pygame.image.load('./images/background.png').convert()   
    
    player = PlayerTank(100, SCREEN_HEIGHT - 50)
    player_group = pygame.sprite.Group(player)

    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
  
    boss = None
    score = 0
    running = True
    game_over = False
    # Create initial enemies for level 1
    for _ in range(total_enemies):
        enemy = EnemyTank( level)
        enemies.add(enemy)

    

    # Add obstacles at specific positions (x, y)
    for obs_cor in OBSTACLE_COORDINATES:
        obstacles.add(Obstacle(obs_cor[0],obs_cor[1]))
   
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over and event.key == pygame.K_SPACE:
                    # Create a projectile that fires in the direction the tank is facing
                    projectile = Projectile(player.rect.centerx, player.rect.centery, player.direction)
                    projectiles.add(projectile)

                # Jump to Level 3 if '1' is pressed
                if event.key == pygame.K_1:
                    level = 3
                    total_enemies = enemies_per_level_3
                    enemies.empty()  # Clear any existing enemies
                    boss = BossEnemy( level, boss_hits_required)  # Create the boss
                    enemies.add(boss)  # Add boss to enemies
                    # Create additional regular enemies for level 3
                    for _ in range(total_enemies - 1):  # One less for the boss
                        enemy = EnemyTank( level)
                        enemies.add(enemy)

                # Restart the game if game over and player presses R
                if game_over and event.key == pygame.K_r:
                    GAME_OVER_TEXT = "Game Over! Press R to Restart"
                    game_loop()  # Restart the game loop
                    return

        if not game_over:
            # Update game objects
            player_group.update(obstacles)
            projectiles.update(obstacles)
            enemies.update(obstacles)

            # Check for collision between player and enemy tanks
            if pygame.sprite.spritecollideany(player, enemies):
                game_over = True

            # Check for projectile and enemy collisions
            for projectile in projectiles:
                hit_enemies = pygame.sprite.spritecollide(projectile, enemies, False)
                for enemy in hit_enemies:
                    projectile.kill()  # Destroy the projectile on hit
                    if enemy.hit():  # Reduce enemy health and check if it was killed
                        score += 10  # Increment score for killing an enemy
                        break  # Break after the first hit to prevent multiple kills with one projectile

            # Check if boss is hit
            if boss and pygame.sprite.spritecollideany(boss, projectiles):
                if boss.hit():  # Reduce boss health and check if it was killed
                    score += 50  # Increment score for killing the boss
                    boss = None  # Remove the boss

            # Check if all enemies are killed to proceed to the next level
            if len(enemies) == 0 :  
                if level < 3 : # Level 3 does not have a next level
                    pygame.time.wait(1000)  # Wait for 1 second before transitioning to the next level
                    level += 1
                    if level == 2:
                        total_enemies = enemies_per_level_2
                    elif level == 3:
                        total_enemies = enemies_per_level_3                    
                    enemies.empty()  # Clear any existing enemies
                    # Create new enemies for the next level
                    for _ in range(total_enemies):
                        enemy = EnemyTank( level)
                        enemies.add(enemy)
                    if level==3:
                        # if its level 3, add a boss
                        boss = BossEnemy( level, boss_hits_required) 
                        enemies.add(boss)
                else:
                    GAME_OVER_TEXT= "Congratulations!! Press R to start again"
                    game_over = True

        # Draw everything
        screen.blit(background_image, (0, 0))  # Draw the background image
        player_group.draw(screen)
        projectiles.draw(screen)
        enemies.draw(screen)
        obstacles.draw(screen) 

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display current level
        level_text = font.render(f'Level: {level}', True, WHITE)
        screen.blit(level_text, (10, 50))

        # Display game over message
        if game_over:
            game_over_text = font.render(GAME_OVER_TEXT, True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
            control_text = font.render("Use arrows to move and space to shoot.", True, WHITE)
            screen.blit(control_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT -50 ))

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Limit frame rate

    pygame.quit()

# Start the game loop
game_loop()