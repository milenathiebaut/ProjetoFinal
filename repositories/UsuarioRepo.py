import sqlite3
from typing import List, Optional
from models.Usuario import Usuario
from sql.UsuarioSql import *
from util.bancodedados import criar_conexao


class UsuarioRepo:
    @classmethod
    def criar_tabela(cls) -> bool or False:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_CRIAR_TABELA)
                return True
        except sqlite3.Error:
            return False

    @classmethod
    def criar_administrador_padrao(cls) -> bool or False:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR_ADMINISTRADOR_PADRAO)
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @classmethod
    def criar_usuario_padrao(cls) -> bool or False:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR_USUARIO_PADRAO)
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    @classmethod
    def inserir(cls, usuario: Usuario) -> Optional[Usuario]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (usuario.nome, usuario.email, usuario.senha,
                    usuario.admin),
                )
                if cursor.rowcount > 0:
                    usuario.id = cursor.lastrowid
                    return usuario
        except sqlite3.Error:
            return False

    @classmethod
    def alterar(cls, usuario: Usuario) -> bool or False:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                SQL_ALTERAR,
                (
                    usuario.nome,
                    usuario.email,
                    usuario.admin,
                    usuario.id,
                ),
            )
            return cursor.rowcount > 0
    
    @classmethod
    def alterarSenha(cls, usuario: Usuario) -> bool or False:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                SQL_ALTERAR_SENHA,
                (
                    usuario.senha,
                    usuario.id,
                ),
            )
            return cursor.rowcount > 0


    @classmethod
    def alterar_token_por_email(cls, token: str, email: str) -> bool or False:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_ALTERAR_TOKEN_POR_EMAIL, (token, email))
            return cursor.rowcount > 0

    @classmethod
    def excluir(cls, id_usuario: int) -> bool:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_EXCLUIR, (id_usuario,))
            return cursor.rowcount > 0

    @classmethod
    def obter_todos(cls) -> List[Usuario]:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
            objetos = [
                Usuario(id=t[0], nome=t[1], email=t[2], admin=t[3]) for t in
                tuplas
            ]
            return objetos

    @classmethod
    def obter_por_id(cls, id_usuario: int) -> Optional[Usuario]:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            tupla = cursor.execute(SQL_OBTER_POR_ID,
                           (id_usuario,)).fetchone()
            if tupla:
                objeto = Usuario(
                    id=tupla[0], nome=tupla[1], email=tupla[2],
                    admin=tupla[3]
                )
                return objeto
            else:
                return None

    @classmethod
    def obter_por_token(cls, token: str) -> Optional[Usuario]:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            tupla = cursor.execute(SQL_OBTER_POR_TOKEN, (token,)).fetchone()
            if tupla:
                objeto = Usuario(
                    id=tupla[0], nome=tupla[1], email=tupla[2],
                    admin=tupla[3]
            )
                return objeto

    @classmethod
    def obter_por_email(cls, email: str) -> Optional[Usuario]:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            tupla = cursor.execute(SQL_OBTER_POR_EMAIL, (email,)).fetchone()
            if tupla:
                objeto = Usuario(
                    id=tupla[0], nome=tupla[1], email=tupla[2],
                    admin=tupla[3]
            )
            return objeto

    @classmethod
    def obter_senha_por_email(cls, email: str) -> Optional[str]:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            resultado = cursor.execute(SQL_OBTER_SENHA_POR_EMAIL,
                               (email,)).fetchone()
            if resultado:
                return str(resultado[0])

    @classmethod
    def existe_email(cls, email: str) -> bool or False:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            resultado = cursor.execute(SQL_EXISTE_EMAIL,
                               (email,)).fetchone()
            if resultado:
                return bool(resultado[0])
    
