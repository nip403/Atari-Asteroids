from Asteroid import Asteroid
from Player import Spaceship,Bullet

import pygame
import math
import random

s = [1000,700]

pygame.init()
screen = pygame.display.set_mode(s,0,32)
clock = pygame.time.Clock()
pygame.display.set_caption("Asteroids by NIP")

def main():
    while True:
        ship = Spaceship(screen)
        frame = 0
        rocks = []

        for i in range(1):
            rocks.append(Asteroid(screen,5))

        while True:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ship.shoot()

            if pygame.key.get_pressed()[pygame.K_UP]:
                ship.shove()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                ship.rotate_left()
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                ship.rotate_right()

            screen.fill((0,0,0))
            ship.draw()
            ship.move()

            rocks = ship.break_rocks(rocks)

            for i in rocks:
                i.draw()
                i.move()

            pygame.display.flip()

            if ship.collide(rocks) or not len(rocks):
                break

if __name__ == "__main__":
    main()
