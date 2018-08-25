import pygame
import math
import random

class Asteroid:
    maxstage = 5
    
    def __init__(self,surf,stage=None,pos=[0,0],vector=[0,0],speed=1.5):
        self.stage = self.maxstage if stage is None else stage
        self.size = self.stage*2 + 1
        self.surf = surf

        self.speed = speed
        self.radius = self.size * 15

        if self.stage >= self.maxstage:
            if random.randint(0,1):
                self.pos = [random.randint(0,self.surf.get_width()),0 if random.randint(0,1) else self.surf.get_height()]
            else:
                self.pos = [0 if random.randint(0,1) else self.surf.get_width(),random.randint(0,self.surf.get_height())]

            self.vector = [self.surf.get_size()[i]/2 - self.pos[i] for i in range(2)]
            self.vector = [i/math.sqrt(sum(e**2 for e in self.vector)) * self.speed for i in self.vector]

        else:
            self.vector = vector
            self.pos = pos
            
    def get_size(self):
        return (self.sides*5)**1.5

    def children(self):
        if self.stage <= 1:
            return []
        else:
            a = Asteroid(self.surf,self.stage-1,[i+random.randint(-10,10) for i in self.pos],self.rotate(self.vector,-80),self.speed+0.2)
            b = Asteroid(self.surf,self.stage-1,[i+random.randint(-10,10) for i in self.pos],self.rotate(self.vector,80),self.speed+0.2)

            return [Asteroid(self.surf,self.stage-1,[i+random.randint(-10,10) for i in self.pos],self.rotate(self.vector,360/(abs(self.stage-self.maxstage)+2) * j),self.speed+0.2) for j in range(abs(self.stage-self.maxstage)+2)]

    def rotate(self,vector,deg):
        return [vector[0]*math.cos(math.radians(deg)) - vector[1]*math.sin(math.radians(deg)),vector[0]*math.sin(math.radians(deg)) + vector[1]*math.cos(math.radians(deg))]

    def draw(self):
        pygame.draw.polygon(self.surf,(255,255,255),[[self.pos[0]+self.radius*math.cos(math.radians(i)),self.pos[1]+self.radius*math.sin(math.radians(i))] for i in range(0,360,int(360/self.size))],1)

    def move(self):
        self.pos = [self.pos[i] + self.vector[i] for i in range(2)]

        if self.pos[0] < -self.radius:
            self.pos[0] = self.surf.get_width()+self.radius
        elif self.pos[0] > self.surf.get_width() + self.radius:
            self.pos[0] = -self.radius

        if self.pos[1] < -self.radius:
            self.pos[1] = self.surf.get_height() + self.radius
        elif self.pos[1] > self.surf.get_height() + self.radius:
            self.pos[1] = -self.radius
