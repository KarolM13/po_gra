import pygame 
from character import Character
from magicBook import MagicBook
from wand import Wand
from iceWand import IceWand
class Player(Character):
    """Klasa gracza, dziedziczy po Character."""
    def __init__(self , x ,y):
        """Inicjalizuje gracza z domyślnymi parametrami i ładuje grafiki postaci."""
        super().__init__(x, y , max_health=100, speed=10, size=100 , sprite_path="./assets/ziutek.png")
        self.xp = 0
        self.xp_to_next_level = 100
        self.level = 1
        self.weapons = []
        self.flip = pygame.transform.flip(self.sprite, True, False)
        self.img_back =pygame.transform.scale(pygame.image.load("./assets/ziutek_tyl.png"), (self.size, self.size))
        self.img_front = pygame.transform.scale(pygame.image.load("./assets/ziutek_przod.png"), (self.size, self.size))
        self.equip_weapon(Wand())
        self.weapon_choice_pending = False

    def equip_weapon(self, weapon):
        """Dodaje nową broń lub ulepsza istniejącą."""
        print("Próba dodania broni:", weapon.name)
        for w in self.weapons:
            print("Porównuję z:", w.name)
            if w.name == weapon.name:
                print("Znaleziono, ulepszam poziom!")
                w.level += 1
                w.damage += 5
                w.attack_speed = max(w.attack_speed - 100, 100)
                print(self.weapons)
                return
        print("Dodaję nową broń:", weapon.name)
        weapon.assign_owner(self)
        self.weapons.append(weapon)

    def add_xp(self, amount,screen):
        """Dodaje punkty doświadczenia i sprawdza awans na wyższy poziom."""
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level_up(screen)

    def level_up(self,screen):
        """Zwiększa poziom gracza, wyświetla menu ulepszeń i obsługuje wybór broni co 5 poziomach."""
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        upgrades = [
            {"name": "Zdrowie", "description": "Zwiększ maksymalne zdrowie o 20"},
            {"name": "Obrażenia", "description": "Zwiększ obrażenia o 5"},
            {"name": "Szybkość", "description": "Zwiększ szybkość ruchu o 2"}
        ]
        screen.draw_level_up_menu(upgrades)
        print(f"Level up! Teraz poziom {self.level}. XP do następnego poziomu: {self.xp_to_next_level}")
        if self.level % 5 == 0:
            self.weapon_choice_pending = True


    def get_xp_percentage(self):
        """Zwraca procent zdobytego doświadczenia do następnego poziomu."""
        return (self.xp / self.xp_to_next_level) * 100 if self.xp_to_next_level > 0 else 0

    def input(self):
        """Obsługuje sterowanie ruchem gracza i zmianę grafiki postaci."""
        keys = pygame.key.get_pressed()
        self.direction_x = 0
        self.direction_y = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction_y -=1
            self.sprite = self.img_front
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction_y += 1
            self.sprite = self.img_back
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction_x -= 1
            self.sprite = self.flip
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction_x += 1
            self.sprite = pygame.transform.flip(self.flip, True, False)
        self.x += self.direction_x * self.speed 
        self.y += self.direction_y * self.speed
        screen_width = 1980
        screen_height = 1080
        self.x = max(0, min(self.x, screen_width - self.size))
        self.y = max(0, min(self.y, screen_height - self.size))
    def update(self , enemies=[]):
        """Aktualizuje stan gracza i jego broni."""
        self.input()
        for weapon in self.weapons:
            weapon.update(enemies)
