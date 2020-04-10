import pygame
import random
from enum import Enum
#pylint: disable=no-member

pygame.init()
screen = pygame.display.set_mode((800, 600))

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    STAY = 5

class Tank:

    def __init__(self, x, y, speed, color, d_right = pygame.K_RIGHT, d_left = pygame.K_LEFT, d_up = pygame.K_UP, d_down = pygame.K_DOWN):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT
        
        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT, d_up: Direction.UP, d_down: Direction.DOWN}

    def draw(self):
        tank_c = (self.x + self.width // 2, self.y +self.width // 2)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, self.width // 2)

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c, (self.x + 3*self.width//2, self.y + self.width//2), 4)
        
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x - self.width//2, self.y + self.width//2), 4)
        
        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width//2, self.y - self.width//2), 4)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width//2, self.y + 3*self.width//2), 4)


    def changeDirection(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        
        if self.direction == Direction.UP:
            self.y -= self.speed

        if self.direction == Direction.DOWN:
            self.y += self.speed
        self.draw()


mainloop = True
tank1 = Tank(300, 300, 1, (255, 0, 0))
tank2 = Tank(100, 100, 1, (0, 255, 0), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
tanks = [tank1, tank2]

clock = pygame.time.Clock()

while mainloop:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            
            # for tank in tanks:
            #     if event.key in tank.KEY.keys():
            #         tank.changeDirection(tank.KEY[event.key])

    pressed = pygame.key.get_pressed()
    for tank in tanks:
        # print(tank.direction)
        stay = True
        for key in tank.KEY.keys():
            if pressed[key]:
                tank.changeDirection(tank.KEY[key])
                stay = False
        if stay:
            tank.changeDirection(Direction.STAY)

    screen.fill((0, 0, 0))
    for tank in tanks:
        tank.move()
    pygame.display.flip()

pygame.quit()