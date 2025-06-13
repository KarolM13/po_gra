import pygame
import math

class Projectile:
    def __init__(self, x, y, direction_x, direction_y, speed, damage, range, sprite_path=None):
        self.x = x
        self.y = y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = speed
        self.damage = damage
        self.range = range
        self.distance_traveled = 0
        self.sprite = None
        self.size = 20

        # Ładowanie sprite'a pocisku
        if sprite_path:
            try:
                self.sprite = pygame.image.load(sprite_path)
                self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
            except pygame.error as e:
                print(f"Błąd ładowania sprite'a pocisku: {e}")
                self.sprite = None

    def update(self):
        # Aktualizacja pozycji
        movement_x = self.direction_x * self.speed
        movement_y = self.direction_y * self.speed
        self.x += movement_x
        self.y += movement_y

        # Aktualizacja przebytej odległości
        distance_moved = math.sqrt(movement_x**2 + movement_y**2)
        self.distance_traveled += distance_moved

        # Sprawdź, czy pocisk przekroczył zasięg
        return self.distance_traveled <= self.range

    def draw(self, screen):
        if self.sprite:
            screen.surface.blit(self.sprite, (self.x - self.size/2, self.y - self.size/2))
        else:
            # Domyślny wygląd pocisku
            pygame.draw.circle(screen.surface, (255, 255, 0), (int(self.x), int(self.y)), 5)

    def get_rect(self):
        return pygame.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size)