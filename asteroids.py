# area for imports -->
import pygame
import random
import time
import math
# <--

# makes it so each asteroid is its own object -->
class Asteroid:
    def __init__(self, x, y, radius, xspeed, yspeed, color, child):
        self.x = x
        self.y = y
        self.child = child
        self.radius = radius
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.color = color
        self.initTimer = 0 # determines when self.initialized will be true
        self.initialized = self.child # this changes the state of the asteroids... if it is a child it will be immediatel initialized

    def move(self):
        if not self.initialized:
            self.checkAsteroid()

        self.x += self.xspeed
        self.y += self.yspeed

    def checkAsteroid(self):

        if self.initTimer > 100:
            self.initialized = True
        else:
            self.initTimer += 1

    def draw(self):
        if self.initialized:
            circle(self.x, self.y, self.radius, self.color)
        else:
            circle(self.x, self.y, self.radius, green)


# <--

# turns bullets into objects so they are easier to handle -->
class Bullet:
    def __init__(self, x, y, angle, timer):
        self.x = x
        self.y = y
        self.angle = angle
        self.timer = timer
        self.maxSpeed = 10
        self.xspeed = math.cos(self.angle) * self.maxSpeed
        self.yspeed = math.sin(self.angle) * self.maxSpeed
        self.radius = 5

    def move(self):
        self.x += self.xspeed
        self.y += self.yspeed

    def draw(self):
        self.timer += 1 # this timer will tell the bullet when to stop being drawn
        circle(int(self.x), int(self.y), self.radius, white)
# <--

# general functions -->

def addText(text, x, y, fontSize, color):
    myfont = pygame.font.SysFont('phosphate', fontSize) #phosphate

    textsurface = myfont.render(text, True, color)
    gameDisplay.blit(textsurface, (x, y))

def wrapEdges(x, y, wrapRadius):

    # function that will make it so any x and y value
    # can never fall off screen. this will be shared
    # by many different objects
    # the wrap radius tells where to wrap it for each
    # object... each object needs to appear slightly different
    # amounts off screen, and this handles it


    if x > displayWidth + wrapRadius:
        x = -wrapRadius
    elif x < -wrapRadius:
        x = displayWidth + wrapRadius

    if y > displayHeight + wrapRadius:
        y = -wrapRadius
    elif y < -wrapRadius:
        y = displayHeight + wrapRadius

    return x, y

def touching(x1, y1, x2, y2, r1, r2):
    # functin that can be called to check the distance
    # between two objects
    # easy to use because all objects are circles
    # so they must be touching if their distance is
    # less than the sum of their radii

    diffX = x2 - x1
    diffY = y2 - y1

    distance = math.sqrt((diffX**2) + (diffY**2))

    if distance < (r1 + r2):
        return True

    return False

def checkLives(lives):
    global asteroids
    global brokenPieces
    global bullets
    global playerX
    global playerY
    global xPortion
    global yPortion

    if lives < 1:
        exitGame()

    else:
        asteroids = []
        brokenPieces = []
        bullets = []

        playerX = displayWidth / 2
        playerY = displayHeight / 2

        xPortion = 0
        yPortion = 0

        lives -= 1
        return lives

def exitGame():
    pygame.quit()
    quit()
# <--

# initializing asteroids window -->
pygame.init()
pygame.font.init()

displayWidth = 600
displayHeight = 400
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('asteroids')
# <--

# colors -->
red = (255, 0, 0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
darkGray = (100,100,100)
lightGray = (200,200,200)
# <--

# handles the framerates -->
FPS = 60
clock = pygame.time.Clock()
# <--

# variables surrounding the asteroids -->
asteroids = []
brokenPieces = []
brokenChildren = []
# <--

# variables and functions surrounding the player -->
playerX = 300
playerY = 200
playerRadius = 15
playerSpeedX = 0
playerSpeedY = 0
direction = 0
degreeMove = 0
gunLen = 30
xPortion = 0
yPortion = 0
friction = 0
speedMag = 0
friction = 0
starter = False # this will give the player an initial velocity
score = 0
lives = 3

def drawPlayer(x, y, angle):
    circle(x, y, playerRadius, white)

    gunX = playerX + (math.cos(angle) * gunLen)
    gunY = playerY + (math.sin(angle) * gunLen)

    line(playerX, playerY, gunX, gunY, white, 2)

    return gunX, gunY
# <--

# variables surrounding the bullet -->
bullets = []
# <--

# variables surrounding the asteroid -->
maxAsteroids = 2
# <--

# shortcuts for drawing functions -->
def rect(x, y, w, h, color):
    pygame.draw.rect(gameDisplay, color, (x,y,w,h))

def circle(x, y, r, color):
    pygame.draw.circle(gameDisplay, color, [int(x),int(y)], int(r))

def triangle(x, y, w, h, color):
    pygame.draw.polygon(gameDisplay, color, [(x, y), (x - w, y + h), (x + w, y + h)])

def line(x1, y1, x2, y2, color, width):
    pygame.draw.line(gameDisplay, color, (x1, y1), (x2, y2), width)
# <--

# allows this to be called multiple times whenever needed -->
def initializeAsteroids():
    randX = random.randint(0, displayWidth)
    randY = random.randint(0, displayHeight)
    randRad = random.randint(15, 30)
    randSpeedX = random.randint(-5, 5)
    randSpeedY = random.randint(-5, 5)

    asteroid = Asteroid(randX, randY, randRad, randSpeedX, randSpeedY, red, False)

    asteroids.append(asteroid)
# <--

# initializes screen with two asteroids -->
for i in range(2):
    initializeAsteroids()
# <--

# main game loop -->
alive = True
while alive:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                degreeMove -= 0.1

            elif event.key == pygame.K_d:
                degreeMove += 0.1

            elif event.key == pygame.K_w:
                speedMag = 5
                friction = 0

                xPortion = math.cos(direction)
                yPortion = math.sin(direction)

                starter = True

            elif event.key == pygame.K_j:
                bullets.append(Bullet(gunx, guny, direction, 0))


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                degreeMove = 0

            elif event.key == pygame.K_w:
                friction = 0.01

    gameDisplay.fill(black)
    addText('score: ' + str(score) , 0, 0, 30, white) # draws the score to the screen
    addText('lives: ' + str(lives) , displayWidth - 100, 0, 30, white)

    # handles the movement of the ship and its slowing down -->
    direction += degreeMove

    speedMag *= (1-friction)
    if speedMag < 1:
        speedMag = 0

    if starter:
        playerSpeedX = xPortion * speedMag
        playerSpeedY = yPortion * speedMag
    else:
        playerSpeedX = 3


    playerX += playerSpeedX
    playerY += playerSpeedY

    playerX, playerY = wrapEdges(playerX, playerY, 20)

    gunx, guny = drawPlayer(int(playerX), int(playerY), direction)
    # <--

    # draws each asteroid object in the asteroids array and checks if they have touched the player -->
    for ast in asteroids:
        ast.x, ast.y = wrapEdges(ast.x, ast.y, ast.radius)

        ast.move()
        ast.draw()

        if touching(ast.x, ast.y, playerX, playerY, ast.radius, playerRadius) and ast.initialized:
            lives = checkLives(lives)
    # <--

    # draws each bullet in the bullets array and checks if they need to be removed -->
    for bul in bullets:
        bul.x, bul.y = wrapEdges(bul.x, bul.y, bul.radius)

        bul.move()
        bul.draw()

        if bul.timer >= 50:
            bullets.remove(bul)

        for ast in asteroids:
            if touching(ast.x, ast.y, bul.x, bul.y, ast.radius, bul.radius) and ast.initialized:

                score += 50

                childRight = Asteroid(ast.x, ast.y, ast.radius / 2, ast.xspeed * random.uniform(0.1, 2), ast.yspeed * random.uniform(0.1, 2), blue, True)
                childLeft = Asteroid(ast.x, ast.y,  ast.radius / 2, -ast.xspeed * random.uniform(0.1, 2), ast.yspeed * random.uniform(0.1, 2), blue, True)

                brokenPieces.append(childRight)
                brokenPieces.append(childLeft)

                bullets.remove(bul)
                asteroids.remove(ast)


    # <--

    # draws each broken piece of the asteroid as a new asteroid object -->
    for piece in brokenPieces:
        piece.x, piece.y = wrapEdges(piece.x, piece.y, int(piece.radius / 2))

        piece.move()
        piece.draw()

        if touching(piece.x, piece.y, playerX, playerY, piece.radius, playerRadius) and piece.initialized:
            lives = checkLives(lives)

        for bul in bullets:
            if touching(piece.x, piece.y, bul.x, bul.y, piece.radius, bul.radius):

                score += 100

                bullets.remove(bul)
                brokenPieces.remove(piece)

    if len(asteroids) < 1 and len(brokenPieces) < 1:
        maxAsteroids += 1
        asteroidNumber = random.randint(0, maxAsteroids)

        for i in range(asteroidNumber):
            initializeAsteroids()
    # <--

    pygame.display.update()
    clock.tick(FPS)
# <--
