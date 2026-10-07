import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

class NeuralCore extends StatelessWidget {
  const NeuralCore({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xff111827),
        borderRadius: BorderRadius.circular(24),
      ),
      child: Center(
        child: Container(
          width: 280,
          height: 280,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: const RadialGradient(
              colors: [
                Color(0xff9D4DFF),
                Color(0xff3D7EFF),
                Colors.black,
              ],
            ),
            boxShadow: const [
              BoxShadow(
                color: Color(0xff7B61FF),
                blurRadius: 60,
                spreadRadius: 8,
              ),
            ],
          ),
        )
            .animate(onPlay: (c) => c.repeat())
            .scale(
              duration: 2.seconds,
              begin: const Offset(.95, .95),
              end: const Offset(1.05, 1.05),
            ),
      ),
    );
  }
}