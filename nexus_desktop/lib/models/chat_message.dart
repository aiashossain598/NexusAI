class ChatMessageModel {
  final String id;
  final String role;
  final String content;
  final List<Map<String, dynamic>> toolEvents;
  final String? confirmationId;
  final bool isPendingConfirmation;
  final DateTime timestamp;

  const ChatMessageModel({
    required this.id,
    required this.role,
    required this.content,
    this.toolEvents = const [],
    this.confirmationId,
    this.isPendingConfirmation = false,
    required this.timestamp,
  });

  ChatMessageModel copyWith({
    String? id,
    String? role,
    String? content,
    List<Map<String, dynamic>>? toolEvents,
    String? confirmationId,
    bool? isPendingConfirmation,
    DateTime? timestamp,
  }) {
    return ChatMessageModel(
      id: id ?? this.id,
      role: role ?? this.role,
      content: content ?? this.content,
      toolEvents: toolEvents ?? this.toolEvents,
      confirmationId: confirmationId ?? this.confirmationId,
      isPendingConfirmation:
          isPendingConfirmation ?? this.isPendingConfirmation,
      timestamp: timestamp ?? this.timestamp,
    );
  }
}
