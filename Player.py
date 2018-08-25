import pygame
import math
import random

class Bullet:
    def __init__(self,surf,direction,pos):
        self.speed = 10
        self.vector = [0,0]
        self.direction = direction
        self.surf = surf
        self.pos = pos

    def draw(self):
        pygame.draw.circle(self.surf,(255,255,255),list(map(int,self.pos)),2,0)

    def move(self):
        self.vector = [math.cos(math.radians(self.direction)),math.sin(math.radians(self.direction))]
        self.vector = [i/math.sqrt(sum(e**2 for e in self.vector)) * self.speed for i in self.vector]
        self.pos = [self.pos[i] + self.vector[i] for i in range(2)]

class Spaceship:
    def __init__(self,surf):
        self.bullets = []
        self.momentum = 0
        self.velocity = 0

        self.surf = surf
        self.s = self.surf.get_size()

        self.pos = [i/2 for i in self.s]
        self.direction = -90
        self.radius = 20

        self.bullets = []

    def draw(self):
        pygame.draw.circle(self.surf,(200*(self.momentum/5)+40,20*(self.momentum/5)+40,40 if not self.momentum else 0),[int(i) for i in self.pos],self.radius,0)
        pygame.draw.polygon(self.surf,(255,255,255),[[self.pos[0]+self.radius*math.cos(math.radians(self.direction)),self.pos[1]+self.radius*math.sin(math.radians(self.direction))],[self.pos[0]+self.radius*math.cos(math.radians(self.direction-130)),self.pos[1]+self.radius*math.sin(math.radians(self.direction-130))],self.pos,[self.pos[0]+self.radius*math.cos(math.radians(self.direction+130)),self.pos[1]+self.radius*math.sin(math.radians(self.direction+130))]],1)

        for i in self.bullets:
            i.draw()
            i.move()

        self.bullets = [i for i in self.bullets if all(0 <= i.pos[e] <= self.surf.get_size()[e] for e in range(2))]

    def rotate_left(self):
        self.direction -= 3.5

    def rotate_right(self):
        self.direction += 3.5

    def shoot(self):
        self.bullets.append(Bullet(self.surf,self.direction,[self.pos[0]+20*math.cos(math.radians(self.direction)),self.pos[1]+20*math.sin(math.radians(self.direction))]))
        
    def shove(self):
        self.momentum = 5
        self.vector = [math.cos(math.radians(self.direction)),math.sin(math.radians(self.direction))]
        self.vector = [i/math.sqrt(sum(e**2 for e in self.vector)) * self.momentum for i in self.vector]
        self.pos = [self.pos[i] + self.vector[i] for i in range(2)]

    def move(self):
        self.momentum -= 0.1

        if self.momentum <= 0:
            self.momentum = 0
        elif self.momentum > 5:
            self.momentum = 5
            
        self.vector = [math.cos(math.radians(self.direction)),math.sin(math.radians(self.direction))]
        self.vector = [i/math.sqrt(sum(e**2 for e in self.vector)) * self.momentum for i in self.vector]
        self.pos = [self.pos[i] + self.vector[i] for i in range(2)]

        if self.pos[0] < 0:
            self.pos[0] = self.surf.get_width()
        elif self.pos[0] > self.surf.get_width():
            self.pos[0] = 0

        if self.pos[1] < 0:
            self.pos[1] = self.surf.get_height()
        elif self.pos[1] > self.surf.get_height():
            self.pos[1] = 0

    def collide(self,rocks):
        for r in rocks:
            dist = math.sqrt(sum(i**2 for i in [self.pos[e]-r.pos[e] for e in range(2)]))

            if dist - self.radius - r.radius < 0:
                return True

        return False

    def break_rocks(self,rocks):
        posb = []
        posr = []
        
        for p1,b in enumerate(self.bullets):
            for p2,r in enumerate(rocks):
                dist = math.sqrt(sum(i**2 for i in [b.pos[e]-r.pos[e] for e in range(2)]))
                
                if dist - r.radius < 0:
                    posb.append(p1)
                    posr.append(p2)

        self.bullets = [i for p,i in enumerate(self.bullets) if not p in posb]
        new = []

        for p,r in enumerate(rocks):
            if not p in posr:
                new.append(r)
            else:
                new += r.children()

        return new
