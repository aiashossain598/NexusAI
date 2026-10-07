import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../providers/dashboard/dashboard_provider.dart';

class SystemMonitor extends ConsumerWidget {
  const SystemMonitor({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final system = ref.watch(dashboardProvider);

    return system.when(
      loading: () => const Center(
        child: CircularProgressIndicator(),
      ),

      error: (error, _) => Center(
        child: Text(
          "Backend Offline\n$error",
          textAlign: TextAlign.center,
        ),
      ),

      data: (data) {
        return Row(
          children: [
            Expanded(
              child: _Card(
                title: "CPU",
                value: "${data["cpu"]}%",
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _Card(
                title: "RAM",
                value: "${data["ram"]}%",
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: _Card(
                title: "GPU",
                value: "${data["gpu"]}%",
              ),
            ),
          ],
        );
      },
    );
  }
}

class _Card extends StatelessWidget {
  final String title;
  final String value;

  const _Card({
    required this.title,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 120,
      decoration: BoxDecoration(
        color: const Color(0xFF1B1F2A),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              title,
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 8),
            Text(
              value,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Colors.cyanAccent,
              ),
            ),
          ],
        ),
      ),
    );
  }
}