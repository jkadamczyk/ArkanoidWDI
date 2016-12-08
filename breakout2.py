import sys
import pygame
import math

# defined colors to use later
black = (0, 0, 0)
white = (255, 255, 255)
pink = (255, 105, 180)

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight - self.height


isRunning = True
# some variables i need in order to control the game

clock = pygame.time.Clock()  # loading clock in order to limit to certain FPS
gameOver = False
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption('Arkanoid Jakub Adamczyk')
background = pygame.Surface(screen.get_size())
spriteElements = pygame.sprite.Group()
paddle = Paddle() #paddle object
spriteElements.add(paddle)


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

    spriteElements.draw()

pygame.quit()  # game termination
