from Asteroid import Asteroid, Base_stats
from Player import Spaceship, Bullet

import pygame
import math
import random
import sys

pygame.init()
font = pygame.font.SysFont("Garamond MS", 20)
clock = pygame.time.Clock()

# Asteroid layers, speed=0, linear=0, amount
levelData = {
    1:  [2, 0, 1, 3],
    2:  [2, 0, 1, 5],
    3:  [2, 2, 1, 7],
    4:  [2, 2, 0, 9],
    
    5:  [3, 0, 1, 3],
    6:  [3, 0, 1, 4],
    7:  [3, 0, 1, 5],
    8:  [3, 2, 1, 6],
    9:  [3, 2, 1, 7],
    10: [3, 2, 0, 8],
    
    11: [4, 0, 1, 3],
    12: [4, 0, 1, 3],
    13: [4, 2, 1, 4],
    14: [4, 2, 1, 4],
    15: [4, 2, 1, 5],
    16: [4, 3, 1, 5],
    17: [4, 3, 1, 5],
    18: [4, 3, 0, 6],

    19: [5, 0, 1, 2],
    20: [5, 0, 1, 2],
    21: [5, 0, 1, 2],
    22: [5, 2, 1, 3],
    23: [5, 2, 1, 3],
    24: [5, 2, 1, 3],
    25: [5, 2, 1, 4],
    26: [5, 2, 1, 4],
    27: [5, 3, 1, 4],
    28: [5, 3, 0, 3],
    
    29: [6, 0, 1, 1],
    30: [6, 0, 1, 1],
    31: [6, 0, 1, 1],
    32: [6, 2, 1, 2],
    33: [6, 2, 1, 2],
    34: [6, 2, 1, 2],
    35: [6, 3, 1, 1],
    36: [6, 3, 1, 2],
    37: [6, 3, 1, 3],
    38: [6, 3, 1, 4],
    39: [6, 4, 1, 3],
    40: [6, 4, 1, 2],

    41: [7, 0, 0, 1],
    42: [8, 0, 0, 1],
    43: [9, 0, 0, 1],
    44: [10,0, 0, 1],

    45: [7, 2, 0, 2],
    46: [8, 2, 0, 2],
    47: [9, 2, 0, 2],
    48: [10,2, 0, 2],
         
    49: [10,4, 0, 2],
    50: [10,2, 0, 3]
}

__LEVEL_COUNT__ = len(levelData.keys())
__BOSS_LEVELS__ = [4, 10, 18, 28, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
__FINAL_LEVEL__ = 50

def pause_screen(surf, ship, asteroids):
    head = pygame.font.SysFont("Garamond MS", 50).render("Game Paused", True, (255, 255, 255))
    foot = pygame.font.SysFont("Garamond MS", 20).render("Press ESC to resume", True, (255, 255, 255))

    pause_surf = pygame.Surface(surf.get_size())
    pause_surf.fill((0, 0, 0))
    pause_surf.set_alpha(140)
    pause_surf.blit(head, head.get_rect(center=[pause_surf.get_width()/2, pause_surf.get_height()/2 - 20]))
    pause_surf.blit(foot, foot.get_rect(center=[pause_surf.get_width()/2, pause_surf.get_height()/2 + 50]))
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        for i in asteroids:
            i.draw()

        ship.draw()
        surf.blit(pause_surf, (0, 0))

        pygame.display.flip()
    
class Levelmaster:
    def __init__(self, surf, level):
        self.surf = surf
        self.lives = 5 + (5 * (level + 1 in (__BOSS_LEVELS__ + [__FINAL_LEVEL__])))
        self.level = level + 1

    def get_rocks(self):
        # any, 1.5, True
        stage, speed, linear, amount = levelData[self.level]

        Base_stats.base_stage = stage
        Base_stats._speed = speed if speed else Base_stats._speed
        Base_stats.linear_divide = linear

        return [Asteroid(self.surf) for _ in range(amount)]
        
    def run(self):
        ship = Spaceship(self.surf)
        #lvl = font.render(f"Level {self.level}", True, (0, 255, 0))
        lvl = font.render("Level {}".format(self.level), True, (0, 255, 0))
        rocks = self.get_rocks()

        while True:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ship.shoot()

                    elif event.key in [pygame.K_e,pygame.K_SLASH]:
                        ship.shoot()

                    elif event.key == pygame.K_ESCAPE:
                        pause_screen(self.surf,ship,rocks)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        ship.shoot()

            if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                ship.boost()
            if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                ship.rotate_left()
            if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                ship.rotate_right()

            self.surf.fill((0, 0, 0))
            ship.draw()
            ship.move()

            rocks = ship.break_rocks(rocks)

            for i in rocks:
                i.draw()
                i.move()

            for i in range(self.lives):
                pygame.draw.circle(self.surf, (200, 40, 20), [20 + (i*15), 40], 6, 1)
                
            self.surf.blit(lvl, lvl.get_rect(topleft=[20, 20 - (0.5 * lvl.get_height())]))

            pygame.display.flip()

            if ship.collide(rocks):
                self.lives -= 1
                ship.set_blinking()
                    
            if not self.lives or not len(rocks):
                return {"Lives": self.lives, "Level": self.level}

class Level_manager:
    def __init__(self, surf):
        self.surf = surf

    def run(self, level):
        return Endless(self.surf).run() if level == -1 else Levelmaster(self.surf, level).run()

class Endless:
    def __init__(self, surf):
        self.surf = surf
        self.level = 1
        self.lives = 5
        self.ship = Spaceship(self.surf)

    def next_level(self):
        self.level += 1
        self.run()

    def get_rocks(self, level):
        if level <= 3:
            Base_stats.base_stage = 2
            return [Asteroid(self.surf) for _ in range(level)]
        
        elif level <= 6:
            Base_stats.base_stage = 3
            Base_stats.linear_divide = level % 2
            return [Asteroid(self.surf) for _ in range(level)]
        
        elif level <= 10:
            Base_stats.base_stage = 4
            Base_stats._speed = 2
            Base_stats.linear_divide = level % 3
            return [Asteroid(self.surf) for _ in range(int(level//1.2))]
        
        elif level <= 15:
            Base_stats.base_stage = 5
            Base_stats._speed = 2.5
            Base_stats.linear_divide = level % 4
            return [Asteroid(self.surf) for _ in range(int(level//1.5))]
        
        elif level <= 20:
            Base_stats.base_stage = 6
            Base_stats._speed = 3
            Base_stats.linear_divide = level % 5
            return [Asteroid(self.surf) for _ in range(int(level//1.7))]
        
        elif level <= 25:
            Base_stats.base_stage = 7
            Base_stats._speed = 4
            Base_stats.linear_divide = level % 5
            return [Asteroid(self.surf) for _ in range(int(level//2))]
        
        else:
            Base_stats.base_stage = 8
            Base_stats._speed = 5
            Base_stats.linear_divide = level % 5
            return [Asteroid(self.surf) for _ in range(level)]
        
    def run(self):
        rocks = self.get_rocks(self.level)
        #lvl = font.render(f"Level: {self.level}", True, (0, 255, 0))
        lvl = font.render("Level: {}".format(self.level), True, (0, 255, 0))

        while True:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ship.shoot()

                    elif event.key in [pygame.K_e, pygame.K_SLASH]:
                        self.ship.shoot()

                    elif event.key == pygame.K_ESCAPE:
                        pause_screen(self.surf, self.ship, rocks)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.ship.shoot()

            if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                self.ship.boost()
            if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                self.ship.rotate_left()
            if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                self.ship.rotate_right()

            self.surf.fill((0, 0, 0))
            self.ship.draw()
            self.ship.move()

            rocks = self.ship.break_rocks(rocks)

            for i in rocks:
                i.draw()
                i.move()

            for i in range(self.lives):
                pygame.draw.circle(self.surf, (200, 40, 20), [20 + (i*15), 40], 6, 1)
                
            self.surf.blit(lvl, lvl.get_rect(topleft=[20, 20 - (0.5 * lvl.get_height())]))

            pygame.display.flip()

            if self.ship.collide(rocks):
                self.lives -= 1
                self.ship.set_blinking()
                    
            if not self.lives:
                return {"Endless": True, "Level": self.level}
            
            if not len(rocks):
                break
            
        self.next_level()
        return {"Endless": True, "Level": self.level}
