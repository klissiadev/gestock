import time
import psycopg
import requests
import smtplib
import concurrent.futures
from dotenv import load_dotenv
import os
from admin_module.utils.database import get_db_connection

class SystemHealth:
    def __init__(self):
        
        load_dotenv()
        self.config = {
            "db": {"url": os.getenv("DATABASE_URL"), "slow": 1.5, "timeout": 5},
            "ollama": {"url": "http://localhost:11434/api/tags", "slow": 1, "timeout": 5},
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
            with db_pool.connection() as conn:
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
                return self._calc_status(latency, "ollama"), round(latency * 1000, 2)
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
                return self._calc_status(latency, "smtp"), round(latency * 1000, 2)
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
        
