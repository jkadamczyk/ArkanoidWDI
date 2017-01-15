import math
import pygame

# global hardcoded variables for easier use of colors (RGB format):
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
pink = (255, 105, 180)
grey = (192, 192, 192)
dark_grey = (105, 105, 105)
red = (255, 0, 0)

# hardcoded global block dimensions:
block_width = 58
block_height = 20

'''
Classes inherit from sprite class that is predefined in Pygame, and used for easier creating of game objects
(e.g built-in collide function)
'''


class Block(pygame.sprite.Sprite):
    """Class represents Block, element of the game that is intended to be destroyed by ball"""

    def __init__(self, color, x, y):
        """ Constructor requires color, and coordinates
        color - color of block
        x - x coordinate for block location
        y - y coordinate for block location on screen"""

        # using super class constructor
        super().__init__()

        # creates Blocks surface
        self.image = pygame.Surface([block_width, block_height])

        # fill block with color entered in constructor
        self.image.fill(color)

        # make object a rectangle with dimensions of image
        self.rect = self.image.get_rect()

        # setting rectangle placement using arguments entered
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """Class represents Ball, our main item that bounces when coliding with paddle
     used to destroy blocks"""

    # declaring speed of ball
    speed = 7.0

    # initialising variables for ball coordinates(they will change, but place/memory for them is necessary)
    x = 0.0
    y = 0.0

    # initial declaration for angle in which Ball is moving
    direction = 0

    # determines whether ball is active (moving) at start of game
    # (e.g. it is used when you press space to release the ball)
    isActive = False

    # fixed ball dimensions
    width = 10
    height = 10

    def __init__(self):
        """Ball constructor"""

        # super class constructor is imported
        super().__init__()

        # creating surface of the ball
        self.image = pygame.Surface([self.width, self.height])

        # fill surface with color(red)
        self.image.fill(red)

        # making it a rectangle object
        self.rect = self.image.get_rect()

        # getting main game surface dimensions for class wide use
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, angle_difference):
        """function makes possible for the ball to bounce"""
        self.direction = (180 - self.direction) % 360
        self.direction -= angle_difference

    def update(self):
        """function that updates position of ball
        I have a condition isActive that determines whether we want the ball to behave statically
        ie. when it is above paddle(waiting to press space and start playing), or actively, so it actually moves,
        bounces etc. + returns True when we hit bottom,
        so we use the function to determine life loss or game over state"""

        if self.isActive:
            # converting degrees to radians in order to use it for sine, and cosine
            direction_in_radians = math.radians(self.direction)

            # updating coordinates with actual speed calculated based on direction
            self.x += self.speed * math.sin(direction_in_radians)
            self.y -= self.speed * math.cos(direction_in_radians)

            # moving image accordingly to our calculated coordinates
            self.rect.x = self.x
            self.rect.y = self.y

            # determining top wall bounce
            if self.y <= 0:
                # angle_difference is equal to 0
                self.bounce(0)
                self.y = 1
            # determining left wall bounce
            if self.x <= 0:
                self.direction = (360 - self.direction) % 360
                self.x = 1
            # determining right wall bounce
            if self.x > self.screenwidth - self.width:
                self.direction = (360 - self.direction) % 360
                self.x = self.screenwidth - self.width - 1

            # checking whether we did hit bottom not the paddle
            if self.y > 600:
                return True
            else:
                return False
        else:
            # Get actual mouse position
            pos = pygame.mouse.get_pos()

            # update coordinates so that ball moves when we move paddle
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

        # importing super class constructor
        super().__init__()

        # defining height and width of paddle
        self.width = 90
        self.height = 15

        # set surface of certain size
        self.image = pygame.Surface([self.width, self.height])

        # Fill it with color
        self.image.fill(white)

        # Create rectangular object so that we have it physically
        self.rect = self.image.get_rect()

        # Getting main surface dimensions for class wide use
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        # Setting start position for paddle (middle of surface)
        self.rect.x = 0
        self.rect.y = self.screenheight - self.height

    def update(self):
        """Updating paddles position"""

        # Getting mouse location
        pos = pygame.mouse.get_pos()

        # setting x coord to be paddle position
        self.rect.x = pos[0]

        # Locking it in main game surface
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

"""Here starts our game logic"""
pygame.init()

# Points and lives variable that are displayed in corners(top right and left)
points = 0
lives = 3

# declaring window dimensions
screen = pygame.display.set_mode([800, 600])

# Window label is being set to game name
pygame.display.set_caption('Arkanoid by Jakub Adamczyk')

# making mouse disappear when it is hovering over game window by default
# it is changing during the game ie. in menu it is off
pygame.mouse.set_visible(1)

# declaring main game font + its size (font rendering)
font = pygame.font.Font(None, 36)

# create background/surface that all objects appear on
background = pygame.Surface(screen.get_size())

# our objects containers are being declared here
# allsprites is an Group object that contains all sprite objects (those that are colliding)
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

# Five rows of blocks are crated
for row in range(4):
    # 12 columns of blocks are created
    for column in range(0, blockcount):
        # 2 different colors of blocks
        if row % 2 == 0:
            block = Block(pink, column * (block_width + 5) + 22, top)
        else:
            block = Block(blue, column * (block_width + 5) + 22, top)
        blocks.add(block)
        allsprites.add(block)

    # Move the top of the next row down a little
    top += block_height + 5

# Initialize Clock to limit speed
clock = pygame.time.Clock()

# game over state variable
game_over = False

# program close variable terminates main game  if true
exit_game = False

# variable that makes menu possible when true menu is rendered instead of actual game
playing = False

# start menu buttons rectangles
start = pygame.Rect(250, 200, 300, 50)
quit_game = pygame.Rect(250, 300, 300, 50)

# Main game loop
while not exit_game:

    # checking state in order to show game or menu
    if playing:
        # making ball movable
        pygame.event.set_grab(ball.isActive)

        # Limit to 60 fps, refresh rate
        clock.tick(60)

        # screen refresh (clearing it)
        screen.fill(black)

        # Prints label with points, number of blocks that we destroyed
        labelPoints = font.render("Points: "+str(points), 1, white)
        screen.blit(labelPoints, (5, 5))

        # Prints label with lives left
        labelLives = font.render("Lives: "+str(lives), 1, white)
        screen.blit(labelLives, (700, 5))

        # Process the events in the game
        for event in pygame.event.get():
            # Clicking window X, red, close button
            if event.type == pygame.QUIT:
                exit_game = True
            # Conditions for keypress
            elif event.type == pygame.KEYDOWN:
                # Releasing ball form paddle
                if event.key == pygame.K_SPACE:
                    ball.isActive = True

                # Rematch, replay game
                elif event.key == pygame.K_RETURN and game_over is True:
                    # Reinitializing all game objects, so that we start fresh
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

                # Going back to menu and resetting game
                elif event.key == pygame.K_ESCAPE and game_over is True:
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
                    playing = False
                    # Showing mouse so that we can see what are we clicking in the menu
                    pygame.mouse.set_visible(1)

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
            info = font.render("Press Escape to go back to menu, Enter to play again!", True, white)
            info_position = info.get_rect(centerx=background.get_width() / 2)
            info_position.top = 360
            screen.blit(info, info_position)

        # See if the ball hits the player paddle
        if pygame.sprite.spritecollide(player, balls, False):

            # The 'angle_difference' lets you try to bounce the ball left or right
            # depending where on the paddle you hit it max difference is 22,5 degree
            angle_difference = ((player.rect.x + player.width / 2) - (ball.rect.x + ball.width / 2))/2

            # Set the ball's y position in case
            # we hit the ball on the edge of the paddle
            ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
            ball.bounce(angle_difference)

        # Check for collisions between the ball and the blocks
        deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

        # If we actually hit a block, bounce the ball
        if len(deadblocks) > 0:
            ball.bounce(0)
            # adding points
            points += len(deadblocks)

            # Game ends if all the blocks are gone
            if len(blocks) == 0:
                game_over = True

        # Draw Everything
        allsprites.draw(screen)

        # Flip the screen and show what we've drawn
        pygame.display.flip()

    else:
        # This is the option when game menu is active or playing False in other words
        # Getting and handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
        # Painting surface black
        screen.fill(black)

        # getting mouse position
        mouse = pygame.mouse.get_pos()

        # Getting info whether we click left mouse button
        click = pygame.mouse.get_pressed()
        # Limiting frame rate
        clock.tick(60)
        #Printing text in blocks so in result buttons
        start_text = font.render("START GAME", 1, white)
        start_text_position = start_text.get_rect(centerx=background.get_width() / 2)
        start_text_position.top = 215
        quit_game_text = font.render("QUIT GAME", 1, white)
        quit_game_text_position = quit_game_text.get_rect(centerx=background.get_width() / 2)
        quit_game_text_position.top = 315
        game_title_text = font.render("ARKANOID", 1, white)
        game_title_text_position = game_title_text.get_rect(centerx=background.get_width() / 2)
        game_title_text_position.top = 100


        if 250 <= mouse[0] <= 550 and 200 <= mouse[1] <= 250:
            pygame.draw.rect(screen, dark_grey, start)
            if click[0] == 1:
                playing = True
                pygame.mouse.set_visible(0)


        else:
            pygame.draw.rect(screen, grey, start)

        if 250 <= mouse[0] <= 550 and 300 <= mouse[1] <= 350:
            pygame.draw.rect(screen, dark_grey, quit_game)
            if click[0] == 1:
                exit_game = True
        else:
            pygame.draw.rect(screen, grey, quit_game)

        screen.blit(start_text, start_text_position)
        screen.blit(quit_game_text, quit_game_text_position)
        screen.blit(game_title_text, game_title_text_position)

        # Showing drawn elements
        pygame.display.flip()

# After the loop exit game
pygame.quit()
