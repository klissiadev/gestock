from backend.database.base import get_connection

def test_connection():
    try:
        conn = get_connection()
        print("✅ Conexão com o banco estabelecida com sucesso!")
        
        # Teste se a tabela existe
        cursor = conn.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'logimportacao'
            );
        """)
        exists = cursor.fetchone()['exists']
        print(f"✅ Tabela 'logimportacao' existe: {exists}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    test_connection()