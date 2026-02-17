from typing import Annotated
from fastapi import  HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from auth_module.models.User import UserCreate, UserDB, UserPublic, UserLogin
from auth_module.utils.database import this_user_exists, register_user, get_user_by_email
from auth_module.utils.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Registra um novo usuário no sistema.
    """
    if this_user_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail='Email já está em uso',
        )
    
    # Converte a senha para hash binário
    hashed_password_bytes = get_password_hash(user.password)
    
    new_user = UserDB(
        nome=user.nome,
        email=user.email,
        senha_hash=hashed_password_bytes,
        papel=user.papel
    )

    try:
        register_user(new_user)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao cadastrar usuário no banco de dados"
        )
    
    return {"message": "Usuário cadastrado com sucesso!"}

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Rota de login compatível com OAuth2 (Swagger).
    Ele valida as informações do usuário.
    Busca se o e-mail está no banco de dados
    Verifica se a senha está correta
    Retorna um token de acesso com e-mail do usuário
    """
    try:
        user_info = UserLogin(email=form_data.username, password=form_data.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de e-mail ou senha inválido"
        )
    
    user = get_user_by_email(user_info.email)

    if not user or not verify_password(user_info.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: Annotated[UserPublic, Depends(get_current_user)]):
    """
    Retorna os dados do usuário autenticado.
    Dados: nome, email e papel
    A dependência get_current_user já filtra os dados sensíveis.
    """
    return current_user

