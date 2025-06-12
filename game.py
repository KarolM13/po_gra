import pygame
from screen import Screen
from player import Player
from enemy import Enemy
from character import Character
class Game:
    def __init__(self):
        pygame.init()
        self.screen = Screen()
        self.player = Player(100, 100) 
        self.running = True 
        self.enemy = Enemy(
            300,300)
        self.immunity_time = 0
        self.game_over = False
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
                            self.enemy = Enemy(300, 300)
                            self.game_over = False
                            self.immunity_time = 0

                if not self.game_over:
                    self.player.update()
                    self.enemy.patrol(self.player)

                    current_time = pygame.time.get_ticks()
                    if self.player.get_rect().colliderect(self.enemy.get_rect()) and current_time > self.immunity_time:
                        print("Collision detected!")
                        self.player.take_damage(self.enemy.damage)
                        self.immunity_time = pygame.time.get_ticks() + 1000

                    if self.player.health <= 0:
                        self.game_over = True

                if self.game_over:
                    self.screen.show_game_over()
                else:
                    self.screen.surface.blit(self.screen.game_map, (0, 0))
                    self.enemy.draw(self.screen)
                    self.screen.draw_hud(self.player)
                    self.player.draw(self.screen)
                    self.screen.update()





            
                
