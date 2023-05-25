import numpy as np
from numpy.lib.stride_tricks import broadcast_arrays
from scipy.signal import convolve2d
from Settings import *
import pygame
from pygame.locals import *
import math


def crearTablero():
    """Create the board with NFilas y NColumnas"""
    Tablero = np.zeros((NFilas, NColumnas))
    return Tablero


def soltarPieza(Tablero, y, x, Pieza):
    """Drop the piece at the specified coordinates"""
    Tablero[x][y] = Pieza


def movidaLegal(Tablero, x):
    """Informs if the movement is valid"""
    if Tablero[NFilas-1][x] == 0:
        return True
    else:
        print('Ya no caben fichas ahí!')
        return False


def filaDisp(Tablero, x):
    """Informs of the available rows"""
    for i in range(NFilas):
        if Tablero[i][x] == 0:
            return i


def Orientacion(Tablero):
    """Flip the board"""
    #print(np.flip(Tablero, 0))


def jugadaGanadora(board, piece):
    """"Check locations for winning last move"""
    # Check horizontal locations for win
    for c in range(NColumnas-3):
        for r in range(NFilas):
            if board[r][c] == piece \
               and board[r][c+1] == piece \
               and board[r][c+2] == piece \
               and board[r][c+3] == piece:
                    return True

    # Check vertical locations for win
    for c in range(NColumnas):
        for r in range(NFilas-3):
            if board[r][c] == piece \
               and board[r+1][c] == piece \
               and board[r+2][c] == piece \
               and board[r+3][c] == piece:
                    return True

    # Check positively sloped diaganols
    for c in range(NColumnas-3):
        for r in range(NFilas-3):
            if board[r][c] == piece \
               and board[r+1][c+1] == piece \
               and board[r+2][c+2] == piece \
               and board[r+3][c+3] == piece:
                    return True

    # Check negatively sloped diaganols
    for c in range(NColumnas-3):
        for r in range(3, NFilas):
            if board[r][c] == piece \
               and board[r-1][c+1] == piece \
               and board[r-2][c+2] == piece \
               and board[r-3][c+3] == piece:
                    return True

def DibujaRaya(ventana, F1, C1, F2, C2, F3, C3, F4, C4):
    """Marca la jugada ganadora final"""
    pygame.draw.rect(ventana, BLANCO,
                    (C1*TAMFI, ALTURA-F1*TAMFI, TAMFI, TAMFI))
    pygame.draw.rect(ventana, BLANCO,
                    (C2*TAMFI, ALTURA-F2*TAMFI, TAMFI, TAMFI))
    pygame.draw.rect(ventana, BLANCO,
                    (C3*TAMFI, ALTURA-F3*TAMFI, TAMFI, TAMFI))
    pygame.draw.rect(ventana, BLANCO,
                    (C4*TAMFI, ALTURA-F4*TAMFI, TAMFI, TAMFI))
    pygame.display.update()

    pygame.time.wait(3500)
    


def SumaPesos(F, C, vpesos):
    """Sum the weights for the selection of differents
    cells of the board based on the updated player position
    """
    F1 = F+vpesos[0]
    C1 = C+vpesos[1]
    F2 = F+vpesos[2]
    C2 = C+vpesos[3]
    F3 = F+vpesos[4]
    C3 = C+vpesos[5]
    F4 = F+vpesos[6]
    C4 = C+vpesos[7]

    return F1, C1, F2, C2, F3, C3, F4, C4


def CasillasGanadoras(TipoVictoria, F, C):
    """Select the winning cells in function of type of
    of victory
    """
    if TipoVictoria == 0: # Gana de forma horizontal
        print('Gano de manera horizontal')
        vpesos=[1, 0, 1, 1, 1, 2, 1, 3] # Pesos a sumar hor
        F1, C1, F2, C2, F3, C3, F4, C4 = SumaPesos(F, C, vpesos) 
        return F1, C1, F2, C2, F3, C3, F4, C4

    elif TipoVictoria == 1: # Gana de forma vertical
        print('Gano de manera vertical')
        vpesos=[1, 0, 2, 0, 3, 0, 4, 0] # Pesos a sumar ver
        F1, C1, F2, C2, F3, C3, F4, C4 = SumaPesos(F, C, vpesos) 
        return F1, C1, F2, C2, F3, C3, F4, C4

    elif TipoVictoria == 2: # Gana de forma diagonal Positiva
        print('Gano de manera diagonal positiva')
        vpesos=[1, 0, 2, 1, 3, 2, 4, 3] # Pesos a sumar ver
        F1, C1, F2, C2, F3, C3, F4, C4 = SumaPesos(F, C, vpesos) 
        return F1, C1, F2, C2, F3, C3, F4, C4

    elif TipoVictoria == 3: # Gana de forma diagonal Negativa
        print('Gano de manera diagonal negativa')
        vpesos=[1, 0, 0, 1, -1, 2, -2, 3] # Pesos a sumar ver
        F1, C1, F2, C2, F3, C3, F4, C4 = SumaPesos(F, C, vpesos) 
        return F1, C1, F2, C2, F3, C3, F4, C4

    else:
        print('Victoria no se encuentra entre los valores reconocidos')


def Ganar(Tablero, Pieza, ventana):
    """Similar as winning_move but drawing if it wins a 4x1 rectangle"""
    # Ganar horizontalmente
    for C in range(NColumnas-3):
        for F in range(NFilas):
            if Tablero[F][C] == Pieza and Tablero[F][C+1] == Pieza \
               and Tablero[F][C+2] == Pieza and Tablero[F][C+3] == Pieza:
                    F1, C1, F2, C2, F3, C3, F4, C4 = CasillasGanadoras(0, F, C)
                    DibujaRaya(ventana, F1, C1, F2, C2, F3, C3, F4, C4)
                    return True

    # Ganar verticalmente
    for C in range(NColumnas):
        for F in range(NFilas-3):
            if Tablero[F][C] == Pieza and Tablero[F+1][C] == Pieza \
                and Tablero[F+2][C] == Pieza and Tablero[F+3][C] == Pieza:
                    F1, C1, F2, C2, F3, C3, F4, C4 = CasillasGanadoras(1, F, C)
                    DibujaRaya(ventana, F1, C1, F2, C2, F3, C3, F4, C4)
                    return True

    # Ganar Diagonalmente Positivamente
    for C in range(NColumnas-3):
        for F in range(NFilas-3):
            if Tablero[F][C] == Pieza and Tablero[F+1][C+1] == Pieza \
                and Tablero[F+2][C+2] == Pieza \
                and Tablero[F+3][C+3] == Pieza:
                    F1, C1, F2, C2, F3, C3, F4, C4 = CasillasGanadoras(2, F, C)
                    DibujaRaya(ventana, F1, C1, F2, C2, F3, C3, F4, C4)
                    return True

    # Ganar Diagonalmente Negativamente
    for C in range(NColumnas-3):
        for F in range(3, NFilas):
            if Tablero[F][C] == Pieza and Tablero[F-1][C+1] == Pieza \
                and Tablero[F-2][C+2] == Pieza \
                and Tablero[F-3][C+3] == Pieza:
                    F1, C1, F2, C2, F3, C3, F4, C4 = CasillasGanadoras(3, F, C)
                    DibujaRaya(ventana, F1, C1, F2, C2, F3, C3, F4, C4)
                    return True


def dibTablero(Tablero, ventana):
    """Draw the board knowing the measures of the window and spaces"""
    for C in range(NColumnas):
        for F in range(NFilas):
            pygame.draw.rect(ventana, AZUL,
                            (C*TAMFI, F*TAMFI+TAMFI, TAMFI, TAMFI))
            pygame.draw.circle(ventana, NEGRO,
                              (int(C*TAMFI+TAMFI/2),
                               int(F*TAMFI+TAMFI+TAMFI/2)),
                              RAD)

        for C in range(NColumnas):
            for F in range(NFilas):
                if Tablero[F][C] == 1:
                    pygame.draw.circle(ventana, ROJO,
                                      (int(C*TAMFI+TAMFI/2),
                                       ALTURA-int(F*TAMFI+TAMFI/2)),
                                      RAD)
                elif Tablero[F][C] == 2:
                    pygame.draw.circle(ventana, AMARILLO,
                                      (int(C*TAMFI+TAMFI/2),
                                       ALTURA-int(F*TAMFI+TAMFI/2)),
                                      RAD)

    pygame.display.update()


def dibText(words, ventana, pos, size, colour, font_name, centered=False):
        """Draw the messages that we could read in the upper part 
        of the board
        """
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        pos = list(pos)
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        ventana.blit(text, pos)


def initText(draw_text, ventana):
        """Function that initializes the fixed text in the board"""
        ventana.fill(NEGRO)
        draw_text('Select IA Dificulty with 1-5', ventana, (ANCHO//2, 10+100),
                 START_TEXT_SIZE, AMARILLO, START_FONT, centered=True)
        draw_text('1 = Easy', ventana, (10, 50+100),
                 START_TEXT_SIZE, ROJO, START_FONT, centered=False)
        draw_text('2 = Medium', ventana, (10, 70+100),
                 START_TEXT_SIZE, ROJO, START_FONT, centered=False)
        draw_text('3 = Expert', ventana, (10, 90+100),
                 START_TEXT_SIZE, ROJO, START_FONT, centered=False)
        draw_text('4 = Master', ventana, (10, 110+100),
                 START_TEXT_SIZE, ROJO, START_FONT, centered=False)
        draw_text('5 = Imposible', ventana, (10, 130+100),
                 START_TEXT_SIZE, ROJO, START_FONT, centered=False)
        
        draw_text('Jugador vs IA', ventana, (ANCHO//2, ALTURA//2+50),
                 START_TEXT_SIZE, (30, 30, 150), START_FONT, centered=True)
        draw_text('Conecta 4 con MINIMAX', ventana,
                 (ANCHO//2, ALTURA//2+85), START_TEXT_SIZE,
                 (255, 255, 255), START_FONT, centered=True)
        draw_text('Equipo 1 IA MUAR UPM 2021-2022', ventana,
                 (ANCHO//2, ALTURA//2+110), START_TEXT_SIZE, (30, 200, 150),
                 START_FONT, centered=True)
        pygame.display.update()
        
def Player(draw_text, ventana, PL):
    """Function introduce the text of the different turns"""
    pygame.draw.rect(ventana, NEGRO, (0, 0, NColumnas*TAMFI, TAMFI))
    pygame.display.update()
    FONT = pygame.font.SysFont("monospace", int(TAMFI/3))
    STR = str(PL)
    if(PL == AI_PIECE):
        S = 'Turno de la IA. Click para jugar'
    else:
        S = 'Turno del jugador ' + STR + '. Sel. Columna'

    TXT1 = FONT.render(S, 1, BLANCO)
    ventana.blit(TXT1, (10, 10))
    pygame.display.update()


def GetDificulty(draw_text, ventana, DIF, state):
    FONT = pygame.font.SysFont("monospace", int(TAMFI/3))
    for event in pygame.event.get():
        if  event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                DIF = 1
                DIFI = str(1)
                ST = 'You have chosen level ' + DIFI
                TXT1 = FONT.render(ST, 1, BLANCO)
                ventana.blit(TXT1, (ANCHO//2-200, ALTURA/2+150))
                pygame.display.update()
                pygame.time.wait(3000)
                
        if  event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                DIF = 2
                DIFI = str(2)
                ST = 'You have chosen level ' + DIFI
                TXT1 = FONT.render(ST, 1, BLANCO)
                ventana.blit(TXT1, (ANCHO//2-200, ALTURA/2+150))
                pygame.display.update()
                pygame.time.wait(3000)
        if  event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                DIF = 3
                DIFI = str(3)
                ST = 'You have chosen level ' + DIFI
                TXT1 = FONT.render(ST, 1, BLANCO)
                ventana.blit(TXT1, (ANCHO//2-200, ALTURA/2+150))
                pygame.display.update()
                pygame.time.wait(3000)
        if  event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                DIF = 4
                DIFI = str(4)
                ST = 'You have chosen level ' + DIFI
                TXT1 = FONT.render(ST, 1, BLANCO)
                ventana.blit(TXT1, (ANCHO//2-200, ALTURA/2+150))
                pygame.display.update()
                pygame.time.wait(3000)
        if  event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                DIF = 5
                DIFI = str(5)
                ST = 'You have chosen level ' + DIFI
                TXT1 = FONT.render(ST, 1, BLANCO)
                ventana.blit(TXT1, (ANCHO//2-200, ALTURA/2+150))
                pygame.display.update()
                pygame.time.wait(3000)
    return DIF


def turnoJugador(player, tablero, ventana, event, font, FIN):
    """Involves all the previous functions that have to deal 
    with the player turn and its"""
    posx = event.pos[0]
    x = int(math.floor(posx/TAMFI))
    if movidaLegal(tablero, x):
        y = filaDisp(tablero, x)
        soltarPieza(tablero, x, y, player)
        if Ganar(tablero, player, ventana):
            pygame.draw.rect(ventana, NEGRO, (0, 0, NColumnas*TAMFI, TAMFI))
            SPL = str(player)
            S = 'The Player WIINS!'
            TXT = font.render(S, 1, BLANCO)
            ventana.blit(TXT, (10, 10))
            FIN = True
            pygame.display.update()
            pygame.time.wait(3000)

    Player(dibText, ventana, AI_PIECE)
    
    return FIN
