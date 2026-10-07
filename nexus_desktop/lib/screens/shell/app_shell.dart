import 'package:flutter/material.dart';

import '../../theme/app_colors.dart';
import '../../widgets/sidebar/sidebar.dart';
import '../../widgets/titlebar/title_bar.dart';

/// Window chrome shared by all main screens: title bar + sidebar + content.
class AppShell extends StatelessWidget {
  final Widget child;
  const AppShell({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: RadialGradient(
            center: Alignment(0, -1),
            radius: 1.3,
            colors: [AppColors.glowTop, AppColors.background],
            stops: [0, .7],
          ),
        ),
        child: Column(
          children: [
            const NexusTitleBar(),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(24, 0, 24, 24),
                child: Row(
                  children: [
                    const NexusSidebar(),
                    const SizedBox(width: 24),
                    Expanded(child: child),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
