import secrets
from typing import Optional
import bcrypt
from fastapi import Request
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo


async def obter_usuario_logado(request: Request) -> Optional[Usuario]:
    try:
        token = request.cookies["auth_token"]
        if token.strip() == "":
            return None
        usuario = UsuarioRepo.obter_por_token(token)
        return usuario
    except KeyError:
        return None


def obter_hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""


def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False


def gerar_token(length: int = 32) -> str:
    try:
        return secrets.token_hex(length)
    except ValueError:
        return ""


def adicionar_cookie_autenticacao(response, token):
    response.set_cookie(
        key="auth_token",
        value=token,
        max_age=1800,
        httponly=True,
        samesite="lax",
    )
    return response


def excluir_cookie_autenticacao(response):
    response.delete_cookie(key="auth_token")
    return response


async def atualizar_cookie_autenticacao(request: Request, call_next):
    response = await call_next(request)
    usuario = await obter_usuario_logado(request)
    if usuario:
        token = request.cookies["auth_token"]
        response.set_cookie(
            key="auth_token",
            value=token,
            max_age=1800,
            httponly=True,
            samesite="lax",
        )
    return response
