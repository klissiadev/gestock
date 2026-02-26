import platform
import psutil
import time

if platform.system() == "Windows":
    try:
        import wmi
    except ImportError:
        wmi = None
else:
    wmi = None

class HardwareMonitor:
    def __init__(self):
        self.os = platform.system()
        self._wmi_conn = None
        
        # Aviso se o sistema operacional não for Windows
        if self.os != "Windows":
            print("\n" + "!"*60)
            print("AVISO: Monitoramento de GPU AMD/Intel não é suportada no Linux.")
            print("Apenas métricas de CPU, RAM e o monitoramento de Placas NVIDIA funcionarão.")
            print("!"*60 + "\n")
        
        # WMI: Se for windows e tiver importado
        if self.os == "Windows" and wmi is not None:
            try:
                self._wmi_conn = wmi.WMI(namespace="root\\CIMV2")
            except Exception as e:
                print(f"Erro ao iniciar WMI: {e}")

        self.gpu_type = self._detect_gpu_type()
        print(f"Monitor iniciado | SO: {self.os} | GPU Alvo: {self.gpu_type.upper()}")
        
    def _detect_gpu_type(self):
        try:
            import GPUtil
            if GPUtil.getGPUs():
                return "nvidia"
        except:
            pass
        return "amd_or_intel"
    
    def _get_nvidia_metrics(self):
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return {
                    "name": gpu.name,
                    "usage": gpu.load * 100,
                    "vram_used_mb": gpu.memoryUsed,
                    "vram_total_mb": gpu.memoryTotal,
                    "temp": gpu.temperature
                }
        except:
            pass
        return None
        
    def _get_wmi_metrics(self):
        """ Fallback para WMI se houver GPU AMD ou Intel
            Caso seja Linux: Ele vai falar que está indisponivel e sempre mostrar uso ZERO
        """
        if self.os != "Windows" or self._wmi_conn is None:
            return {"name": "Indisponível (Non-Windows)", "usage": 0}

        try:
            usage_query = "SELECT UtilizationPercentage FROM Win32_PerfFormattedData_GPUPerformanceCounters_GPUEngine WHERE Name LIKE '%3D%'"
            mem_query = "SELECT Name, DedicatedUsage FROM Win32_PerfFormattedData_GPUPerformanceCounters_GPUAdapterMemory"
            
            usage_res = self._wmi_conn.query(usage_query)
            mem_res = self._wmi_conn.query(mem_query)

            usage = max([int(r.UtilizationPercentage) for r in usage_res]) if usage_res else 0
            vram = max([int(r.DedicatedUsage) for r in mem_res]) if mem_res else 0
            
            name = "GPU Genérica (WMI)"
            try:
                name = self._wmi_conn.Win32_VideoController()[0].Name
            except: pass

            return {
                "name": name,
                "usage": usage,
                "vram_used_mb": round(vram / (1024**2), 2),
                "vram_total_mb": "N/A",
                "temp": "N/A"
            }
        except:
            return "Erro na coleta WMI"
        
    def _get_uptime(self):
        try:
            # Quando o sistema ligou - O tempo agora
            boot_time_timestamp = psutil.boot_time()
            uptime_seconds = time.time() - boot_time_timestamp
            
            # Formatação amigável
            days, rem = divmod(uptime_seconds, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, seconds = divmod(rem, 60)
            
            if days > 0:
                return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        except:
            return "Indisponível"
        
    def get_metrics(self):
        gpu_data = self._get_nvidia_metrics() if self.gpu_type == "nvidia" else self._get_wmi_metrics()
        
        return {
            "cpu": psutil.cpu_percent(interval=None),
            "ram": psutil.virtual_memory().percent,
            "gpu": gpu_data,
            "uptime": self._get_uptime()
        }

def testes():
    monitor = HardwareMonitor()
    try:
        while True:
            print(monitor.get_metrics())
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitor encerrado.")

if __name__ == "__main__":
    testes()