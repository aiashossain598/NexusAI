import platform
import psutil

try:
    import GPUtil
except ImportError:
    GPUtil = None


class SystemService:

    @staticmethod
    def get_system_info():

        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        gpu_name = "Not Detected"
        gpu_load = 0

        if GPUtil:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_name = gpus[0].name
                gpu_load = round(gpus[0].load * 100)

        battery = psutil.sensors_battery()

        return {
            "os": platform.system(),
            "release": platform.release(),
            "processor": platform.processor(),

            "cpu": round(psutil.cpu_percent()),

            "ram": round(memory.percent),

            "disk": round(disk.percent),

            "gpu": gpu_load,

            "gpu_name": gpu_name,

            "battery": None if battery is None else battery.percent,
        }