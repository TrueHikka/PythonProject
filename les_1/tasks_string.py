#Task 1
x = input("Enter a string: ")
y = int(input("Enter a number: "))

print(x + " " + str(y))

x2 = int(input("Enter a number: "))
y2 = input("Enter a string: ")

print(str(x2) + " " + y2)


#Task 2
x3 = input("Enter a string: ")
y3 = int(input("Enter a number: "))

print(len(x3 + str(y3)))

x4 = input("Enter a string with a space: ")
y4 = int(input("Enter a number: "))

print(len(x4 + str(y4)))


#Task 3
input('Ввод: с клавиатуры, значения должны вводиться на этой же строке, справа от текста подсказки: ' + '\n' + '\n'
)

str1 = input('Введите первую строку (например, Яблоко): ')
str2 = input('Введите вторую строку (например, Груша): ')

lengthStr2 = len(str2)

print('Длина второго слова: ' + str(lengthStr2))

resultString = (str1 + str2) * lengthStr2

print('Итоговый результат: ' + resultString)

# Или так
str1 = input('Введите первую строку (например, Яблоко): ')
str2 = input('Введите вторую строку (например, Груша): ')
n = int(input('Введите число N (например, 2): '))

result = (str1 + str2) * n

print('Результат: ' + result)
