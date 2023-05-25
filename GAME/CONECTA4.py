from numpy.lib.stride_tricks import broadcast_arrays
from scipy.signal import convolve2d
import pygame
import sys
from pygame.locals import *
from Settings import *
from gameFunctions import *
from functionsAI import *

# Inicializacion de las variables y de programas
pygame.init()

tablero = crearTablero()
ventana = pygame.display.set_mode(TAMVEN)
FONT = pygame.font.SysFont("monospace", int(TAMFI/1.5))
STATE = 'start'
FIN = False
Turno = 0
DIFICULTY = 0

pygame.display.update()

# ----------------- Programa principal --------------------- #

while not FIN:
    if STATE == 'start':
        initText(dibText, ventana)
        if DIFICULTY == 0:
         DIFICULTY = GetDificulty(dibText, ventana, DIFICULTY, STATE)
        if DIFICULTY != 0:
            STATE = 'playing'
    
    elif STATE == 'playing':
        dibTablero(tablero, ventana)
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    FIN = TurnoJugadores(Turno, tablero, ventana, event, FONT, FIN, DIFICULTY)
                    dibTablero(tablero, ventana)
                    Turno = CambioTurno(Turno)