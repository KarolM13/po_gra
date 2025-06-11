import pygame

class Screen:
    def __init__(self):
        self._width = 1280
        self._height = 720
        self.surface = pygame.display.set_mode((self._width, self._height))
        self.game_map = pygame.transform.scale(pygame.image.load("./assets/background.png"), (self._width, self._height))
        self.clock = pygame.time.Clock()
        
    def update(self):
        pygame.display.flip()
        self.clock.tick(60)
        