import sys
import pygame
import math

# defined colors to use later
black = (0, 0, 0)
white = (255, 255, 255)
pink = (255, 105, 180)


isRunning = True
# some variables i need in order to control the game

clock = pygame.time.Clock()  # loading clock in order to limit to certain FPS
gameOver = False
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption('Arkanoid Jakub Adamczyk')
background = pygame.Surface(screen.get_size())


# Main game loop is below

pygame.init()  # game initialization

while isRunning:
    clock.tick()
    screen.fill(black)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False


pygame.quit()  # game termination
