from PIL import Image as img
import numpy as np

def Image2Array (name = 'Test.jpg'):
    im_array = np.array(img.open(name).convert('L')) # Откроем изображение и переведём его в полутоновое
    print("Высота изображения: ", im_array.shape[0])
    print("Ширина изображения: ", im_array.shape[1])
    print("\nМассив значений пикселей массива", im_array)

if __name__ == "__main__":
    im = img.open("Test.jpg")  # Открываем изображение
    im_copy = im.copy()  # Сделаем копию исходного изображения
    im_copy.show()  # Выводим изображение на экран
    Image2Array()
