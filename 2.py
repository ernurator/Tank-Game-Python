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


##########################################    Bullet    ##########################################


class Bullet:

    def __init__(self, tank):
        self.tank = tank
        self.color = tank.color
        self.width = 4
        self.length = 6
        self.direction = tank.direction
        self.speed = 500
        if tank.direction == Direction.RIGHT:
            self.x = tank.x + 3*tank.width//2
            self.y = tank.y + tank.width//2
            self.height = 4
            self.width = 6
        
        if tank.direction == Direction.LEFT:
            self.x = tank.x - tank.width//2
            self.y = tank.y + tank.width//2
            self.height = 4
            self.width = 6
        
        if tank.direction == Direction.UP:
            self.x = tank.x + tank.width//2
            self.y = tank.y - tank.width//2
            self.height = 6
            self.width = 4

        if tank.direction == Direction.DOWN:
            self.x = tank.x + tank.width//2
            self.y = tank.y + 3*tank.width//2
            self.height = 6
            self.width = 4
        
    def draw(self):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def move(self, sec):
        if self.direction == Direction.RIGHT:
            self.x += int(self.speed * sec)
        
        if self.direction == Direction.LEFT:
            self.x -= int(self.speed * sec)
        
        if self.direction == Direction.UP:
            self.y -= int(self.speed * sec)

        if self.direction == Direction.DOWN:
            self.y += int(self.speed * sec)
        self.draw()
    

##########################################    Tanks    ##########################################


class Tank:

    def __init__(self, x, y, speed, color, d_right = pygame.K_RIGHT, d_left = pygame.K_LEFT, d_up = pygame.K_UP, d_down = pygame.K_DOWN, fire = pygame.K_SPACE):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT
        self.is_static = True
        self.fire_key = fire
        
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

    def move(self, sec):
        if not self.is_static:
            if self.direction == Direction.RIGHT:
                self.x += int(self.speed * sec)
                if self.x > screen.get_size()[0]:
                    self.x = 0 - 40
            
            if self.direction == Direction.LEFT:
                self.x -= int(self.speed * sec)
                if self.x < -self.width:
                    self.x = screen.get_size()[0] + 40
            
            if self.direction == Direction.UP:
                self.y -= int(self.speed * sec)
                if self.y < -self.width:
                    self.y = screen.get_size()[1] + 40

            if self.direction == Direction.DOWN:
                self.y += int(self.speed * sec)
                if self.y > screen.get_size()[1]:
                    self.y = 0 - 40
        self.draw()


##########################################    Collisions    ##########################################


def checkCollisions(bullet):
    global tanks    
    for i in range(len(tanks)):
        dist_x = bullet.x - tanks[i].x
        dist_y = bullet.y - tanks[i].y
        if -bullet.width <= dist_x <= tanks[i].width and -bullet.height <= dist_y <= tanks[i].width and bullet.tank != tanks[i]:
            del tanks[i]
            return True
    return False


##########################################    Init    ##########################################


mainloop = True
arys = Tank(300, 300, 800//6, (255, 0, 0))
era = Tank(100, 100, 800//6, (0, 255, 0), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_1)
# tank3 = Tank(100, 100, 800//6, (0, 0, 0xff), pygame.K_h, pygame.K_f, pygame.K_t, pygame.K_g, pygame.K_2)
# tank4 = Tank(100, 100, 800//6, (0xff, 255, 0), pygame.K_l, pygame.K_j, pygame.K_i, pygame.K_k, pygame.K_3)
tanks = [arys, era]
bullets = []

clock = pygame.time.Clock()
FPS = 60


##########################################    Main loop    ##########################################


while mainloop:
    millis = clock.tick(FPS)
    seconds = millis / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            
            for tank in tanks:
                if event.key == tank.fire_key:
                    bullets.append(Bullet(tank))

    pressed = pygame.key.get_pressed()
    for tank in tanks:
        # print(tank.direction)
        stay = True
        for key in tank.KEY.keys():
            if pressed[key]:
                tank.changeDirection(tank.KEY[key])
                tank.is_static = False
                stay = False
        if stay:
            tank.is_static = True
            

    screen.fill((0, 0, 0))
    for tank in tanks:
        tank.move(seconds)
    for i in range(len(bullets)):
        if i >= len(bullets): break
        bullets[i].move(seconds)
        if checkCollisions(bullets[i]): del bullets[i]

    pygame.display.flip()

pygame.quit()