import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'app_colors.dart';

class AppText {
  /// Bangla glyphs are taller; keep these fallbacks + height 1.6.
  static List<String> get bnFallback => [
        GoogleFonts.hindSiliguri().fontFamily!,
        GoogleFonts.notoSansBengali().fontFamily!,
      ];

  static TextStyle display(double size, {Color color = AppColors.text}) =>
      GoogleFonts.cormorantGaramond(
        fontSize: size,
        fontWeight: FontWeight.w500,
        color: color,
        height: 1.2,
      ).copyWith(fontFamilyFallback: bnFallback);

  static TextStyle heading = GoogleFonts.manrope(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: AppColors.text,
  );

  static TextStyle body = GoogleFonts.manrope(
    fontSize: 15,
    height: 1.6,
    color: AppColors.text,
  ).copyWith(fontFamilyFallback: bnFallback);

  static TextStyle meta = GoogleFonts.manrope(
    fontSize: 13,
    color: AppColors.textSecondary,
  ).copyWith(fontFamilyFallback: bnFallback);

  static TextStyle caption = GoogleFonts.manrope(
    fontSize: 11,
    letterSpacing: .44,
    color: AppColors.textMuted,
  );

  static TextStyle code = GoogleFonts.jetBrainsMono(
    fontSize: 13,
    height: 1.6,
    color: AppColors.platinum,
  );
}
