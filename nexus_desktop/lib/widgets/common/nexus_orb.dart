import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../../theme/app_colors.dart';

/// The living orb: gold core, violet rim, soft bloom, slow breathing.
class NexusOrb extends StatelessWidget {
  final double size;
  final bool breathe;

  const NexusOrb({super.key, this.size = 220, this.breathe = true});

  @override
  Widget build(BuildContext context) {
    final orb = Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: const RadialGradient(
          center: Alignment(-.3, -.4),
          radius: .95,
          colors: [AppColors.goldLight, AppColors.gold, AppColors.violet],
          stops: [0, .38, 1],
        ),
        boxShadow: [
          BoxShadow(
            color: AppColors.gold.withValues(alpha: .30),
            blurRadius: size * .5,
            spreadRadius: size * .04,
          ),
          BoxShadow(
            color: AppColors.violet.withValues(alpha: .25),
            blurRadius: size * .3,
          ),
        ],
      ),
    );
    if (!breathe) return orb;
    return orb
        .animate(onPlay: (c) => c.repeat(reverse: true))
        .scale(
          begin: const Offset(1, 1),
          end: const Offset(1.04, 1.04),
          duration: 4.seconds,
          curve: Curves.easeInOut,
        );
  }
}
