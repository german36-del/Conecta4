#Definir el numero de final y columnas que tendrá el juego
NFilas = 6
NColumnas = 7

#Definir el tipo de juego Ej conecta4 o conecta5 o conecta6 etc
JUEGODE = 4

#Definir dificultad de la IA - Profundidad de búsqueda de forma manual
PROFUNDIDAD = 1

## Parametros juegos
LIMITEHOR = 3
LIMITEVER = 2

ANCHO_VENTANA = 4
VACIO = 0
FIN = False

START_TEXT_SIZE = 16
START_FONT = 'arial black'

Turno = 0

num1 = JUEGODE*5
num2 = JUEGODE*3

TAMFI = 80

ANCHO = NColumnas*TAMFI
ALTURA = (NFilas+1)*TAMFI

TAMVEN = (ANCHO, ALTURA)

RAD = int(TAMFI/2 - 5 )

#Definir la paleta de colores (en RGB) con la que se desea jugar

AZUL = (0,0,255)
NEGRO = (0,0,0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)

PLAYER=0
AI=1
PLAYER_PIECE=1
AI_PIECE=2