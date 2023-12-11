import sqlite3


def criar_conexao():
    conexao = sqlite3.connect("dados.db")
    return conexao
