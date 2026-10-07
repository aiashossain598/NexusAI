import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../theme/app_colors.dart';
import '../../theme/app_text.dart';
import '../common/glass_container.dart';
import 'sidebar_item.dart';

class NexusSidebar extends StatelessWidget {
  const NexusSidebar({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 260,
      child: GlassContainer(
        padding: const EdgeInsets.fromLTRB(16, 24, 16, 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(children: [
              Container(
                width: 16,
                height: 16,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: const RadialGradient(
                    center: Alignment(-.3, -.4),
                    colors: [
                      AppColors.goldLight,
                      AppColors.gold,
                      AppColors.bronze
                    ],
                  ),
                  boxShadow: [
                    BoxShadow(
                        color: AppColors.gold.withValues(alpha: .5),
                        blurRadius: 16),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              Text('NexusAI', style: AppText.display(24)),
            ]),
            const SizedBox(height: 24),
            _NewChatButton(onTap: () => context.go('/')),
            const SizedBox(height: 16),
            const _SearchField(),
            const SizedBox(height: 24),
            Text('TODAY', style: AppText.caption),
            const SizedBox(height: 8),
            // TODO(backend-integration): bind to real conversation history.
            const SidebarItem(title: 'Plan my week ahead', active: true),
            const SidebarItem(title: 'Draft reply to landlord'),
            const SizedBox(height: 16),
            Text('YESTERDAY', style: AppText.caption),
            const SizedBox(height: 8),
            const SidebarItem(title: 'Explain vector databases'),
            const Spacer(),
            const _ProfileCard(),
          ],
        ),
      ),
    );
  }
}

class _NewChatButton extends StatelessWidget {
  final VoidCallback onTap;
  const _NewChatButton({required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(10),
      onTap: onTap,
      child: Container(
        height: 40,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        decoration: BoxDecoration(
          gradient: AppColors.goldGradient,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(children: [
              const Icon(Icons.add, size: 18, color: AppColors.background),
              const SizedBox(width: 8),
              Text('New chat',
                  style: AppText.meta.copyWith(
                      color: AppColors.background,
                      fontWeight: FontWeight.w600,
                      fontSize: 14)),
            ]),
            Text('Ctrl+N',
                style: AppText.caption
                    .copyWith(color: AppColors.background.withValues(alpha: .7))),
          ],
        ),
      ),
    );
  }
}

class _SearchField extends StatelessWidget {
  const _SearchField();

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 40,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        color: Colors.white.withValues(alpha: .03),
        border: Border.all(color: AppColors.divider),
      ),
      child: Row(children: [
        const Icon(Icons.search, size: 18),
        const SizedBox(width: 8),
        Expanded(child: Text('Search', style: AppText.meta)),
        Text('Ctrl+K', style: AppText.caption),
      ]),
    );
  }
}

class _ProfileCard extends StatelessWidget {
  const _ProfileCard();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.divider),
      ),
      child: Row(children: [
        Container(
          width: 32,
          height: 32,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: AppColors.surface,
            border: Border.all(color: AppColors.borderHover),
          ),
          child: Text('N',
              style: AppText.meta.copyWith(color: AppColors.gold)),
        ),
        const SizedBox(width: 8),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Nexus User', style: AppText.meta.copyWith(color: AppColors.text)),
              Text('Private plan', style: AppText.caption),
            ],
          ),
        ),
        const Icon(Icons.settings_outlined),
      ]),
    );
  }
}
