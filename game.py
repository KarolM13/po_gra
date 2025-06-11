import pygame
from screen import Screen
def game():
    pygame.init()
    running = True
    screen = Screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.surface.blit(screen.game_map, (0, 0))
        pygame.display.flip()
        screen.clock.tick(screen.fps)