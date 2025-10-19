'''
Задание 4: Scat_or_scat.py
Автор: Дуплей Максим Игоревич / Дарья Руслановна Оборотова

Задача:
Считывать строки до тех пор, пока не встретится строка, содержащая слово "Scat" (регистр может быть любым — "scat", "SCAT", "Scat" и т.д.).
Из всех введённых до этой строки нужно выбрать только те, которые содержат восклицательный знак ! — это и есть «похвалы котику».
Затем вычислить среднюю длину этих похвал (в символах) и округлить до 5 знаков после запятой.

Пример ввода:
Sweet bun!
Good girl!
The beauty!
You're my fuzzy!
What stripes you have!
So scat!

Вывод:
13.8
'''

praises = [] # Список для хранения похвал котику

while True:
    line = input().strip()
    if "scat" in line.lower():  # Проверяем наличие слова "scat" в любом регистре
        break
    if '!' in line:  # Проверяем наличие восклицательного знака
        praises.append(line)

# if praises:  # Если есть похвалы
#     avg_length = sum(len(praise) for praise in praises) / len(praises)
#     print(f"{avg_length:.2f}")
# else:
#     print("0.00")

if len(praises) > 0:
    total_length = 0
    for praise in praises:
        total_length += len(praise)
    average_length = total_length / len(praises)
    print(f"{average_length:.2f}")