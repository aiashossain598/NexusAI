import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

class AnimatedGlow extends StatelessWidget {
  final Widget child;

  const AnimatedGlow({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return child
        .animate(
          onPlay: (controller) => controller.repeat(reverse: true),
        )
        .scale(
          begin: const Offset(.98, .98),
          end: const Offset(1.03, 1.03),
          duration: 1800.ms,
        );
  }
}