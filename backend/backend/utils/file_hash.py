import hashlib

def generate_file_hash_stream(file) -> str:
    hash_obj = hashlib.sha256()
    # lê em blocos de 4KB
    for chunk in iter(lambda: file.read(4096), b""):
        hash_obj.update(chunk)
    file.seek(0)  # volta o ponteiro para leitura posterior
    return hash_obj.hexdigest()
