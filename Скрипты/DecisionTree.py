#Библиотеки
from __future__ import division, print_function
import warnings
warnings.filterwarnings('ignore')
import numpy as np
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier

#Функция, которая будет возвращать решётку для дальнейшей визуализации
def get_grid (data):
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    return np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))

#Первый класс
np.speed = 7
train_data = np.random.normal(size=(100,2)) #Данные
train_labels = np.zeros(100) # Метка для ранее сгенерированных данных (100 нулей)
print("Первый класс данных:")
print(train_data)
print("Его метка:")
print(train_labels)

#Добавляем второй класс
#Новые данные, про np.r_ можно прочитать здесь https://numpy.org/doc/stable/reference/generated/numpy.r_.html
train_data = np.r_[train_data, np.random.normal(size=(100, 2), loc=2)]
train_labels = np.r_[train_labels, np.ones(100)] # Метка для ранее сгенерированных данных (100 единиц)
print("\nПервый и второй классы данных:")
print(train_data)
print("Их метки:")
print(train_labels)

#Классификация
clf_tree = DecisionTreeClassifier(criterion = 'entropy', max_depth = 3, random_state = 17)

#Обучаем дерево
clf_tree.fit(train_data, train_labels)

#----------Отрисовка графиков----------
plt.figure(figsize=(10, 6))
plt.title('Классификация методом решающих деревьев')
plt.xlabel('x')
plt.ylabel('y')
xx, yy = get_grid(train_data)
predicted = clf_tree.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
plt.pcolormesh(xx, yy, predicted, cmap='autumn')
plt.scatter(train_data[:, 0], train_data[:, 1], c=train_labels, s=100, cmap='autumn', edgecolors='black', linewidths=1.5)
plt.show()
