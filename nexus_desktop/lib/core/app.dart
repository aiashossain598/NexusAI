import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import 'router.dart';

class NexusApp extends StatelessWidget {
  const NexusApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      debugShowCheckedModeBanner: false,
      title: 'NexusAI',
      theme: AppTheme.dark,
      routerConfig: appRouter,
    );
  }
}
