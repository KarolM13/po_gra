import pygame
import xp
class Screen:
    def __init__(self):
        self.upgrades = [
        {"name": "Runetracer", "description": "Passes through enemies, bounces around."},
        {"name": "Whip", "description": "Attacks horizontally, passes through enemies."},
        {"name": "Lightning Ring", "description": "Strikes at random enemies."}]   
        self._width = 1980
        self._height = 1080
        self.surface = pygame.display.set_mode((self._width, self._height))
        self.game_map = pygame.transform.scale(pygame.image.load("./assets/background.png"), (self._width, self._height))
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(60) / 1000.0 
        self.start_ticks = pygame.time.get_ticks()
        self.menu_background = pygame.transform.scale(pygame.image.load("./assets/menu_background.png"), (self._width, self._height))
        self.gameover_background = pygame.transform.scale(pygame.image.load("./assets/gameover_background.png"), (self._width, self._height))
        self.menu_music_path = "./assets/menu_start.mp3"
        self.gameover_music_path = "./assets/game_over.mp3"
        self.victory_background = pygame.transform.scale(
            pygame.image.load("./assets/victory.png"), (self._width, self._height)
        )
    def update(self):
        pygame.display.flip()
        self.clock.tick(60)

    def draw_hud(self, player):
        font = pygame.font.Font(None, 28)
        offset_x = 50
        offset_y = 40

        # Pasek HP
        bar_width = 300
        bar_height = 30
        hp_ratio = player.health / player.max_health if player.max_health > 0 else 0
        hp_bar_rect = pygame.Rect(10 + offset_x, 10 + offset_y, bar_width, bar_height)
        pygame.draw.rect(self.surface, (60, 60, 60), hp_bar_rect)  # tło
        pygame.draw.rect(self.surface, (200, 0, 0),
                         (10 + offset_x, 10 + offset_y, int(bar_width * hp_ratio), bar_height))  # pasek HP
        hp_text = font.render(f"HP: {player.health}/{player.max_health}", True, (255, 255, 255))
        self.surface.blit(hp_text, (15 + offset_x, 15 + offset_y))

        # Pasek XP
        xp_bar_rect = pygame.Rect(10 + offset_x, 50 + offset_y, bar_width, bar_height)
        xp_ratio = player.xp / player.xp_to_next_level if player.xp_to_next_level > 0 else 0
        pygame.draw.rect(self.surface, (60, 60, 60), xp_bar_rect)  # tło
        pygame.draw.rect(self.surface, (0, 120, 255),
                         (10 + offset_x, 50 + offset_y, int(bar_width * xp_ratio), bar_height))  # pasek XP
        xp_text = font.render(f"XP: {player.xp}/{player.xp_to_next_level}", True, (255, 255, 255))
        self.surface.blit(xp_text, (15 + offset_x, 55 + offset_y))

        # Poziom gracza
        level_text = font.render(f"Level: {player.level}", True, (255, 255, 255))
        self.surface.blit(level_text, (10 + offset_x, 90 + offset_y))

        # Timer
        total_seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        timer_text = font.render(f"Czas: {minutes:02}:{seconds:02}", True, (0, 0, 0))
        timer_rect = timer_text.get_rect(center=(self._width // 2, 20 + offset_y))
        self.surface.blit(timer_text, timer_rect)



    def draw_boss_hp_bar(self, boss):
        bar_width = 800
        bar_height = 40
        x = (self._width - bar_width) // 2
        y = self._height - bar_height - 30  # 30 px od dołu
        hp_ratio = boss.health / boss.max_health if boss.max_health > 0 else 0
        pygame.draw.rect(self.surface, (60, 60, 60), (x, y, bar_width, bar_height))  # tło
        pygame.draw.rect(self.surface, (200, 0, 0), (x, y, int(bar_width * hp_ratio), bar_height))  # pasek HP
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f"BOSS HP: {int(boss.health)}/{boss.max_health}", True, (255, 255, 255))
        self.surface.blit(hp_text, (x + 20, y + 5))

    def show_game_over(self):  
        if not hasattr(self, "_gameover_music_played") or not self._gameover_music_played:
            pygame.mixer.music.load(self.gameover_music_path)
            pygame.mixer.music.play()
            self._gameover_music_played = True

        self.surface.blit(self.gameover_background, (0, 0))
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

    def show_victory(self):
        self.surface.blit(self.victory_background, (0, 0))
        pygame.display.update()
        pygame.time.wait(5000)

    def draw_start_menu(self):
        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.02)
        self.surface.blit(self.menu_background, (0, 0))
        font = pygame.font.Font(None, 74)
        title_text = font.render('BURATO SURVIVORS', True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 2 - 300))

        font_small = pygame.font.Font(None, 36)
        start_text = font_small.render('Naciśnij ENTER aby rozpocząć', True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(self.surface.get_width() // 2,
                                                  self.surface.get_height() // 2 + 60))

        # Rysowanie dużego czerwonego X w prawym górnym rogu
        x_size = 80
        x_margin = 30
        x_rect = pygame.Rect(self._width - x_size - x_margin, x_margin, x_size, x_size)
        pygame.draw.rect(self.surface, (200, 0, 0), x_rect, border_radius=18)
        x_font = pygame.font.Font(None, 90)
        x_text = x_font.render('X', True, (255, 255, 255))
        x_text_rect = x_text.get_rect(center=x_rect.center)
        self.surface.blit(x_text, x_text_rect)
        self.menu_x_rect = x_rect  # zapisz do obsługi kliknięcia

        self.surface.blit(title_text, title_rect)
        self.surface.blit(start_text, start_rect)
        pygame.display.update()
