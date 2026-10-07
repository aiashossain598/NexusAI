import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'app_colors.dart';

class AppTheme {
  static ThemeData dark = ThemeData(
    brightness: Brightness.dark,
    useMaterial3: true,
    scaffoldBackgroundColor: AppColors.background,
    textTheme: GoogleFonts.manropeTextTheme(ThemeData.dark().textTheme)
        .apply(bodyColor: AppColors.text, displayColor: AppColors.text),
    colorScheme: const ColorScheme.dark(
      primary: AppColors.gold,
      secondary: AppColors.platinum,
      surface: AppColors.surface,
      error: AppColors.danger,
    ),
    dividerColor: AppColors.divider,
    focusColor: AppColors.gold,
    iconTheme: const IconThemeData(color: AppColors.platinum, size: 20),
  );
}
