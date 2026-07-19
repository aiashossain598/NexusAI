import 'package:flutter/material.dart';
import 'sidebar_item.dart';

class NexusSidebar extends StatelessWidget {
  const NexusSidebar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 240,
      color: const Color(0xFF111827),
      padding: const EdgeInsets.symmetric(vertical: 20),
      child: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 20),
            child: Text(
              "Nexus AI",
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          SizedBox(height: 30),
          SidebarItem(icon: Icons.chat_bubble_outline, title: "Chat"),
          SidebarItem(icon: Icons.memory, title: "Memory"),
          SidebarItem(icon: Icons.smart_toy_outlined, title: "Agents"),
          SidebarItem(icon: Icons.folder_open, title: "Files"),
          SidebarItem(icon: Icons.language, title: "Internet"),
          SidebarItem(icon: Icons.settings, title: "Settings"),
        ],
      ),
    );
  }
}