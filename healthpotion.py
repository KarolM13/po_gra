import pygame

class HealthPotion:
    """Reprezentuje miksturę zdrowia na planszy."""
    def __init__(self, x, y, value=10):
        """Inicjalizacja mikstury zdrowia na podanych współrzędnych."""
        self.x = x
        self.y = y
        self.value = value
        # Wczytaj i przeskaluj grafikę mikstury
        self.img = pygame.transform.scale(pygame.image.load("./assets/potion.png"), (50, 50))

    def draw(self, screen):
        """Rysuje miksturę na ekranie gry."""
        screen.surface.blit(self.img, (self.x, self.y))

    def get_rect(self):
        """Zwraca prostokąt kolizji mikstury (do sprawdzania kolizji z graczem)."""
        return pygame.Rect(self.x, self.y, 50, 50)