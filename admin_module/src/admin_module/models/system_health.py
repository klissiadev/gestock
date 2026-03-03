import time
import requests
import smtplib
import concurrent.futures
from admin_module.utils.database import get_db_connection
from admin_module.utils.env_loader import load_env_from_root

class SystemHealth:
    def __init__(self):
        load_env_from_root()
        self.config = {
            "db": {"slow": 1.5, "timeout": 5},
            "ollama": {"url": "http://127.0.0.1:11434/", "slow": 1, "timeout": 5},
            "smtp": {"host": "smtp.gmail.com", "port": 587, "slow": 2, "timeout": 8}
        }
        
    def _calc_status(self, latency, service_key):
        """Classifica os serviços em: Offline, Degradado e Online"""
        
        if latency is None: return "Offline"
        if latency > self.config[service_key]["timeout"]: return "Offline"
        if latency > self.config[service_key]["slow"]: return "Degradado"
        return "Online"
    
    def check_db(self):
        """Verifica o status do banco de dados"""
        start = time.perf_counter()
        try:
            with get_db_connection(timeout=2.0) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    latency = time.perf_counter() - start
                    status = self._calc_status(latency, "db")
                    return {"status": status, "latency": round(latency * 1000, 2)}
        except Exception as e:
            # Erros gerais
            return {"status": "Offline", "latency": None, "error": str(e)}
        
    def check_ollama(self):
        """Verifica o status do Ollama """
        start = time.perf_counter()
        try:
            response = requests.get(self.config["ollama"]["url"], timeout=self.config["ollama"]["timeout"])
            if response.status_code == 200:
                latency = time.perf_counter() - start
                status = self._calc_status(latency, "ollama") if response.status_code == 200 else "Degradado"
                return {"status": status, "latency": round(latency * 1000, 2)}
            return "Degradado", None # Respondeu mas não com 200 OK
        except:
            return "Offline", None

    def check_smtp(self):
        start = time.perf_counter()
        try:
            # Conecta ao SMTP do Google
            with smtplib.SMTP(self.config["smtp"]["host"], self.config["smtp"]["port"], 
                              timeout=self.config["smtp"]["timeout"]) as server:
                server.ehlo() #  Faz um ping no servidor
                latency = time.perf_counter() - start
                status = self._calc_status(latency, "smtp")
                return {"status": status, "latency": round(latency * 1000, 2)}
        except:
            return "Offline", None
        
    def get_all_statuses(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                "database": executor.submit(self.check_db),
                "ollama": executor.submit(self.check_ollama),
                "google_smtp": executor.submit(self.check_smtp)
            }
            
            return {service: future.result() for service, future in futures.items()}
        
def testes():
    sys = SystemHealth()
    while True:
        print(sys.get_all_statuses())
        time.sleep(1)

if __name__ == '__main__':
    testes()