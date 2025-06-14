import pygame
import xp
class Screen:
    def __init__(self):
        self.upgrades = [
        {"name": "Runetracer", "description": "Passes through enemies, bounces around."},
        {"name": "Whip", "description": "Attacks horizontally, passes through enemies."},
        {"name": "Lightning Ring", "description": "Strikes at random enemies."}]   
        self._width = 1280
        self._height = 720
        self.surface = pygame.display.set_mode((self._width, self._height))
        self.game_map = pygame.transform.scale(pygame.image.load("./assets/background.png"), (self._width, self._height))
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60) / 1000.0 
        self.start_ticks = pygame.time.get_ticks()
        
    def update(self):
        pygame.display.flip()
        self.clock.tick(60)
    def draw_hud(self, player):
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player.health}/{player.max_health}", True, (255, 255, 255))
        level_text = font.render(f"Level: {player.level}", True, (255, 255, 255))
        self.surface.blit(health_text, (10, 10))
        self.surface.blit(level_text, (10, 40))
        # XP HUD - bez warunku, zawsze wyświetlaj
        xp_text = font.render(f"XP: {player.xp} / {player.xp_to_next_level}", True, (255, 255, 255))
        self.surface.blit(xp_text, (10, 70))
        # Liczenie czasu od startu gry
        total_seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        timer_text = font.render(f"Czas: {minutes:02}:{seconds:02}", True, (0, 0, 0))
        # Wyśrodkowanie na górze
        timer_rect = timer_text.get_rect(center=(self._width // 2, 20))
        self.surface.blit(timer_text, timer_rect)

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
        # Zerowanie czasu po pokazaniu game over
        self.start_ticks = pygame.time.get_ticks()
    def draw_level_up_menu(self, upgrades, selected_idx=None, player=None):
        # Pobierz rozmiar ekranu i przygotuj główny box menu
        screen_rect = self.surface.get_rect()
        width = 400
        height = 500
        box_rect = pygame.Rect(0, 0, width, height)
        box_rect.center = screen_rect.center
        pygame.draw.rect(self.surface, (40, 40, 90), box_rect)  # tło menu
        pygame.draw.rect(self.surface, (255, 200, 100), box_rect, 4)  # ramka menu
        # Tytuł menu
        font = pygame.font.Font(None, 41)
        title_text = font.render("LEVEL UP!", True, (255, 255, 255))
        tittle_rect = title_text.get_rect(center=(screen_rect.centerx, screen_rect.top + 60))
        self.surface.blit(title_text, tittle_rect)
        # Statystyki gracza po lewej stronie
        if player is not None:
            stat_font = pygame.font.Font(None, 28)
            stats = [
                f"HP: {player.health}/{player.max_health}",
                f"DMG: {getattr(player, 'damage', '?')}",
                f"Speed: {player.speed}"
            ]
            for i, stat in enumerate(stats):
                stat_text = stat_font.render(stat, True, (255, 255, 255))
                self.surface.blit(stat_text, (box_rect.left - 180, box_rect.top + 40 + i * 40))
        # Czcionka do przycisków
        font_small = pygame.font.Font(None, 21)
        self.button_rects = []  # lista prostokątów przycisków do obsługi kliknięć
        mouse_pos = pygame.mouse.get_pos()  # pozycja myszy
        button_width = 350
        button_height = 70
        total_buttons = len(upgrades)
        total_height = total_buttons * button_height + (total_buttons - 1) * 30
        start_y = screen_rect.centery - total_height // 2  # wyśrodkowanie pionowe
        for i, upgrade in enumerate(upgrades):
            # Wylicz pozycję każdego przycisku
            button_x = screen_rect.centerx - button_width // 2
            button_y = start_y + i * (button_height + 30)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.button_rects.append(button_rect)
            # Podświetlenie: jeśli najechane myszką lub wybrane klawiaturą
            hovered = button_rect.collidepoint(mouse_pos) or (selected_idx == i)
            color = (120, 120, 200) if hovered else (60, 60, 120)  # kolor tła przycisku
            border_color = (255, 255, 0) if hovered else (255, 255, 255)  # kolor ramki
            pygame.draw.rect(self.surface, color, button_rect)
            pygame.draw.rect(self.surface, border_color, button_rect, 4)
            # Tekst na przycisku
            upgrade_text = font_small.render(f"{i + 1}. {upgrade['name']}: {upgrade['description']}", True, (255, 255, 255))
            upgrade_rect = upgrade_text.get_rect(center=button_rect.center)
            self.surface.blit(upgrade_text, upgrade_rect)
