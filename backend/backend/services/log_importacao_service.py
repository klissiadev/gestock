import psycopg2
from psycopg2.extras import RealDictCursor
from backend.models.log_importacao import LogImportacaoCreate, LogImportacao


def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="db_gestock",
        user="postgres",
        password="sua_senha"
    )


def criar_log_importacao(log: LogImportacaoCreate) -> LogImportacao:
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = """
        INSERT INTO "LogImportacao" 
        (nome_arquivo, qntd_registros, data_importacao, status, msg_erro, id_usuario)
        VALUES (%s, %s, NOW(), %s, %s, %s)
        RETURNING 
            id_log_importacao,
            nome_arquivo,
            qntd_registros,
            data_importacao,
            status,
            msg_erro,
            id_usuario;
    """

    cur.execute(
        query,
        (
            log.nome_arquivo,
            log.qntd_registros,
            log.status,
            log.msg_erro,
            log.id_usuario
        )
    )

    resultado = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return LogImportacao(**resultado)
