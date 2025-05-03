import 'dart:math';
import 'package:flutter/material.dart';

class Game2048 extends ChangeNotifier {
  List<List<int>> grid = List.generate(4, (_) => List.filled(4, 0));
  int score = 0;
  int bestScore = 0;
  bool isGameOver = false;

  Game2048() {
    _loadBestScore();
    _addNewTile();
    _addNewTile();
  }

  // Загрузка рекорда
  Future<void> _loadBestScore() async {
    final prefs = await SharedPreferences.getInstance();
    bestScore = prefs.getInt('bestScore') ?? 0;
    notifyListeners();
  }

  // Сохранение рекорда
  Future<void> _saveBestScore() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('bestScore', bestScore);
  }

  // Добавление новой плитки
  void _addNewTile() {
    List<Point> emptyCells = [];
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        if (grid[i][j] == 0) emptyCells.add(Point(i, j));
      }
    }
    if (emptyCells.isNotEmpty) {
      final cell = emptyCells[Random().nextInt(emptyCells.length)];
      grid[cell.x][cell.y] = Random().nextDouble() < 0.9 ? 2 : 4;
    }
    notifyListeners();
  }

  // Проверка на конец игры
  void _checkGameOver() {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
        if (grid[i][j] == 0) return;
        if (i < 3 && grid[i][j] == grid[i + 1][j]) return;
        if (j < 3 && grid[i][j] == grid[i][j + 1]) return;
      }
    }
    isGameOver = true;
    if (score > bestScore) {
      bestScore = score;
      _saveBestScore();
    }
    notifyListeners();
  }

  // Обработка свайпа
  void move(Direction direction) {
    if (isGameOver) return;

    List<List<int>> newGrid = List.generate(4, (_) => List.filled(4, 0));
    bool moved = false;

    for (int i = 0; i < 4; i++) {
      List<int> row = [];
      for (int j = 0; j < 4; j++) {
        switch (direction) {
          case Direction.up:
            row.add(grid[j][i]);
            break;
          case Direction.down:
            row.add(grid[3 - j][i]);
            break;
          case Direction.left:
            row.add(grid[i][j]);
            break;
          case Direction.right:
            row.add(grid[i][3 - j]);
            break;
        }
      }

      List<int> merged = _merge(row);
      for (int j = 0; j < 4; j++) {
        int val = (j < merged.length) ? merged[j] : 0;
        switch (direction) {
          case Direction.up:
            newGrid[j][i] = val;
            break;
          case Direction.down:
            newGrid[3 - j][i] = val;
            break;
          case Direction.left:
            newGrid[i][j] = val;
            break;
          case Direction.right:
            newGrid[i][3 - j] = val;
            break;
        }
      }

      if (row.toString() != merged.toString()) moved = true;
    }

    if (moved) {
      grid = newGrid;
      _addNewTile();
      _checkGameOver();
    }
  }

  // Логика слияния плиток
  List<int> _merge(List<int> row) {
    List<int> nonZero = row.where((num) => num != 0).toList();
    for (int i = 0; i < nonZero.length - 1; i++) {
      if (nonZero[i] == nonZero[i + 1]) {
        nonZero[i] *= 2;
        score += nonZero[i];
        nonZero.removeAt(i + 1);
        nonZero.add(0);
      }
    }
    return nonZero..addAll(List.filled(4 - nonZero.length, 0));
  }

  // Сброс игры
  void reset() {
    grid = List.generate(4, (_) => List.filled(4, 0));
    score = 0;
    isGameOver = false;
    _addNewTile();
    _addNewTile();
    notifyListeners();
  }
}

enum Direction { up, down, left, right }

class Point {
  int x, y;
  Point(this.x, this.y);
}

Future<void> saveGame() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setInt('score', score);
  await prefs.setString('grid', jsonEncode(grid));
}

Future<void> loadGame() async {
  final prefs = await SharedPreferences.getInstance();
  score = prefs.getInt('score') ?? 0;
  final gridData = jsonDecode(prefs.getString('grid') ?? '[]');
  grid = List.generate(4, (i) => List.generate(4, (j) => gridData[i][j]));
  notifyListeners();
}
