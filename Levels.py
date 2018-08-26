from StandardLevels import Levelmaster
from Asteroid import Asteroid,Base_stats
from Player import Spaceship,Bullet

import pygame
import sys

pygame.init()

clock = pygame.time.Clock()
font = pygame.font.SysFont("Garamond MS",50)
font2 = pygame.font.SysFont("Garamond MS",20)

class Level_manager:
    def __init__(self,surf):
        self.surf = surf

    def run(self,level):
        return Endless(self.surf).run() if level == -1 else Levelmaster(self.surf,level).run()

class Endless:
    def __init__(self,surf):
        self.surf = surf
        self.level = 1
        self.lives = 5

    def next_level(self):
        self.level += 1
        self.run()

    def get_rocks(self,level):
        if level <= 3:
            Base_stats.base_stage = 2
            return [Asteroid(self.surf) for _ in range(level)]
        elif level <= 6:
            Base_stats.base_stage = 3
            return [Asteroid(self.surf) for _ in range(level)]
        elif level <= 10:
            Base_stats.base_stage = 4
            Base_stats._speed = 2
            return [Asteroid(self.surf) for _ in range(int(level//1.2))]
        elif level <= 15:
            Base_stats.base_stage = 5
            Base_stats._speed = 2.5
            return [Asteroid(self.surf) for _ in range(int(level//1.5))]
        elif level <= 20:
            Base_stats.base_stage = 6
            Base_stats._speed = 3
            return [Asteroid(self.surf) for _ in range(int(level//1.7))]
        elif level <= 25:
            Base_stats.base_stage = 7
            Base_stats._speed = 4
            return [Asteroid(self.surf) for _ in range(int(level//2))]
        else:
            Base_stats.base_stage = 8
            Base_stats._speed = 5
            return [Asteroid(self.surf) for _ in range(level)]
        
    def run(self):
        ship = Spaceship(self.surf)
        rocks = self.get_rocks(self.level)
        lvl = font2.render(f"Level: {self.level}",True,(0,255,0))

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

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        ship.shoot()

            if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                ship.boost()
            if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                ship.rotate_left()
            if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                ship.rotate_right()

            self.surf.fill((0,0,0))
            ship.draw()
            ship.move()

            rocks = ship.break_rocks(rocks)

            for i in rocks:
                i.draw()
                i.move()

            for i in range(self.lives):
                pygame.draw.circle(self.surf,(200,40,20),[20+(i*15),40],6,1)
            self.surf.blit(lvl,lvl.get_rect(topleft=[20,20-(0.5*lvl.get_height())]))

            pygame.display.flip()

            if ship.collide(rocks):
                self.lives -= 1

                for iteration in range(50):
                    if ship.collide(rocks):
                        ship.reposition()
                    else:
                        break
                else:
                    if not ship.reposition(True,rocks):
                        self.lives = 0
                    
            if not self.lives:
                return {"Endless":True,"Level":self.level}
            if not len(rocks):
                break
            
        self.next_level()
        return {"Endless":True,"Level":self.level}
