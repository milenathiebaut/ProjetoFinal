from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from util.mensagem import adicionar_cookie_mensagem
from util.seguranca import obter_usuario_logado
templates = Jinja2Templates(directory="templates")


def configurar_paginas_de_erro(app: FastAPI):
    @app.exception_handler(401)
    async def erro_401(request: Request, _):
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(
            f"/login{return_url}", status_code=status.HTTP_302_FOUND
        )
        adicionar_cookie_mensagem(
            response, f"Você deve estar autenticado para acessar a rota <b>{request.url.path}</b> .",
        )
        return response

    @app.exception_handler(403)
    async def erro_403(request: Request, _):
        usuario = await obter_usuario_logado(request)
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(
            f"/login{return_url}",
            status_code=status.HTTP_302_FOUND,
        )
        adicionar_cookie_mensagem(
            response,
            f"Você deve ser um administrador para acessar a rota < b > {request.url.path} < /b > .",
        )
        return response

    @app.exception_handler(404)
    async def erro_404(
        request: Request,
        usuario: Usuario = Depends(obter_usuario_logado),
    ):
        return templates.TemplateResponse(
            "root/404.html",
            {"request": request, "usuario": usuario},
        )

    @app.exception_handler(HTTPException)
    async def erro_http_exception(
        request: Request,
        ex: HTTPException,
        usuario: Usuario = Depends(obter_usuario_logado),
    ):
        return templates.TemplateResponse(
            "root/erro.html",
            {
                "request": request,
                "usuario": usuario,
                "detail": ex.detail,
            },
            status_code=ex.status_code,
        )

    @app.exception_handler(Exception)
    async def erro_exception(
        request: Request,
        ex: Exception,
        usuario: Usuario = Depends(obter_usuario_logado),
    ):
        return templates.TemplateResponse(
            "root/erro.html",
            {
                "request": request,
                "usuario": usuario,
                "detail": "Erro interno do servidor.",
            },
            status_code=500,
        )
