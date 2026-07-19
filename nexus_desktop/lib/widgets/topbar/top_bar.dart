import 'package:flutter/material.dart';

import 'profile_card.dart';
import 'status_card.dart';

class NexusTopBar extends StatelessWidget {
  const NexusTopBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 90,
      padding: const EdgeInsets.all(16),
      child: const Row(
        children: [
          StatusCard(title: "CPU", value: "23%"),
          SizedBox(width: 16),
          StatusCard(title: "RAM", value: "61%"),
          SizedBox(width: 16),
          StatusCard(title: "GPU", value: "38%"),
          Spacer(),
          ProfileCard(),
        ],
      ),
    );
  }
}