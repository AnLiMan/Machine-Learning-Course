#Библиотеки
import numpy as np
import matplotlib.pyplot as plt

#Настройки
degree_list = [1, 2, 3, 5, 7, 10] # список степеней p полиномов, который мы протестируем

#Переменные
data = {} #Исходные данные
w_list = [] # Список точек для построения регрессии n-й степени
err = [] # Список среднеквадратичных отклонений

#Функция генерации данных
def generate_wave_set(n_support=1000, n_train=25, std=0.3):
    # выберем некоторое количество точек из промежутка от 0 до 2*pi
    data['support'] = np.linspace(0, 2*np.pi, num=n_support)
    # для каждой посчитаем значение sin(x) + 1
    # это будет ground truth
    data['values'] = np.sin(data['support']) + 1
    # из support посемплируем некоторое количество точек с возвратом, это будут признаки
    data['x_train'] = np.sort(np.random.choice(data['support'], size=n_train, replace=True))
    # опять посчитаем sin(x) + 1 и добавим шум, получим целевую переменную
    data['y_train'] = np.sin(data['x_train']) + 1 + np.random.normal(0, std, size=data['x_train'].shape[0])
    return data

#Функция отрисовки оригинальных данных
def drawing_original_data():
    # отрисовка графика
    plt.figure(figsize=(10, 6))
    plt.grid()
    plt.plot(data['support'], data['values'], 'b--', alpha=0.5, label='Реальные данные')
    plt.scatter(data['x_train'], data['y_train'], 20, 'g', 'o', alpha=0.8, label='Зашумлённые данные')
    plt.xlim(data['x_train'].min(), data['x_train'].max())
    plt.ylim(data['y_train'].min(), data['y_train'].max())
    plt.legend(loc='upper right', prop={'size': 10})
    plt.title('Реальные и зашумлённые данные')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

#Функция расчёта полиномов и отрисовки данных
def polyregression():
    cmap = plt.get_cmap('jet')
    colors = [cmap(i) for i in np.linspace(0, 1, len(degree_list))]
    # Отрисовка графика
    plt.figure(figsize=(10, 6))
    plt.grid()
    plt.plot(data['support'], data['values'], 'b--', alpha=0.5, label='Реальные данные')
    plt.scatter(data['x_train'], data['y_train'], 20, 'g', 'o', alpha=0.8, label='Зашумлённые данные')

    for ix, degree in enumerate(degree_list):
        # список с предрасчитанными степенями признака
        dlist = [np.ones(data['x_train'].shape[0])] + list(map(lambda n: data['x_train']**n, range(1, degree + 1)))
        X = np.array(dlist).T
        w = np.dot(np.dot(np.linalg.inv(np.dot(X.T, X)), X.T), data['y_train']) # шаг обучения - здесь мы ищем лучшую гипотезу h
        w_list.append((degree, w))
        y_hat = np.dot(w, X.T) # шаг применения: посчитаем прогноз
        err.append(np.mean((data['y_train'] - y_hat)**2))
        plt.plot(data['x_train'], y_hat, color=colors[ix], label='Спепень полинома: %i' % degree)

    #Дотрисовка графика
    plt.xlim(data['x_train'].min(), data['x_train'].max())
    plt.ylim(data['y_train'].min(), data['y_train'].max())
    plt.legend(loc='upper right', prop={'size': 10})
    plt.title('Полиноминальная регрессия')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

if __name__ == "__main__":
    data = generate_wave_set(1000, 50)
    drawing_original_data()
    polyregression()