from PIL import Image as img
import numpy as np
import cv2 as cv

#Изображение в массив
def Image2Array (name = 'Test.jpg'):
    im_array = np.array(img.open(name).convert('L')) # Откроем изображение и переведём его в полутоновое
    print("Высота изображения: ", im_array.shape[0])
    print("Ширина изображения: ", im_array.shape[1])
    print("\nМассив значений пикселей массива", im_array)

# Кроп изображения
def CropImage (size = (100, 300, 500, 700), name = "Test.jpg"):
    im = img.open(name)
    im_copy = im.copy()  # Сделаем копию исходного изображения
    cropped_img = im_copy.crop(size)
    cropped_img.show()
    cropped_img.save("Cropped_img.jpg") #Сохраним изображение

#Задание 1 на PIL, забинаривание изображений
def binaryImg (im_name = 'Test.jpg', threshold = 127):
    #Конвертируем изображение в полутоновое
    im = img.open(im_name)
    im_2 = im.convert('L')
    width, height = im_2.size

    #Проходим по всем пикселям
    for x in range(width):
        for y in range(height):

            #Если интенсивность ниже порога тогда цвет - чёрный (0)
            if im_2.getpixel((x, y)) < threshold:
                im_2.putpixel((x, y), 0)
            #Если выше цвет белый (1)
            else:
                im_2.putpixel((x, y), 255)
    im_2.show()
    im_2.save("Binary-Cat.jpg") #Сохраним изображение

# Примеры работы с OpenCV
def cv_examples(name):
    img = cv.imread(name) #Откроем изображение
    #cv.imshow("Image Teast in OpenCV",  img) #Показ изображения

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV) #Преобразуем в HSV-пространство
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Преобразуем изображение в полутоновое
    cv.imwrite("Gray-Cat.jpg", gray)  # Сохраним изображение
    ret, threshold_image = cv.threshold(gray, 127, 255, 0) # Забинарим
    cv.imshow("HSV-Cat", hsv) #Покажем изображение
    cv.imshow("Gray-Cat", gray)  # Покажем изображение
    cv.imshow("Binary-Cat", threshold_image) #Покажем изображение
    cv.imwrite("Binary-Cat-2.jpg", threshold_image) #Сохраним изображение
    cv.imwrite("HSV-Cat.jpg", hsv) #Сохраним изображение

    cv.waitKey(0) #Подождём действий от пользователя
    cv.destroyAllWindows() #Закроем все окна

#Задание 1 на OpenCV, сложение изображений
def add_imgages (name_1 = "Gray-Cat.jpg", name_2 = "HSV-Cat.jpg"):
    img_1 = cv.imread(name_1)
    img_2 = cv.imread(name_2)
    add_img = cv.add(img_1, img_2)
    cv.imwrite("Add-Img.jpg", add_img)
    cv.imshow("Add Image", add_img)
    cv.waitKey(0) #Подождём действий от пользователя
    cv.destroyAllWindows() #Закроем все окна

if __name__ == "__main__":
    im = img.open("Test.jpg")  # Открываем изображение
    im.show()  # Выводим изображение на экран
    Image2Array()
    CropImage()
    binaryImg()
    cv_examples("Test.jpg")
    add_imgages()