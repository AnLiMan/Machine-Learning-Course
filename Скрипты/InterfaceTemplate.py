#Библиотеки
from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtGui import QPixmap
import sys

#Постоянные
windowName = "Main.ui"
picture = "Test.jpg"

#---Функции--

#Вывод в textBrowser
def Print():
    main_window.textBrowser.append("\n")
    main_window.textBrowser.append(f"Фамилия - {main_window.LastNameValue.text()}")
    main_window.textBrowser.append(f"Имя - {main_window.NameValue.text()}")
    main_window.textBrowser.append(f"Отчество - {main_window.MiddleNameValue.text()}")

#Очистка содержимого всех QLineEdit
def Clear():
    main_window.LastNameValue.clear()
    main_window.NameValue.clear()
    main_window.MiddleNameValue.clear()

#Очистка содержимого textBrowser
def Clear_2():
    main_window.textBrowser.clear()

#Закрыть все окна
def CloseAllWindows():
    sys.exit(app.exit())

#Отработка Check Box
def Check():
    if main_window.checkGraph.isChecked() == True:
        label = main_window.GraphLabel
        pixmap = QPixmap(picture)
        label.setPixmap(pixmap)
    else:
        main_window.GraphLabel.setText("Здесь будет изображение")

if __name__ == "__main__":
    app = QtWidgets.QApplication([]) #Запускаем приложение
    # Загружаем ранее созданный интерфейс,  здесь и далее  мы будем обращаться к
    #объекту main_window как к нашему основному интерфейсу
    main_window = uic.loadUi(windowName)
    main_window.setWindowTitle("Пример программы") #Задаём название окна
    main_window.show() #Показываем окно интерфейса

    # Отработка нажатия кнопок
    main_window.PrintButt.clicked.connect(Print) # Вывести содержимое в консоль
    main_window.ClearButt.clicked.connect(Clear) # Очистить содержимое
    main_window.ClearButt_2.clicked.connect(Clear_2)  # Очистить содержимое
    main_window.CloseWindow.triggered.connect(CloseAllWindows) #Закрыть окно
    main_window.checkGraph.clicked.connect(Check) # Нажали на Check Box

    sys.exit(app.exec()) # Крутим приложение по кругу