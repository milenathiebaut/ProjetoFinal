from fastapi import status
from fastapi.responses import RedirectResponse


def adicionar_cookie_mensagem(response, mensagem):
    response.set_cookie(
        key="mensagem",
        value=mensagem,
        max_age=1,
        httponly=True,
        samesite="lax",
    )


def redirecionar_com_mensagem(url_destino: str, mensagem: str):
    response = RedirectResponse(
        url_destino,
        status_code=status.HTTP_303_SEE_OTHER,
    )
    adicionar_cookie_mensagem(response, mensagem)
    return response
