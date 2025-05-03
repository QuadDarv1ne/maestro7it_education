import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class Game2048 extends ChangeNotifier {
  static const int _gridSize = 4;
  static const double _newTile2Probability = 0.9;

  List<List<int>> _grid = List.generate(
    _gridSize,
    (_) => List.filled(_gridSize, 0),
  );
  int _score = 0;
  int _bestScore = 0;
  bool _isGameOver = false;
  bool _hasWon = false;

  List<List<int>> get grid => _grid;
  int get score => _score;
  int get bestScore => _bestScore;
  bool get isGameOver => _isGameOver;
  bool get hasWon => _hasWon;

  Game2048() {
    _loadGame();
  }

  Future<void> _loadGame() async {
    final prefs = await SharedPreferences.getInstance();
    _bestScore = prefs.getInt('bestScore') ?? 0;
    _score = prefs.getInt('currentScore') ?? 0;

    final gridData = prefs.getString('grid');
    if (gridData != null) {
      try {
        final List<dynamic> decoded = jsonDecode(gridData);
        _grid = List.generate(
          _gridSize,
          (i) => List.generate(_gridSize, (j) => decoded[i][j] as int),
        );
      } catch (e) {
        _resetGrid();
      }
    } else {
      _resetGrid();
    }
    _checkGameState();
    notifyListeners();
  }

  Future<void> _saveGame() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('bestScore', _bestScore);
    await prefs.setInt('currentScore', _score);
    await prefs.setString('grid', jsonEncode(_grid));
  }

  void _resetGrid() {
    _grid = List.generate(_gridSize, (_) => List.filled(_gridSize, 0));
    _addNewTile();
    _addNewTile();
  }

  void _addNewTile() {
    final emptyCells = <Point>[];
    for (int i = 0; i < _gridSize; i++) {
      for (int j = 0; j < _gridSize; j++) {
        if (_grid[i][j] == 0) emptyCells.add(Point(i, j));
      }
    }

    if (emptyCells.isNotEmpty) {
      final cell = emptyCells[Random().nextInt(emptyCells.length)];
      _grid[cell.x][cell.y] =
          Random().nextDouble() < _newTile2Probability ? 2 : 4;
      _saveGame();
    }
    notifyListeners();
  }

  void _checkGameState() {
    bool hasEmpty = false;
    bool hasPossibleMoves = false;
    _hasWon = false;

    for (int i = 0; i < _gridSize; i++) {
      for (int j = 0; j < _gridSize; j++) {
        if (_grid[i][j] == 2048) _hasWon = true;
        if (_grid[i][j] == 0) hasEmpty = true;

        if (i < _gridSize - 1 && _grid[i][j] == _grid[i + 1][j]) {
          hasPossibleMoves = true;
        }
        if (j < _gridSize - 1 && _grid[i][j] == _grid[i][j + 1]) {
          hasPossibleMoves = true;
        }
      }
    }

    _isGameOver = !hasEmpty && !hasPossibleMoves;
    if (_score > _bestScore) {
      _bestScore = _score;
      _saveGame();
    }
    notifyListeners();
  }

  void move(Direction direction) {
    if (_isGameOver || _hasWon) return;

    final newGrid = List.generate(_gridSize, (_) => List.filled(_gridSize, 0));
    bool moved = false;

    for (int i = 0; i < _gridSize; i++) {
      final List<int> row = _getRow(direction, i);
      final List<int> mergedRow = _mergeRow(row);

      if (row.toString() != mergedRow.toString()) {
        moved = true;
      }

      _updateGrid(direction, i, mergedRow, newGrid);
    }

    if (moved) {
      _grid = newGrid;
      _addNewTile();
      _checkGameState();
    }
  }

  List<int> _getRow(Direction direction, int index) {
    switch (direction) {
      case Direction.up:
        return [for (int j = 0; j < _gridSize; j++) _grid[j][index]];
      case Direction.down:
        return [for (int j = _gridSize - 1; j >= 0; j--) _grid[j][index]];
      case Direction.left:
        return _grid[index];
      case Direction.right:
        return _grid[index].reversed.toList();
    }
  }

  void _updateGrid(
    Direction direction,
    int index,
    List<int> mergedRow,
    List<List<int>> newGrid,
  ) {
    switch (direction) {
      case Direction.up:
        for (int j = 0; j < _gridSize; j++) {
          newGrid[j][index] = mergedRow[j];
        }
        break;
      case Direction.down:
        for (int j = 0; j < _gridSize; j++) {
          newGrid[_gridSize - 1 - j][index] = mergedRow[j];
        }
        break;
      case Direction.left:
        newGrid[index] = mergedRow;
        break;
      case Direction.right:
        newGrid[index] = mergedRow.reversed.toList();
        break;
    }
  }

  List<int> _mergeRow(List<int> row) {
    final nonZero = row.where((num) => num != 0).toList();
    final merged = <int>[];
    bool skipNext = false;

    for (int i = 0; i < nonZero.length; i++) {
      if (skipNext) {
        skipNext = false;
        continue;
      }

      if (i < nonZero.length - 1 && nonZero[i] == nonZero[i + 1]) {
        merged.add(nonZero[i] * 2);
        _score += nonZero[i] * 2;
        skipNext = true;
      } else {
        merged.add(nonZero[i]);
      }
    }

    return merged..addAll(List.filled(_gridSize - merged.length, 0));
  }

  void reset() {
    _grid = List.generate(_gridSize, (_) => List.filled(_gridSize, 0));
    _score = 0;
    _isGameOver = false;
    _hasWon = false;
    _addNewTile();
    _addNewTile();
    notifyListeners();
  }
}

enum Direction { up, down, left, right }

class Point {
  final int x;
  final int y;

  const Point(this.x, this.y);
}
