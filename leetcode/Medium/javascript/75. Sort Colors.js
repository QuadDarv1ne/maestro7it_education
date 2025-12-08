/**
 * Сортировка цветов (Dutch National Flag алгоритм)
 * 
 * Алгоритм: Three-way partition
 * Сложность: O(n) по времени, O(1) по памяти
 * 
 * @param {number[]} nums - массив целых чисел (0, 1, 2)
 * @return {void} - сортирует массив на месте
 */
var sortColors = function(nums) {
    let low = 0;          // Конец нулей
    let mid = 0;          // Текущий элемент
    let high = nums.length - 1;  // Начало двоек
    
    while (mid <= high) {
        if (nums[mid] === 0) {
            // Обмен и сдвиг для нулей
            [nums[low], nums[mid]] = [nums[mid], nums[low]];
            low++;
            mid++;
        } else if (nums[mid] === 1) {
            // Единицы остаются на месте
            mid++;
        } else { // nums[mid] === 2
            // Обмен и сдвиг для двоек
            [nums[mid], nums[high]] = [nums[high], nums[mid]];
            high--;
            // Не увеличиваем mid, нужно проверить новый элемент
        }
    }
};

/**
 * Альтернативное решение: counting sort
 */
var sortColorsCounting = function(nums) {
    let count0 = 0, count1 = 0, count2 = 0;
    
    // Подсчет элементов
    for (let num of nums) {
        if (num === 0) count0++;
        else if (num === 1) count1++;
        else count2++;
    }
    
    // Заполнение массива
    let index = 0;
    for (let i = 0; i < count0; i++) nums[index++] = 0;
    for (let i = 0; i < count1; i++) nums[index++] = 1;
    for (let i = 0; i < count2; i++) nums[index++] = 2;
};

/**
 * Расширенная версия для k цветов
 */
var sortColorsK = function(nums, k) {
    const count = new Array(k + 1).fill(0);
    
    // Подсчет каждого цвета
    for (let num of nums) {
        count[num]++;
    }
    
    // Заполнение массива
    let index = 0;
    for (let color = 0; color <= k; color++) {
        for (let i = 0; i < count[color]; i++) {
            nums[index++] = color;
        }
    }
};

/**
 * Визуализация процесса сортировки
 */
var sortColorsWithVisualization = function(nums) {
    console.log("Начальный массив:", [...nums]);
    
    let low = 0, mid = 0, high = nums.length - 1;
    let step = 1;
    
    while (mid <= high) {
        console.log(`\nШаг ${step++}:`);
        console.log(`low=${low}, mid=${mid}, high=${high}`);
        console.log("Текущий массив:", [...nums]);
        console.log(`nums[${mid}] = ${nums[mid]}`);
        
        if (nums[mid] === 0) {
            [nums[low], nums[mid]] = [nums[mid], nums[low]];
            console.log(`Обменяли nums[${low}] и nums[${mid}]`);
            low++;
            mid++;
        } else if (nums[mid] === 1) {
            console.log("Пропускаем единицу");
            mid++;
        } else {
            [nums[mid], nums[high]] = [nums[high], nums[mid]];
            console.log(`Обменяли nums[${mid}] и nums[${high}]`);
            high--;
        }
    }
    
    console.log("\nФинальный массив:", nums);
    return nums;
};

// Тестирование
function testSortColors() {
    const testCases = [
        { input: [2,0,2,1,1,0], expected: [0,0,1,1,2,2] },
        { input: [2,0,1], expected: [0,1,2] },
        { input: [0], expected: [0] },
        { input: [1,0], expected: [0,1] },
        { input: [2,2,2,2], expected: [2,2,2,2] },
        { input: [1,1,1,1], expected: [1,1,1,1] },
        { input: [0,0,0,0], expected: [0,0,0,0] },
        { input: [2,1,0], expected: [0,1,2] }
    ];
    
    console.log("Тестирование Dutch National Flag алгоритма:\n");
    
    testCases.forEach((testCase, index) => {
        const nums = [...testCase.input];
        sortColors(nums);
        
        const passed = JSON.stringify(nums) === JSON.stringify(testCase.expected);
        console.log(passed ? "✓" : "✗", `Тест ${index + 1}:`);
        console.log(`  Вход:    [${testCase.input}]`);
        console.log(`  Результат: [${nums}]`);
        console.log(`  Ожидалось: [${testCase.expected}]`);
    });
    
    console.log("\n--- Визуализация процесса ---");
    const demoArray = [2,0,2,1,1,0];
    sortColorsWithVisualization([...demoArray]);
}