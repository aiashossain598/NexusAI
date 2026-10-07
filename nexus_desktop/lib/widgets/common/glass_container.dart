import 'dart:ui';
import 'package:flutter/material.dart';

import '../../theme/app_colors.dart';

/// Glass surface: 24px blur, 1px gold-tinted border, faint top highlight.
class GlassContainer extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final double radius;
  final bool active;

  const GlassContainer({
    super.key,
    required this.child,
    this.padding,
    this.radius = 20,
    this.active = false,
  });

  @override
  Widget build(BuildContext context) {
    final r = BorderRadius.circular(radius);
    return ClipRRect(
      borderRadius: r,
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 24, sigmaY: 24),
        child: Container(
          padding: padding ?? const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: r,
            color: AppColors.surface.withValues(alpha: .65),
            border: Border.all(
              color: active ? AppColors.borderHover : AppColors.border,
            ),
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.center,
              colors: [
                Colors.white.withValues(alpha: .08),
                Colors.transparent,
              ],
            ),
          ),
          child: child,
        ),
      ),
    );
  }
}
