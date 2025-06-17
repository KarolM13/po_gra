import pygame
import math
import random
from projectile import Projectile

class Weapon:
    """Bazowa klasa broni, z której dziedziczą inne bronie."""
    def __init__(self, name, damage, projectile_speed, attack_speed, range, projectile_sprite=None, sound_path=None):
        """Inicjalizuje broń z podstawowymi parametrami."""
        self.name = name
        self.damage = damage
        self.projectile_speed = projectile_speed
        self.attack_speed = attack_speed
        self.range = range
        self.level = 1
        self.last_attack_time = 0
        self.projectiles = []
        self.owner = None
        self.sound = None
        self.projectile_sprite = projectile_sprite
        # Wczytaj dźwięk jeśli podano
        if sound_path:
            try:
                self.sound = pygame.mixer.Sound(sound_path)
            except pygame.error as e:
                print(f"Błąd ładowania dźwięku broni: {e}")
                self.sound = None

    def assign_owner(self, character):
        """Przypisuje właściciela broni (gracza lub przeciwnika)."""
        self.owner = character

    def update(self, enemies):
        """Aktualizuje stan broni i pocisków."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_speed:
            self.attack(enemies)
            self.last_attack_time = current_time
        self.update_projectiles()
        self.check_projectile_collisions(enemies)

    def attack(self, enemies):
        """Wystrzeliwuje pocisk w kierunku najbliższego przeciwnika."""
        if not self.owner or not enemies:
            return
        closest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            dx = enemy.x + enemy.size / 2 - (self.owner.x + self.owner.size / 2)
            dy = enemy.y + enemy.size / 2 - (self.owner.y + self.owner.size / 2)
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        if not closest_enemy:
            return
        dx = closest_enemy.x + closest_enemy.size / 2 - (self.owner.x + self.owner.size / 2)
        dy = closest_enemy.y + closest_enemy.size / 2 - (self.owner.y + self.owner.size / 2)
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance
        else:
            direction_x, direction_y = 1, 0
        num_projectiles = 1
        for i in range(num_projectiles):
            angle_offset = 10 * (i - (num_projectiles - 1) / 2)
            angle = math.degrees(math.atan2(direction_y, direction_x)) + angle_offset
            rad_angle = math.radians(angle)
            adjusted_dir_x = math.cos(rad_angle)
            adjusted_dir_y = math.sin(rad_angle)
            new_projectile = Projectile(
                self.owner.x + self.owner.size // 2,
                self.owner.y + self.owner.size // 2,
                adjusted_dir_x,
                adjusted_dir_y,
                self.projectile_speed,
                self.damage,
                self.range,
                self.projectile_sprite
            )
            self.projectiles.append(new_projectile)

    def update_projectiles(self):
        """Aktualizuje listę pocisków (usuwa te poza zasięgiem)."""
        self.projectiles = [proj for proj in self.projectiles if proj.update()]

    def check_projectile_collisions(self, enemies):
        """Sprawdza kolizje pocisków z przeciwnikami."""
        for enemy in enemies:
            for proj in self.projectiles[:]:
                if enemy.get_rect().colliderect(proj.get_rect()):
                    enemy.take_damage(self.damage)
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    break

    def draw(self, screen):
        """Rysuje wszystkie pociski wystrzelone przez broń."""
        for projectile in self.projectiles:
            projectile.draw(screen)