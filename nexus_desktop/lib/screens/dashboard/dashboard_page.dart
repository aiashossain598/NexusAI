import 'package:flutter/material.dart';
import '../../widgets/dashboard/dashboard_body.dart';
import 'dashboard_layout.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return const DashboardLayout(
      child: DashboardBody(),
    );
  }
}