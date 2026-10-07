import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../providers/chat_provider.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text.dart';
import '../../widgets/chat/chat_input_bar.dart';
import '../../widgets/common/glass_container.dart';
import '../../widgets/common/nexus_orb.dart';

class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  static const _suggestions = [
    (Icons.event_note_outlined, 'Plan my day', 'Shape priorities into a calm schedule'),
    (Icons.description_outlined, 'Summarize a document', 'Distill any file to what matters'),
    (Icons.mail_outline, 'Write an email', 'Draft in the right tone, any language'),
    (Icons.lightbulb_outline, 'Explain simply', 'Clear answers without jargon'),
  ];

  void _send(BuildContext context, WidgetRef ref, String text) {
    ref.read(chatProvider.notifier).send(text);
    context.go('/chat');
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Center(
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const NexusOrb(size: 220),
            const SizedBox(height: 48),
            Text.rich(TextSpan(children: [
              TextSpan(text: 'Good evening, ', style: AppText.display(40)),
              // TODO(backend-integration): use the signed-in user's first name.
              TextSpan(
                  text: 'Nexus',
                  style: AppText.display(40, color: AppColors.gold)),
            ])),
            const SizedBox(height: 8),
            Text('How can I help you today?', style: AppText.meta.copyWith(fontSize: 15)),
            const SizedBox(height: 32),
            ChatInputBar(
              onSend: (t) => _send(context, ref, t),
              // TODO: open voice mode route.
              onMic: () {},
            ),
            const SizedBox(height: 16),
            ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 760),
              child: Row(
                children: [
                  for (var i = 0; i < _suggestions.length; i++) ...[
                    if (i > 0) const SizedBox(width: 16),
                    Expanded(
                      child: InkWell(
                        borderRadius: BorderRadius.circular(14),
                        onTap: () => _send(context, ref, _suggestions[i].$2),
                        child: GlassContainer(
                          radius: 14,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Icon(_suggestions[i].$1, color: AppColors.gold),
                              const SizedBox(height: 8),
                              Text(_suggestions[i].$2,
                                  style: AppText.meta.copyWith(
                                      color: AppColors.text,
                                      fontWeight: FontWeight.w600,
                                      fontSize: 14)),
                              const SizedBox(height: 4),
                              Text(_suggestions[i].$3,
                                  style: AppText.meta.copyWith(fontSize: 12)),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(height: 32),
            Text('NexusAI can make mistakes. Check important information.',
                style: AppText.caption),
          ],
        ),
      ),
    );
  }
}
