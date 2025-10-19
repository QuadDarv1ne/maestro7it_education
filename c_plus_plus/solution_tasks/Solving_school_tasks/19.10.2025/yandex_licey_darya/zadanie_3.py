'''
Задание 3: dlinnaya_doroga.py
Автор: Дуплей Максим Игоревич / Дарья Руслановна Оборотова

Задача:
Имеются три возможные дороги, каждая из которых представляет собой последовательность прописных латинских букв.
Каждая буква обозначает город, через который проходит дорога.

Пример ввода (задание №2):
ABCDFENHG
HABVDM
NHAMBDFH
D
C

Вывод:
8

Пример ввода (задание №3):
ABC
BCD
DEFB
B
E

Вывод:
3
'''

# Считываем три дороги
road1 = input().strip()
road2 = input().strip()
road3 = input().strip()

# Считываем начальный и конечный города
must_have = input().strip()
must_not_have = input().strip()

# Список дорог для обработки
roads = [road1, road2, road3]

max_length = 0

for road in roads:
    # Проверяем наличие обязательного города и отсутствие запрещённого
    if must_have in road and must_not_have not in road:
        # Обновляем максимальную длину, если нужно
        if len(road) > max_length:
            max_length = len(road)

print(max_length)