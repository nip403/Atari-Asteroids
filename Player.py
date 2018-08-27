import pygame
import math
import random

def rotate(vector,deg):
    return [vector[0]*math.cos(math.radians(deg)) - vector[1]*math.sin(math.radians(deg)),vector[0]*math.sin(math.radians(deg)) + vector[1]*math.cos(math.radians(deg))]

class Bullet:
    def __init__(self,surf,direction,pos):
        self.speed = 15
        self.vector = [0,0]
        self.direction = direction
        self.surf = surf
        self.pos = pos

    def draw(self):
        pygame.draw.circle(self.surf,(25,180,150),list(map(int,self.pos)),2,0)

    def move(self):
        self.vector = [math.cos(math.radians(self.direction)),math.sin(math.radians(self.direction))]
        self.vector = [i/math.sqrt(sum(e**2 for e in self.vector)) * self.speed for i in self.vector]
        self.pos = [self.pos[i] + self.vector[i] for i in range(2)]

class Particle:
    def __init__(self,surf,pos,player_vector,speed=10,decay=5):
        self.surf = surf
        self.pos = [pos[0] + random.randint(-5,5),pos[1] + random.randint(-10,10)]
        self.red = 255
        self.speed = speed
        self.decay = decay
        self.vector = rotate([-i/math.sqrt(sum(e**2 for e in [-i for i in player_vector]))*self.speed for i in player_vector],random.randint(-10,10))

    def draw(self):
        pygame.draw.circle(self.surf,(self.red if self.red >= 0 else 0,self.red-100 if self.red-100 >= 0 else 0,0),list(map(int,self.pos)),1,1)
        self.red -= self.decay
        self.pos = [self.pos[i]+self.vector[i] for i in range(2)]

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
        self.particles = []
        self.ghost_rocks = []
        self.ghost_decay = 20

    def draw(self):
        #pygame.draw.circle(self.surf,(255*(self.momentum/5),70*(self.momentum/5),0),[int(i) for i in self.pos],self.radius,0)
        pygame.draw.polygon(self.surf,(255,255,255),[[self.pos[0]+self.radius*math.cos(math.radians(self.direction)),self.pos[1]+self.radius*math.sin(math.radians(self.direction))],[self.pos[0]+self.radius*math.cos(math.radians(self.direction-130)),self.pos[1]+self.radius*math.sin(math.radians(self.direction-130))],self.pos,[self.pos[0]+self.radius*math.cos(math.radians(self.direction+130)),self.pos[1]+self.radius*math.sin(math.radians(self.direction+130))]],1)

        for i in self.bullets:
            i.draw()
            i.move()

        for i in self.particles:
            i.draw()

        for i in self.ghost_rocks:
            i.draw()
            i.colour = [j-self.ghost_decay if j-self.ghost_decay > 0 else 0 for j in i.colour]
    
        self.ghost_rocks = [i for i in self.ghost_rocks if any(i.colour)]
        self.bullets = [i for i in self.bullets if all(0 <= i.pos[e] <= self.surf.get_size()[e] for e in range(2))]

    def rotate_left(self):
        self.direction -= 5

    def rotate_right(self):
        self.direction += 5

    def shoot(self):
        self.bullets.append(Bullet(self.surf,self.direction,[self.pos[0]+20*math.cos(math.radians(self.direction)),self.pos[1]+20*math.sin(math.radians(self.direction))]))
        
    def boost(self):
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

        if self.pos[0] < -self.radius:
            self.pos[0] = self.surf.get_width()+self.radius
        elif self.pos[0] > self.surf.get_width() + self.radius:
            self.pos[0] = -self.radius

        if self.pos[1] < -self.radius:
            self.pos[1] = self.surf.get_height() + self.radius
        elif self.pos[1] > self.surf.get_height() + self.radius:
            self.pos[1] = -self.radius

        if self.momentum > 4:
            self.particles += [Particle(self.surf,self.pos,self.vector) for _ in range(4)]

        self.particles = [i for i in self.particles if i.red > 0]

    def collide(self,rocks):
        for r in rocks:
            dist = math.sqrt(sum(i**2 for i in [self.pos[e]-r.pos[e] for e in range(2)]))

            if dist - self.radius - r.radius < 0:
                self.particles = [Particle(self.surf,self.pos,rotate([0,1],d),random.uniform(4,10),random.randint(3,5)) for d in range(0,360,2) for _ in range(2)]
                return True

        return False

    def break_rocks(self,rocks):
        posb = []
        posr = []
        
        for p1,b in enumerate(self.bullets):
            for p2,r in enumerate(rocks):
                dist = math.sqrt(sum(i**2 for i in [b.pos[e]-r.pos[e] for e in range(2)]))
                
                if dist - r.radius < 0 and not p1 in posb:
                    posb.append(p1)
                    posr.append(p2)

        self.bullets = [i for p,i in enumerate(self.bullets) if not p in posb]
        new = []

        for p,r in enumerate(rocks):
            if not p in posr:
                new.append(r)
            else:
                r.colour = (255,250,205)
                self.ghost_rocks.append(r)
                new += r.children()

        return new

    def reposition(self,crowded=False,rocks=None):
        if not crowded:
            self.pos = [random.randint(100,self.surf.get_size()[i]-100) for i in range(2)]
            self.direction = -90
        else:
            for x in range(0,self.surf.get_width(),25):
                for y in range(0,self.surf.get_height(),25):
                    self.pos = [x,y]

                    if rocks is not None and not self.collide(rocks):
                        return True

            return False
