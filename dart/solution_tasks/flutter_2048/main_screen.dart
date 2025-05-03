import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:provider/provider.dart';
import 'game2048.dart';

class MainScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final game = Provider.of<Game2048>(context);

    if (game.isGameOver) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        Fluttertoast.showToast(
          msg: "Игра окончена! Счет: ${game.score}",
          toastLength: Toast.LENGTH_LONG,
        );
      });
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('2048'),
        actions: [IconButton(icon: Icon(Icons.refresh), onPressed: game.reset)],
      ),
      body: Column(
        children: [
          Padding(
            padding: EdgeInsets.all(16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Column(
                  children: [
                    Text('Счет', style: TextStyle(fontSize: 16)),
                    Text('${game.score}', style: TextStyle(fontSize: 24)),
                  ],
                ),
                Column(
                  children: [
                    Text('Рекорд', style: TextStyle(fontSize: 16)),
                    Text('${game.bestScore}', style: TextStyle(fontSize: 24)),
                  ],
                ),
              ],
            ),
          ),
          Expanded(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: GestureDetector(
                onVerticalDragEnd: (details) {
                  if (details.primaryVelocity! < 0) {
                    game.move(Direction.up);
                  } else if (details.primaryVelocity! > 0) {
                    game.move(Direction.down);
                  }
                },
                onHorizontalDragEnd: (details) {
                  if (details.primaryVelocity! < 0) {
                    game.move(Direction.left);
                  } else if (details.primaryVelocity! > 0) {
                    game.move(Direction.right);
                  }
                },
                child: GridView.builder(
                  physics: NeverScrollableScrollPhysics(),
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 4,
                    mainAxisSpacing: 8,
                    crossAxisSpacing: 8,
                  ),
                  itemCount: 16,
                  itemBuilder: (context, index) {
                    int x = index ~/ 4;
                    int y = index % 4;
                    int number = game.grid[x][y];
                    return Tile(number: number);
                  },
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class Tile extends StatelessWidget {
  final int number;
  const Tile({required this.number});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: Duration(milliseconds: 150),
      decoration: BoxDecoration(
        color: _getTileColor(number),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Center(
        child: Text(
          number != 0 ? number.toString() : '',
          style: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.bold,
            color: number >= 8 ? Colors.white : Colors.black54,
          ),
        ),
      ),
    );
  }

  Color _getTileColor(int num) {
    Map<int, Color> colors = {
      0: Colors.grey[200]!,
      2: Colors.orange[100]!,
      4: Colors.orange[200]!,
      8: Colors.orange[400]!,
      16: Colors.red[400]!,
      32: Colors.red[600]!,
      64: Colors.purple[400]!,
      128: Colors.purple[600]!,
      256: Colors.blue[400]!,
      512: Colors.blue[600]!,
      1024: Colors.green[400]!,
      2048: Colors.green[600]!,
    };
    return colors[num] ?? Colors.black;
  }
}
