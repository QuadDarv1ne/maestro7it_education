import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'game2048.dart';
import 'main_screen.dart';

void main() {
  // Add performance optimizations
  WidgetsFlutterBinding.ensureInitialized();
  
  // Lock orientation to portrait for better gaming experience
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  
  runApp(
    MyApp(),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => Game2048(),
      child: MaterialApp(
        title: '2048',
        theme: ThemeData(
          primarySwatch: Colors.orange,
          // Add performance enhancements
          visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
        home: MainScreen(),
        debugShowCheckedModeBanner: false, // Remove debug banner for smoother experience
      ),
    );
  }
}