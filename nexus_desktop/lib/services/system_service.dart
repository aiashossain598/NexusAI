import 'package:dio/dio.dart';

import '../config/api.dart';

class SystemService {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: ApiConfig.baseUrl,
      connectTimeout: const Duration(seconds: 5),
      receiveTimeout: const Duration(seconds: 5),
    ),
  );

  Future<Map<String, dynamic>> getSystemInfo() async {
    final response = await _dio.get("/system");

    return Map<String, dynamic>.from(response.data);
  }
}