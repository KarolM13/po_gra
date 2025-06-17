import pygame
import math

class Projectile:
    """Reprezentuje pocisk wystrzeliwany przez broń lub przeciwnika."""
    def __init__(self, x, y, direction_x, direction_y, speed, damage, range, sprite_path=None):
        """Inicjalizuje pocisk z pozycją, kierunkiem, prędkością i grafiką."""
        self.x = x
        self.y = y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = speed
        self.damage = damage
        self.range = range
        self.distance_traveled = 0
        self.sprite = None
        self.size = 50
        # Wczytaj grafikę pocisku jeśli podano
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
            except pygame.error as e:
                print(f"Błąd ładowania sprite'a pocisku: {e}")
                self.sprite = None

    def update(self):
        """Aktualizuje pozycję pocisku i sprawdza zasięg."""
        movement_x = self.direction_x * self.speed
        movement_y = self.direction_y * self.speed
        self.x += movement_x
        self.y += movement_y
        distance_moved = math.sqrt(movement_x**2 + movement_y**2)
        self.distance_traveled += distance_moved
        return self.distance_traveled <= self.range

    def draw(self, screen):
        """Rysuje pocisk na ekranie."""
        if self.sprite:
            screen.surface.blit(self.sprite, (self.x - self.size/2, self.y - self.size/2))
        else:
            pygame.draw.circle(screen.surface, (255, 255, 0), (int(self.x), int(self.y)), 5)

    def get_rect(self):
        """Zwraca prostokąt kolizji pocisku."""
        return pygame.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size)