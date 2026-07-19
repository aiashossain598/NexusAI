import 'package:flutter/material.dart';

import 'left_panel.dart';
import 'center_panel.dart';
import 'right_panel.dart';

class DashboardBody extends StatelessWidget {
  const DashboardBody({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(20),
      child: Row(
        children: [
          Expanded(flex: 2, child: LeftPanel()),
          SizedBox(width: 20),
          Expanded(flex: 5, child: CenterPanel()),
          SizedBox(width: 20),
          Expanded(flex: 3, child: RightPanel()),
        ],
      ),
    );
  }
}