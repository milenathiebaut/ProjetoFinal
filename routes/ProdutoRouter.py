from io import BytesIO
import os
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
    Form,
    File,
    UploadFile,
    Path,
)
from PIL import Image
from fastapi.templating import Jinja2Templates
from models.Produto import Produto
from models.Usuario import Usuario
from repositories.ProdutoRepo import ProdutoRepo
from util.mensagem import redirecionar_com_mensagem
from util.imagem import transformar_em_quadrada
from util.seguranca import obter_usuario_logado
router = APIRouter(prefix="/produto")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_index(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    produtos = ProdutoRepo.obter_todos()
    return templates.TemplateResponse(
        "produto/index.html",
        {"request": request, "usuario": usuario, "produtos": produtos},
    )


@router.get("/inserir")
async def get_inserir(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return templates.TemplateResponse(
        "produto/inserir.html",
        {"request": request, "usuario": usuario},
    )


@router.post("/inserir")
async def post_inserir(
    nome: str = Form(...),
    preco: float = Form(...),
    descricao: str = Form(...),
    arquivoImagem: UploadFile = File(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    produto = Produto(nome=nome, preco=preco, descricao=descricao)
    produto_inserido = ProdutoRepo.inserir(produto)

    if produto_inserido:
        produto_id = produto_inserido.id
        if arquivoImagem.filename:
            conteudo_arquivo = await arquivoImagem.read()
            imagem = Image.open(BytesIO(conteudo_arquivo))
            imagem_quadrada = transformar_em_quadrada(imagem)
            imagem_quadrada.save(f"static/img/produtos/{produto_id:04d}.jpg", "JPEG")


        response = redirecionar_com_mensagem("/produto", "Produto inserido com sucesso!")
        return response

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao inserir o produto.")



@router.get("/excluir/{id_produto:int}")
async def get_excluir(
    request: Request,
    id_produto: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    produto = ProdutoRepo.obter_por_id(id_produto)
    return templates.TemplateResponse(
        "produto/excluir.html",
        {"request": request, "usuario": usuario, "produto": produto},
    )


@router.post("/excluir/{id_produto:int}")
async def post_excluir(
    id_produto: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    ProdutoRepo.excluir(id_produto)
    caminho_imagem = f"static/img/produtos/{id_produto:04d}.jpg"
    if os.path.exists(caminho_imagem):
        os.remove(caminho_imagem)

    response = redirecionar_com_mensagem(
        "/produto", "Produto excluído com sucesso!")
    return response


@router.get("/alterar/{id_produto:int}")
async def get_alterar(
    request: Request,
    id_produto: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    produto = ProdutoRepo.obter_por_id(id_produto)
    return templates.TemplateResponse(
        "produto/alterar.html",
        {"request": request, "usuario": usuario, "produto": produto},
    )


@router.post("/alterar/{id_produto:int}")
async def post_alterar(
    id_produto: int = Path(),
    nome: str = Form(...),
    preco: float = Form(...),
    descricao: str = Form(...),
    arquivoImagem: UploadFile = File(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    ProdutoRepo.alterar(Produto(id_produto, nome, preco, descricao))
    if arquivoImagem.filename:
        conteudo_arquivo = await arquivoImagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/img/produtos/{id_produto:04d}.jpg",
                         "JPEG")
    response = redirecionar_com_mensagem("/produto", "Produto alterado com sucesso!")
    return response

@router.get("/detalhes/{id:int}")
async def getDetalhes(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
    id: int = Path(),
):
    produto = ProdutoRepo.obter_por_id(id)
    return templates.TemplateResponse(
        "produto/detalhes.html",
        {"request": request, "usuario": usuario, "produto": produto},
    )
