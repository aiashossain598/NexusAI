import 'package:flutter/material.dart';

import '../../widgets/neural_core/neural_core.dart';
import '../../widgets/system_monitor/system_monitor.dart';
import 'dashboard_layout.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return DashboardLayout(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: const [
            Expanded(
              flex: 5,
              child: NeuralCore(),
            ),
            SizedBox(height: 20),
            Expanded(
              flex: 2,
              child: SystemMonitor(),
            ),
          ],
        ),
      ),
    );
  }
}