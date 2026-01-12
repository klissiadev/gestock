from psycopg2 import IntegrityError

def file_hash_exists(db, file_hash: str) -> bool:
    query = """
        SELECT 1
        FROM app_logs.arquivos_importados
        WHERE file_hash = %s
    """
    with db.cursor() as cursor:
        cursor.execute(query, (file_hash,))
        return cursor.fetchone() is not None


def save_file_hash(db, filename: str, file_hash: str):
    query = """
        INSERT INTO app_logs.arquivos_importados (file_name, file_hash)
        VALUES (%s, %s)
    """
    with db.cursor() as cursor:
        cursor.execute(query, (filename, file_hash))
    db.commit()