/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * Возвращает все пути от корня до листьев в бинарном дереве.
 * 
 * Алгоритм (рекурсивный DFS):
 * 1. Если узел пустой, возвращаем пустой массив.
 * 2. Если узел - лист, добавляем путь к результату.
 * 3. Рекурсивно обходим левое и правое поддеревья.
 * 
 * Сложность:
 * Время: O(n)
 * Пространство: O(h) для рекурсивного стека
 * 
 * @param {TreeNode} root - Корень бинарного дерева
 * @return {string[]} Массив строк, представляющих пути от корня до листьев
 * 
 * @example
 * // Входное дерево:
 * //       1
 * //     /   \
 * //    2     3
 * //     \
 * //      5
 * // 
 * // Выход: ["1->2->5", "1->3"]
 */
var binaryTreePaths = function(root) {
    const result = [];
    
    if (root) {
        dfs(root, "", result);
    }
    
    return result;
};

/**
 * Рекурсивный обход дерева в глубину.
 * 
 * @param {TreeNode} node - Текущий узел
 * @param {string} path - Текущий путь от корня до данного узла
 * @param {string[]} result - Массив для хранения результатов
 */
function dfs(node, path, result) {
    // Добавляем текущий узел к пути
    let currentPath;
    if (path === "") {
        currentPath = node.val.toString();
    } else {
        currentPath = path + "->" + node.val;
    }
    
    // Если узел - лист, добавляем путь к результату
    if (!node.left && !node.right) {
        result.push(currentPath);
        return;
    }
    
    // Рекурсивно обходим левое и правое поддеревья
    if (node.left) {
        dfs(node.left, currentPath, result);
    }
    if (node.right) {
        dfs(node.right, currentPath, result);
    }
}

/**
 * Итеративное решение с использованием стека (DFS).
 * 
 * Алгоритм:
 * 1. Используем стек для хранения пар (узел, путь)
 * 2. При достижении листа добавляем путь к результату
 * 
 * Сложность:
 * Время: O(n)
 * Пространство: O(n) для стека
 */
var binaryTreePathsIterative = function(root) {
    const result = [];
    if (!root) return result;
    
    const stack = [[root, ""]];
    
    while (stack.length > 0) {
        const [node, path] = stack.pop();
        
        // Обновляем путь для текущего узла
        let currentPath;
        if (path === "") {
            currentPath = node.val.toString();
        } else {
            currentPath = path + "->" + node.val;
        }
        
        // Если узел - лист, добавляем путь к результату
        if (!node.left && !node.right) {
            result.push(currentPath);
        }
        
        // Добавляем потомков в стек
        if (node.right) {
            stack.push([node.right, currentPath]);
        }
        if (node.left) {
            stack.push([node.left, currentPath]);
        }
    }
    
    return result;
};

/**
 * Решение с использованием BFS (очереди).
 * 
 * Алгоритм:
 * 1. Используем очередь для обхода дерева по уровням
 * 2. Храним в очереди пары (узел, путь)
 * 
 * Сложность:
 * Время: O(n)
 * Пространство: O(n) для очереди
 */
var binaryTreePathsBFS = function(root) {
    const result = [];
    if (!root) return result;
    
    const queue = [[root, ""]];
    
    while (queue.length > 0) {
        const [node, path] = queue.shift();
        
        // Обновляем путь для текущего узла
        let currentPath;
        if (path === "") {
            currentPath = node.val.toString();
        } else {
            currentPath = path + "->" + node.val;
        }
        
        // Если узел - лист, добавляем путь к результату
        if (!node.left && !node.right) {
            result.push(currentPath);
        }
        
        // Добавляем потомков в очередь
        if (node.left) {
            queue.push([node.left, currentPath]);
        }
        if (node.right) {
            queue.push([node.right, currentPath]);
        }
    }
    
    return result;
};