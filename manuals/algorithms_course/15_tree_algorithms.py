"""
АЛГОРИТМЫ НА ДЕРЕВЬЯХ (TREE ALGORITHMS)

Дерево — это связный ациклический граф. В информатике деревья являются одной из
важнейших структур данных, используемых для представления иерархий,
организации данных и эффективного поиска.

Основные понятия:
- Корень (root): вершина без родителя
- Лист (leaf): вершина без детей
- Высота (height): длина пути от корня до самого глубокого листа
- Глубина (depth): расстояние от корня до вершины
- Поддерево (subtree): дерево, образованное вершиной и её потомками

Типы деревьев:
1. Бинарное дерево — каждая вершина имеет не более двух детей
2. Бинарное дерево поиска (BST) — левый потомок меньше, правый больше
3. Сбалансированные деревья — AVL, Red-Black
4. N-арное дерево — каждый узел может иметь N детей

Основные операции:
- Обходы: inorder, preorder, postorder, level-order
- Поиск, вставка, удаление
- Подсчёт вершин, высоты, проверка сбалансированности
"""

from typing import List, Optional, Tuple
from collections import deque


# ===== ОПРЕДЕЛЕНИЕ УЗЛА ДЕРЕВА =====

class TreeNode:
    """
    Узел бинарного дерева.
    
    Атрибуты:
        val: значение узла
        left: левый потомок
        right: правый потомок
    """
    
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"


class NaryNode:
    """
    Узел N-арного дерева.
    
    Атрибуты:
        val: значение узла
        children: список детей
    """
    
    def __init__(self, val: int = None, children: List['NaryNode'] = None):
        self.val = val
        self.children = children if children is not None else []
    
    def __repr__(self):
        return f"NaryNode({self.val})"


# ===== ОБХОДЫ ДЕРЕВА =====

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Симметричный (inorder) обход бинарного дерева.
    
    Порядок: левое поддерево -> корень -> правое поддерево.
    Для BST даёт отсортированный порядок значений.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        list: значения узлов в порядке обхода
    
    Сложность: O(n) по времени, O(h) по памяти (h — высота)
    
    Пример:
        >>> #    1
        >>> #   / \\
        >>> #  2   3
        >>> inorder_traversal(root)  # [2, 1, 3]
    """
    result = []
    
    def inorder(node: Optional[TreeNode]):
        if node is None:
            return
        inorder(node.left)
        result.append(node.val)
        inorder(node.right)
    
    inorder(root)
    return result


def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Итеративный inorder обход.
    
    Использует стек вместо рекурсии.
    Полезен для избежания переполнения стека вызовов.
    
    Сложность: O(n) по времени, O(h) по памяти
    """
    result = []
    stack = []
    current = root
    
    while current or stack:
        # Идём влево до упора
        while current:
            stack.append(current)
            current = current.left
        
        # Обрабатываем узел
        current = stack.pop()
        result.append(current.val)
        
        # Переходим вправо
        current = current.right
    
    return result


def preorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Прямой (preorder) обход бинарного дерева.
    
    Порядок: корень -> левое поддерево -> правое поддерево.
    Используется для копирования дерева, сериализации.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        list: значения узлов в порядке обхода
    
    Сложность: O(n)
    """
    result = []
    
    def preorder(node: Optional[TreeNode]):
        if node is None:
            return
        result.append(node.val)
        preorder(node.left)
        preorder(node.right)
    
    preorder(root)
    return result


def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Итеративный preorder обход.
    """
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Правый добавляем первым (LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result


def postorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Обратный (postorder) обход бинарного дерева.
    
    Порядок: левое поддерево -> правое поддерево -> корень.
    Используется для удаления дерева, вычисления размера.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        list: значения узлов в порядке обхода
    
    Сложность: O(n)
    """
    result = []
    
    def postorder(node: Optional[TreeNode]):
        if node is None:
            return
        postorder(node.left)
        postorder(node.right)
        result.append(node.val)
    
    postorder(root)
    return result


def level_order_traversal(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Обход по уровням (BFS).
    
    Посещаем узлы уровень за уровнем, слева направо.
    Также известен как breadth-first traversal.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        list: список списков значений по уровням
    
    Сложность: O(n) по времени, O(w) по памяти (w — максимальная ширина)
    
    Пример:
        >>> #     1
        >>> #    / \\
        >>> #   2   3
        >>> #  / \\
        >>> # 4   5
        >>> level_order_traversal(root)  # [[1], [2, 3], [4, 5]]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result


def zigzag_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Z-образный обход по уровням.
    
    Чередуем направление обхода на каждом уровне.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        list: значения по уровням в зигзагообразном порядке
    
    Пример:
        >>> #     1
        >>> #    / \\
        >>> #   2   3
        >>> #  / \\
        >>> # 4   5
        >>> zigzag_level_order(root)  # [[1], [3, 2], [4, 5]]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        if not left_to_right:
            level.reverse()
        result.append(level)
        left_to_right = not left_to_right
    
    return result


# ===== ВЫСОТА И ГЛУБИНА =====

def max_depth(root: Optional[TreeNode]) -> int:
    """
    Максимальная глубина (высота) бинарного дерева.
    
    Высота = количество узлов на самом длинном пути от корня до листа.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        int: максимальная глубина
    
    Сложность: O(n)
    
    Пример:
        >>> #   1
        >>> #  / \\
        >>> # 2   3
        >>> max_depth(root)  # 2
    """
    if not root:
        return 0
    
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    
    return 1 + max(left_depth, right_depth)


def min_depth(root: Optional[TreeNode]) -> int:
    """
    Минимальная глубина бинарного дерева.
    
    Минимальная глубина = количество узлов на кратчайшем пути
    от корня до ближайшего листа.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        int: минимальная глубина
    
    Сложность: O(n)
    """
    if not root:
        return 0
    
    # Если один из детей отсутствует, берём глубину другого
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)
    
    return 1 + min(min_depth(root.left), min_depth(root.right))


# ===== СБАЛАНСИРОВАННОСТЬ =====

def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    Проверка сбалансированности бинарного дерева.
    
    Дерево сбалансировано, если для каждого узла разница высот
    левого и правого поддеревьев не превышает 1.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        bool: True если дерево сбалансировано
    
    Сложность: O(n) — оптимизированный алгоритм
    
    Пример:
        >>> #     1
        >>> #    / \\
        >>> #   2   3
        >>> #  /
        >>> # 4
        >>> is_balanced(root)  # True
    """
    def check_height(node: Optional[TreeNode]) -> int:
        """
        Проверка высоты и сбалансированности.
        
        Возвращает:
            int: высоту дерева, или -1 если несбалансировано
        """
        if not node:
            return 0
        
        left_height = check_height(node.left)
        if left_height == -1:
            return -1
        
        right_height = check_height(node.right)
        if right_height == -1:
            return -1
        
        if abs(left_height - right_height) > 1:
            return -1
        
        return 1 + max(left_height, right_height)
    
    return check_height(root) != -1


# ===== ДИАМЕТР ДЕРЕВА =====

def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    Диаметр бинарного дерева.
    
    Диаметр = длина самого длинного пути между любыми двумя узлами.
    Путь может проходить через корень или нет.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        int: диаметр (количество рёбер)
    
    Сложность: O(n)
    
    Пример:
        >>> #      1
        >>> #     / \\
        >>> #    2   3
        >>> #   / \\
        >>> #  4   5
        >>> diameter_of_binary_tree(root)  # 3 (путь 4-2-1-3 или 5-2-1-3)
    """
    diameter = 0
    
    def height(node: Optional[TreeNode]) -> int:
        """Вычисление высоты с обновлением диаметра."""
        nonlocal diameter
        
        if not node:
            return 0
        
        left_height = height(node.left)
        right_height = height(node.right)
        
        # Диаметр через текущий узел
        diameter = max(diameter, left_height + right_height)
        
        return 1 + max(left_height, right_height)
    
    height(root)
    return diameter


# ===== БИНАРНОЕ ДЕРЕВО ПОИСКА (BST) =====

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Проверка, является ли дерево бинарным деревом поиска.
    
    BST: для каждого узла все значения в левом поддереве меньше,
    а в правом поддереве больше.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        bool: True если дерево является BST
    
    Сложность: O(n)
    
    Пример:
        >>> #   2
        >>> #  / \\
        >>> # 1   3
        >>> is_valid_bst(root)  # True
    """
    def validate(node: Optional[TreeNode], min_val: float, max_val: float) -> bool:
        """
        Рекурсивная проверка с диапазоном допустимых значений.
        """
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))


def search_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Поиск значения в BST.
    
    Аргументы:
        root: корень BST
        val: искомое значение
    
    Возвращает:
        TreeNode: найденный узел или None
    
    Сложность: O(h), где h — высота дерева
    """
    if not root or root.val == val:
        return root
    
    if val < root.val:
        return search_bst(root.left, val)
    else:
        return search_bst(root.right, val)


def insert_into_bst(root: Optional[TreeNode], val: int) -> TreeNode:
    """
    Вставка значения в BST.
    
    Аргументы:
        root: корень BST
        val: значение для вставки
    
    Возвращает:
        TreeNode: корень дерева после вставки
    
    Сложность: O(h)
    """
    if not root:
        return TreeNode(val)
    
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    
    return root


def delete_from_bst(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    Удаление узла из BST.
    
    Три случая:
    1. Узел без детей — просто удаляем
    2. Узел с одним ребёнком — заменяем на ребёнка
    3. Узел с двумя детьми — заменяем на inorder-преемника
    
    Аргументы:
        root: корень BST
        key: значение для удаления
    
    Возвращает:
        TreeNode: корень дерева после удаления
    
    Сложность: O(h)
    """
    if not root:
        return None
    
    if key < root.val:
        root.left = delete_from_bst(root.left, key)
    elif key > root.val:
        root.right = delete_from_bst(root.right, key)
    else:
        # Нашли узел для удаления
        
        # Случай 1 и 2: один или ноль детей
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        
        # Случай 3: два ребенка
        # Находим inorder-преемника (минимум в правом поддереве)
        successor = find_min(root.right)
        root.val = successor.val
        root.right = delete_from_bst(root.right, successor.val)
    
    return root


def find_min(node: TreeNode) -> TreeNode:
    """Найти узел с минимальным значением в дереве."""
    while node.left:
        node = node.left
    return node


# ===== ОБЩИЙ ПРЕДОК =====

def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Наименьший общий предок (LCA) в бинарном дереве.
    
    LCA — самый глубокий узел, имеющий p и q в качестве потомков.
    
    Аргументы:
        root: корень дерева
        p, q: узлы для поиска предка
    
    Возвращает:
        TreeNode: наименьший общий предок
    
    Сложность: O(n)
    """
    # Базовый случай
    if not root or root == p or root == q:
        return root
    
    # Ищем в поддеревьях
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    # Если найдено в обоих поддеревьях — root и есть LCA
    if left and right:
        return root
    
    # Иначе возвращаем найденный результат
    return left if left else right


def lca_bst(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LCA в бинарном дереве поиска.
    
    Использует свойство BST для оптимизации.
    
    Сложность: O(h)
    """
    if not root:
        return None
    
    # Оба узла в левом поддереве
    if p.val < root.val and q.val < root.val:
        return lca_bst(root.left, p, q)
    
    # Оба узла в правом поддереве
    if p.val > root.val and q.val > root.val:
        return lca_bst(root.right, p, q)
    
    # Узлы в разных поддеревьях — root есть LCA
    return root


# ===== СИММЕТРИЯ И ОТРАЖЕНИЕ =====

def is_symmetric(root: Optional[TreeNode]) -> bool:
    """
    Проверка симметричности бинарного дерева.
    
    Дерево симметрично, если оно зеркально отражается относительно центра.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        bool: True если дерево симметрично
    
    Сложность: O(n)
    
    Пример:
        >>> #     1
        >>> #    / \\
        >>> #   2   2
        >>> #  / \\ / \\
        >>> # 3  4 4  3
        >>> is_symmetric(root)  # True
    """
    def is_mirror(left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
        """Проверка зеркальности двух поддеревьев."""
        if not left and not right:
            return True
        if not left or not right:
            return False
        
        return (left.val == right.val and
                is_mirror(left.left, right.right) and
                is_mirror(left.right, right.left))
    
    if not root:
        return True
    return is_mirror(root.left, root.right)


def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Инвертирование (отражение) бинарного дерева.
    
    Меняет местами левых и правых потомков.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        TreeNode: корень инвертированного дерева
    
    Сложность: O(n)
    
    Пример:
        >>> #      4          4
        >>> #     / \\        / \\
        >>> #    2   7  ->  7   2
        >>> #   / \\ / \\    / \\ / \\
        >>> #  1  3 6  9   9  6 3  1
    """
    if not root:
        return None
    
    # Меняем местами детей
    root.left, root.right = root.right, root.left
    
    # Рекурсивно инвертируем поддеревья
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root


# ===== ПУТИ В ДЕРЕВЕ =====

def binary_tree_paths(root: Optional[TreeNode]) -> List[str]:
    """
    Все пути от корня до листьев.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        list: список путей в формате "1->2->3"
    
    Сложность: O(n)
    """
    result = []
    
    def dfs(node: Optional[TreeNode], path: str):
        if not node:
            return
        
        current_path = path + str(node.val)
        
        # Если лист — добавляем путь
        if not node.left and not node.right:
            result.append(current_path)
            return
        
        # Иначе продолжаем путь
        dfs(node.left, current_path + "->")
        dfs(node.right, current_path + "->")
    
    dfs(root, "")
    return result


def has_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    """
    Проверка существования пути с заданной суммой.
    
    Путь должен идти от корня до листа.
    
    Аргументы:
        root: корень дерева
        target_sum: целевая сумма
    
    Возвращает:
        bool: True если путь существует
    
    Сложность: O(n)
    """
    if not root:
        return False
    
    # Лист — проверяем сумму
    if not root.left and not root.right:
        return root.val == target_sum
    
    remaining = target_sum - root.val
    return (has_path_sum(root.left, remaining) or 
            has_path_sum(root.right, remaining))


def path_sum_all(root: Optional[TreeNode], target_sum: int) -> List[List[int]]:
    """
    Все пути с заданной суммой от корня до листа.
    
    Аргументы:
        root: корень дерева
        target_sum: целевая сумма
    
    Возвращает:
        list: все пути с суммой target_sum
    
    Сложность: O(n)
    """
    result = []
    
    def dfs(node: Optional[TreeNode], remaining: int, path: List[int]):
        if not node:
            return
        
        path.append(node.val)
        
        # Лист — проверяем сумму
        if not node.left and not node.right:
            if remaining == node.val:
                result.append(path[:])
        else:
            dfs(node.left, remaining - node.val, path)
            dfs(node.right, remaining - node.val, path)
        
        path.pop()  # Backtrack
    
    dfs(root, target_sum, [])
    return result


# ===== ПОСТРОЕНИЕ ДЕРЕВЬЕВ =====

def build_tree_from_preorder_inorder(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    Построение дерева из preorder и inorder обходов.
    
    preorder: корень, левое, правое
    inorder: левое, корень, правое
    
    Аргументы:
        preorder: список значений в прямом порядке
        inorder: список значений в симметричном порядке
    
    Возвращает:
        TreeNode: корень построенного дерева
    
    Сложность: O(n) с хеш-таблицей
    
    Пример:
        >>> preorder = [3, 9, 20, 15, 7]
        >>> inorder = [9, 3, 15, 20, 7]
        >>> #      3
        >>> #     / \\
        >>> #    9  20
        >>> #      / \\
        >>> #     15  7
    """
    # Хеш-таблица для быстрого поиска позиции в inorder
    inorder_map = {val: i for i, val in enumerate(inorder)}
    preorder_idx = 0
    
    def build(left: int, right: int) -> Optional[TreeNode]:
        nonlocal preorder_idx
        
        if left > right:
            return None
        
        # Корень — следующий элемент preorder
        root_val = preorder[preorder_idx]
        preorder_idx += 1
        root = TreeNode(root_val)
        
        # Позиция корня в inorder
        idx = inorder_map[root_val]
        
        # Строим поддеревья
        root.left = build(left, idx - 1)
        root.right = build(idx + 1, right)
        
        return root
    
    return build(0, len(inorder) - 1)


def build_tree_from_inorder_postorder(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    """
    Построение дерева из inorder и postorder обходов.
    
    postorder: левое, правое, корень
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}
    postorder_idx = len(postorder) - 1
    
    def build(left: int, right: int) -> Optional[TreeNode]:
        nonlocal postorder_idx
        
        if left > right:
            return None
        
        root_val = postorder[postorder_idx]
        postorder_idx -= 1
        root = TreeNode(root_val)
        
        idx = inorder_map[root_val]
        
        # Важно: сначала правое поддерево!
        root.right = build(idx + 1, right)
        root.left = build(left, idx - 1)
        
        return root
    
    return build(0, len(inorder) - 1)


# ===== СЕРИАЛИЗАЦИЯ =====

def serialize(root: Optional[TreeNode]) -> str:
    """
    Сериализация бинарного дерева в строку.
    
    Использует preorder обход с маркерами для None.
    
    Аргументы:
        root: корень дерева
    
    Возвращает:
        str: сериализованное представление
    
    Пример:
        >>> #   1
        >>> #  / \\
        >>> # 2   3
        >>> serialize(root)  # "1,2,null,null,3,null,null"
    """
    result = []
    
    def dfs(node: Optional[TreeNode]):
        if not node:
            result.append("null")
            return
        
        result.append(str(node.val))
        dfs(node.left)
        dfs(node.right)
    
    dfs(root)
    return ",".join(result)


def deserialize(data: str) -> Optional[TreeNode]:
    """
    Десериализация строки в бинарное дерево.
    
    Аргументы:
        data: сериализованное представление
    
    Возвращает:
        TreeNode: корень восстановленного дерева
    """
    values = data.split(",")
    idx = 0
    
    def build() -> Optional[TreeNode]:
        nonlocal idx
        
        if idx >= len(values):
            return None
        
        val = values[idx]
        idx += 1
        
        if val == "null":
            return None
        
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        
        return node
    
    return build()


# ===== N-АРНОЕ ДЕРЕВО =====

def nary_level_order(root: Optional[NaryNode]) -> List[List[int]]:
    """
    Обход N-арного дерева по уровням.
    
    Аргументы:
        root: корень N-арного дерева
    
    Возвращает:
        list: значения по уровням
    
    Сложность: O(n)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            for child in node.children:
                queue.append(child)
        
        result.append(level)
    
    return result


def nary_max_depth(root: Optional[NaryNode]) -> int:
    """
    Максимальная глубина N-арного дерева.
    """
    if not root:
        return 0
    
    max_child_depth = 0
    for child in root.children:
        max_child_depth = max(max_child_depth, nary_max_depth(child))
    
    return 1 + max_child_depth


# ===== ПОДСЧЁТ УЗЛОВ =====

def count_nodes(root: Optional[TreeNode]) -> int:
    """
    Подсчёт количества узлов в дереве.
    
    Сложность: O(n)
    """
    if not root:
        return 0
    
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def count_nodes_complete(root: Optional[TreeNode]) -> int:
    """
    Подсчёт узлов в полном бинарном дереве.
    
    Полное бинарное дерево: все уровни заполнены, кроме последнего,
    который заполнен слева направо.
    
    Оптимизация: O(log²n) вместо O(n).
    
    Сложность: O(log²n)
    """
    if not root:
        return 0
    
    def get_height(node: Optional[TreeNode], go_left: bool) -> int:
        """Высота, идя всегда влево или всегда вправо."""
        height = 0
        while node:
            height += 1
            node = node.left if go_left else node.right
        return height
    
    left_height = get_height(root, True)
    right_height = get_height(root, False)
    
    # Полное дерево: 2^h - 1 узлов
    if left_height == right_height:
        return (1 << left_height) - 1
    
    # Неполное: рекурсивно считаем
    return 1 + count_nodes_complete(root.left) + count_nodes_complete(root.right)


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    
    # Создаём тестовое дерево
    #       1
    #      / \\
    #     2   3
    #    / \\
    #   4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    print("Тестовое дерево:")
    print("       1")
    print("      / \\")
    print("     2   3")
    print("    / \\")
    print("   4   5")
    
    print("\nОбходы:")
    print(f"  Inorder: {inorder_traversal(root)}")
    print(f"  Preorder: {preorder_traversal(root)}")
    print(f"  Postorder: {postorder_traversal(root)}")
    print(f"  Level order: {level_order_traversal(root)}")
    
    print("\nХарактеристики:")
    print(f"  Максимальная глубина: {max_depth(root)}")
    print(f"  Минимальная глубина: {min_depth(root)}")
    print(f"  Диаметр: {diameter_of_binary_tree(root)}")
    print(f"  Количество узлов: {count_nodes(root)}")
    print(f"  Сбалансировано: {is_balanced(root)}")
    
    print("\nПути:")
    print(f"  Все пути: {binary_tree_paths(root)}")
    print(f"  Путь с суммой 7: {has_path_sum(root, 7)}")
    
    # BST
    print("\nБинарное дерево поиска:")
    bst_root = TreeNode(5)
    bst_root = insert_into_bst(bst_root, 3)
    bst_root = insert_into_bst(bst_root, 7)
    bst_root = insert_into_bst(bst_root, 1)
    bst_root = insert_into_bst(bst_root, 4)
    print(f"  Inorder BST: {inorder_traversal(bst_root)}")
    print(f"  Является BST: {is_valid_bst(bst_root)}")
    
    # Сериализация
    print("\nСериализация:")
    serialized = serialize(root)
    print(f"  Сериализованное: {serialized}")
    restored = deserialize(serialized)
    print(f"  Восстановлено (inorder): {inorder_traversal(restored)}")
    
    # Симметрия
    print("\nСимметрия:")
    sym_root = TreeNode(1)
    sym_root.left = TreeNode(2)
    sym_root.right = TreeNode(2)
    print(f"  Дерево [1,2,2] симметрично: {is_symmetric(sym_root)}")
