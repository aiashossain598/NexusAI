import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/chat_message.dart';
import '../../providers/chat_provider.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text.dart';
import '../../widgets/chat/chat_input_bar.dart';
import '../../widgets/common/glass_container.dart';

class ChatPage extends ConsumerWidget {
  const ChatPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final messages = ref.watch(chatProvider);
    return Column(
      children: [
        Expanded(
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 820),
              child: ListView.separated(
                padding: const EdgeInsets.only(top: 16, bottom: 24),
                itemCount: messages.length,
                separatorBuilder: (_, __) => const SizedBox(height: 24),
                itemBuilder: (_, i) => _Bubble(messages[i]),
              ),
            ),
          ),
        ),
        ChatInputBar(
          hint: 'Message NexusAI...',
          onSend: (t) => ref.read(chatProvider.notifier).send(t),
        ),
      ],
    );
  }
}

class _Bubble extends StatelessWidget {
  final ChatMessage m;
  const _Bubble(this.m);

  @override
  Widget build(BuildContext context) {
    if (m.fromUser) {
      return Align(
        alignment: Alignment.centerRight,
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 560),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: AppColors.gold.withValues(alpha: .12),
              border: Border.all(color: AppColors.gold.withValues(alpha: .3)),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(14),
                bottomLeft: Radius.circular(14),
                bottomRight: Radius.circular(14),
                topRight: Radius.circular(4),
              ),
            ),
            child: Text(m.text, style: AppText.body),
          ),
        ),
      );
    }
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 28,
          height: 28,
          decoration: const BoxDecoration(
            shape: BoxShape.circle,
            gradient: RadialGradient(
              center: Alignment(-.3, -.4),
              colors: [AppColors.goldLight, AppColors.gold, AppColors.violet],
              stops: [0, .4, 1],
            ),
          ),
        ),
        const SizedBox(width: 16),
        Flexible(
          child: GlassContainer(
            radius: 14,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            child: Text(m.text, style: AppText.body),
          ),
        ),
      ],
    );
  }
}
