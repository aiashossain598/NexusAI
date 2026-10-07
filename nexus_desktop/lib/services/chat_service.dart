import 'package:dio/dio.dart';

import '../config/api.dart';

class ChatService {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: ApiConfig.baseUrl,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 60),
      headers: {
        'Content-Type': 'application/json',
      },
    ),
  );

  Future<Map<String, dynamic>> sendMessage({
    required String instruction,
    String sessionId = 'desktop',
    String? confirmationId,
  }) async {
    final data = <String, dynamic>{
      'instruction': instruction,
      'session_id': sessionId,
    };
    if (confirmationId != null) {
      data['confirmation_id'] = confirmationId;
    }
    final response = await _dio.post(
      '/api/chat/',
      data: data,
    );
    return Map<String, dynamic>.from(response.data);
  }

  Future<Map<String, dynamic>> confirmAction({
    required String confirmationId,
    required bool approved,
  }) async {
    final response = await _dio.post(
      '/api/chat/confirm',
      data: {
        'confirmation_id': confirmationId,
        'approved': approved,
      },
    );
    return Map<String, dynamic>.from(response.data);
  }

  Future<List<Map<String, dynamic>>> getHistory(String sessionId) async {
    final response = await _dio.get('/api/chat/history/$sessionId');
    final data = Map<String, dynamic>.from(response.data);
    final rawList = data['messages'] as List<dynamic>? ?? [];
    return rawList.map((e) => Map<String, dynamic>.from(e as Map)).toList();
  }
}
