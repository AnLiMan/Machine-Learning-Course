#------Библиотеки----------
from dataclasses import dataclass
import numpy as np
import pygame
import sys
import time
from settings import *

#----Расчёт позиции агента-----
def action(x, y, a):
    flag = NONE_FLAG  #Сброс флага
    #Инициализация дельт
    dx = 0
    dy = 0
    if (a == 0):  # N (север)
        if (y > 0):
            dy = -1
    elif (a == 1):  # NE (северо-восток)
        if ((y > 0) and (x < (SIZE - 1))):
            dy = -1
            dx = 1
    elif (a == 2):  # E (восток)
        if (x < (SIZE - 1)):
            dx = 1
    elif (a == 3):  # SE (юго-восток)
        if ((y < (SIZE - 1)) and (x < (SIZE - 1))):
            dy = 1
            dx = 1
    elif (a == 4):  # S (юг)
        if (y < (SIZE - 1)):
            dy = 1
    elif (a == 5):  # SW (юго-запад)
        if ((y < (SIZE - 1)) and (x > 0)):
            dy = 1
            dx = -1
    elif (a == 6):  # W (запад)
        if (x > 0):
            dx = -1
    elif (a == 7):  # NW (север-запад)
        if ((y > 0) and (x > 0)):
            dy = -1
            dx = -1
    if ((dx == 0) and (dy == 0)):  #Граница
        flag = BORDER_FLAG
    if ((x + dx, y + dy) in WALLS):  #Стена
        dx = 0
        dy = 0
        flag = WALL_FLAG
    if ((x + dx, y + dy) in TRAPS):  #Ловушка
        dx = X_START - x
        dy = Y_START - y
        x = X_START
        y = Y_START
        flag = TRAP_FLAG
    #Расчёт бонуса
    bonus = STEP_PENALTY  #Штаф за кол-во шагов
    if (((x + dx) == X_FINISH) and ((y + dy) == Y_FINISH)):  #Если агент оказался на финише
        bonus = bonus + FINISH_BONUS #Прибавить к счёту бонус за финиш
        flag = FINISH_FLAG
    return dx, dy, bonus, flag

#Расчёт размеров поля
def state(x, y):
    return x + y * SIZE

@dataclass
class Pos: #Класс позиции агента
    x: int
    y: int

#----Основная программа------
def main():

    np.random.seed(SEED)
    episodes_max = int(input("Episodes number?"))  #Сколько попыток (эпизодов) даётся агенту
    # Создание Q-таблицы, ставит в соответствие действиям, которые выполняются в том или ином состоянии агента,
    # число (q-value), характеризующее «полезность» этого действия для агента
    q = np.empty((ACTIONS, SIZE * SIZE), dtype=float)
    q[:] = np.NINF  #инициализация элементов таблицы Q

    #-----Настройки игрового окна-------
    pygame.init()  # Pygame initialization
    pygame.display.set_caption("Q-learning")
    canvas = pygame.display.set_mode((SIZE * CELL_SIZE + (SIZE - 1) * BORDER_SIZE, SIZE * CELL_SIZE +
            (SIZE - 1) * BORDER_SIZE + STATUS_SIZE))
    canvas.fill(WHITE)
    font = pygame.font.SysFont("comicsansms", FONT_SIZE)  #Шрифт

    #-----Подгрузка изображений-----
    icon = pygame.image.load("walk.png")
    footprint = pygame.image.load("footprints.png")
    bricks = pygame.image.load("wall.png")
    sand = pygame.image.load("sand.png")
    bomb = pygame.image.load("bomb.png")
    start = pygame.image.load("start.png")
    finish = pygame.image.load("finish.png")
    walk = pygame.image.load("walk.png")

    icon.convert()
    pygame.display.set_icon(icon)  #Иконка окна
    footprint.convert() #Создает новую копию поверхности с желаемым форматом пикселей
    bricks.convert()
    sand.convert()
    bomb.convert()
    start.convert()
    finish.convert()
    walk.convert()

    #------Рисование границ ячеек----
    i = 1
    while (i < SIZE):
        pygame.draw.line(canvas, BLACK, (i * CELL_SIZE + (i - 1) * BORDER_SIZE + 1, 0),
              (i * CELL_SIZE + (i - 1) * BORDER_SIZE + 1, SIZE * CELL_SIZE + (SIZE - 1) * BORDER_SIZE - 1), BORDER_SIZE)
        i += 1
    i = 1
    while (i < SIZE):
        pygame.draw.line(canvas, BLACK, (0, i * CELL_SIZE + (i - 1) * BORDER_SIZE + 1), (SIZE * CELL_SIZE +
              (SIZE - 1) * BORDER_SIZE - 1, i * CELL_SIZE + (i - 1) * BORDER_SIZE + 1), BORDER_SIZE)
        i += 1

    episode = 0  #Сброс счетчика эпизодов
    while (episode < episodes_max):  #Пока число эпизодов меньше заданного
        print("EPISODE: " + str(episode + 1))  # episode number output
        if (episode == (episodes_max - 1)):
            epsilon = 0.0 #Скорость воспроизведения для последнего эпизода
        else:
            #Ускоренное время, для тренировки
            epsilon = ((episodes_max - 1) - episode) / (episodes_max - 1) * (EPSILON_START - EPSILON_FINISH) + EPSILON_FINISH
        i = 0 #Pаполнение ячейки
        while (i < SIZE):
            j = 0
            while (j < SIZE):
                canvas.blit(sand, (j * (CELL_SIZE + BORDER_SIZE), i * (CELL_SIZE + BORDER_SIZE)))
                j += 1
            i += 1

        #----Отрисовка стен---------
        for wall in WALLS:
            canvas.blit(bricks, (wall[0] * (CELL_SIZE + BORDER_SIZE), wall[1] * (CELL_SIZE + BORDER_SIZE)))

        #------Отрисовка ловушек----
        for trap in TRAPS:
            canvas.blit(bomb, (trap[0] * (CELL_SIZE + BORDER_SIZE), trap[1] * (CELL_SIZE + BORDER_SIZE)))

        moving = True  #Поднятие флага, разрешающего движение
        pos = Pos(X_START, Y_START)  #Инициализация стартовой позиции агента
        canvas.blit(walk, (pos.x * (CELL_SIZE + BORDER_SIZE), pos.y * (CELL_SIZE + BORDER_SIZE)))  #Отрисовка агента
        f = NONE_FLAG

        step = 0  #Обнуление количества шагов
        scores = 0.0  #Обнуление счёта

        canvas.blit(finish, (X_FINISH * (CELL_SIZE + BORDER_SIZE), Y_FINISH * (CELL_SIZE + BORDER_SIZE)))#Отрисовка финиша
        while (moving):
            pygame.event.pump()

            #----Отрисовка передвижения и информаци о передвижении и счёте----
            canvas.blit(sand, (pos.x * (CELL_SIZE + BORDER_SIZE), pos.y * (CELL_SIZE + BORDER_SIZE)))
            canvas.blit(walk, (pos.x * (CELL_SIZE + BORDER_SIZE), pos.y * (CELL_SIZE + BORDER_SIZE)))
            canvas.fill(WHITE, pygame.Rect(0, SIZE * CELL_SIZE + SIZE * BORDER_SIZE,
                                           SIZE * CELL_SIZE + (SIZE - 1) * BORDER_SIZE, STATUS_SIZE))
            text = font.render("Эпизод:" + str(episode + 1), True, (BLUE))
            canvas.blit(text, (1, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))
            text = font.render("Шагов:" + str(step), True, (BLUE))
            canvas.blit(text, ((SIZE * CELL_SIZE + SIZE * BORDER_SIZE) // 5, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))
            text = font.render("X:" + str(pos.x) + " Y:" + str(pos.y), True, (BLUE))
            canvas.blit(text,
                        ((SIZE * CELL_SIZE + SIZE * BORDER_SIZE) * 2 // 5, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))
            text = font.render(format(scores, '.2f'), True, (RED))
            canvas.blit(text,
                        ((SIZE * CELL_SIZE + SIZE * BORDER_SIZE) * 3 // 5, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))

            if ((episode == (episodes_max - 1)) and ((f == BORDER_FLAG) or (f == WALL_FLAG))):
                text = font.render("LOCK", True, (RED))
                canvas.blit(text, ((SIZE * CELL_SIZE + SIZE * BORDER_SIZE) * 4 // 5, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))
                pygame.display.flip()  # display update
                print("LOCK")  # total scores
                break

            if (f == FINISH_FLAG):  #Агент подошёл к финишу
                i = 0
                while (i < SIZE * SIZE):
                    zero = True
                    #Поиск первого исследованного действия
                    j = 0
                    while (j < ACTIONS):
                        if (np.isneginf(q[j, i]) == False):
                            zero = False  #исследованное действие найдено
                            break
                        j += 1  #Следующее действие
                    if (zero == False):  #исследованное действие существует
                        max = q[j, i]  #текущее максимальное значение q
                        k = j  #текущее оптимальное действие
                        j += 1  #следующее действие
                        while (j < ACTIONS):
                            # check for not nan
                            if (np.isneginf(q[j, i]) == False):
                                # проверить на максимум
                                if (q[j, i] > max):
                                    max = q[j, i]  # новый максимум q-value
                                    k = j  #новое оптимальное действие
                            j += 1  #следующее действие
                        print(DIRS[k], end='')
                    else:
                        print("-", end='')
                    i += 1
                    if ((i % SIZE) == 0):
                        print("")

                text = font.render("FINISH", True, (BLUE))
                canvas.blit(text, ((SIZE * CELL_SIZE + SIZE * BORDER_SIZE) * 4 // 5, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))
                pygame.display.flip()  # display update
                print("Счёт = " + format(scores, '.2f'))  #Текущий счёт
                time.sleep(EPISODE_PAUSE)
                break

            if (f == WALL_FLAG): #Столкновение со стеной
                text = font.render("Стена", True, (RED))
                canvas.blit(text, (
                (SIZE * CELL_SIZE + SIZE * BORDER_SIZE) * 4 // 5, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))

            elif (f == TRAP_FLAG): #Столкновение с ловушкой
                text = font.render("Бомба", True, (RED))
                canvas.blit(text, ((SIZE * CELL_SIZE + SIZE * BORDER_SIZE) * 4 // 5, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))

            elif (f == BORDER_FLAG): #Столкновение с границей
                text = font.render("Граница карты", True, (RED))
                canvas.blit(text, ((SIZE * CELL_SIZE + SIZE * BORDER_SIZE) * 4 // 5, SIZE * CELL_SIZE + SIZE * BORDER_SIZE + 5))
            pygame.display.flip()  # display update
            pygame.event.pump()

            # задержка шага
            if (episode == (episodes_max - 1)):
                time.sleep(STEP_PAUSE)  # testing pause
            else:
                time.sleep(LRN_PAUSE)  # learning pause

            #Cлучайный выбор стратегии
            if (np.random.rand() < epsilon):
                a = np.random.randint(0, ACTIONS) #Исследование
            else:
                zero = True # exploit
                # find first not nan
                j = 0
                while (j < ACTIONS):
                    if (np.isneginf(q[j, state(pos.x, pos.y)]) == False):
                        zero = False  # explored action found
                        break
                    j += 1  #следующее действие
                if (zero == False):  #Исследованное действие существует
                    max = q[j, state(pos.x, pos.y)]  # текущий максимум q-value
                    k = j  #текущее оптимальное действие
                    j += 1  #следующее действие
                    while (j < ACTIONS):
                        # check for not nan
                        if (np.isneginf(q[j, state(pos.x, pos.y)]) == False):
                            if (q[j, state(pos.x, pos.y)] > max):
                                max = q[j, state(pos.x, pos.y)]  # новый максимум q-value
                                k = j  #новое оптимальное действие
                        j += 1  # следующее действие
                    # exploit
                    a = k  # Выбор оптимального действия
                else:  # no action explored
                    # Исследование
                    a = np.random.randint(0, ACTIONS)  # random action select

            dx, dy, r, f = action(pos.x, pos.y, a)
            if ((dx != 0) or (dy != 0)):  #Агент движется
                canvas.blit(sand,
                            (pos.x * (CELL_SIZE + BORDER_SIZE), pos.y * (CELL_SIZE + BORDER_SIZE)))  # clean source cell
                canvas.blit(footprint,
                            (pos.x * (CELL_SIZE + BORDER_SIZE), pos.y * (CELL_SIZE + BORDER_SIZE)))  # footprint drawing

            #Обновление Q-таблицы
            if (episode != (episodes_max - 1)):
                if (np.isneginf(q[a, state(pos.x, pos.y)]) == False):
                    if (np.isneginf(np.max(q[:, state(pos.x + dx, pos.y + dy)])) == False):
                        q[a, state(pos.x, pos.y)] = q[a, state(pos.x, pos.y)] + ALPHA * (r + GAMMA * np.max(q[:, state(pos.x + dx, pos.y + dy)]) - q[a, state(pos.x, pos.y)])
                    else:
                        q[a, state(pos.x, pos.y)] = q[a, state(pos.x, pos.y)] + ALPHA * (r - q[a, state(pos.x, pos.y)])
                else:
                    if (np.isneginf(np.max(q[:, state(pos.x + dx, pos.y + dy)])) == False):
                        q[a, state(pos.x, pos.y)] = ALPHA * (r + GAMMA * np.max(q[:, state(pos.x + dx, pos.y + dy)]))
                    else:
                        q[a, state(pos.x, pos.y)] = ALPHA * r
            scores = scores + r  #Обновление счёта

            pos.x = pos.x + dx #Передвижение агента на dx
            pos.y = pos.y + dy #Передвижение агента на dy
            step += 1  #Шаг++
            pygame.event.pump()
            for event in pygame.event.get():  # event checking
                if event.type == pygame.QUIT:
                    sys.exit(0)  # exit from the program
        episode += 1  #Эпизод++

    # ----Ожидание закрытия окна---
    while (True):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)  #Выход из программы

if (__name__ == "__main__"):
    main()