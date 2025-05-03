import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'game2048.dart';
import 'main_screen.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => Game2048(),
      child: MaterialApp(
        title: '2048',
        theme: ThemeData(primarySwatch: Colors.orange),
        home: MainScreen(),
      ),
    ),
  );
}
