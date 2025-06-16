import pygame
from game import Game

def main():
    while True:
        g = Game()
        should_continue = g.game()
        if should_continue is False:
            break

if __name__ == "__main__":
    main()