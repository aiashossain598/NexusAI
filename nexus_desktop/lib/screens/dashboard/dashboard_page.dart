import 'package:flutter/material.dart';
import 'dashboard_layout.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return DashboardLayout(
      child: Center(
        child: Text(
          "Dashboard",
          style: Theme.of(context).textTheme.headlineMedium,
        ),
      ),
    );
  }
}