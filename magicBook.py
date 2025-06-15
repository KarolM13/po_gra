import math
from weapons import Weapon
from projectile import Projectile
import pygame

class MagicBook(Weapon):
    def __init__(self):
        super().__init__(
            name="MagicBook",
            damage=10,
            projectile_speed=3,
            attack_speed=4000,
            range=1500,
            projectile_sprite="assets/kamien.png"
        )
        self.sprite = None
        self.size = 40
        try:
            self.sprite = pygame.image.load("assets/magic wand.png")
            self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        except pygame.error as e:
            print(f"Błąd ładowania sprite'a różdżki: {e}")
            self.sprite = None

    def attack(self, enemies):
        if not self.owner:
            return
        num_projectiles = 6
        angle_step = 360 / num_projectiles
        for i in range(num_projectiles):
            angle_deg = i * angle_step
            angle_rad = math.radians(angle_deg)
            dir_x = math.cos(angle_rad)
            dir_y = math.sin(angle_rad)
            new_projectile = Projectile(
                self.owner.x + self.owner.size // 2,
                self.owner.y + self.owner.size // 2,
                dir_x,
                dir_y,
                self.projectile_speed,
                self.damage,
                self.range,
                self.projectile_sprite
            )
            self.projectiles.append(new_projectile)

    def draw(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)