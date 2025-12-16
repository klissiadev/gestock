from psycopg2 import IntegrityError

def file_hash_exists(db, file_hash: str) -> bool:
    query = "SELECT 1 FROM arquivos_importados WHERE file_hash = %s"
    with db.cursor() as cursor:
        cursor.execute(query, (file_hash,))
        return cursor.fetchone() is not None


def save_file_hash(db, filename: str, file_hash: str):
    query = """
        INSERT INTO arquivos_importados (filename, file_hash)
        VALUES (%s, %s)
    """
    try:
        with db.cursor() as cursor:
            cursor.execute(query, (filename, file_hash))
            db.commit()
    except IntegrityError:
        db.rollback()
        raise
