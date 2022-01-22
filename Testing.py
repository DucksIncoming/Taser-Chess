#import chess
#import chess.engine
#import time
#from pyfirmata import Arduino
import pygame

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run =False

pygame.quit()