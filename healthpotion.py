import pygame

class HealthPotion:
    def __init__(self, x, y, value=10):
        self.x = x
        self.y = y
        self.value = value
        self.img = pygame.transform.scale(pygame.image.load("./assets/potion.png"), (50, 50))

    def draw(self, screen):
        screen.surface.blit(self.img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)