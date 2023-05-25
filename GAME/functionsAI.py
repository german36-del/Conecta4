import pygame
import random
from Settings import *
from gameFunctions import *


# Funciones de la IA del juego
def funcionPuntua(ventana_deslizante, Pieza):
    """On the first attempt of the IA the function
    which introduce the weights to calculate the
    punctuation of every move
    """
    puntuacion = 0
    pieza_contrario = PLAYER_PIECE
    if Pieza == PLAYER_PIECE:
        pieza_contrario = AI_PIECE
    if ventana_deslizante.count(Pieza) == 4:
            puntuacion += 100
    elif ventana_deslizante.count(Pieza) == 3 \
            and ventana_deslizante.count(VACIO) == 1:
            puntuacion += 5
    elif ventana_deslizante.count(Pieza) == 2 \
            and ventana_deslizante.count(VACIO) == 2:
            puntuacion += 2
    if ventana_deslizante.count(pieza_contrario) == 3 \
            and ventana_deslizante.count(VACIO) == 1:
            puntuacion -= 4

    return puntuacion


def puntuacionHeuristica(Tablero, Pieza):
    """Function which returns the accumulated punctuation
    en each case: horizontal, vertical and the two types
    of diagonal
    """
    puntuacion = 0
    vector_centro = [int(i) for i in list(Tablero[:, NColumnas//2])]
    cuenta_centro = vector_centro.count(Pieza)
    puntuacion += cuenta_centro * 3

    # Puntuar horizontalmente
    for F in range(NFilas):
        vector_filas = [int(t) for t in list(Tablero[F, :])]
        for C in range(NColumnas-3):
            ventana_deslizante = vector_filas[C:C+ANCHO_VENTANA]
            puntuacion += funcionPuntua(ventana_deslizante, Pieza)

    # Puntuar verticalmente
    for C in range(NColumnas):
        vector_columnas = [int(i) for i in list(Tablero[:, C])]
        for F in range(NFilas-3):
            ventana_deslizante = vector_columnas[F:F+ANCHO_VENTANA]
            puntuacion += funcionPuntua(ventana_deslizante, Pieza)

    # Puntuar diagonalmente positivo
    for F in range(NFilas-3):
        for C in range(NColumnas-3):
            ventana_deslizante = [Tablero[F+i][C+i]
                                  for i in range(ANCHO_VENTANA)]
            puntuacion += funcionPuntua(ventana_deslizante, Pieza)

    # Puntuar diagonalmente negativo
    for F in range(NFilas-3):
        for C in range(NColumnas-3):
            ventana_deslizante = [Tablero[F+3-i][C+i]
                                  for i in range(ANCHO_VENTANA)]
            puntuacion += funcionPuntua(ventana_deslizante, Pieza)

    return puntuacion


def es_nodoFinal(Tablero):
    """Check if the node that is being checked is final node"""
    return jugadaGanadora(Tablero, PLAYER_PIECE) \
        or jugadaGanadora(Tablero, AI_PIECE) \
        or len(posValidas(Tablero)) == 0


def posValidas(Tablero):
    """Returns a vector of the valid positions that could be played"""
    posiciones_v = []
    for col in range(NColumnas):
        if movidaLegal(Tablero, col):
            posiciones_v.append(col)

    return posiciones_v


def minimax(Tablero, profundidad, alpha, beta, maximizingPlayer):
    """Minimax algorythm with alpha-beta pruning method"""
    localizaciones_validas = posValidas(Tablero)
    nodo_final = es_nodoFinal(Tablero)
    if profundidad == 0 or nodo_final:
        if nodo_final:
            if jugadaGanadora(Tablero, AI_PIECE):
                return (None, 1000000000000000000)  # inf
            elif jugadaGanadora(Tablero, PLAYER_PIECE):
                return (None, -10000000000000000000)  # menos inf
            else:  # No + mov validos
                return (None, 0)
        else:  # Profundidad 0
            return (None, puntuacionHeuristica(Tablero, AI_PIECE))

    if maximizingPlayer:
        valor = -math.inf
        columna = random.choice(localizaciones_validas)
        for col in localizaciones_validas:
            row = filaDisp(Tablero, col)
            copia_tablero = Tablero.copy()
            #print("MAX: ", row, " - ", col)
            soltarPieza(copia_tablero, col, row, AI_PIECE)  # col row change
            nueva_puntuacion = minimax(copia_tablero, profundidad-1,
                                       alpha, beta, False)[1]
            if nueva_puntuacion > valor:
                valor = nueva_puntuacion
                columna = col
            alpha = max(alpha, valor)
            if alpha >= beta:
                break
        return columna, valor

    else:
        valor = math.inf
        columna = random.choice(localizaciones_validas)
        for col in localizaciones_validas:
            row = filaDisp(Tablero, col)
            copia_tablero = Tablero.copy()
            #print("MIN: ", row, " - ", col)
            soltarPieza(copia_tablero, col, row, PLAYER_PIECE)  # colrow change
            nueva_puntuacion = minimax(copia_tablero, profundidad-1,
                                       alpha, beta, True)[1]
            if nueva_puntuacion < valor:
                valor = nueva_puntuacion
                columna = col
            beta = min(beta, valor)
            if alpha >= beta:
                break
        return columna, valor


def agente(Tablero, Pieza):
    """Agent that plays with a more elementary artificial intelligence"""
    posiciones_v = posValidas(Tablero)
    mejor_puntuacion = 100000
    mejor_col = random.choice(posiciones_v)
    for y in posiciones_v:
        x = filaDisp(Tablero, y)
        Tablero_auxiliar = Tablero.copy()
        soltarPieza(Tablero_auxiliar, y, x, Pieza)
        puntuacion = puntuacionHeuristica(Tablero_auxiliar, Pieza)
        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_col = y

    return mejor_col

def TurnoJugadores(Turno, tablero, ventana, event, FONT, FIN, DIF):
    """ In function of the type of turn do one thing or 
    another 
    """
    # Jugador 1
    if Turno == PLAYER:
        FIN = turnoJugador(PLAYER_PIECE, tablero, ventana,
                            event, FONT, FIN)
        return FIN
    # Jugador 2 - AI
    else:
        FIN = juega_AI(tablero, ventana, FONT, FIN, DIF)
        return FIN
    

def CambioTurno(Turno):
    """Realiza el cambio de turno"""
    Turno += 1
    Turno = Turno % 2

    return Turno


def juega_AI(tablero, ventana, font, FIN, DIF):
    """Agent that plays with the minmax algorythm"""
        # x = agente(tablero,AI_PIECE)
    x, minimax_score = minimax(tablero, DIF, -math.inf, math.inf, True)

    if movidaLegal(tablero, x):
        pygame.time.wait(500)
        y = filaDisp(tablero, x)
        soltarPieza(tablero, x, y, AI_PIECE)
        if Ganar(tablero, AI_PIECE, ventana):
            pygame.draw.rect(ventana, NEGRO, (0, 0, NColumnas*TAMFI, TAMFI))
            SPL = str(AI_PIECE)
            S = 'IA WIIIINS !!!'
            TXT = font.render(S, 1, BLANCO)
            ventana.blit(TXT, (10, 10))
            FIN = True
            pygame.display.update()
            pygame.time.wait(3000)
    Player(dibText, ventana, PLAYER_PIECE)
    return FIN
