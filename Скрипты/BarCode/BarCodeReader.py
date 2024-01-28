"""""
Установка библиотек
pip install python-barcode
pip install pyzbar
pip install opencv-python
pip install pyserial
pip install numpy
pip install colorama
pip install art
pip install opencv-python

Материал для чтения
1.Распознавание штрих-кодов https://www.geeksforgeeks.org/how-to-make-a-barcode-reader-in-python/ 
2. Генерация штрих-кода https://www.geeksforgeeks.org/how-to-generate-barcode-in-python/ 
3. Работа с Ардуино https://pyserial.readthedocs.io/en/latest/shortintro.html
"""""
# -----Библиотеки-----
from barcode import EAN13 #Есть и другие варианты: EAN-8, EAN-13, EAN-14, UPC-A, JAN, ISBN-10, ISBN-13
from barcode.writer import ImageWriter #Для генерации Штрих-кода
from pyzbar.pyzbar import decode #Для распознавания кода на изображении
import cv2 as cv #Библиотека OpenCV
import serial #Библиотка для работы с последовательным портом
import time #Библиотка для работы со временем
import colorama as cl #Для красивого текста консоли
import art #Тоже для красивого текста

#----Постоянные----
ArduinoControl = False #Вывод сигналов на последовательный порт
ArduinoPort = 'COM6' #Порт с подключенной дуиной
ArduinoSpeed = 19200 #Скорость передачи данных в бодах

CheckCode = "NewCode.png" #Код для проверки без камеры
acsees_list = [1234567891231] #Список допущенных
CamWork = False # Включение поиска кода через камеру

tickTimer = 0.5 # Таймер сна, для более медленного выполнения кода, значения в секундах

#Генерация штрих-кода
def BarCodeGenerate(number = "0000000000000",name = "Default"):
    my_code = EAN13(number, writer=ImageWriter())
    my_code.save(name)
    print(cl.Fore.BLACK + "Для номера " + str(number) + " сохранён код под названием: "+ str(name))
    acsees_list.append(number)
    print(cl.Fore.BLACK + "Список допущенных: " +str (acsees_list))

#Чтение штрих-кода
def BarcodeReader():
    #Если включено распознавание при помощи камеры
    if CamWork:
        cap = cv.VideoCapture(0)  # Подключаемся (захватываем) к камере. 0 — это индекс камеры, если их несколько то будет 0 или 1 и т.д.
        ret, img = cap.read()  # Читаем с устройства кадр, метод возвращает флаг ret (True , False) и img — саму картинку (массив numpy)
        #cv.imshow("Camera view", img)
        cv.imwrite("Screen.jpg", img)
        barcode = cv.imread("Screen.jpg") #Читаем изображение
        detectedBarcodes = decode(barcode)  # Распознаём штрих-код

    #Иначе читаем заготовленный заранее
    elif CamWork == False:
        barcode = cv.imread(CheckCode)  # Читаем изображение
        detectedBarcodes = decode(barcode)  # Распознаём штрих-код

    # Если код не распознан
    if not detectedBarcodes:
        print(cl.Fore.RED + "Штрих-код не распознан, он либо пустой, либо повреждён!")
        if ArduinoControl:
            SendData(0) #Отправим на Ардуино сигнал об этом
    else:
        # Просмотр всех обнаруженных штрих-кодов на изображении
        for barcode in detectedBarcodes:
            # Определяем положение штрих-кода на изображении
            (x, y, w, h) = barcode.rect

            # Пометим прямоугольником распознанную область
            if CamWork:
                cv.rectangle(img, (x - 10, y - 10),
                         (x + w + 10, y + h + 10),
                         (255, 0, 0), 2)

            # Если данные не пустые
            if barcode.data != "":
                # Выведем код и его тип
                data = int(barcode.data)
                print(cl.Fore.BLACK + "Данные на штрих-коде: : " + str(data))
                print(cl.Fore.BLACK + "Тип штрих-кода : " + str(barcode.type))

                if ArduinoControl:
                    SendData(1)  # Отправим на Ардуино сигнал об этом
                for i in range(0, len(acsees_list)):
                    if data == acsees_list[i]:
                        if ArduinoControl:
                            SendData(2) # Отправим на Ардуино сигнал об этом
                        print(cl.Fore.GREEN + "Доступ разрешён!")
                    else:
                        print(cl.Fore.RED + "Доступ запрещён!")

def SendData(x):
    ser.write(bytes(x, 'utf-8'))
    print(cl.Fore.BLACK + "Bytes: " + str(bytes(x, 'utf-8')))
    time.sleep(0.05)
    data = ser.readline()
    print(cl.Fore.BLACK + "Data: " + str(data))

if __name__ == "__main__":
    if ArduinoControl:
        ser = serial.Serial(ArduinoPort, ArduinoSpeed, timeout=0.1)

    art.tprint("Barcode Reader")
    print(cl.Fore.MAGENTA + "Новые данные вводим? Y/N")
    choise = input()
    if choise.lower() == "y":
        print(cl.Fore.BLACK  + "Ок, введите 13 цифр")
        num = input()
        print(cl.Fore.BLACK + "Введите имя")
        name = input()
        BarCodeGenerate(num, name)
    else:
        print(cl.Fore.BLACK  + "Ок, тогда пошли дальше")

    while True:
        BarcodeReader()
        time.sleep(tickTimer)