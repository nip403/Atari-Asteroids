import StandardLevels

import pygame
import numpy
import math
import sys

pygame.init()

class CommonScreens:
    def __init__(self,surf):
        self.surf = surf
        self.s = self.surf.get_size()
        self.font = pygame.font.SysFont("Garamond MS",50)
        self.font2 = pygame.font.SysFont("Garamond MS",20)

    def startscreen(self):
        title = self.font.render("Atari Asteroids",True,(255,255,255))
        sub = self.font2.render("Version Alpha 0.0.2",True,(255,255,255))
        foot = self.font2.render("Made by NIP",True,(255,255,255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return

            self.surf.fill((0,0,0))
            
            self.surf.blit(title,title.get_rect(center=[self.s[0]/2,self.s[1]/2-60]))
            self.surf.blit(sub,sub.get_rect(center=[self.s[0]/2,self.s[1]/2+30]))
            self.surf.blit(foot,foot.get_rect(center=[self.s[0]/2,self.s[1]/2+50]))

            pygame.display.flip()

    def deathscreen(self,result):
        title = self.font.render(f"You died on round {result['Level']}" if result.get("Endless",False) else f"You {'beat' if result['Lives'] else 'died on'} level {result['Level']} with {result['Lives']} lives left",True,(255,255,255))
        sub = self.font2.render("Click to go to main menu",True,(255,255,255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return

            self.surf.fill((0,0,0))
            
            self.surf.blit(title,title.get_rect(center=[self.s[0]/2,self.s[1]/2-60]))
            self.surf.blit(sub,sub.get_rect(center=[self.s[0]/2,self.s[1]/2+30]))
            
            pygame.display.flip()

    def main_menu(self):
        title = self.font.render("Choose a gamemode",True,(255,255,255))
        text_b1 = self.font2.render("Campaign",True,(255,255,255))
        text_b2 = self.font2.render("Endless",True,(255,255,255))

        box1 = pygame.Rect(150,300,200,200)
        box2 = pygame.Rect(650,300,200,200)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.Rect(list(map(lambda i: i-1,pygame.mouse.get_pos())),[2,2])
                    
                    if mouse.colliderect(box1):
                        return False
                    elif mouse.colliderect(box2):
                        return True

            self.surf.fill((0,0,0))
            
            self.surf.blit(title,title.get_rect(center=[self.s[0]/2,self.s[1]/2-200]))
            self.surf.blit(text_b1,text_b1.get_rect(center=box1.center))
            self.surf.blit(text_b2,text_b2.get_rect(center=box2.center))

            pygame.draw.rect(self.surf,(255,255,255),box1,1)
            pygame.draw.rect(self.surf,(255,255,255),box2,1)

            pygame.display.flip()
            
        return True

    def level_menu(self):
        startx = 75
        starty = 75
        
        title = self.font.render("Levels",True,(255,255,255))
        page_lim = [6,4] # x,y button res, size=100,100
        capacity = int(numpy.prod(page_lim))

        pagesR = [[pygame.Rect(startx+((i%page_lim[0])*150),starty+((i//page_lim[0])*150),100,100) for i in range(capacity if n < math.ceil(StandardLevels.__LEVEL_COUNT__/capacity)-1 else StandardLevels.__LEVEL_COUNT__ % capacity)] for n in range(math.ceil(StandardLevels.__LEVEL_COUNT__/capacity))]
        current_page = 0
        buttons = pygame.Surface([24*len(pagesR),24],pygame.SRCALPHA)

        back = pygame.Surface([25,25],pygame.SRCALPHA)
        pygame.draw.line(back,(255,0,0),(0,0),(25,25),1)
        pygame.draw.line(back,(255,0,0),(25,0),(0,25),1)
        
        for i in range(len(pagesR)):
            pygame.draw.circle(buttons,(255,255,255),(12+(24*i),12),6,1 if not i == current_page else 0)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        current_page += 1

                    elif event.key == pygame.K_LEFT:
                        current_page -= 1

                    if current_page < 0:
                        current_page = len(pagesR) - 1
                    elif current_page > len(pagesR) - 1:
                        current_page = 0

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(list(map(lambda i: i-1,pygame.mouse.get_pos())),[2,2]).colliderect(back.get_rect(topleft=[20,20])):
                        return self.main_menu()
                    
                    for p,b in enumerate(pagesR[current_page]):
                        if pygame.Rect(list(map(lambda i: i-1,pygame.mouse.get_pos())),[2,2]).colliderect(b):
                            return p+(current_page*capacity)

            self.surf.fill((0,0,0))
            self.surf.blit(back,(20,20))

            for p,r in enumerate(pagesR[current_page]):
                pygame.draw.rect(self.surf,(255,255,255) if not 1+p+(current_page*capacity) in StandardLevels.__BOSS_LEVELS__+[StandardLevels.__FINAL_LEVEL__] else (255,0,0),r,0 if p == StandardLevels.__FINAL_LEVEL__ else 1)

                l = self.font2.render(f"Level {p+1+(current_page*capacity)}",True,(255,255,255))
                self.surf.blit(l,l.get_rect(center=r.center))

            buttons.fill((0,0,0))
            for i in range(len(pagesR)):
                pygame.draw.circle(buttons,(255,255,255),(12+(24*i),12),6,1 if not i == current_page else 0)

            self.surf.blit(title,title.get_rect(center=[self.s[0]/2,40]))
            self.surf.blit(buttons,buttons.get_rect(center=[self.surf.get_width()/2,self.surf.get_height()-25]))

            pygame.display.flip()
