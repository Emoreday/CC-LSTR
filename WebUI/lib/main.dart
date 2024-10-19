import 'package:flutter/material.dart';
import 'package:logic_system/pages/welcome/welcome.dart';
// import 'package:logic_system/pages/page.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Material App',
      // routes: staticRoutes,
      home: WelcomePage(),
    );
  }
}
