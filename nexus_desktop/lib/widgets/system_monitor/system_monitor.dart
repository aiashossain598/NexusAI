import 'package:flutter/material.dart';

class SystemMonitor extends StatelessWidget {
  const SystemMonitor({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: const [
        Expanded(child: _Card(title: 'CPU')),
        SizedBox(width: 16),
        Expanded(child: _Card(title: 'RAM')),
        SizedBox(width: 16),
        Expanded(child: _Card(title: 'GPU')),
      ],
    );
  }
}

class _Card extends StatelessWidget {
  final String title;

  const _Card({required this.title});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 120,
      decoration: BoxDecoration(
        color: const Color(0xFF1B1F2A),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Center(
        child: Text(
          title,
          style: const TextStyle(fontSize: 22),
        ),
      ),
    );
  }
}