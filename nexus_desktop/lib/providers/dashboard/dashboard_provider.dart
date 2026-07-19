import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/system_stats.dart';

final dashboardProvider =
    StateProvider<SystemStats>((ref) => SystemStats.initial());