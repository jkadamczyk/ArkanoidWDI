import math
import pygame

# global hardcoded variables for easier use of colors:
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
pink = (255, 105, 180)
red = (255, 0, 0)
# hardcoded global block dimensions:
block_width = 58
block_height = 20


class Menu:
    """Class used to create menu object"""

    def __init__(self):



class Block(pygame.sprite.Sprite):
    """Class represents Block, element of the game that is intended to be destroyed by ball"""

    def __init__(self, color, x, y):
        """ Constructor requires color, and coordinates """
        super().__init__()
        # creates Blocks surface
        self.image = pygame.Surface([block_width, block_height])
        # fill block with color
        self.image.fill(color)
        # make object a rectangle with dimensions of image
        self.rect = self.image.get_rect()
        # place object where it should be placed
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """Class represents Ball, our main item that is bounced with paddle, used to destroy blocks"""

    # some class wide variables name says for itself
    speed = 7.0
    x = 0.0
    y = 0.0
    direction = 0 # in degrees
    isActive = False # determines whether ball is active (moving) at start of game
    width = 10
    height = 10

    def __init__(self):
        super().__init__()
        # creating surface of the ball
        self.image = pygame.Surface([self.width, self.height])
        # fill surface with some color
        self.image.fill(red)
        # Make proper rectangle that is filled with our surface and color
        self.rect = self.image.get_rect()
        # storing class-wide our display surface dimesnions
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        """function makes possible for the ball to bounce"""
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        """function that updates position of ball
        i have a condition isActive that determines whether we want the ball to behave statically
        ie. when it is above paddle, or actively, so it actually moves, bounces etc. + returns True when we hit bottom,
        so we use the function to determine life loss or game over state"""
        if self.isActive:
            # converting degrees to radians in order to use it for sine, and cosine
            direction_radians = math.radians(self.direction)
            # updating coords with actual speed calculated based on direction
            self.x += self.speed * math.sin(direction_radians)
            self.y -= self.speed * math.cos(direction_radians)
            # moving image accordingly to our coords
            self.rect.x = self.x
            self.rect.y = self.y
            # determining top wall bounce
            if self.y <= 0:
                self.bounce(0) # diff is equal to 0
                self.y = 1
            # determining left wall bounce
            if self.x <= 0:
                self.direction = (360 - self.direction) % 360
                self.x = 1
            # determining right wall bounce
            if self.x > self.screenwidth - self.width:
                self.direction = (360 - self.direction) % 360
                self.x = self.screenwidth - self.width - 1
            # checking whether we did hit botto m not the paddle
            if self.y > 600:
                return True
            else:
                return False
        else:
            # Get actual mouse position
            pos = pygame.mouse.get_pos()
            self.x = pos[0] + 45 - self.width/2
            self.y = self.screenheight - 30
            # Checking if our ball doesn't go to far right
            if self.x > self.screenwidth - 45 - self.width/2:
                self.x = self. screenwidth - 45 - self.width/2
            # Giving the object actual coordinates
            self.rect.x = self.x
            self.rect.y = self.y


class Paddle(pygame.sprite.Sprite):
    """Class represents paddle that we use to bounce the ball in block direction"""

    def __init__(self):
        """Constructor for paddle"""
        super().__init__()
        # Define objects attributes
        self.width = 90
        self.height = 15
        # set surface of certain size
        self.image = pygame.Surface([self.width, self.height])
        # Fill it with color
        self.image.fill(white)
        # Fetch rectangle on the coloured surface
        self.rect = self.image.get_rect()
        # Getting our main surface/background dimensions
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        # Setting default position for paddle it needs some
        self.rect.x = 0
        self.rect.y = self.screenheight - self.height

    def update(self):
        """Updating paddles position"""
        # Getting mouse location
        pos = pygame.mouse.get_pos()
        # setting x coord to be paddle position
        self.rect.x = pos[0]
        # Check whether the paddle doesn't go too far right
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

"""Here starts our game logic"""
pygame.init()
# Points and lives variable that is diplayed int op corners
points = 0
lives = 3
#declaring window dimensions
screen = pygame.display.set_mode([800, 600])
# Window label is being set to game name
pygame.display.set_caption('Arkanoid by Jakub Adamczyk')
# making mouse disappear when it is hovering over game window
pygame.mouse.set_visible(0)
# declaring main game font + its size
font = pygame.font.Font(None, 36)
# create background/surface that all objects appear on
background = pygame.Surface(screen.get_size())
# our objects containers are being declared here
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
# creating paddle object and adding it to allsprites group
player = Paddle()
allsprites.add(player)
# creating the ball object and adding it to balls group and allsprites group
ball = Ball()
allsprites.add(ball)
balls.add(ball)
# determining how far from top blocks are starting to generate
top = 80
# determining number of blocks in a row
blockcount = 12
# Five rows of blocks
for row in range(4):
    # 12 columns of blocks
    for column in range(0, blockcount):
        # 2 different colors of blocks
        if row % 2 == 0:
            block = Block(pink, column * (block_width + 5) + 22, top)
        else:
            block = Block(blue, column * (block_width + 5) + 22, top)
        blocks.add(block)
        allsprites.add(block)
    # Move the top of the next row down
    top += block_height + 5
# Clock to limit speed
clock = pygame.time.Clock()
# game over state variable
game_over = False
# program close variable temrinates main game  if true
exit_game = False
# Main game loop
while not exit_game:
    pygame.event.set_grab(ball.isActive)
    # Limit to 45 fps also determines speed of game
    clock.tick(60)
    # screen refresh (clearing it)
    screen.fill(black)
    # Prints label with points, blocks that we destroyed
    labelPoints = font.render("Points: "+str(points), 1, white)
    screen.blit(labelPoints, (5, 5))

    # Prints label with lives left
    labelLives = font.render("Lives: "+str(lives), 1, white)
    screen.blit(labelLives, (700, 5))

    # Process the events in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.isActive = True

            elif event.key == pygame.K_RETURN and game_over == True:
                points = 0
                lives = 3
                game_over = False
                allsprites.empty()
                balls.empty()
                blocks.empty()
                player = Paddle()
                allsprites.add(player)
                ball = Ball()
                allsprites.add(ball)
                balls.add(ball)
                top = 80
                for row in range(4):
                    for column in range(0, blockcount):
                        # Create a block (color,x,y)
                        if row % 2 == 0:
                            block = Block(pink, column * (block_width + 5) + 22, top)
                        else:
                            block = Block(blue, column * (block_width + 5) + 22, top)
                        blocks.add(block)
                        allsprites.add(block)
                    # Move the top of the next row down
                    top += block_height + 5


    # Update the ball and player position as long
    # as the game is not over.
    if not game_over:
        # Update the player and ball positions
        player.update()
        if ball.update():
            lives -= 1
            ball.isActive = False
            ball.direction = 0
            if lives == 0:
                game_over = True
                ball.isActive = False

    # If we are done, print game over
    if game_over:
        if points == 48:
            text = font.render("YOU WON!", True, white)
        else:
            text = font.render("Game Over!", True, white)
        text_position = text.get_rect(centerx=background.get_width() / 2)
        text_position.top = 300
        screen.blit(text, text_position)
        score = font.render("You scored " + str(points) + " points!", True, white)
        score_position = score.get_rect(centerx=background.get_width() / 2)
        score_position.top = 330
        screen.blit(score, score_position)

    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player, balls, False):
        # The 'diff' lets you try to bounce the ball left or right
        # depending where on the paddle you hit it
        diff = (player.rect.x + player.width / 2) - (ball.rect.x + ball.width / 2)

        # Set the ball's y position in case
        # we hit the ball on the edge of the paddle
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)

    # Check for collisions between the ball and the blocks
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

    # If we actually hit a block, bounce the ball
    if len(deadblocks) > 0:
        ball.bounce(0)
        points += len(deadblocks)

        # Game ends if all the blocks are gone
        if len(blocks) == 0:
            game_over = True

    # Draw Everything
    allsprites.draw(screen)

    # Flip the screen and show what we've drawn
    pygame.display.flip()

pygame.quit()
