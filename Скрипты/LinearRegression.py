#Библиотеки
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

#Загрузка датасета диабета
diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y = True)
# Используем из него только 1 признак
diabetes_X = diabetes_X[:, np.newaxis, 2]
# Разделяем данные на тестовые и тренировочные
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]
# Разделим метки на тестовый и тренировочный набор
diabetes_y_train = diabetes_y[:-20]
diabetes_y_test = diabetes_y[-20:]

# Создадим объект линейной регрессии
regr = linear_model.LinearRegression()
# Тестовая модель, построенная на тренировочном наборе
regr.fit(diabetes_X_train, diabetes_y_train)
# Сделаем предсказания, используя тестовую модель
diabetes_y_pred = regr.predict(diabetes_X_test)

# Коэффициенты
print("Коэффициент: \n", regr.coef_)
# Среднеквадратическая ошибка
print("Среднеквадратическая ошибка: %.2f" % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# Коэффициент детерминации: 1 – идеальный прогноз
print("Коэффициент детерминации: %.2f" % r2_score(diabetes_y_test, diabetes_y_pred))

# Строим график
plt.figure(figsize = (10,6)) #Задание размера окна с графиками
plt.scatter(diabetes_X_test, diabetes_y_test, color="black") #Отображение точек датасета. Сначала X, потом Y, после цвет
plt.plot(diabetes_X_test, diabetes_y_pred, color="blue", linewidth=3) #Построение графика. Сначала X, потом Y, после цвет
plt.grid() #Сетка
plt.title("График линейной регрессии") #Название графика
plt.xlabel("X") #Название оси Х
plt.ylabel('Y') #Название оси Y
plt.show() #Показать график