import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:provider/provider.dart';
import 'game2048.dart';

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: Duration(milliseconds: 300),
      vsync: this,
    );
    _scaleAnimation = Tween<double>(begin: 1.0, end: 1.1).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

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
                    AnimatedSwitcher(
                      duration: Duration(milliseconds: 300),
                      transitionBuilder: (child, animation) {
                        return ScaleTransition(
                          scale: animation,
                          child: child,
                        );
                      },
                      child: Text(
                        '${game.score}',
                        key: ValueKey<int>(game.score),
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ),
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
                onVerticalDragUpdate: (details) {
                  // Visual feedback during drag
                  if (details.delta.dy.abs() > details.delta.dx.abs()) {
                    if (!_animationController.isAnimating) {
                      _animationController.forward();
                    }
                  }
                },
                onVerticalDragEnd: (details) {
                  _animationController.reverse();
                  if (details.primaryVelocity! < -500) {
                    game.move(Direction.up);
                  } else if (details.primaryVelocity! > 500) {
                    game.move(Direction.down);
                  }
                },
                onHorizontalDragUpdate: (details) {
                  // Visual feedback during drag
                  if (details.delta.dx.abs() > details.delta.dy.abs()) {
                    if (!_animationController.isAnimating) {
                      _animationController.forward();
                    }
                  }
                },
                onHorizontalDragEnd: (details) {
                  _animationController.reverse();
                  if (details.primaryVelocity! < -500) {
                    game.move(Direction.left);
                  } else if (details.primaryVelocity! > 500) {
                    game.move(Direction.right);
                  }
                },
                child: AnimatedBuilder(
                  animation: _scaleAnimation,
                  builder: (context, child) {
                    return Transform.scale(
                      scale: _scaleAnimation.value,
                      child: child,
                    );
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
                      bool isMerged = game.mergedTiles[x][y];
                      return Tile(number: number, isMerged: isMerged);
                    },
                  ),
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
  final bool isMerged;
  
  const Tile({required this.number, this.isMerged = false});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: Duration(milliseconds: isMerged ? 300 : 150),
      curve: isMerged ? Curves.elasticOut : Curves.easeInOut,
      decoration: BoxDecoration(
        color: _getTileColor(number),
        borderRadius: BorderRadius.circular(8),
        boxShadow: isMerged
            ? [
                BoxShadow(
                  color: Colors.black26,
                  blurRadius: 8,
                  offset: Offset(0, 4),
                )
              ]
            : [],
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