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
	for i in range(times):
		print(str(i + 1) + " Заданная надпись: " + str(label))

#Основной код
if __name__ == "__main__":
	print("---Демонстрация---")
	#Task_1()
	#Task_2()
	#Task_3()
	#Task_4()
	#Task_5("hhhh", 10)
