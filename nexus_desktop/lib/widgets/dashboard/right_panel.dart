import 'package:flutter/material.dart';

class RightPanel extends StatelessWidget {
  const RightPanel({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xff1B1F2A),
        borderRadius: BorderRadius.circular(20),
      ),
      child: const Center(
        child: Text(
          "AI Chat",
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}