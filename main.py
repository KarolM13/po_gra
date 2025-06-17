import pygame
from game import Game

def main():
    """Główna pętla gry. Restartuje grę po zakończeniu, dopóki użytkownik nie wyjdzie."""
    while True:
        g = Game()
        should_continue = g.game()
        if should_continue is False:
            break

if __name__ == "__main__":
    main()