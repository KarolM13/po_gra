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
                        enemy.patrol(self.player)
                        if self.player.get_rect().colliderect(enemy.get_rect()):
                            print("Collision detected!")
                            enemy.attack(self.player)
                        new_enemies.append(enemy)
                    else:
                        print(f"Enemy died")
                        
                                   
                        self.xp_drops.append(XP(self.player, enemy.x, enemy.y))
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
                        self.player.xp += 10
                        xp_drop.add_xp(10)
                        self.xp_drops.remove(xp_drop)

                for enemy in self.enemies:
                    enemy.draw(self.screen)


                for weapon in self.player.weapons:
                    weapon.draw(self.screen)
                
                self.screen.draw_hud(self.player)
                self.player.draw(self.screen)
                self.screen.update()
           