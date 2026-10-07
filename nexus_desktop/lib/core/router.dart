import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../screens/chat/chat_page.dart';
import '../screens/home/home_page.dart';
import '../screens/shell/app_shell.dart';

CustomTransitionPage<void> _page(GoRouterState s, Widget w) =>
    CustomTransitionPage<void>(
      key: s.pageKey,
      child: w,
      transitionDuration: const Duration(milliseconds: 250),
      transitionsBuilder: (context, anim, _, child) {
        final c = CurvedAnimation(parent: anim, curve: Curves.easeOut);
        return FadeTransition(
          opacity: c,
          child: SlideTransition(
            position: Tween(begin: const Offset(0, .01), end: Offset.zero)
                .animate(c),
            child: child,
          ),
        );
      },
    );

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    ShellRoute(
      builder: (context, state, child) => AppShell(child: child),
      routes: [
        GoRoute(path: '/', pageBuilder: (c, s) => _page(s, const HomePage())),
        GoRoute(path: '/chat', pageBuilder: (c, s) => _page(s, const ChatPage())),
      ],
    ),
  ],
);
