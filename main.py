from Displays import CommonScreens
from Levels import Level_manager

import pygame
import math
import random
import sys

s = [1000,700]

pygame.init()
screen = pygame.display.set_mode(s,0,32)
clock = pygame.time.Clock()
pygame.display.set_caption("Asteroids by NIP")

def main():
    c = CommonScreens(screen)
    l = Level_manager(screen)
    c.startscreen()

    while True:
        c.deathscreen(l.run(-1 if c.main_menu() else c.level_menu()))

if __name__ == "__main__":
    main()
