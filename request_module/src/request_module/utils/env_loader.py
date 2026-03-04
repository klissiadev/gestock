import os
from pathlib import Path
from dotenv import load_dotenv

def load_env_from_root(target_file=".env"):
    """
    Sobe os níveis de diretório a partir do arquivo atual 
    até encontrar o arquivo alvo (ex: .env).
    """
    current_path = Path(__file__).resolve()
    
    # Percorre todos os pais do diretório atual
    for parent in current_path.parents:
        env_path = parent / target_file
        if env_path.exists():
            print(f"Carregando {target_file} de: {env_path}")
            load_dotenv(dotenv_path=env_path)
            return True
    return False

if __name__ == "__main__":
    loaded = load_env_from_root()
    if not loaded:
        print(f"Arquivo .env não encontrado em nenhum diretório pai.")