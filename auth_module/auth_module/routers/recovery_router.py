from fastapi import  HTTPException, APIRouter, BackgroundTasks
from auth_module.utils.database import get_user_by_email, change_user_password
from auth_module.utils.security import ( create_password_reset_token, verify_reset_token, get_password_hash)
from auth_module.utils.mail_service import send_recovery_email
from auth_module.models.Recovery import RecoveryRequest, PasswordResetConfirm


router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/forgot-password")
async def forgot_password(email_data: RecoveryRequest, background_tasks: BackgroundTasks):
    email = email_data.email
    user = get_user_by_email(email)

    if user:
        token = create_password_reset_token(user)
        link = f"http://localhost:5173/reset-password?token={token}"
        background_tasks.add_task(send_recovery_email, user.email, link)
        
    # aqui disparo do email
    return {"message": "Se o e-mail estiver cadastrado, um link será enviado."}


@router.post("/reset-password")
async def reset_password(data: PasswordResetConfirm):

    user_id = verify_reset_token(data.token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Token expirado ou já utilizado.")
    
    new_password = get_password_hash(data.new_password)
    change_user_password(id=user_id, senha=new_password)

    return {"message": "Senha atualizada com sucesso."}

    
