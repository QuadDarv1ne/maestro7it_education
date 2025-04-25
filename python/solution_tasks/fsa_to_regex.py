'''
FSA to RegExp Translator

fsa - сокращение от Finite State Automaton (Конечный Автомат)
to_regex - указывает на преобразование в регулярное выражение
.py - стандартное расширение для Python-файлов
'''

import sys
import re
from collections import defaultdict, deque

def main():
    """
    Основная функция программы для преобразования конечного автомата (FSA) в регулярное выражение.
    
    Чтение и обработка ввода, валидация данных, преобразование FSA в регулярное выражение 
    с использованием алгоритма Клини и вывод результата или сообщения об ошибке.
    """
    try:
        # Чтение и предварительная обработка входных данных
        input_lines = [line.strip() for line in sys.stdin if line.strip()]
        if len(input_lines) != 6:
            print("Input is malformed.")
            return

        # Разбор строк ввода в словарь
        parsed = {}
        for line in input_lines:
            if '=' not in line:
                print("Input is malformed.")
                return
            key, value = line.split('=', 1)
            parsed[key] = value

        # Проверка наличия всех обязательных ключей
        required_keys = ['type', 'states', 'alphabet', 'initial', 'accepting', 'transitions']
        if not all(k in parsed for k in required_keys):
            print("Input is malformed.")
            return

        # Разбор типа автомата
        fsa_type = parsed['type'].strip('[]')
        if fsa_type not in ['deterministic', 'non-deterministic']:
            print("Input is malformed.")
            return

        # Разбор состояний
        states_str = parsed['states'].strip('[]')
        states = [s.strip() for s in states_str.split(',')] if states_str else []
        for state in states:
            if not re.fullmatch(r'[a-zA-Z0-9_]+', state):
                print("Input is malformed.")
                return
        states_set = set(states)

        # Разбор алфавита
        alphabet_str = parsed['alphabet'].strip('[]')
        alphabet = [a.strip() for a in alphabet_str.split(',')] if alphabet_str else []
        for symbol in alphabet:
            if not re.fullmatch(r'[a-zA-Z0-9_]+', symbol):
                print("Input is malformed.")
                return
        alphabet_set = set(alphabet)

        # Разбор начального состояния
        initial_str = parsed['initial'].strip('[]')
        initial = initial_str.strip()
        if not initial:
            print("Initial state is not defined.")
            return
        if initial not in states_set:
            print(f"A state '{initial}' is not in the set of states.")
            return

        # Разбор допускающих состояний
        accepting_str = parsed['accepting'].strip('[]')
        accepting = [s.strip() for s in accepting_str.split(',')] if accepting_str else []
        for state in accepting:
            if state not in states_set:
                print(f"A state '{state}' is not in the set of states.")
                return
        if not accepting:
            print("Set of accepting states is empty.")
            return

        # Разбор переходов
        transitions_str = parsed['transitions'].strip('[]')
        transitions_list = [t.strip() for t in transitions_str.split(',')] if transitions_str else []
        transitions = defaultdict(lambda: defaultdict(list))
        transition_map = defaultdict(lambda: defaultdict(list))
        has_eps = False

        for transition in transitions_list:
            parts = transition.split('>')
            if len(parts) != 3:
                print("Input is malformed.")
                return
            src, symbol, dest = parts
            if src not in states_set:
                print(f"A state '{src}' is not in the set of states.")
                return
            if dest not in states_set:
                print(f"A state '{dest}' is not in the set of states.")
                return
            if symbol != 'eps' and symbol not in alphabet_set:
                print(f"A transition symbol '{symbol}' is not in the alphabet.")
                return
            if symbol == 'eps':
                has_eps = True
            transitions[src][dest].append(symbol)
            transition_map[src][symbol].append(dest)

        # Проверка на недетерминированность для детерминированного автомата
        if fsa_type == 'deterministic':
            if has_eps:
                print("FSA is non-deterministic.")
                return
            for src in transition_map:
                for symbol in transition_map[src]:
                    if len(transition_map[src][symbol]) > 1:
                        print("FSA is non-deterministic.")
                        return

        # Проверка связности состояний
        if not is_fsa_connected(states_set, initial, accepting, transitions):
            print("Some states are disjoint.")
            return

        # Преобразование FSA в регулярное выражение с помощью алгоритма Клини
        regex = kleenes_algorithm(states, initial, accepting, transitions)
        print(regex)

    except Exception as e:
        print("Input is malformed.")
        return

def is_fsa_connected(states, initial, accepting, transitions):
    """
    Проверяет связность конечного автомата.
    
    Аргументы:
        states: множество всех состояний
        initial: начальное состояние
        accepting: список допускающих состояний
        transitions: словарь переходов
        
    Возвращает:
        True если автомат связный (все состояния достижимы из начального
        и могут достичь допускающего состояния), иначе False
    """
    # Проверка достижимости из начального состояния
    reachable = set()
    queue = deque([initial])
    reachable.add(initial)
    
    while queue:
        current = queue.popleft()
        for neighbor in transitions.get(current, {}):
            if neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)
    
    # Проверка достижимости всех допускающих состояний
    for acc in accepting:
        if acc not in reachable:
            return False
    
    # Проверка возможности достичь допускающего состояния (обратный граф)
    reverse_transitions = defaultdict(set)
    for src in transitions:
        for dest in transitions[src]:
            reverse_transitions[dest].add(src)
    
    accepting_set = set(accepting)
    can_reach_accepting = accepting_set.copy()
    queue = deque(accepting)
    
    while queue:
        current = queue.popleft()
        for neighbor in reverse_transitions.get(current, set()):
            if neighbor not in can_reach_accepting:
                can_reach_accepting.add(neighbor)
                queue.append(neighbor)
    
    # Проверка что все состояния могут достичь хотя бы одного допускающего
    for state in states:
        if state not in can_reach_accepting:
            return False
    
    return True

def kleenes_algorithm(states, initial, accepting, transitions):
    """
    Реализация алгоритма Клини для преобразования FSA в регулярное выражение.
    
    Аргументы:
        states: список всех состояний
        initial: начальное состояние
        accepting: список допускающих состояний
        transitions: словарь переходов
        
    Возвращает:
        Строку с регулярным выражением, эквивалентным языку FSA
    """
    n = len(states)
    state_to_idx = {state: i for i, state in enumerate(states)}
    
    # Инициализация R[k][i][j] - трехмерный массив регулярных выражений
    R = [[[None for _ in range(n)] for __ in range(n)] for ___ in range(n+1)]
    
    # Базовый случай R^0 (прямые переходы без промежуточных состояний)
    for i in range(n):
        for j in range(n):
            src = states[i]
            dest = states[j]
            symbols = transitions.get(src, {}).get(dest, [])
            
            if not symbols:
                if i == j:
                    R[0][i][j] = "eps"  # Пустой переход в себя
                else:
                    R[0][i][j] = "∅"    # Нет перехода
            else:
                # Обработка символов в лексикографическом порядке с eps в конце
                unique_symbols = sorted(set(symbols))
                if 'eps' in unique_symbols:
                    unique_symbols.remove('eps')
                    unique_symbols.append('eps')
                expr_parts = []
                for sym in unique_symbols:
                    if sym == 'eps':
                        expr_parts.append('eps')
                    else:
                        expr_parts.append(sym)
                if len(expr_parts) == 1:
                    expr = expr_parts[0]
                else:
                    expr = "|".join(expr_parts)
                R[0][i][j] = expr
    
    # Рекурсивный случай - построение выражений с промежуточными состояниями
    for k in range(1, n+1):
        for i in range(n):
            for j in range(n):
                part1 = R[k-1][i][k-1]  # Пути из i в k-1
                part2 = R[k-1][k-1][k-1] # Циклы в k-1
                part3 = R[k-1][k-1][j]  # Пути из k-1 в j
                part4 = R[k-1][i][j]    # Прямые пути из i в j
                
                # Построение нового выражения по формуле Клини
                if part2 == "∅":
                    new_expr = part4
                else:
                    if part1 == "∅" or part3 == "∅":
                        star_part = "∅"
                    else:
                        if part2 == "eps":
                            star_part = "eps*"
                        else:
                            star_part = f"({part2})*"
                        
                        if part1 == "eps" and part3 == "eps":
                            concat = star_part
                        elif part1 == "eps":
                            concat = f"{star_part}({part3})"
                        elif part3 == "eps":
                            concat = f"({part1}){star_part}"
                        else:
                            concat = f"({part1}){star_part}({part3})"
                    
                    if part4 == "∅":
                        new_expr = concat if concat != "∅" else "∅"
                    else:
                        if concat == "∅":
                            new_expr = part4
                        else:
                            new_expr = f"({concat})|({part4})"
                
                R[k][i][j] = new_expr
    
    # Получение всех путей из начального в допускающие состояния
    initial_idx = state_to_idx[initial]
    accepting_idxs = [state_to_idx[state] for state in accepting]
    
    # Объединение всех путей в допускающие состояния
    final_exprs = []
    for acc_idx in accepting_idxs:
        expr = R[n][initial_idx][acc_idx]
        if expr != "∅":
            final_exprs.append(expr)
    
    if not final_exprs:
        return "∅"
    
    # Объединение выражений через ИЛИ с сортировкой
    final_exprs_sorted = sorted(final_exprs)
    if len(final_exprs_sorted) == 1:
        return final_exprs_sorted[0]
    else:
        return "|".join(f"({expr})" for expr in final_exprs_sorted)

if __name__ == "__main__":
    main()

'''
Дата: 25.04.2025
TG: @quadd4rv1n7
Преподаватель: Дуплей Максим Игоревич
'''
