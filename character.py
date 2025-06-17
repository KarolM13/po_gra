import pygame

class Character:
    """Bazowa klasa postaci w grze (gracz, przeciwnik itp.)."""
    def __init__(self , x ,y = 0,delta_time=0, max_health = 100, speed = 5, size = 50 , damage = 10, range = 100, sprite_path = None):
        """Inicjalizuje postać z podstawowymi parametrami i ładuje grafikę."""
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
        self.damage = damage
        self.range = range
        try:
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        except pygame.error as e:
            print(f"Error loading sprite: {e}")
            self.sprite = None
            
    def draw(self ,screen):
        """Rysuje postać na ekranie."""
        screen.surface.blit(self.sprite, (self.x, self.y))

    def move(self):
        """Porusza postacią zgodnie z kierunkiem i prędkością."""
        self.x += self.direction_x * self.speed 
        self.y += self.direction_y * self.speed

    def die(self):
        """Ustawia postać jako martwą i zeruje zdrowie."""
        self.alive = False
        self.health = 0

    def take_damage(self, amount):
        """Zmniejsza zdrowie postaci o podaną wartość."""
        self.health -= amount
        if self.health <= 0:
            self.die()
    def heal(self, amount):
        """Leczy postać o podaną wartość (nie przekracza max zdrowia)."""
        if self.alive:
            self.health += amount
            if self.health > self.max_health:
                self.health = self.max_health
    
    def get_rect(self):
        """Zwraca prostokąt kolizji postaci."""
        return pygame.Rect(self.x, self.y, self.size, self.size)