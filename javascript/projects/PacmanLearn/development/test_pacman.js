// Тест для класса Pacman
console.log('Запуск тестов для класса Pacman...');

// Создаем экземпляр Пакмана
const pacman = new Pacman(10, 15);

// Тест начальной позиции
console.assert(pacman.x === 10, 'Начальная позиция X должна быть 10');
console.assert(pacman.y === 15, 'Начальная позиция Y должна быть 15');
console.log('Тест начальной позиции пройден');

// Тест установки направления
pacman.setNextDirection('up');
console.assert(pacman.nextDirection === 'up', 'Направление должно быть "up"');
console.log('Тест установки направления пройден');

// Тест активации режима силы
pacman.activatePowerMode(5000);
console.assert(pacman.powerMode === true, 'Режим силы должен быть активен');
console.assert(pacman.powerModeTimer === 5000, 'Таймер режима силы должен быть 5000');
console.log('Тест активации режима силы пройден');

// Тест анимации рта
const initialMouthAngle = pacman.mouthAngle;
pacman.animateMouth();
console.assert(pacman.mouthAngle !== initialMouthAngle, 'Угол рта должен измениться');
console.log('Тест анимации рта пройден');

// Тест сброса позиции
pacman.resetPosition();
console.assert(pacman.x === pacman.startX, 'Позиция X должна быть сброшена');
console.assert(pacman.y === pacman.startY, 'Позиция Y должна быть сброшена');
console.assert(pacman.powerMode === false, 'Режим силы должен быть отключен');
console.log('Тест сброса позиции пройден');

console.log('Все тесты для класса Pacman пройдены успешно!');