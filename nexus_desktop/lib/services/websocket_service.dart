import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

import '../config/api.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  final _messageController =
      StreamController<Map<String, dynamic>>.broadcast();

  Stream<Map<String, dynamic>> get stream => _messageController.stream;
  bool get isConnected => _channel != null;

  void connect() {
    if (_channel != null) return;

    try {
      final uri = Uri.parse(ApiConfig.websocket);
      _channel = WebSocketChannel.connect(uri);

      _subscription = _channel!.stream.listen(
        (dynamic raw) {
          try {
            final parsed = jsonDecode(raw.toString());
            if (parsed is Map<String, dynamic>) {
              _messageController.add(parsed);
            }
          } catch (_) {}
        },
        onError: (dynamic error) {
          disconnect();
        },
        onDone: () {
          disconnect();
        },
      );
    } catch (_) {
      disconnect();
    }
  }

  void sendChat(String instruction, {String sessionId = 'desktop'}) {
    if (_channel == null) {
      connect();
    }
    final payload = jsonEncode({
      'type': 'chat',
      'instruction': instruction,
      'session_id': sessionId,
    });
    _channel?.sink.add(payload);
  }

  void sendConfirmation(String confirmationId, bool approved) {
    if (_channel == null) return;
    final payload = jsonEncode({
      'type': 'confirm',
      'confirmation_id': confirmationId,
      'approved': approved,
    });
    _channel?.sink.add(payload);
  }

  void disconnect() {
    _subscription?.cancel();
    _subscription = null;
    _channel?.sink.close();
    _channel = null;
  }

  void dispose() {
    disconnect();
    _messageController.close();
  }
}
