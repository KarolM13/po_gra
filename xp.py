import pygame

class XP:
    def __init__(self, x, y, value=100):
        self.x = x
        self.y = y
        self.value = value  # ile XP daje ten obiekt
        self.img = pygame.transform.scale(pygame.image.load("./assets/xp.png"), (50, 50))

    def draw(self, screen):
        screen.surface.blit(self.img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)