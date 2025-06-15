import pygame
import random
from screen import Screen
from player import Player
from enemy import Enemy, TankEnemy, FastEnemy, NormalEnemy
from wand import Wand
from iceWand import IceWand
from magicBook import MagicBook
from character import Character
from xp import XP
from healthpotion import HealthPotion


class Game:
    def __init__(self):
        pygame.init()
        self.screen = Screen()
        self.player = Player(100, 100)
        self.running = True
        self.enemies = []
        self.start_time = pygame.time.get_ticks()
        self.immunity_time = 0
        self.game_over = False
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.enemy_spawn_cooldown = 3000
        self.max_enemies = 3
        self.xp_drops = []
        self.potions = []
        self.level_up_pending = False
        self.level_up_upgrades = []
        self.random_choices = [1,2,3,4,5,6,7,8,9,10]

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
            enemy_type = random.choice([TankEnemy, FastEnemy , NormalEnemy, FastEnemy , NormalEnemy, FastEnemy , NormalEnemy, FastEnemy , NormalEnemy  ])
            self.enemies.append(enemy_type(x, y))

    def game(self):
        selected_upgrade = None

        while self.running:
            elapsed_minutes = (pygame.time.get_ticks() - self.start_time) // 60000
            self.max_enemies = 10 + 5 * elapsed_minutes  # co 1 minuta +5 wrogów
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.player = Player(100, 100)
                        self.enemies = [Enemy(300, 300)]
                        self.xp_drops.clear()
                        self.potions.clear()
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


            if getattr(self.player, "weapon_choice_pending", False):
                weapon_classes = [Wand, IceWand, MagicBook]
                weapon_names = ["Wand", "IceWand", "MagicBook"]
                weapon_descriptions = [
                    "Szybkie pociski",
                    "Zamraża wrogów",
                    "Pociski w 6 kierunkach"
                ]
                upgrades = [
                    {"name": weapon_names[i], "description": weapon_descriptions[i]}
                    for i in range(len(weapon_classes))
                ]
                selected_weapon = 0
                choosing = True
                while choosing:
                    self.screen.surface.blit(self.screen.game_map, (0, 0))
                    self.screen.draw_level_up_menu(upgrades, selected_idx=selected_weapon, player=self.player)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            choosing = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key in [pygame.K_1, pygame.K_KP1]:
                                selected_weapon = 0
                            elif event.key in [pygame.K_2, pygame.K_KP2]:
                                selected_weapon = 1
                            elif event.key in [pygame.K_3, pygame.K_KP3]:
                                selected_weapon = 2
                            elif event.key == pygame.K_UP:
                                selected_weapon = (selected_weapon - 1) % len(upgrades)
                            elif event.key == pygame.K_DOWN:
                                selected_weapon = (selected_weapon + 1) % len(upgrades)
                            elif event.key == pygame.K_RETURN:
                                weapon_class = weapon_classes[selected_weapon]
                                self.player.equip_weapon(weapon_class())
                                self.player.weapon_choice_pending = False
                                choosing = False
                                self.player.weapon_choice_pending = False
                                choosing = False
                    self.screen.clock.tick(60)
                continue

            if self.level_up_pending:
                if selected_upgrade is None:
                    selected_upgrade = 0
                self.screen.surface.blit(self.screen.game_map, (0, 0))
                self.screen.draw_level_up_menu(self.level_up_upgrades, selected_idx=selected_upgrade, player=self.player)
                pygame.display.flip()
                continue

            if not self.game_over:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_enemy_spawn_time >= self.enemy_spawn_cooldown and len(self.enemies) < self.max_enemies:
                    enemies_to_spawn = min(3, self.max_enemies - len(self.enemies))
                    self.spawn_enemy(enemies_to_spawn)
                    self.last_enemy_spawn_time = current_time

                self.player.update(self.enemies)

                new_enemies = []
                for enemy in self.enemies:
                    if enemy.alive:
                        enemy.patrol(self.player, self.enemies)
                        if self.player.get_rect().colliderect(enemy.get_rect()):
                            print("Collision detected!")
                            enemy.attack(self.player)
                        new_enemies.append(enemy)
                    else:
                        print(f"Enemy died")
                        if random.choice(self.random_choices) == 3:
                            self.potions.append(HealthPotion(enemy.x, enemy.y, value=20))
                        else:
                            xp_value = 11202
                            if isinstance(enemy, TankEnemy):
                                xp_value = 11502
                            self.xp_drops.append(XP(enemy.x, enemy.y, value=xp_value))
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
                            if self.player.level % 5 == 0:
                                self.player.weapon_choice_pending = True
                        self.xp_drops.remove(xp_drop)
                for potion in self.potions[:]:
                    potion.draw(self.screen)
                    if self.player.get_rect().colliderect(potion.get_rect()) and self.player.health < self.player.max_health:
                        self.player.heal(potion.value)
                        self.potions.remove(potion)

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
            self.player.damage += 5
            for w in self.player.weapons:
                w.damage += 5
        elif upgrade["name"] == "Szybkość":
            self.player.speed += 2
        self.level_up_pending = False
        self.level_up_upgrades = []