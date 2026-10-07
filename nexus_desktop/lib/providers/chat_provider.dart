import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/chat_message.dart';

class ChatNotifier extends StateNotifier<List<ChatMessage>> {
  ChatNotifier() : super(const []);

  void send(String text) {
    final t = text.trim();
    if (t.isEmpty) return;
    state = [...state, ChatMessage(t, fromUser: true)];
    // TODO(backend-integration): send via ChatService / websocket and
    // append the streamed AI reply. Placeholder reply for UI only.
    state = [
      ...state,
      const ChatMessage('Connect the chat service to see real replies.',
          fromUser: false),
    ];
  }
}

final chatProvider =
    StateNotifierProvider<ChatNotifier, List<ChatMessage>>((ref) => ChatNotifier());
