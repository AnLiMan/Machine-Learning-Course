#------Multi-class AdaBoosted Decision Trees-----
# Дополнительные комментарии к коду приведены здесь:
# https://scikit-learn.org/stable/auto_examples/ensemble/plot_adaboost_multiclass.html#sphx-glr-auto-examples-ensemble-plot-adaboost-multiclass-py

#-----Библиотеки----
from sklearn.datasets import make_gaussian_quantiles
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pandas as pd

#Постоянные
n_estimators = 300 # Максимальное количество оценок, при которых повышение прекращается. В случае идеального соответствия процедура обучения прекращается досрочно.
g_q_samples = 2000 #Количество образцов для генерации Гауссова квантиля (подробнее https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_gaussian_quantiles.html#sklearn.datasets.make_gaussian_quantiles)
g_q_features = 10 # Количество признаков
g_q_classes = 3 # Количество классов

train_split = 0.7 # Процент данных для тренировки

#Вычисление отклонения истинного значения от предсказанного
def misclassification_error(y_true, y_pred):
    return 1 - accuracy_score(y_true, y_pred)

#Вычисление ошибок и построение графиков
def ErrorCalculations():
    # Вычисление ошибок
    boosting_errors = pd.DataFrame(
        {
            "Число деревьев": range(1, n_estimators + 1),
            "AdaBoost": [
                misclassification_error(y_test, y_pred)
                for y_pred in adaboost_clf.staged_predict(X_test)
            ],
        }
    ).set_index("Число деревьев")
    ax = boosting_errors.plot()
    ax.set_ylabel("Ошибка классификации на тестовом наборе")
    ax.set_title("Сходимость алгоритма AdaBoost")
    plt.grid()
    plt.plot(
        [boosting_errors.index.min(), boosting_errors.index.max()],
        [weak_learners_misclassification_error, weak_learners_misclassification_error],
        color="tab:orange",
        linestyle="dashed",
    )
    plt.plot(
        [boosting_errors.index.min(), boosting_errors.index.max()],
        [
            dummy_classifiers_misclassification_error,
            dummy_classifiers_misclassification_error,
        ],
        color="c",
        linestyle="dotted",
    )
    plt.legend(["AdaBoost", "DecisionTree", "DummyClassifier"], loc=1)
    plt.show()

    # Графики показывают ошибку классификации в тестовом наборе после каждой итерации бустинга. dataFrame - создание структурированных данных
    weak_learners_info = pd.DataFrame(
        {
            "Число деревьев": range(1, n_estimators + 1),
            "Ошибка": adaboost_clf.estimator_errors_,
            "Веса": adaboost_clf.estimator_weights_,
        }
    ).set_index("Число деревьев")

    axs = weak_learners_info.plot(subplots=True, layout=(1, 2), figsize=(10, 4), legend=False, color="tab:blue")
    axs[0, 0].set_ylabel("Ошибка при обучении")
    axs[0, 0].set_title("Ошибка Weak learner на тренировочном наборе")
    axs[0, 1].set_ylabel("Веса")
    axs[0, 1].set_title("Веса Weak learner")
    fig = axs[0, 0].get_figure()
    fig.suptitle("Ошибки Weak learner и веса для AdaBoost")
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Создание датасета (набора данных)
    X, y = make_gaussian_quantiles(n_samples=g_q_samples, n_features=g_q_features, n_classes=g_q_classes)
    # Разделение на тренировочную и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_split)

    # Decision Tree (решающие деревья) https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn-tree-decisiontreeclassifier
    weak_learner = DecisionTreeClassifier(max_leaf_nodes=8)
    # AdaBoost https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html#sklearn.ensemble.AdaBoostClassifier
    adaboost_clf = AdaBoostClassifier(estimator=weak_learner, n_estimators=n_estimators, algorithm="SAMME").fit(X_train, y_train)
    # Глупый классификатор https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html#sklearn.dummy.DummyClassifier
    #DummyClassifier делает прогнозы, игнорируя входные объекты. Этот классификатор служит простой базой для
    #сравнения с другими, более сложными классификаторами.
    dummy_clf = DummyClassifier()

    # ---Анализ----
    weak_learners_misclassification_error = misclassification_error(y_test, weak_learner.fit(X_train, y_train).predict(X_test))
    dummy_classifiers_misclassification_error = misclassification_error(y_test, dummy_clf.fit(X_train, y_train).predict(X_test))

    print("Ошибка предсказания Decision Tree: "f"{weak_learners_misclassification_error:.3f}")
    print("Ошибка предсказания Dummy Classifier: "f"{dummy_classifiers_misclassification_error:.3f}")

    ErrorCalculations()