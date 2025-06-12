import pygame

class Screen:
    def __init__(self):
        
        self._width = 1280
        self._height = 720
        self.surface = pygame.display.set_mode((self._width, self._height))
        self.game_map = pygame.transform.scale(pygame.image.load("./assets/background.png"), (self._width, self._height))
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60) / 1000.0 
        
    def update(self):
        pygame.display.flip()
        self.clock.tick(60)
    def draw_hud(self, player):
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player.health}/{player.max_health}", True, (255, 255, 255))
        level_text = font.render(f"Level: {player.level}", True, (255, 255, 255))
        self.surface.blit(health_text, (10, 10))
        self.surface.blit(level_text, (10, 40))

    def show_game_over(self):
        self.surface.fill((0, 0, 0))

        font = pygame.font.Font(None, 74)
        text = font.render('GAME OVER', True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2))

        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render('Naciśnij R aby zacząć od nowa', True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.surface.get_width() // 2,
                                                     self.surface.get_height() // 2 + 60))

        self.surface.blit(text, text_rect)
        self.surface.blit(restart_text, restart_rect)
        pygame.display.update()

        