"""
Gra:
    Samochodzik - Samochód z określoną prędkością i mozliwością skrętu
    stara się jak najdłuzej pozostać przy zyciu nie uderzając w ścianę.

Autorzy:
    Aleksander Dudek s20155
    Jakub Słomiński  s18552

Przygotowanie środowiska:
    Do działania potrzebny jest język Python, najlepiej python3
    Musimy zainstalować bibliotekę PyGame: python3 -m pip install -U pygame --user
    Aby upewnić się, czy biblioteka PyGame działa poprawnie
    skorzystajmy z tej instrukcji: python3 -m pygame.examples.aliens
    Jeśli wszystko jest skonfigurowane, uruchamiamy grę: python3 cargame.py

"""

import pygame
import math
pygame.init()

"""
Helper function making rotating images easier
"""


def blit_rotate_center(window, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rect.topleft)


"""
Constant values
"""
SCREEN_SIZE = WIDTH, HEIGHT = 1200, 1200
SPEED = [0, 0]
BLACK = 0, 0, 0
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CAR_SPEED = 8
CAR_ROTATION_SPEED = 6
CAR = pygame.transform.scale(pygame.image.load("CAR.png"), (100, 50))
CAR = pygame.transform.rotate(CAR, -90.0)
TRACK = pygame.transform.scale(pygame.image.load("TRACK.png"), (WIDTH, HEIGHT))
TRACK_MASK = pygame.mask.from_surface(TRACK)
CLOCK = pygame.time.Clock()

"""
PlayerCar class handling all the car functionalities
"""


class PlayerCar:
    """
    Initializes the car velocity, rotation velocity, image and starting position
    """

    def __init__(self, vel, rotation_vel, img, start_pos):
        self.img = img
        self.vel = vel
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = start_pos

    """
    Rotation function setting the car angle
    """

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    """
    How to draw our car
    """

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    """
    Update our car position, move it forward
    """

    def move_forward(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

    """
    Check car collision
    """

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        intersection = mask.overlap(car_mask, offset)
        return intersection


class DebugLine():
    """
    Initializes the screen where to draw, the surface
    the debug line is supposed to be attached to
    and line angle
    """

    def __init__(self, surface, player_car, angle):
        self.surface = surface
        self.player_car = player_car
        self.angle = angle  # 0.5
        self.endX = 0
        self.endY = 0

    """
    Update our line position according to the attached object
    and display it on the screen
    """

    def update(self):
        startX = player_car.x + CAR.get_size()[0] / 2
        startY = player_car.y + CAR.get_size()[1] / 2
        radians = math.radians(player_car.angle) + self.angle
        vertical = math.cos(radians) * 130
        horizontal = math.sin(radians) * 130
        self.endY = startY - vertical
        self.endX = startX - horizontal
        pygame.draw.line(SCREEN, (255, 255, 255),
                         (startX, startY), (self.endX, self.endY))
        pygame.display.update()

    """
    Checking collision at the tip of the line
    """

    def collide(self, mask, x=0, y=0):
        dot_mask = pygame.mask.Mask(size=(1, 1), fill=True)
        offset = (int(self.endX - x), int(self.endY - y))
        intersection = mask.overlap(dot_mask, offset)
        return intersection


"""
Draw multiple images using one function
"""


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()


"""
Initialize our main game objects
"""
playing = True
CLOCK = pygame.time.Clock()
images = [(TRACK, (0, 0))]
player_car = PlayerCar(CAR_SPEED, CAR_ROTATION_SPEED, CAR, (120, 400))
debug_line_left = DebugLine(SCREEN, player_car, 0.5)
debug_line_right = DebugLine(SCREEN, player_car, -0.5)


"""
Main game loop
"""
while playing:
    CLOCK.tick(60)
    """
    Close the application when the game comes to an end
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            break

    """
    Move the car forward
    """
    player_car.move_forward()

    """
    Check the debug lines collision and rotate the car accordingly
    """
    if debug_line_left.collide(TRACK_MASK) != None:
        player_car.rotate(right=True)
    if debug_line_right.collide(TRACK_MASK) != None:
        player_car.rotate(left=True)

    """
    Game is lost, close the application when the car hits the wall
    """
    if player_car.collide(TRACK_MASK) != None:
        print("Collide")
        playing = False
        break

    """
    Update and draw all objects
    """
    SCREEN.fill(BLACK)
    draw(SCREEN, images, player_car)
    debug_line_left.update()
    debug_line_right.update()

pygame.quit()
