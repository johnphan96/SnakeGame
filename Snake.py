import random
import math
import tkinter as tk
from tkinter import messagebox

import pygame


class cube(object):
    rows = 20
    w = 500

    # Cube object with direction and color
    def __init__(self, start, dirnx=1, dirny=0, color=(0, 255, 0)):
        self.pos = start
        self.directionX = 1
        self.directionY = 0
        self.color = color

    # Move cube
    def move(self, dirnx, dirny):
        self.directionX = dirnx
        self.directionY = dirny
        self.pos = (self.pos[0] + self.directionX, self.pos[1] + self.directionY)

    # Draw cube
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            lefteye = (i * dis + centre - radius, j * dis + 8)
            righteye = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), lefteye, radius)
            pygame.draw.circle(surface, (0, 0, 0), righteye, radius)


class snake(object):
    body = []
    turns = {}

    # Snake object with color, position, head, body, and direction
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.directionX = 0
        self.directionY = 1

    # Add turns to turn list on key input
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                # Turn left
                if keys[pygame.K_LEFT] and self.directionX != 1:
                    self.directionX = -1
                    self.directionY = 0
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                # Turn right
                elif keys[pygame.K_RIGHT] and self.directionX != -1:
                    self.directionX = 1
                    self.directionY = 0
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                # Turn up
                elif keys[pygame.K_UP] and self.directionY != 1:
                    self.directionX = 0
                    self.directionY = -1
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                # Turn down
                elif keys[pygame.K_DOWN] and self.directionY != -1:
                    self.directionX = 0
                    self.directionY = 1
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            # Make c turn at p
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # If on last cube, remove turn
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            else:
                if c.directionX == -1 and c.pos[0] <= 0:  # Left edge check
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.directionX == 1 and c.pos[0] >= c.rows - 1:  # Right edge check
                    c.pos = (0, c.pos[1])
                elif c.directionY == 1 and c.pos[1] >= c.rows - 1:  # Bottom edge check
                    c.pos = (c.pos[0], 0)
                elif c.directionY == -1 and c.pos[1] <= 0:  # Top edge check
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.directionX, c.directionY)  # Keep moving forward

    # Reset game
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directionX = 0
        self.directionY = 1

    # Add cube to snake
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.directionX, tail.directionY

        # Check which direction tail moving in to add cube to proper position
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        # Give new cube direction same with tail
        self.body[-1].directionX = dx
        self.body[-1].directionY = dy

    # draw snake
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:  # To identify head of snake
                c.draw(surface, True)
            else:
                c.draw(surface)


# Draw grid
def drawGrid(w, rows, surface):
    sizeBetween = w // rows

    x = 0
    y = 0
    for line in range(rows):
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


# Put a snack on screen at random location
def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # Filter out positions of the snake
            continue
        else:
            break

    return (x, y)


# Pop-up tkinter window
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global height, width, rows, s, snack
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width, height))
    s = snake((0, 255, 255), (10, 10))
    snack = cube(randomSnack(rows, s), color=(255, 0, 0))
    flag = True

    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(255, 0, 0))

        # Game over if run into own body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                message_box("Game Over!", ("Score: ", len(s.body)))
                s.reset((10, 10))
                break

        redrawWindow(win)

    pass


main()
