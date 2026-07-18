import 'package:flutter/material.dart';
import '../../widgets/sidebar/sidebar.dart';
import '../../widgets/topbar/top_bar.dart';

class DashboardLayout extends StatelessWidget {
  final Widget child;

  const DashboardLayout({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          const NexusSidebar(),
          Expanded(
            child: Column(
              children: [
                const NexusTopBar(),
                Expanded(child: child),
              ],
            ),
          ),
        ],
      ),
    );
  }
}