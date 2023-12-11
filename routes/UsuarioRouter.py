from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
    Path,
    Form,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_hash_senha, obter_usuario_logado, conferir_senha
from util.seguranca import *
from util.filtros import *
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.validacao import *
router = APIRouter(prefix="/usuario")
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_index(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    usuarios = UsuarioRepo.obter_todos()
    return templates.TemplateResponse(
        "usuario/index.html",
        {"request": request, "usuario": usuario, "usuarios": usuarios},
    )


@router.get("/excluir/{id_usuario:int}", response_class=HTMLResponse)
async def get_excluir(
    request: Request,
    id_usuario: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    usuario_excluir = UsuarioRepo.obter_por_id(id_usuario)
    return templates.TemplateResponse(
        "usuario/excluir.html",
        {"request": request, "usuario": usuario, "usuario_excluir":
         usuario_excluir},
    )


@router.post("/excluir/{id_usuario:int}", response_class=HTMLResponse)
async def post_excluir(
    usuario: Usuario = Depends(obter_usuario_logado),
    id_usuario: int = Path(),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if id_usuario == 1:
        response = redirecionar_com_mensagem(
            "/usuario",
            "Não é possível excluir o administrador padrão do sistema.",
        )
        return response

    if id_usuario == usuario.id:
        response = redirecionar_com_mensagem(
            "/usuario",
            "Não é possível excluir o próprio usuário que está logado.",
        )
        return response

    UsuarioRepo.excluir(id_usuario)
    response = redirecionar_com_mensagem(
        "/usuario",
        "Usuário excluído com sucesso.",
    )
    return response


@router.get("/alterar/{id_usuario:int}", response_class=HTMLResponse)
async def get_alterar(
    request: Request,
    id_usuario: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    usuario_alterar = UsuarioRepo.obter_por_id(id_usuario)
    return templates.TemplateResponse(
        "usuario/alterar.html",
        {"request": request, "usuario": usuario, "usuario_alterar":
         usuario_alterar},
    )


@router.post("/alterar/{id_usuario:int}", response_class=HTMLResponse)
async def post_alterar(
    id_usuario: int = Path(),
    nome: str = Form(...),
    email: str = Form(...),
    administrador: bool = Form(False),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if id_usuario == 1:
        response = redirecionar_com_mensagem(
            "/usuario",
            "Não é possível alterar dados do administrador padrão.",
        )
        return response

    UsuarioRepo.alterar(
        Usuario(id=id_usuario, nome=nome, email=email, admin=administrador)
    )
    response = redirecionar_com_mensagem(
        "/usuario",
        "Usuário alterado com sucesso.",
    )
    return response

@router.get("/novo")
async def get_Novo(
    request: Request, usuario: Usuario = Depends(obter_usuario_logado)):
    return templates.TemplateResponse(
        "usuario/novo.html",
        {"request": request,"usuario": usuario}
    )

@router.post("/novo")
async def postNovo(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
    nome: str = Form(" "),
    email: str = Form(" "),
    senha: str = Form(" "),
    confsenha: str = Form(""),
    admin: bool = False,
):
    nome = capitalizar_nome_proprio(nome).strip()
    email = email.lower().strip()
    senha = senha.strip()
    confsenha = confsenha.strip()

    erros = {}
    is_not_empty(nome, "nome", erros)
    is_person_fullname(nome, "nome", erros)
    is_not_empty(email, "email", erros)
    if is_email(email, "email", erros):
        if UsuarioRepo.existe_email(email):
            add_error("email", "Já existe um usuário cadastrado com este e-mail.", erros)
    is_not_empty(senha, "senha", erros)
    is_password(senha, "senha", erros)
    is_not_empty(confsenha, "confsenha", erros)
    is_matching_fields(confsenha, "confsenha", senha, "senha", erros)

    if len(erros) > 0:
        valores = {}
        valores["nome"] = nome
        valores["email"] = email.lower()
        return templates.TemplateResponse(
            "usuario/novo.html",
            {
                "request": request,
                "erros": erros,
                "valores": valores,
            },
        )

    UsuarioRepo.inserir(0, nome, email, obter_hash_senha(senha), admin)

    return templates.TemplateResponse(
    "root/login.html",
    {
      "request": request,
      "usuario": usuario
    },
  )

@router.get("/arearestrita")
async def get_arearestrita(
    request: Request, usuario: Usuario = Depends(obter_usuario_logado)):
    return templates.TemplateResponse(
        "usuario/arearestrita.html",
        {"request": request,"usuario": usuario}
    )

@router.post("/alterarsenha", response_class=HTMLResponse)
async def postAlterarsenha(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
    senha_atual: str = Form(""),
    nova_senha: str = Form(""),
    conf_nova_senha: str = Form(""),    
):
    senha_atual = senha_atual.strip()
    nova_senha = nova_senha.strip()
    conf_nova_senha = conf_nova_senha.strip()    

    erros = {}
    is_not_empty(senha_atual, "senha_atual", erros)
    is_password(senha_atual, "senha_atual", erros)    
    is_not_empty(nova_senha, "nova_senha", erros)
    is_password(nova_senha, "nova_senha", erros)
    is_not_empty(conf_nova_senha, "conf_nova_senha", erros)
    is_matching_fields(
        conf_nova_senha, "conf_nova_senha", nova_senha, "nova_senha", erros)

    if len(erros) == 0:    
        hash_senha_bd = UsuarioRepo.obter_senha_por_email(usuario.email)
        if hash_senha_bd:
            if not conferir_senha(senha_atual, hash_senha_bd):            
                add_error("senha_atual", "Senha atual está incorreta.", erros)
    
    # se tem erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}        
        return templates.TemplateResponse(
            "usuario/alterarSenha.html",
            {
                "request": request,
                "usuario": usuario,                
                "erros": erros,
                "valores": valores,
            },
        )

    hash_nova_senha = obter_hash_senha(nova_senha)
    if usuario:
        UsuarioRepo.alterarSenha(usuario.id, hash_nova_senha)
    
    return templates.TemplateResponse(
        "usuario/arearestrita.html",
        {"request": request, "usuario": usuario},
    )
    