import pygame
from weapons import Weapon

class Wand(Weapon):
    """Podstawowa broń gracza wystrzeliwująca pociski."""
    def __init__(self):
        """Inicjalizuje różdżkę z domyślnymi parametrami."""
        super().__init__(
            name="Wand",
            damage=111,
            projectile_speed=7,
            attack_speed=220,
            range=350,
            projectile_sprite="assets/fireball.png"
        )

        self.sprite = None
        self.size = 40
        # Wczytaj grafikę różdżki
        try:
            self.sprite = pygame.image.load("assets/magic wand.png")
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        except pygame.error as e:
            print(f"Błąd ładowania sprite'a różdżki: {e}")
            self.sprite = None

    def draw(self, screen):
        """Rysuje wszystkie pociski wystrzelone przez różdżkę."""
        for projectile in self.projectiles:
            projectile.draw(screen)

