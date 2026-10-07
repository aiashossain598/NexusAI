import 'package:flutter/material.dart';

import '../../theme/app_colors.dart';
import '../../theme/app_text.dart';
import '../common/glass_container.dart';

class ChatInputBar extends StatefulWidget {
  final ValueChanged<String> onSend;
  final String hint;
  final VoidCallback? onMic;

  const ChatInputBar({
    super.key,
    required this.onSend,
    this.hint = 'Ask NexusAI anything...',
    this.onMic,
  });

  @override
  State<ChatInputBar> createState() => _ChatInputBarState();
}

class _ChatInputBarState extends State<ChatInputBar> {
  final _c = TextEditingController();
  final _focus = FocusNode();

  @override
  void initState() {
    super.initState();
    _focus.addListener(() => setState(() {}));
  }

  @override
  void dispose() {
    _c.dispose();
    _focus.dispose();
    super.dispose();
  }

  void _submit() {
    final t = _c.text;
    if (t.trim().isEmpty) return;
    widget.onSend(t);
    _c.clear();
  }

  @override
  Widget build(BuildContext context) {
    return ConstrainedBox(
      constraints: const BoxConstraints(maxWidth: 760),
      child: SizedBox(
        height: 64,
        child: GlassContainer(
          active: _focus.hasFocus,
          padding: const EdgeInsets.fromLTRB(24, 0, 12, 0),
          child: Row(children: [
            const Icon(Icons.attach_file),
            const SizedBox(width: 16),
            Expanded(
              child: TextField(
                controller: _c,
                focusNode: _focus,
                onSubmitted: (_) => _submit(),
                style: AppText.body,
                cursorColor: AppColors.gold,
                decoration: InputDecoration(
                  border: InputBorder.none,
                  hintText: widget.hint,
                  hintStyle: AppText.body.copyWith(color: AppColors.textMuted),
                ),
              ),
            ),
            IconButton(
              onPressed: widget.onMic,
              icon: const Icon(Icons.mic_none),
            ),
            const SizedBox(width: 8),
            InkWell(
              customBorder: const CircleBorder(),
              onTap: _submit,
              child: Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: AppColors.goldGradient,
                  boxShadow: [
                    BoxShadow(
                        color: AppColors.gold.withValues(alpha: .25),
                        blurRadius: 24),
                  ],
                ),
                child: const Icon(Icons.arrow_upward,
                    size: 20, color: AppColors.background),
              ),
            ),
          ]),
        ),
      ),
    );
  }
}
