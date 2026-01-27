from uuid import uuid4
from datetime import datetime

# armazenamento em memória (TESTES)
_sessions: dict[str, dict] = {}

def list_sessions():
    return [
        {
            "session_id": sid,
            "created_at": data["created_at"]
        }
        for sid, data in _sessions.items()
    ]

def create_session():
    session_id = str(uuid4())
    _sessions[session_id] = {
        "created_at": datetime.utcnow(),
    }
    return session_id

def session_exists(session_id: str) -> bool:
    return session_id in _sessions
