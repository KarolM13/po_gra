import pygame 
from character import Character
class Player(Character):
    def __init__(self , x ,y):
        super().__init__(x, y , max_health=100, speed=5, size=100 , sprite_path="./assets/ziutek.png")
        self.experience = 0
        self.level = 1
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction_x = 0
        self.direction_y = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction_y -=1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction_y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction_x += 1
        self.x += self.direction_x * self.speed 
        self.y += self.direction_y * self.speed
    def update(self):
        self.input()    
    