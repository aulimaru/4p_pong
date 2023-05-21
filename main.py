import pygame
import sys


pygame.init()
screen_size = (1000, 1000)
screen = pygame.display.set_mode(screen_size)
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
collision_tolerance = 10


class Ball():
    def __init__(self,x,y,length):
        self.rect = pygame.Rect(0, 0, length, length)
        self.rect.center = (x, y)
        self.speed_x = 2
        self.speed_y = 2

    def move(self):
        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y

    def render(self):
        pygame.draw.rect(screen, 0xffffff, self.rect) # draw the ball on screen

    def check_collision(self):
        if self.rect.top < screen_rect.top or self.rect.bottom > screen_rect.bottom or self.rect.left < screen_rect.left or self.rect.right > screen_rect.right:
            pass
            # game_over()

        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if abs(self.rect.top - platform.rect.bottom) <= collision_tolerance and self.speed_y < 0:
                    self.speed_y = abs(self.speed_y)
                if abs(self.rect.bottom - platform.rect.top) <= collision_tolerance and self.speed_y > 0:
                    self.speed_y = -abs(self.speed_y)
                if abs(self.rect.left - platform.rect.right) <= collision_tolerance and self.speed_x < 0:
                    self.speed_x = abs(self.speed_x)
                if abs(self.rect.right - platform.rect.left) <= collision_tolerance and self.speed_x > 0:
                    self.speed_x = -abs(self.speed_x)


class Platform():
    def __init__(self, x, y, width, height, keymaps):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.keymaps = keymaps
        self.speed = 10

    def render(self):
        pygame.draw.rect(screen, 0xffffff, self.rect)

    def control(self):
        # sets direction when key pressed
        self.direction = (0, 0)
        pressed_keys = pygame.key.get_pressed()
        for keymap in self.keymaps:
            if pressed_keys[keymap]:
                self.direction = self.keymaps.get(keymap)
    
    def move(self):
        # moves platform according to direction
        if self.direction == (0, -1):
            self.rect.y -= self.speed
        elif self.direction == (0, 1):
            self.rect.y += self.speed
        elif self.direction == (-1, 0):
            self.rect.x -= self.speed
        elif self.direction == (1, 0):
            self.rect.x += self.speed

    def check_collision(self):
        # prevent the platform from going outside screen
        if self.rect.top < screen_rect.top:
            self.rect.top = screen_rect.top
        if self.rect.bottom > screen_rect.bottom:
            self.rect.bottom = screen_rect.bottom
        if self.rect.left < screen_rect.left:
            self.rect.left = screen_rect.left
        if self.rect.right > screen_rect.right:
            self.rect.right = screen_rect.right

        # prevent platforms from going inside each other
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if abs(self.rect.top - platform.rect.bottom) <= collision_tolerance and self.direction == (0, -1):
                    self.rect.top = platform.rect.bottom
                if abs(self.rect.bottom - platform.rect.top) <= collision_tolerance and self.direction == (0, 1):
                    self.rect.bottom = platform.rect.top
                if abs(self.rect.left - platform.rect.right) <= collision_tolerance and self.direction == (-1, 0):
                    self.rect.left = platform.rect.right
                if abs(self.rect.right - platform.rect.left) <= collision_tolerance and self.direction == (1, 0):
                    self.rect.right = platform.rect.left



#set up
ball = Ball(screen_rect.width/2, screen_rect.height/2,5)
platforms = [
        Platform(50, screen_rect.height // 2, 10, 100, {pygame.K_w: (0, -1), pygame.K_s: (0, 1)}),
        Platform(screen_rect.width - 50, screen_rect.height // 2, 10, 100, {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}),
        Platform(screen_rect.width // 2, 50, 100, 10, {pygame.K_a: (-1, 0), pygame.K_d: (1, 0)}),
        Platform(screen_rect.width // 2, screen_rect.height - 50, 100, 10, {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}),
]


while True:
    screen.fill(0x000000)
    for event in pygame.event.get(): # poll for events, pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # RENDER YOUR GAME HERE
    ball.move()
    ball.check_collision()
    ball.render()

    for platform in platforms:
        platform.control()
        platform.move()
        platform.check_collision()
        platform.render()
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
