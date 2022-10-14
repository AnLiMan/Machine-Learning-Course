#---------Библиотеки---------
from scipy.stats import sem
from numpy import mean
from numpy import std
from sklearn.datasets import make_classification
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot

#----------Настройки----------
n_splits = 10 #Количество складок (разбиений)
n_repeats = 15 #Количество повторов (максимальное)
random_state = 1 #Управляет случайностью каждого повторного экземпляра при перекрестной проверке

#Оценка модели с заданным количеством повторов
def evaluate_model(X, y, repeats):
    # Повторяется K-Fold n раз с различной рандомизацией в каждом повторении
    cv = RepeatedKFold(n_splits = n_splits, n_repeats = repeats, random_state = random_state)
    model = LogisticRegression() # Разделение данных на 2 класса, методом логической регрессии
    scores = cross_val_score(model, X, y, scoring = 'accuracy', cv = cv, n_jobs = -1) # Оценка модели
    return scores

#Сгенерированные сэмплы - X, wелочисленные метки для принадлежности к классу каждого образца - y
X, y = make_classification(n_samples = 1000, n_features = 20, n_informative = 15, n_redundant = 5, random_state = 1) #Создание датасета
repeats = range(1, n_repeats + 1) # конфигурация для тестирования
results = list()

for r in repeats:
    scores = evaluate_model(X, y, r) #Оценка, при заданном количестве повторов
    #Подведение итогов
    print('при количестве повторов = %d средняя точность = %.4f, а стандартное отклонение = %.3f' % (r, mean(scores)*100, sem(scores)*100))
    results.append(scores)  # store

#Построение графиков
pyplot.boxplot(results, labels=[str(r) for r in repeats], showmeans = True)
pyplot.show()

"""""""""
Оранжевая линия указывает на медианное значение распределения, а зеленый треугольник представляет 
собой среднее арифметическое.Если эти символы (значения) совпадают, это говорит о разумном симметричном
распределении и о том, что среднее значение может хорошо отражать центральную тенденцию. Это может 
предоставить дополнительную эвристику для выбора подходящего количества повторов для тестовой выборки.
"""""""""
