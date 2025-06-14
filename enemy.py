import pygame
from character import Character
from player import Player
class Enemy(Character):
    def __init__(self, x, y=0, delta_time=0, max_health=100, speed=3, size=100, damage=10, range=100, sprite_path="assets/vampire.png"):
        super().__init__(x, y, delta_time, max_health, speed, size, damage, range, sprite_path)
        self.patrol_points = []
        self.current_patrol_index = 0
        self.directnion = 0
        self.last_attack_time = pygame.time.get_ticks()

    def patrol(self, player, all_enemies=None):
        # Oblicz kierunek do gracza
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            return
        dx /= distance
        dy /= distance
        # Proponowana nowa pozycja
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        new_rect = pygame.Rect(new_x, new_y, self.size, self.size)
        # Sprawdź kolizję z innymi wrogami
        if all_enemies:
            for enemy in all_enemies:
                if enemy is not self and new_rect.colliderect(enemy.get_rect()):
                    return  # kolizja, nie ruszaj się
        # Jeśli nie ma kolizji, zaktualizuj pozycję
        self.x = new_x
        self.y = new_y

    def attack(self, player):
        cooldown = 10
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= cooldown:
            player.take_damage(self.damage)
            self.last_attack_time = current_time
            print(f"Enemy attacked player for {self.damage} damage. Player health: {player.health}/{player.max_health}")