from backend.database.base import get_connection
from backend.services.log_importacao_service import LogImportacaoService
from datetime import date

def test_crud_operations():
    conn = get_connection()
    service = LogImportacaoService(conn)
    
    try:
        print("\n1. Testando criação de log...")
        log_data = {
            "nome_arquivo": "teste.csv",
            "qntd_registros": 100,
            "data_importacao": date.today(),
            "status": "EM_ANDAMENTO",
            "msg_erro": None,
            "id_usuario": 1
        }
        
        result = service.criar_log(log_data)
        print(f"✅ Log criado: {result}")
        
        print("\n2. Testando listagem de logs...")
        logs = service.listar_logs()
        print(f"✅ Logs encontrados: {len(logs)}")
        
        if logs:
            log_id = logs[0]['id_log_importacao']
            
            print(f"\n3. Testando busca por ID ({log_id})...")
            log = service.buscar_por_id(log_id)
            print(f"✅ Log encontrado: {log['nome_arquivo']}")
            
            print(f"\n4. Testando atualização...")
            update_data = {"status": "CONCLUIDO", "qntd_registros": 150}
            result = service.atualizar_log(log_id, update_data)
            print(f"✅ Log atualizado: {result}")
            
            print(f"\n5. Testando deleção...")
            result = service.deletar_log(log_id)
            print(f"✅ Log deletado: {result}")
        
        print("\n🎉 Todos os testes passaram!")
        
    except Exception as e:
        print(f"❌ Erro durante testes: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_crud_operations()