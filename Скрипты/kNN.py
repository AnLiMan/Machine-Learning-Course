#------------Библиотеки---------------
import random
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

#----------Параметры системы-------------
classes = 3 #Количество классов
numbers = 40 #Количество точек
k = 3 #Значение k для алгоритма классификации (количество соседей)
Range = 5 #Для определения случайного центра на двумерном пространстве от 0 до Range

#---------------Списки данных--------------
data = [] #Список тренировочных даннных
trainData = []  #Список для обучающей выборки
testData = []  #Тестовая выборка
testLabels = [] #Список классов

#----------------Функции--------------------
#Генератор тренировочных данных
def generateData (numberOfClassEl, numberOfClasses):
    for classNum in range(numberOfClasses):
        centerX, centerY = random.random()*Range, random.random()*Range #Выбор случайного центра на двумерном пространстве от 0 до Range
        for rowNum in range(numberOfClassEl): #Генерация n-классов данных
            data.append([[random.gauss(centerX,0.5), random.gauss(centerY,0.5)], classNum])
    return data

#Получение обучающей и тестовой выборки
def splitTrainTest (data, testPercent):
    for row in data:
        if random.random() < testPercent:
            testData.append(row) #data*testPercent
        else:
            trainData.append(row)
    return trainData, testData #data*(1-testPercent)

#Классификация по методу ближайших соседей
def classifyKNN (trainData, testData, k, numberOfClasses):
    #Вычисление евклидова расстояния между 2-мя точками
    def dist (a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    for testPoint in testData:
        # Расчёт расстояния между точкой из testData и всеми точками из trainData
        testDist = [ [dist(testPoint, trainData[i][0]), trainData[i][1]] for i in range(len(trainData))]
        stat = [0 for i in range(numberOfClasses)] #Сколько точек из каждого класса среди ближайших k
        for d in sorted(testDist)[0:k]:
            stat[d[1]] += 1
        # Назначение класса с наибольшим количеством вхождений среди k ближайших соседей
        testLabels.append( sorted(zip(stat, range(numberOfClasses)), reverse=True)[0][1] ) #Assign a class with the most number of occurences among K nearest neighbours
    return testLabels

#Визуализация результатов
def showDataOnMesh (nClasses, nItemsInClass, k):
    #Генерация сетки узлов, охватывающая все тренировочные данные
    def generateTestMesh (trainData):
        x_min = min( [trainData[i][0][0] for i in range(len(trainData))] ) - 1.0
        x_max = max( [trainData[i][0][0] for i in range(len(trainData))] ) + 1.0
        y_min = min( [trainData[i][0][1] for i in range(len(trainData))] ) - 1.0
        y_max = max( [trainData[i][0][1] for i in range(len(trainData))] ) + 1.0
        h = 0.05
        testX, testY = np.meshgrid(np.arange(x_min, x_max, h),
                                   np.arange(y_min, y_max, h))
        return [testX, testY]

    trainData = generateData (nItemsInClass, nClasses)
    testMesh = generateTestMesh (trainData)
    testMeshLabels = classifyKNN (trainData, zip(testMesh[0].ravel(), testMesh[1].ravel()), k, nClasses)
    classColormap = ListedColormap(['#0000FF', '#00FF00', '#FF0000'])
    testColormap = ListedColormap(['#b9b8ff', '#a5ffa3', '#ffb1bb'])

    #Строим картину распределения
    plt.figure(figsize=(10, 6))  # Задание размера окна с графиками
    plt.pcolormesh(testMesh[0],
                  testMesh[1],
                  np.asarray(testMeshLabels).reshape(testMesh[0].shape),
                  cmap=testColormap)
    plt.scatter([trainData[i][0][0] for i in range(len(trainData))],
               [trainData[i][0][1] for i in range(len(trainData))],
               c=[trainData[i][1] for i in range(len(trainData))],
               cmap=classColormap)
    plt.title("Классификация методом k-ближайших соседей")  # Название графика
    plt.xlabel("X")  # Название оси Х
    plt.ylabel('Y')  # Название оси Y
    plt.show()

#Основной код
if __name__ == "__main__":
    showDataOnMesh(classes, numbers, k)