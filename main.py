import pygame
screen_width = 1280
screen_height = 720
screen_size = (screen_width, screen_height)
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True
class Ball():
    def __init__(self,x,y,radius):

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
