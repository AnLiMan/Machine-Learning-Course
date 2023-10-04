import math

#Задание 1
def Task_1():
	print("---Первое задание---")
	print("Hello World!")
	print("\n Hello World!" * 15)
	print(len("Hello World!"))

#Задание 2
def Task_2():
	print("---Второе задание---")
	list1 = ["12", "Слово", 2, 1.2, "1 + 2"]
	print("Исходный список: " + str(list1))
	print("Введите данные...")
	inputData = input()
	list1.append(inputData)
	print("Изменённый список: " + str(list1))
	print("Элементы с 1-го по 3-й: " + str(list1[1:4:]))

#Задание 3
def Task_3 ():
	print("---Третье задание---")
	list2 = []
	print("Введите 5 элементов")
	for i in range(5):
		inputData = input()
		list2.append(inputData)
	print(list2)
	list2.sort()
	print(list2)
	print("Введите индекс элемента для удаления")
	inputIndex = int(input())
	try:
		list2.pop(inputIndex)
		print(list2)
	except:
		print("Больше нечего удалять!")

#Задание 4
def Task_4():
	print("---Четвёртое задание---")
	for i in range(1,151):
		print("Итерация №" + str(i) + "\nHello World!")
	print("Привет или пока? Введите либо 1, либо 2")

	inputCommand = int(input())
	if inputCommand == 1:
		for i in range(1,151):
			print("Итерация №" + str(i) + "\nHello World!")
	elif inputCommand == 2:
		for i in range(1, 151):
			print("Итерация №" + str(i) + "\By World!")
	else:
		print("Синтаксическая ошибка")

#Задание 5
def Task_5(label = "default", times = 1):
	print("---Пятое задание---")
	for i in range(times):
		print(str(i + 1) + " Заданная надпись: " + str(label))

#Задание 6
def Task_6 ():
	print("---Шестое задание---")
	try:
		x = int(input())
		print("Вы ввели: " + str(x))
	except ValueError:
		print("Вы ввели не число")
	try:
		print("1 / x = " + str(1 / x))
	except ZeroDivisionError:
		print("Деление 1 на 0!, я такое считать не буду")

#Задание 7
def Task_7 ():
	print("---Седьмое задание---")
	f = open('D:/Programs/PyCharm Community Edition 2022.2.2/Projects2/text.txt', 'w', encoding="utf-8")
	f.write("Расчёт синуса от 0 до 180 градусов")
	for i in range(0, 180):
		f.write("\n При x = " + str(i) + " ,sin = ")
		f.write(str(round((math.sin(i/57.2958)), 3)))
	print("Расчёт синуса закончен")
	f.close()

	#Основной код
if __name__ == "__main__":
	print("---Демонстрация---")
	#Task_1()
	#Task_2()
	#Task_3()
	#Task_4()
	#Task_5("hhhh", 10)
	#Task_6()
	#Task_7()

