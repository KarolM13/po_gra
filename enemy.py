import pygame
from character import Character
from player import Player
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
    def __init__(self, x ,y):
        super().__init__(x, y , speed = 5 ,size=300, max_health = 200 , damage = 20, sprite_path="./assets/wojfer.png")

class FastEnemy(Enemy):
    def __init__(self, x ,y):
        super().__init__(x, y , speed = 10 , max_health = 30 , damage = 5, sprite_path="./assets/vampire.png")

class NormalEnemy(Enemy):
    def __init__(self, x ,y):
        super().__init__(x, y , speed = 5 ,size=200, max_health = 200 , damage = 20, sprite_path="./assets/tusk.png")
