import 'package:flutter/material.dart';

class NeuralCore extends StatelessWidget {
  const NeuralCore({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF1B1F2A),
        borderRadius: BorderRadius.circular(20),
      ),
      child: const Center(
        child: Text(
          'Neural Core',
          style: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}