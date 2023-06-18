# Параметры обучения
ALPHA = 1.0 # learning rate
GAMMA = 0.95 # discount

SIZE = 15  #Размер поля

#Координаты бомб
TRAPS = {(2,2), (3,6), (12, 13)}
#Координаты стен
WALLS = {(2,4), (3,4), (4,4), (5,4), (6,4), (10,8), (9,8), (10,6), (9,6), (8,6), (7,6), (6,6), (5,6), (1,7), (1,8), (1,9)}

# epsilon
EPSILON_START = 1.0
EPSILON_FINISH = 0.01

#Старотовая позиция
X_START = 0
Y_START = 0
#Конечная позиция
X_FINISH = SIZE - 1
Y_FINISH = SIZE - 1

ACTIONS = 8 # Количество возможных ходов
DIRS = ["W", "E", "D", "C", "X", "Z", "A", "Q"]

STEP_PENALTY = -1.0 #Штраф за шаг
FINISH_BONUS = 100.0 #Величина награды

SEED = 12345678

#Настройки для pygame
CELL_SIZE = 32
BORDER_SIZE = 4
FONT_SIZE = 16
STATUS_SIZE = FONT_SIZE*2+5
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)

STEP_PAUSE = 0.5
LRN_PAUSE = 0.001
EPISODE_PAUSE = 0.1

NONE_FLAG = 0
WALL_FLAG = 1
TRAP_FLAG = 2
BORDER_FLAG = 3
FINISH_FLAG = 4