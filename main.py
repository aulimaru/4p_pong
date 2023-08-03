import random

import pygame
import sys
import math

class Ball():
    def __init__(self, x, y, length):
        self.rect = pygame.Rect(0, 0, length, length)
        self.length = length
        self.center = (x, y)
        self.speed = 3
        self.velocity = self.init_velocity()
        self.accel = 0.02  # (0,1] smaller the value, slower the ac/deceleration, 1 will set speed to self.speed always.
        self.owner = None

    def vector_to_speed(self, x):
        return math.sqrt(x.x**2+x.y**2)

    def init_velocity(self):
        x = 0.13+random.random()*0.86  # to make the first ball never go towards the platform, x = 0.13 ~ 0.99
        y = math.sqrt(1-x**2)
        x *= (random.randint(0, 1) - 0.5) * 2
        y *= (random.randint(0, 1) - 0.5) * 2
        return pygame.math.Vector2(x*self.speed, y*self.speed)


    def move(self):
        self.center += self.velocity
        self.rect.center=self.center
        self.velocity /= (self.vector_to_speed(self.velocity) / self.speed - 1) * self.accel + 1  # de/acceleration

    def render(self):
        pygame.draw.line(screen, "red", self.rect.center, self.velocity*1024+self.rect.center)
        pygame.draw.line(screen, "green", self.rect.center, self.rect.center+self.velocity*10)  # the direction line and prediction line are bad because of int problem, but IDK how.
        pygame.draw.rect(screen, "white", self.rect)  # draw the ball on screen

    def check_outside(self):
        if screen_rect.contains(self.rect):
            return
        if self.owner is not None:
            self.owner.score += 1
        if self.rect.top < screen_rect.top:
            platforms[0].score -= 1
        if self.rect.bottom > screen_rect.bottom:
            platforms[1].score -= 1
        if self.rect.left < screen_rect.left:
            platforms[2].score -= 1
        if self.rect.right > screen_rect.right:
            platforms[3].score -= 1
        main()

    def check_collision(self):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if abs(self.rect.top - platform.rect.bottom) <= COLLISION_TOLERANCE and self.velocity.y < 0:
                    self.velocity.reflect_ip(DOWN)
                    self.velocity+=platform.direction*platform.speed
                elif abs(self.rect.bottom - platform.rect.top) <= COLLISION_TOLERANCE and self.velocity.y > 0:
                    self.velocity.reflect_ip(UP)
                    self.velocity += platform.direction * platform.speed
                elif abs(self.rect.left - platform.rect.right) <= COLLISION_TOLERANCE and self.velocity.x < 0:
                    self.velocity.reflect_ip(RIGHT)
                    self.velocity += platform.direction * platform.speed
                elif abs(self.rect.right - platform.rect.left) <= COLLISION_TOLERANCE and self.velocity.x > 0:
                    self.velocity.reflect_ip(LEFT)
                    self.velocity += platform.direction * platform.speed
                self.owner = platform


class Platform():
    def __init__(self, x, y, width, height, keymaps, algorithm):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.keymaps = keymaps
        self.speed = 10
        self.score = 0
        self.direction = pygame.Vector2(0, 0)
        self.algorithm = algorithm

    def render(self):
        pygame.draw.rect(screen, "white", self.rect)
        text_surface = FONT.render(f"{self.score}", True, "white")
        screen.blit(text_surface, self.rect.bottomright)

    #  Algorithms
    def alg_manual(self):
        # sets direction when key pressed
        direction = pygame.Vector2(0, 0)
        pressed_keys = pygame.key.get_pressed()
        for keymap in self.keymaps:
            if pressed_keys[keymap]:
                direction += self.keymaps.get(keymap)
        return direction

    def alg_chaseball(self):
        pass  # I can't fucking do this, so hard

    def control(self):
        match self.algorithm:
            case "manual":
                self.direction = self.alg_manual()

    def move(self):
        # moves platform according to direction
        self.rect.move_ip(self.direction * self.speed)

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
                if abs(self.rect.top - platform.rect.bottom) <= COLLISION_TOLERANCE and self.direction == UP:
                    self.rect.top = platform.rect.bottom
                if abs(self.rect.bottom - platform.rect.top) <= COLLISION_TOLERANCE and self.direction == DOWN:
                    self.rect.bottom = platform.rect.top
                if abs(self.rect.left - platform.rect.right) <= COLLISION_TOLERANCE and self.direction == LEFT:
                    self.rect.left = platform.rect.right
                if abs(self.rect.right - platform.rect.left) <= COLLISION_TOLERANCE and self.direction == RIGHT:
                    self.rect.right = platform.rect.left


def main():
    #set up
    ball = Ball(screen_rect.width // 2, screen_rect.height // 2, 5)

    platforms[0].rect.center = (screen_rect.width // 2, GAP)
    platforms[1].rect.center = (screen_rect.width // 2, screen_rect.height - GAP)
    platforms[2].rect.center = (GAP, screen_rect.height // 2)
    platforms[3].rect.center = (screen_rect.width - GAP, screen_rect.height // 2)


    while True:
        screen.fill("black")
        for event in pygame.event.get(): # poll for events, pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # RENDER YOUR GAME HERE
        for platform in platforms:
            platform.control()
            platform.check_collision()
            platform.move()
            platform.render()

        ball.move()
        ball.check_collision()
        ball.check_outside()
        ball.render()


        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

if __name__ == "__main__":
    pygame.init()
    screen_size = (1024, 1024)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont("None", 24)
    COLLISION_TOLERANCE = 10
    UP = pygame.Vector2(0, -1)
    DOWN = pygame.Vector2(0, 1)
    LEFT = pygame.Vector2(-1, 0)
    RIGHT = pygame.Vector2(1, 0)
    GAP = 100
    platforms = [
            Platform(screen_rect.width // 2, GAP, 100, 10, {pygame.K_a: LEFT, pygame.K_d: RIGHT}, "manual"),
            Platform(screen_rect.width // 2, screen_rect.height - GAP, 100, 10, {pygame.K_LEFT: LEFT, pygame.K_RIGHT: RIGHT}, "manual"),
            Platform(GAP, screen_rect.height // 2, 10, 100, {pygame.K_w: UP, pygame.K_s: DOWN}, "manual"),
            Platform(screen_rect.width - GAP, screen_rect.height // 2, 10, 100, {pygame.K_UP: UP, pygame.K_DOWN: DOWN}, "manual"),
    ]
    main()
