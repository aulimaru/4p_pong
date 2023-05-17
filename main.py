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
        self.speed_x = 0 # speed_x and speed_y are depend on direction and speed, generated by function genspeedxy()
        self.speed_y = 0
        self.radius = radius
    def genspeedxy(self):
        self.speed_x = math.sin(self.direction)*self.speed # calculate speed_x and speed_y using trigonometry
        self.speed_y = math.cos(self.direction)*self.speed
    def move(self):
        self.genspeedxy() # regenerate speed_x and speed_y before using them
        self.x+=self.speed_x # change the pos of ball depend on speed_x and speed_y
        self.y+=self.speed_y
    def render(self):
        pygame.draw.circle(screen,0xffffff,(self.x,self.y),self.radius) # draw the ball on screen


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
