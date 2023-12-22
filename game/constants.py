import os
import pygame


WIDTH = 400
HEIGHT = 600
FPS = 60
LASER_PRICE = 5
GAME_CHANCES = 3
SHOOT_DELAY = 250
LAST_SHOT = pygame.time.get_ticks()

GAME_FOLDER = os.path.dirname(__file__)
IMG_FOLDER = os.path.join(GAME_FOLDER, 'img')
