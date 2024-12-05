# Task 1
x = int(input('Enter the first number: '))
y = int(input('Enter the second number: '))
if x + y > 10:
    print('Сумма больше 10')
elif x + y < 10:
    print('Сумма меньше 10')
else:
    print('Сумма равна 10')

# Task 2
x2 = int(input('Enter an integer number: '))
if x2 > 0:
    print(int(True))
elif x2 == 0:
    print(int(False))
else:
    print(int(True) * (-1))

# Task 3
x3 = int(input('Enter the first integer number: '))
y3 = int(input('Enter the second integer number: '))
if x3 > y3 and y3 < x3:
    print(y3)
elif x3 < y3 and y3 > x3:
    print(x3)
else:
    print('Числа совпадают')