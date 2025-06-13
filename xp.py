import pygame

class XP:
    def __init__(self, player,x,y):
        self.player = player
        self.xp = 0
        self.level = 1
        self.xp_to_next_level = 100
        self.img = pygame.transform.scale(pygame.image.load("./assets/xp.png"), (50, 50))
        self.x = x
        self.y = y
        
    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)  
        print(f"Level up! Now at level {self.level}. XP to next level: {self.xp_to_next_level}")

    def get_xp_percentage(self):
        return (self.xp / self.xp_to_next_level) * 100 if self.xp_to_next_level > 0 else 0
    def draw(self, screen):
        screen.surface.blit(self.img, (self.x, self.y))
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)