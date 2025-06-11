import pygame
from character import Character
from player import Player
class Enemy(Character):
    def __init__(self, x, y=0, delta_time=0, max_health=100, speed=3, size=100, damage=10, range=100, sprite_path="assets/vampire.png"):
        super().__init__(x, y, delta_time, max_health, speed, size, damage, range, sprite_path)
        self.patrol_points = []
        self.current_patrol_index = 0
        self.directnion = 0

    def patrol(self,player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        dx /= distance
        dy /= distance
        self.x += dx * self.speed
        self.y += dy * self.speed

    