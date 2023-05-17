import pygame
import math
width = 1280
height = 720
screen_size = (width, height)
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True
class Ball():
    def __init__(self,x,y,radius):
        self.speed = 0 # the movement speed of the ball
        self.direction = 0 # the direction of the ball, using bearing degree
        self.x = x
        self.y = y
        self.radius = radius
    def move(self):
        pass

class Platform():
    def __init__(self, x, y, length, height):
        self.x = x
        self.y = y
        self.length = length
        self.height = height

while running:
    for event in pygame.event.get(): # poll for events, pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False # if event type is pygame.QUIT, then quit
    # RENDER YOUR GAME HERE



    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
