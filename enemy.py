import pygame
from character import Character
from player import Player
from projectile import Projectile
import math
class Enemy(Character):
    def __init__(self, x, y=0, delta_time=0, max_health=100, speed=3, size=100, damage=10, range=100, sprite_path="assets/vampire.png"):
        super().__init__(x, y, delta_time, max_health, speed, size, damage, range, sprite_path)
        self.patrol_points = []
        self.current_patrol_index = 0
        self.direction = 0
        self.last_attack_time = pygame.time.get_ticks()
        self.slowed_until = 0
        self.base_speed = self.speed
        self.facing_right = True

    def apply_slow(self, duration, slow_factor=0.5):
        self.slowed_until = pygame.time.get_ticks() + duration
        self.speed = self.base_speed * slow_factor

    def update_slow(self):
        if pygame.time.get_ticks() > self.slowed_until:
            self.speed = self.base_speed

    def patrol(self, player, all_enemies=None):
        # Oblicz kierunek do gracza
        self.update_slow()
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            return
        dx /= distance
        dy /= distance
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False
        # Proponowana nowa pozycja
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        new_rect = pygame.Rect(new_x, new_y, self.size, self.size)
        # Sprawdź kolizję z innymi wrogami

        # Jeśli nie ma kolizji, zaktualizuj pozycję
        self.x = new_x
        self.y = new_y
    def draw(self, screen):
        if self.sprite:
            if self.facing_right:
                img = self.sprite
            else:
                img = pygame.transform.flip(self.sprite, True, False)
            screen.surface.blit(img, (self.x, self.y))

    def attack(self, player):
        cooldown = 500
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= cooldown:
            player.take_damage(self.damage)
            self.last_attack_time = current_time
            print(f"Enemy attacked player for {self.damage} damage. Player health: {player.health}/{player.max_health}")
class TankEnemy(Enemy):
    def __init__(self, x, y, difficulty_level=0):
        hp = 200 + 40 * difficulty_level
        dmg = 20 + 4 * difficulty_level
        speed = 5 + 0.5 * difficulty_level
        super().__init__(x, y, speed=speed, max_health=hp, damage=dmg, sprite_path="./assets/zombie.png")

class FastEnemy(Enemy):
    def __init__(self, x, y, difficulty_level=0):
        hp = 30 + 10 * difficulty_level
        dmg = 5 + 2 * difficulty_level
        speed = 10 + 1 * difficulty_level
        super().__init__(x, y, speed=speed, max_health=hp, damage=dmg, sprite_path="./assets/vampire.png")

class NormalEnemy(Enemy):
    def __init__(self, x, y, difficulty_level=0):
        hp = 100 + 20 * difficulty_level
        dmg = 10 + 2 * difficulty_level
        speed = 5 + 0.5 * difficulty_level
        super().__init__(x, y, sprite_path="./assets/bat.png")
class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, speed=3, size=400, max_health=1500, damage=50, sprite_path="./assets/wojfer.png")

class ShooterEnemy(Enemy):
    def __init__(self, x, y, difficulty_level=0):
        super().__init__(x, y, speed=4, max_health=80, damage=10, sprite_path="./assets/shooter.png")
        self.projectiles = []
        self.shoot_cooldown = 1500  # ms
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, player):
        self.patrol(player)
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_cooldown:
            self.shoot(player)
            self.last_shot_time = now
        # Aktualizuj pociski
        for proj in self.projectiles[:]:
            if not proj.update():
                self.projectiles.remove(proj)

    def shoot(self, player):
        dx = player.x + player.size // 2 - (self.x + self.size // 2)
        dy = player.y + player.size // 2 - (self.y + self.size // 2)
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        dir_x = dx / dist
        dir_y = dy / dist
        proj = Projectile(
            self.x + self.size // 2,
            self.y + self.size // 2,
            dir_x, dir_y,
            speed=7,
            damage=self.damage,
            range=600,
            sprite_path="./assets/arrow.png"
        )
        if proj.sprite:
            angle = math.degrees(math.atan2(-dir_y, dir_x))
            proj.sprite = pygame.transform.rotate(proj.sprite, angle)
        self.projectiles.append(proj)

    def draw(self, screen):
        super().draw(screen)
        for proj in self.projectiles:
            proj.draw(screen)