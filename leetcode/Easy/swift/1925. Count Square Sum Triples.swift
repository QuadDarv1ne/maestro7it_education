/**
 * Решение задачи "Count Square Sum Triples" (LeetCode 1925)
 * 
 * @file CountSquareSumTriples.swift
 * @brief Подсчёт всех упорядоченных троек Пифагора в диапазоне [1, n]
 * 
 * @author Дулей Максим Игоревич
 * @see ORCID: https://orcid.org/0009-0007-7605-539X
 * @see GitHub: https://github.com/QuadDarv1ne/
 * 
 * @details
 * Алгоритм: Перебор всех пар (a, b) с проверкой целочисленности √(a² + b²)
 * Сложность: O(n²) времени, O(1) памяти
 * 
 * @approach
 * 1. Используем вложенные циклы для генерации всех пар (a, b)
 * 2. Для каждой пары вычисляем c = √(a² + b²)
 * 3. Проверяем, что c - целое число и ≤ n
 * 4. Увеличиваем счётчик при выполнении условий
 */

import Foundation

class Solution {
    /**
     * Подсчитывает количество упорядоченных троек (a, b, c)
     * 
     * @param n Верхняя граница для a, b, c (1 ≤ n ≤ 250)
     * @return Int Количество троек, удовлетворяющих a² + b² = c²
     * 
     * @example
     * let solution = Solution()
     * print(solution.countTriples(5))   // 2
     * print(solution.countTriples(10))  // 4
     * 
     * @note
     * - Тройки считаются упорядоченными: (3,4,5) и (4,3,5) - разные тройки
     * - Используется Double для вычисления квадратного корня
     * - Проверка целочисленности: c * c == a² + b²
     */
    func countTriples(_ n: Int) -> Int {
        var count = 0
        
        // Перебор всех возможных значений a и b
        for a in 1...n {
            for b in 1...n {
                let cSquared = a * a + b * b
                let c = Int(sqrt(Double(cSquared)))
                
                // Проверяем условия Пифагоровой тройки
                if c <= n && c * c == cSquared {
                    count += 1
                }
            }
        }
        
        return count
    }
    
    /**
     * Альтернативная реализация с использованием множества квадратов
     * 
     * @param n Верхняя граница диапазона
     * @return Int Количество троек
     * 
     * @complexity
     * - Время: O(n²) для создания множества + O(n²) для проверки
     * - Память: O(n) для хранения множества квадратов
     */
    func countTriplesSet(_ n: Int) -> Int {
        var squares = Set<Int>()
        
        // Предварительно вычисляем все квадраты
        for i in 1...n {
            squares.insert(i * i)
        }
        
        var count = 0
        
        // Проверяем все комбинации квадратов
        for aSq in squares {
            for bSq in squares {
                if squares.contains(aSq + bSq) {
                    count += 1
                }
            }
        }
        
        return count
    }
}

// Расширение для функционального стиля
extension Solution {
    /**
     * Функциональная реализация с использованием высших функций
     * 
     * @param n Верхняя граница диапазона
     * @return Int Количество троек
     */
    func countTriplesFunctional(_ n: Int) -> Int {
        return (1...n).reduce(0) { total, a in
            total + (1...n).reduce(0) { subTotal, b in
                let cSq = a * a + b * b
                let c = Int(Double(cSq).squareRoot())
                return subTotal + (c <= n && c * c == cSq ? 1 : 0)
            }
        }
    }
}

// Модульное тестирование
import XCTest

class CountSquareSumTriplesTests: XCTestCase {
    func testBasicCases() {
        let solution = Solution()
        
        XCTAssertEqual(solution.countTriples(5), 2)
        XCTAssertEqual(solution.countTriples(10), 4)
        XCTAssertEqual(solution.countTriples(1), 0)
        XCTAssertEqual(solution.countTriples(2), 0)
        XCTAssertEqual(solution.countTriples(13), 6)
    }
    
    func testPerformance() {
        let solution = Solution()
        
        measure {
            _ = solution.countTriples(250)
        }
    }
}

// Использование в SwiftUI (пример)
// import SwiftUI

// struct ContentView: View {
//     @State private var n = "10"
//     @State private var result = 0
    
//     var body: some View {
//         VStack(spacing: 20) {
//             Text("Count Square Sum Triples")
//                 .font(.largeTitle)
//                 .fontWeight(.bold)
            
//             TextField("Enter n (1-250)", text: $n)
//                 .textFieldStyle(RoundedBorderTextFieldStyle())
//                 .keyboardType(.numberPad)
//                 .padding()
            
//             Button("Calculate") {
//                 if let nValue = Int(n), nValue >= 1 && nValue <= 250 {
//                     result = Solution().countTriples(nValue)
//                 }
//             }
//             .padding()
//             .background(Color.blue)
//             .foregroundColor(.white)
//             .cornerRadius(10)
            
//             Text("Result: \(result)")
//                 .font(.title)
//                 .padding()
//         }
//         .padding()
//     }
// }