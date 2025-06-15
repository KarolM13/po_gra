import pygame
from weapons import Weapon

class IceWand(Weapon):
    def __init__(self):
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
        try:
            self.sprite = pygame.image.load("assets/magic wand.png")
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        except pygame.error as e:
            print(f"Błąd ładowania sprite'a różdżki: {e}")
            self.sprite = None

    def draw(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)
    def check_projectile_collisions(self, enemies):
        for enemy in enemies:
            for proj in self.projectiles[:]:
                if enemy.get_rect().colliderect(proj.get_rect()):
                    enemy.take_damage(self.damage)
                    enemy.apply_slow(duration=2000, slow_factor=0.4)  # 2 sekundy, 40% prędkości
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    break

    def update(self, enemies):
        super().update(enemies)
        self.check_projectile_collisions(enemies)