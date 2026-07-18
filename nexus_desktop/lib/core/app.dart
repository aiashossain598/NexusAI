import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../screens/dashboard/dashboard_page.dart';

class NexusApp extends StatelessWidget {
  const NexusApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Nexus AI',
      theme: AppTheme.dark,
      home: const DashboardPage(),
    );
  }
}