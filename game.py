import pygame
from screen import Screen
from player import Player
class Game:
    def __init__(self):
        pygame.init()
        self.screen = Screen()
        self.player = Player(100, 100) 
        self.running = True 
    def game(self):
        while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    # Dodaj ESC do zamykania
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                
                # Aktualizuj gracza
                self.player.update()
                
                # Rysuj wszystko
                self.screen.surface.blit(self.screen.game_map, (0, 0))
                self.player.draw(self.screen)
                self.screen.update()