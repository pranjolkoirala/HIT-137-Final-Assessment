import pygame



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./images/wall.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale the normal image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Set position of the obstacle

