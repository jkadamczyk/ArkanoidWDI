import pygame, sys
from pygame.locals import *

# Determines frames per seconf changing it speeds up or slows down game
FPS = 60

# Global variable for setting window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Variables for paddle size
PADDLE_SIZE = 125
PADDLE_THICKNESS = 10

# ball dimensions:
BALL_HEIGHT = 10
BALL_WIDTH = 10

# Variables for global color names:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREY = (168, 168, 168)


def updatePaddle(x):
    pos = pygame.mouse.get_pos()
    x = pos[0]


def drawBall(ball):
    pygame.draw.rect(DISPLAY_SURFACE, WHITE, ball)


def drawPaddle(paddle):
    if paddle.left < 0:
        paddle.left = 0
    if paddle.left > WINDOW_WIDTH - PADDLE_SIZE:
        paddle.left = WINDOW_WIDTH - PADDLE_SIZE
    pygame.draw.rect(DISPLAY_SURFACE, GREY, paddle)


def main():
    pygame.init()
    global DISPLAY_SURFACE
    clock = pygame.time.Clock()

    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption('Arkanoid') # sets label on window in my case it's game name 'arkanoid'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(FPS)
        pygame.mouse.set_visible(0)

        # update coords:
        pos = pygame.mouse.get_pos()
        PADDLE_X = pos[0]
        PADDLE_Y = WINDOW_HEIGHT - PADDLE_THICKNESS - 10
        BALL_X = PADDLE_X + (PADDLE_SIZE - BALL_WIDTH) / 2
        BALL_Y = PADDLE_Y - PADDLE_THICKNESS

        ball = pygame.Rect(BALL_X, BALL_Y, BALL_WIDTH, BALL_HEIGHT)
        paddle = pygame.Rect(PADDLE_X, PADDLE_Y, PADDLE_SIZE, PADDLE_THICKNESS)

        # drawing elements:
        DISPLAY_SURFACE.fill(BLACK)
        drawPaddle(paddle)
        drawBall(ball)


if __name__ == '__main__':
    main()