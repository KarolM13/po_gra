import pygame 
from character import Character
class Player(Character):
    def __init__(self , x ,y):
        super().__init__(x, y , max_health=100, speed=10, size=100 , sprite_path="./assets/ziutek.png")
        self.experience = 0
        self.level = 1
        self.flip = pygame.transform.flip(self.sprite, True, False)
        self.img_back =pygame.transform.scale(pygame.image.load("./assets/ziutek_tyl.png"), (self.size, self.size))
        self.img_front = pygame.transform.scale(pygame.image.load("./assets/ziutek_przod.png"), (self.size, self.size))
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction_x = 0
        self.direction_y = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction_y -=1
            self.sprite = self.img_front
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction_y += 1
            self.sprite = self.img_back
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction_x -= 1
            self.sprite = self.flip
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction_x += 1
            self.sprite = pygame.transform.flip(self.flip, True, False)
        self.x += self.direction_x * self.speed 
        self.y += self.direction_y * self.speed
    def update(self):
        self.input()    
    