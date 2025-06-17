import pygame
from weapons import Weapon

class IceWand(Weapon):
    """Broń wystrzeliwująca pociski lodowe, które spowalniają wrogów."""
    def __init__(self):
        """Inicjalizuje IceWand z domyślnymi parametrami i ładuje grafikę."""
        super().__init__(
            name="IceWand",
            damage=30,
            projectile_speed=3,
            attack_speed=500,
            range=500,
            projectile_sprite="assets/ice bullet.png"
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
        """Rysuje wszystkie pociski wystrzelone przez IceWand."""
        for projectile in self.projectiles:
            projectile.draw(screen)
    def check_projectile_collisions(self, enemies):
        """Sprawdza kolizje pocisków z wrogami i nakłada efekt spowolnienia."""
        for enemy in enemies:
            for proj in self.projectiles[:]:
                if enemy.get_rect().colliderect(proj.get_rect()):
                    enemy.take_damage(self.damage)
                    enemy.apply_slow(duration=2000, slow_factor=0.4)
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    break

    def update(self, enemies):
        """Aktualizuje stan broni i sprawdza kolizje pocisków."""
        super().update(enemies)
        self.check_projectile_collisions(enemies)