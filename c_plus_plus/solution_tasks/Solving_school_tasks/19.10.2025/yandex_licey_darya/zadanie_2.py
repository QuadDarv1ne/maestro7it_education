'''
Задание 2: brevity_talent_sister.py
Автор: Дуплей Максим Игоревич / Дарья Руслановна Оборотова

Задача:
Найти самую короткую строку (по количеству символов) из введённых, исключая строку "end",
которая служит признаком окончания ввода.
Если таких самых коротких строк несколько — выбрать последнюю по порядку ввода.

Пример ввода:
A day without a smile is a lost day.
Dance as if no one is looking at you.
Feel the tailwind in your sail.
Sing as if no one can hear you.
Love as if you've never been betrayed.
Everything must be fine in the end.

Вывод:
Sing as if no one can hear you.
'''

min_length = float('inf')
shortest_line = None

while True:
    line = input().strip()
    # print(f"[DEBUG] Получена строка: '{line}'")
    if line == "end":
        break
    if line == "":
        continue
    line_length = len(line)
    # Выбираем последнюю строку с минимальной длиной
    if line_length <= min_length:
        min_length = line_length
        shortest_line = line

if shortest_line is not None:
    print(shortest_line)