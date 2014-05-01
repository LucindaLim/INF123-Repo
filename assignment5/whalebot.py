from random import randint
from time import sleep
import random
import common
################### CONTROLLER #############################

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RCTRL, K_LCTRL, K_c

class Controller():
    def __init__(self, m):
        self.m = m
        pygame.init()
    
    def poll(self):
        cmd = None
#         x = random.randint(0,3)
#         if x == 0:
#                 cmd = 'up'
#         elif x == 1:
#             cmd = 'down'
#         elif x == 2:
#             cmd = 'left'
#         elif x == 3:
#             cmd = 'right'
            
        pelletPosition = self.m.pellets[0]
        pelletPositionX = pelletPosition[0]
        pelletPositionY = pelletPosition[1]
        differenceX = self.m.mybox[0] - pelletPositionX
        differenceY =  self.m.mybox[1] - pelletPositionY
        if differenceY > 0:
            cmd = 'up'
        elif differenceY < 0:
            cmd = 'down'
        elif differenceX > 0:
            cmd = 'left'
        elif differenceX < 0:
            cmd = 'right'
        for event in pygame.event.get():  # inputs
            keys = pygame.key.get_pressed()
            if event.type == QUIT:
                cmd = 'quit'
            if event.type == KEYDOWN:
                key = event.key
                if keys[K_LCTRL] and keys[K_c]:
                    cmd = 'quit'
                elif keys[K_RCTRL] and keys[K_c]:
                    cmd = 'quit'
#                 elif key == K_UP: #Assignment states that user input is not required
#                     cmd = 'up'    # It didn't say to remove user input
#                 elif key == K_DOWN:# so I left it. :D
#                     cmd = 'down'
#                 elif key == K_LEFT:
#                     cmd = 'left'
#                 elif key == K_RIGHT:
#                     cmd = 'right'
        if cmd:
            self.m.do_cmd(cmd)

################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        
    def display(self):
        screen = self.screen
        borders = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
        pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
        b = self.m.mybox
        myrect = pygame.Rect(b[0], b[1], b[2], b[3])
        fps = pygame.time.get_ticks()
        if fps%50 == 0:
            print "Position: " , b[0], " ,", b[1]
        screen.fill((0, 0, 64))  # dark blue
        pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
        [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
        [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
        pygame.display.update()
    
################### LOOP #############################

model = common.Model()
c = Controller(model)
v = View(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()
