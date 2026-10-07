import 'package:flutter/material.dart';

/// NexusAI "quiet luxury" palette: obsidian + champagne gold.
class AppColors {
  // Backgrounds
  static const background = Color(0xff0A0A0F);
  static const midnight = Color(0xff11121A);
  static const glowTop = Color(0xff1A1B2E);
  static const surface = Color(0xff171826); // use at 60-70% opacity for glass

  // Gold accent
  static const gold = Color(0xffD4AF37);
  static const goldLight = Color(0xffF2D98B);
  static const goldDeep = Color(0xffA8841F);
  static const bronze = Color(0xff8C6B1F);

  // Secondary
  static const platinum = Color(0xffC9CCD6);
  static const violet = Color(0xff7B6CF6); // orb only

  // Text
  static const text = Color(0xffF5F1E6);
  static const textSecondary = Color(0xffA8A9B8);
  static const textMuted = Color(0xff6B6C7D);

  // Status
  static const success = Color(0xff4FBF9F);
  static const warning = Color(0xffE0A84A);
  static const danger = Color(0xffD96C7A);

  // Lines
  static final border = gold.withValues(alpha: .18);
  static final borderHover = gold.withValues(alpha: .40);
  static final divider = Colors.white.withValues(alpha: .06);

  static const goldGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [goldLight, gold, goldDeep],
  );
}
