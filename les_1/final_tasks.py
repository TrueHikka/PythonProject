#Task 1
name = input('Enter your name: ')
profession = input('Enter your profession: ')
age = int(input('Enter your age: '))

print(f'\nName: {name} \nProfession: {profession} \nAge: {age}')

#Task 2
x = int(input('Enter the first number: '))
y = int(input('Enter the second number: '))
a = int(input('Enter the third number: '))
b = int(input('Enter the fourth number: '))

print((x + y) / (a + b))

#Task 3
x1 = int(input('Enter the first number: '))
y1 = int(input('Enter the second number: '))
z1 = int(input('Enter the third number: '))

# if x1 > y1 and x1 > z1:
#     print(x1)
# elif y1 > x1 and y1 > z1:
#     print(y1)
# else:
#     print(z1)

if x1 > y1:
    if x1 > z1:
        print(x1)
    else:
        print(z1)
else:
    if y1 > z1:
        print(y1)
    else:
        print(z1)


#Task 4
x2 = int(input('Enter the first number: '))
y2 = int(input('Enter the second number: '))
z2 = int(input('Enter the third number: '))

if y2 < x2 < z2:
    print(x2)
elif x2 < y2 < z2:
    print(y2)
else:
    print(z2)

# 5
x3 = int(input('Enter an integer number: '))
print('Следующее число для числа', x3, 'это', x3 + 1)
print('Предыдущее число для числа', x3, 'это', x3 - 1)
# Или
print(f'Следующее число для числа {x3} это {x3 + 1}')
print(f'Предыдущее число для числа {x3} это {x3 - 1}')

#Task 6
breadCost = 30
milkCost = 50
cheeseCost = 100

totalCost = breadCost + milkCost + cheeseCost

budget = int(input('Сколько у вас денег? '))

if budget > totalCost:
    print(f'\nОбщая стоимость товаров: {totalCost}')
    print(f'Ваша сдача: {budget - totalCost}')
elif budget < totalCost:
    print('Недостаточно денег')
else:
    print('Спасибо, что без сдачи!')

# Task 7
x = int(input('Recommended number of meters to run per week: '))
y = int(input('It is not recommended to run more than meters per week: '))
z = int(input('Now Masha runs the number of meters per week: '))

if x <= z <= y:
    print('Это нормально')
elif z < x:
    print('Слишком мало бегаете')
else:
    print('Много бегать вредно')