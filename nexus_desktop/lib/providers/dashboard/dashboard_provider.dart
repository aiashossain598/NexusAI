import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../services/system_service.dart';

final dashboardProvider =
    FutureProvider<Map<String, dynamic>>((ref) async {
  return SystemService().getSystemInfo();
});