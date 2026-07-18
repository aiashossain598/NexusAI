import 'package:flutter/material.dart';

class NexusTopBar extends StatelessWidget {
  const NexusTopBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70,
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: const Row(
        children: [
          Text(
            "NEXUS AI",
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          Spacer(),
          Text("CPU"),
          SizedBox(width: 20),
          Text("RAM"),
          SizedBox(width: 20),
          Text("GPU"),
        ],
      ),
    );
  }
}