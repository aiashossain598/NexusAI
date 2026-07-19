class SystemStats {
  final int cpu;
  final int ram;
  final int gpu;

  const SystemStats({
    required this.cpu,
    required this.ram,
    required this.gpu,
  });

  factory SystemStats.initial() {
    return const SystemStats(
      cpu: 23,
      ram: 61,
      gpu: 38,
    );
  }
}