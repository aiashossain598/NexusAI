import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/chat_message.dart';
import '../../services/chat_service.dart';

class ChatState {
  final List<ChatMessageModel> messages;
  final bool isSending;
  final String? activeConfirmationId;
  final String? errorMessage;

  const ChatState({
    this.messages = const [],
    this.isSending = false,
    this.activeConfirmationId,
    this.errorMessage,
  });

  ChatState copyWith({
    List<ChatMessageModel>? messages,
    bool? isSending,
    String? activeConfirmationId,
    String? errorMessage,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isSending: isSending ?? this.isSending,
      activeConfirmationId: activeConfirmationId,
      errorMessage: errorMessage,
    );
  }
}

class ChatNotifier extends StateNotifier<ChatState> {
  final ChatService _service = ChatService();

  ChatNotifier()
      : super(
          ChatState(
            messages: [
              ChatMessageModel(
                id: 'welcome',
                role: 'assistant',
                content:
                    'Nexus AI ready. Ask a question, request code generation, or ask to inspect files.',
                timestamp: DateTime.now(),
              ),
            ],
          ),
        );

  Future<void> sendMessage(String text) async {
    final trimmed = text.trim();
    if (trimmed.isEmpty) return;

    final userMsg = ChatMessageModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      role: 'user',
      content: trimmed,
      timestamp: DateTime.now(),
    );

    state = state.copyWith(
      messages: [...state.messages, userMsg],
      isSending: true,
      errorMessage: null,
    );

    try {
      final response = await _service.sendMessage(
        instruction: trimmed,
        sessionId: 'desktop',
      );

      final replyText = response['response'] as String? ?? 'Done.';
      final rawEvents = response['events'] as List<dynamic>? ?? [];
      final toolEvents = rawEvents
          .whereType<Map>()
          .map((e) => Map<String, dynamic>.from(e))
          .toList();

      final confirmationId = response['confirmation_id'] as String?;
      final isPending = response['status'] == 'confirmation_required';

      final assistantMsg = ChatMessageModel(
        id: (DateTime.now().millisecondsSinceEpoch + 1).toString(),
        role: 'assistant',
        content: replyText,
        toolEvents: toolEvents,
        confirmationId: confirmationId,
        isPendingConfirmation: isPending,
        timestamp: DateTime.now(),
      );

      state = state.copyWith(
        messages: [...state.messages, assistantMsg],
        isSending: false,
        activeConfirmationId: isPending ? confirmationId : null,
      );
    } catch (e) {
      final errorMsg = ChatMessageModel(
        id: (DateTime.now().millisecondsSinceEpoch + 1).toString(),
        role: 'assistant',
        content:
            'Unable to reach Nexus backend at http://127.0.0.1:8000. Ensure the core server is running.',
        timestamp: DateTime.now(),
      );

      state = state.copyWith(
        messages: [...state.messages, errorMsg],
        isSending: false,
        errorMessage: e.toString(),
      );
    }
  }

  Future<void> handleConfirmation({
    required String confirmationId,
    required bool approved,
  }) async {
    state = state.copyWith(isSending: true);
    try {
      await _service.confirmAction(
        confirmationId: confirmationId,
        approved: approved,
      );

      final updatedMessages = state.messages.map((m) {
        if (m.confirmationId == confirmationId) {
          return m.copyWith(isPendingConfirmation: false);
        }
        return m;
      }).toList();

      state = state.copyWith(
        messages: updatedMessages,
        isSending: false,
        activeConfirmationId: null,
      );

      // Send follow up to execute approved task
      if (approved) {
        await sendMessage('Proceed with approved action.');
      }
    } catch (e) {
      state = state.copyWith(isSending: false, errorMessage: e.toString());
    }
  }

  void clearChat() {
    state = ChatState(
      messages: [
        ChatMessageModel(
          id: 'welcome',
          role: 'assistant',
          content: 'Chat cleared. Nexus AI ready.',
          timestamp: DateTime.now(),
        ),
      ],
    );
  }
}

final chatProvider = StateNotifierProvider<ChatNotifier, ChatState>((ref) {
  return ChatNotifier();
});
