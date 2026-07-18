import 'package:flutter/material.dart';

class NexusSidebar extends StatelessWidget {
  const NexusSidebar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 90,
      color: const Color(0xff111827),
      child: Column(
        children: const [
          SizedBox(height: 20),
          Icon(Icons.psychology, size: 36),
          SizedBox(height: 30),
          Icon(Icons.dashboard),
          SizedBox(height: 20),
          Icon(Icons.chat),
          SizedBox(height: 20),
          Icon(Icons.memory),
          SizedBox(height: 20),
          Icon(Icons.folder),
          SizedBox(height: 20),
          Icon(Icons.settings),
        ],
      ),
    );
  }
}