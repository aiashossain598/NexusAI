import 'package:flutter/material.dart';

import '../neural_core/neural_core.dart';

class CenterPanel extends StatelessWidget {
  const CenterPanel({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: const [
        Expanded(
          flex: 7,
          child: NeuralCore(),
        ),
        SizedBox(height: 20),
        Expanded(
          flex: 2,
          child: Row(
            children: [
              Expanded(child: _Feature("Vision")),
              SizedBox(width: 16),
              Expanded(child: _Feature("Browser")),
              SizedBox(width: 16),
              Expanded(child: _Feature("Terminal")),
            ],
          ),
        ),
      ],
    );
  }
}

class _Feature extends StatelessWidget {
  final String title;

  const _Feature(this.title);

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xff1B1F2A),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Center(
        child: Text(
          title,
          style: const TextStyle(fontSize: 20),
        ),
      ),
    );
  }
}