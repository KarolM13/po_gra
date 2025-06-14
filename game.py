import pygame
import random
from screen import Screen
from player import Player
from enemy import Enemy
from wand import Wand
from character import Character
from xp import XP


class Game:
    def __init__(self):
        pygame.init()
        self.screen = Screen()
        self.player = Player(100, 100)
        self.running = True
        self.enemies = [Enemy(300, 300)]
        self.immunity_time = 0
        self.game_over = False
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.enemy_spawn_cooldown = 3000
        self.max_enemies = 10
        self.xp_drops = []
        self.level_up_pending = False
        self.level_up_upgrades = []

    def spawn_enemy(self, count=1):
        for _ in range(count):
            side = random.randint(0, 3)
            if side == 0:
                x = random.randint(0, self.screen._width)
                y = -100
            elif side == 1:
                x = self.screen._width + 100
                y = random.randint(0, self.screen._height)
            elif side == 2:
                x = random.randint(0, self.screen._width)
                y = self.screen._height + 100
            else:
                x = -100
                y = random.randint(0, self.screen._height)
            self.enemies.append(Enemy(x, y))

    def game(self):
        selected_upgrade = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.player = Player(100, 100)
                        self.enemies = [Enemy(300, 300)]
                        self.game_over = False
                        self.immunity_time = 0
                    # Obsługa wyboru ulepszenia klawiaturą
                    if self.level_up_pending:
                        if event.key in [pygame.K_1, pygame.K_KP1]:
                            self.apply_upgrade(0)
                        elif event.key in [pygame.K_2, pygame.K_KP2]:
                            self.apply_upgrade(1)
                        elif event.key in [pygame.K_3, pygame.K_KP3]:
                            self.apply_upgrade(2)
                        elif event.key == pygame.K_UP:
                            if selected_upgrade is None:
                                selected_upgrade = 0
                            selected_upgrade = (selected_upgrade - 1) % len(self.level_up_upgrades)
                        elif event.key == pygame.K_DOWN:
                            if selected_upgrade is None:
                                selected_upgrade = 0
                            selected_upgrade = (selected_upgrade + 1) % len(self.level_up_upgrades)
                        elif event.key == pygame.K_RETURN:
                            if selected_upgrade is None:
                                selected_upgrade = 0
                            self.apply_upgrade(selected_upgrade)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.level_up_pending:
                    mouse_pos = pygame.mouse.get_pos()
                    for idx, rect in enumerate(self.screen.button_rects):
                        if rect.collidepoint(mouse_pos):
                            self.apply_upgrade(idx)

            if self.level_up_pending:
                if selected_upgrade is None:
                    selected_upgrade = 0
                self.screen.surface.blit(self.screen.game_map, (0, 0))
                # Przekazujemy player do draw_level_up_menu, żeby wyświetlić statystyki
                self.screen.draw_level_up_menu(self.level_up_upgrades, selected_idx=selected_upgrade, player=self.player)
                pygame.display.flip()
                continue

            if not self.game_over:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_enemy_spawn_time >= self.enemy_spawn_cooldown and len(self.enemies) < self.max_enemies:
                    enemies_to_spawn = min(3, self.max_enemies - len(self.enemies))  # spawn do 3 naraz
                    self.spawn_enemy(enemies_to_spawn)
                    self.last_enemy_spawn_time = current_time

                self.player.update(self.enemies)
                

                new_enemies = []
                for enemy in self.enemies:
                    if enemy.alive:
                        # Przekazujemy listę wszystkich wrogów do patrol, żeby nie wchodziły w siebie
                        enemy.patrol(self.player, self.enemies)
                        if self.player.get_rect().colliderect(enemy.get_rect()):
                            print("Collision detected!")
                            enemy.attack(self.player)
                        new_enemies.append(enemy)
                    else:
                        print(f"Enemy died")
                        # Dodajemy XP drop na pozycji wroga, domyślnie 10 XP
                        self.xp_drops.append(XP(enemy.x, enemy.y, value=100))
                self.enemies = new_enemies
                
                    
                if self.player.health <= 0:
                    self.game_over = True

            if self.game_over:
                self.screen.show_game_over()
                self.xp_drops.clear()  
            else:
                self.screen.surface.blit(self.screen.game_map, (0, 0))            
                for xp_drop in self.xp_drops[:]:
                    xp_drop.draw(self.screen)
                    if self.player.get_rect().colliderect(xp_drop.get_rect()):
                        self.player.xp += xp_drop.value
                        if self.player.xp >= self.player.xp_to_next_level:
                            self.player.xp -= self.player.xp_to_next_level
                            self.player.level += 1
                            self.player.xp_to_next_level = int(self.player.xp_to_next_level * 1.5)
                            self.level_up_pending = True
                            self.level_up_upgrades = [
                                {"name": "Zdrowie", "description": "Zwiększ maksymalne zdrowie o 20"},
                                {"name": "Obrażenia", "description": "Zwiększ obrażenia o 5"},
                                {"name": "Szybkość", "description": "Zwiększ szybkość ruchu o 2"}
                            ]
                        self.xp_drops.remove(xp_drop)

                for enemy in self.enemies:
                    enemy.draw(self.screen)


                for weapon in self.player.weapons:
                    weapon.draw(self.screen)
                
                self.screen.draw_hud(self.player)
                self.player.draw(self.screen)
                self.screen.update()

    def apply_upgrade(self, idx):
        upgrade = self.level_up_upgrades[idx]
        if upgrade["name"] == "Zdrowie":
            self.player.max_health += 20
            self.player.health += 20
        elif upgrade["name"] == "Obrażenia":
            self.player.damage += 5  # Zwiększ DMG gracza (do statystyk)
            for w in self.player.weapons:
                w.damage += 5  # Zwiększ DMG broni
        elif upgrade["name"] == "Szybkość":
            self.player.speed += 2
        self.level_up_pending = False
        self.level_up_upgrades = []
