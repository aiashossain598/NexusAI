import 'package:flutter/material.dart';
import 'package:glassmorphism/glassmorphism.dart';

class GlassCard extends StatelessWidget {
  final Widget child;

  const GlassCard({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return GlassmorphicContainer(
      width: double.infinity,
      height: double.infinity,
      borderRadius: 24,
      blur: 20,
      border: 1,
      linearGradient: LinearGradient(
        colors: [
          Colors.white.withValues(alpha: .08),
          Colors.white.withValues(alpha: .02),
        ],
      ),
      borderGradient: LinearGradient(
        colors: [
          Colors.blue.withValues(alpha: .4),
          Colors.purple.withValues(alpha: .4),
        ],
      ),
      child: child,
    );
  }
}