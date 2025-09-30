# Документация API Pacman Game

## Обзор

Этот документ описывает API для модульной версии игры Pacman. API разделен на несколько классов, каждый из которых отвечает за свою часть функциональности игры.

## Класс Pacman

### Конструктор
```javascript
new Pacman(x, y)
```
Создает новый экземпляр Пакмана на позиции (x, y).

### Свойства
- `x`: Текущая координата X
- `y`: Текущая координата Y
- `direction`: Текущее направление движения
- `nextDirection`: Следующее направление движения
- `mouthAngle`: Угол открытия рта
- `powerMode`: Флаг активного режима силы
- `powerModeTimer`: Таймер режима силы

### Методы

#### move(map, cellSize)
Обновляет позицию Пакмана в соответствии с текущим направлением и картой.

#### getNextPosition(x, y, direction, map, cellSize)
Возвращает следующую позицию на основе текущей позиции, направления и карты.

#### isValidMove(x, y, map)
Проверяет, является ли движение в позицию (x, y) допустимым.

#### resetPosition()
Сбрасывает позицию Пакмана на начальную.

#### animateMouth()
Анимирует открытие и закрытие рта Пакмана.

#### activatePowerMode(duration)
Активирует режим силы на указанное время (в миллисекундах).

#### updatePowerMode(deltaTime)
Обновляет таймер режима силы.

#### setNextDirection(direction)
Устанавливает следующее направление движения.

## Класс Ghost

### Конструктор
```javascript
new Ghost(x, y, color, name, speed)
```
Создает новый экземпляр призрака.

### Свойства
- `x`: Текущая координата X
- `y`: Текущая координата Y
- `direction`: Текущее направление движения
- `color`: Цвет призрака
- `name`: Имя призрака
- `speed`: Скорость призрака

### Методы

#### move(pacmanX, pacmanY, map, powerMode, cellSize)
Обновляет позицию призрака в соответствии с ИИ и текущим состоянием игры.

#### getNextPosition(x, y, direction, map, cellSize)
Возвращает следующую позицию на основе текущей позиции, направления и карты.

#### isValidMove(x, y, map)
Проверяет, является ли движение в позицию (x, y) допустимым.

#### resetPosition()
Сбрасывает позицию призрака на начальную.

#### getInitialDirection()
Возвращает начальное направление призрака.

#### increaseSpeed(amount)
Увеличивает скорость призрака.

#### resetSpeed()
Сбрасывает скорость призрака к значению по умолчанию.

## Класс GameMap

### Конструктор
```javascript
new GameMap()
```
Создает новый экземпляр игровой карты.

### Свойства
- `map`: Стандартная карта уровня
- `levelMaps`: Массив карт для разных уровней

### Методы

#### getLevelMap(level)
Возвращает карту для указанного уровня.

#### countFood(map)
Подсчитывает количество еды на карте.

## Класс SoundManager

### Конструктор
```javascript
new SoundManager()
```
Создает новый экземпляр менеджера звуков.

### Методы

#### playSound(type)
Воспроизводит звук указанного типа.

#### playBackgroundMusic()
Воспроизводит фоновую музыку.

#### pauseBackgroundMusic()
Ставит фоновую музыку на паузу.

## Класс ParticleManager

### Конструктор
```javascript
new ParticleManager()
```
Создает новый экземпляр менеджера частиц.

### Свойства
- `particles`: Массив активных частиц

### Методы

#### createParticles(x, y, color, count)
Создает новые частицы в позиции (x, y).

#### updateParticles()
Обновляет состояние всех частиц.

#### drawParticles(ctx)
Отрисовывает все частицы на холсте.

#### clearParticles()
Очищает массив частиц.

## Класс FruitManager

### Конструктор
```javascript
new FruitManager()
```
Создает новый экземпляр менеджера фруктов.

### Свойства
- `fruitTypes`: Массив типов фруктов
- `fruitVisible`: Флаг видимости фрукта
- `currentFruit`: Текущий фрукт на карте

### Методы

#### spawnFruit(map, foodCount, totalFood, level)
Создает фрукт на карте при определенных условиях.

#### checkFruitCollection(pacmanX, pacmanY, scoreCallback, particleCallback)
Проверяет, собрал ли Пакман фрукт.

#### drawFruits(ctx, cellSize)
Отрисовывает фрукты на холсте.

#### reset()
Сбрасывает состояние менеджера фруктов.

## Класс AchievementManager

### Конструктор
```javascript
new AchievementManager()
```
Создает новый экземпляр менеджера достижений.

### Свойства
- `achievements`: Массив достижений
- `ghostsEaten`: Количество съеденных призраков
- `fruitsCollected`: Количество собранных фруктов

### Методы

#### checkAchievements(score, level, consecutiveEats)
Проверяет, были ли разблокированы какие-либо достижения.

#### unlockAchievement(id)
Разблокирует достижение по ID.

#### showAchievementNotification(achievement)
Отображает уведомление о разблокированном достижении.

#### incrementGhostsEaten()
Увеличивает счетчик съеденных призраков.

#### incrementFruitsCollected()
Увеличивает счетчик собранных фруктов.

#### getStats()
Возвращает статистику достижений.

#### reset()
Сбрасывает все достижения.

## Класс PacmanGame

### Конструктор
```javascript
new PacmanGame()
```
Создает новый экземпляр игры.

### Свойства
- `pacman`: Экземпляр Пакмана
- `ghosts`: Массив призраков
- `gameMap`: Экземпляр игровой карты
- `soundManager`: Экземпляр менеджера звуков
- `particleManager`: Экземпляр менеджера частиц
- `fruitManager`: Экземпляр менеджера фруктов
- `achievementManager`: Экземпляр менеджера достижений

### Методы

#### start()
Запускает игру.

#### pause()
Ставит игру на паузу.

#### reset()
Сбрасывает игру.

#### handleKey(e)
Обрабатывает нажатия клавиш.

#### update(deltaTime)
Обновляет состояние игры.

#### draw()
Отрисовывает игру на холсте.

#### saveHighScore(score)
Сохраняет рекорд в localStorage.

#### loadHighScores()
Загружает рекорды из localStorage.