import pygame
class Character:
    def __init__(self , x ,y = 0,delta_time=0, max_health = 100, speed = 5, size = 50 , damage = 10, range = 100, sprite_path = None):
       
        self.x = x
        self.y = y       
        self.max_health = max_health
        self.health = max_health
        self.speed = speed
        self. size = size
        
        self.alive = True
        self.direction_x = 0
        self.direction_y = 0
        self.sprite = None
        self.sprite_rect = None

        self.damage = damage
        self.range = range
        try:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
            self.sprite_rect = self.sprite.get_rect()
        except pygame.error as e:
            print(f"Error loading sprite: {e}")
            self.sprite = None
            self.sprite_rect = None
            
    def draw(self ,screen):
        screen.surface.blit(self.sprite, (self.x, self.y))

    def move(self):
        self.x += self.direction_x * self.speed 
        self.y += self.direction_y * self.speed

    def die(self):
        self.alive = False
        self.health = 0
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()
    def heal(self, amount):
        if self.alive:
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health
    

    def collide(self, other):
        if self.sprite_rect and other.sprite_rect:
            return self.sprite_rect.colliderect(other.sprite_rect)
        return False