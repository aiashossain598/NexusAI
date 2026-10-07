import 'package:flutter/material.dart';

import '../../theme/app_colors.dart';
import '../../theme/app_text.dart';

/// Conversation history row: one line, ellipsis, gold-tinted when active.
class SidebarItem extends StatelessWidget {
  final String title;
  final bool active;
  final VoidCallback? onTap;

  const SidebarItem({
    super.key,
    required this.title,
    this.active = false,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(10),
      onTap: onTap ?? () {},
      child: Container(
        height: 40,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        alignment: Alignment.centerLeft,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: active ? AppColors.gold.withValues(alpha: .10) : null,
          border: active
              ? const Border(left: BorderSide(color: AppColors.gold, width: 2))
              : null,
        ),
        child: Text(
          title,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: AppText.meta.copyWith(
            fontSize: 14,
            color: active ? AppColors.text : AppColors.textSecondary,
          ),
        ),
      ),
    );
  }
}
