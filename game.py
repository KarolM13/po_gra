import pygame
from screen import Screen
from player import Player
class Game:
    def __init__(self):
        pygame.init()
        self.screen = Screen()
        self.player = Player(100, 100) 
        self.running = True 
    def game():
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.surface.blit(self.screen.game_map, (0, 0))
            pygame.display.flip()
            self.screen.clock.tick(self.screen.fps)