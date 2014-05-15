from random import choice
from time import sleep

from network import Handler, poll
from random import randint
from pygame import Rect

################### MODEL #############################
def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1
    
def make_rect(quad):  # make a pygame.Rect from a list of 4 integers
    x, y, w, h = quad
    return Rect(x, y, w, h)
class NetworkModel(Handler):
    def __init__(self, host, port, sock=None):
        Handler.__init__(self,host,port,sock)
        self.size=None
        self.borders = None
        self.pellets = None
        self.players = None
        self.myname = None
        print "connect"
    def on_close(self):
        print "stop"
        exit()
    def on_msg(self, data):
        self.borders = [make_rect(b) for b in data['borders']]
        self.pellets = [make_rect(p) for p in data['pellets']]
        self.players = {name: make_rect(p) for name, p in data['players'].items()}
        self.myname = data['myname']
        if self.size is not None:
            if self.players[self.myname][3]>self.size:
                print "Ate Pellet"
                self.size=self.players[self.myname][3]
        else:
            self.size=self.players[self.myname][3]
        
    def do_cmd(self, cmd):
        if cmd == 'quit':
            print "QUIT"
            exit()
        else:
            self.do_send({'input':cmd})
            
    def update(self):
        poll()
            


################### CONTROLLER #############################
class NetworkController():
    def __init__(self,m):
        self.m = m

    def move(self):
        if self.m.pellets is not None:
            p = self.m.pellets[0]  # always target the first pellet
            b = self.m.players[self.m.myname]
            if p[0] > b[0]:
                cmd = 'right'
            elif p[0] + p[2] <= b[0]: # p[2] to avoid stuttering left-right movement
                cmd = 'left'
            elif p[1] > b[1]:
                cmd = 'down'
            else:
                cmd = 'up'
            self.m.do_cmd(cmd)


################### CONSOLE VIEW #############################

class ConsoleView():
    def __init__(self, m):
        
        self.m = m
        self.frame_freq = 20
        self.frame_count = 0
        
    def display(self):
        self.frame_count += 1
        if self.frame_count == self.frame_freq:
            self.frame_count = 0


################### PYGAME VIEW #############################
# this view is only here in case you want to see how the bot behaves

import pygame

def make_rect(quad):  # make a pygame.Rect from a list of 4 integers
    x, y, w, h = quad
    return Rect(x, y, w, h)
class PygameView():
    
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        
    def display(self):
        if self.m.borders is not None:
        
            pygame.event.pump()
            screen = self.screen
            borders = self.m.borders
            pellets = self.m.pellets
            players = self.m.players
            screen.fill((0, 0, 64))  # dark blue
            for name, p in players.items():
                if name != self.m.myname:
                    pygame.draw.rect(screen, (255, 0, 0), p)  # red
            if self.m.myname:
                pygame.draw.rect(screen, (0, 191, 255), players[self.m.myname])  # Deep Sky Blue
            [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
            [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
            pygame.display.update()
        
################### LOOP #############################

model = NetworkModel('localhost', 8888)
c = NetworkController(model)
# v = ConsoleView(model)
v2 = PygameView(model)
while 1:
    sleep(0.02)
    model.update()
    c.move()
#     v.display()
    v2.display()
