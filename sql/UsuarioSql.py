SQL_CRIAR_TABELA = """
 CREATE TABLE IF NOT EXISTS usuario (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nome TEXT NOT NULL,
 email TEXT NOT NULL UNIQUE,
 senha TEXT NOT NULL,
 admin BOOLEAN NOT NULL,
 token TEXT)
"""
# senha 1aA@
SQL_INSERIR_ADMINISTRADOR_PADRAO = """
 INSERT OR IGNORE INTO usuario (
 nome, email, senha, admin)
 VALUES ('Administrador do Sistema', 'admin@email.com',
 '$2b$12$oAmErugexoRbXaSy3QEYB.GUueyURF3hqe0XYs5aEicyVs3B1O/zK', 1)
"""
# senha 1aA@
SQL_INSERIR_USUARIO_PADRAO = """
 INSERT OR IGNORE INTO usuario (
 nome, email, senha, admin)
 VALUES ('Usuário Padrão do Sistema', 'usuario@email.com',
 '$2b$12$oAmErugexoRbXaSy3QEYB.GUueyURF3hqe0XYs5aEicyVs3B1O/zK', 0)
"""
SQL_INSERIR = """
 INSERT INTO usuario (
 nome, email, senha, admin)
 VALUES (?, ?, ?, ?)
"""
SQL_ALTERAR = """
 UPDATE usuario
 SET nome=?, email=?, admin=?
 WHERE id=?
"""
SQL_ALTERAR_SENHA = """
 UPDATE usuario
 SET senha=?
 WHERE id=?
"""

SQL_ALTERAR_TOKEN_POR_EMAIL = """
 UPDATE usuario
 SET token=?
 WHERE email=?
"""
SQL_EXCLUIR = """
 DELETE FROM usuario
 WHERE id=?
"""
SQL_OBTER_TODOS = """
 SELECT id, nome, email, admin
 FROM usuario
 ORDER BY nome
"""
SQL_OBTER_POR_ID = """
 SELECT id, nome, email, admin
 FROM usuario
 WHERE id=?
"""
SQL_OBTER_POR_TOKEN = """
 SELECT id, nome, email, admin
 FROM usuario
 WHERE token=?
"""
SQL_OBTER_POR_EMAIL = """
 SELECT id, nome, email, admin
 FROM usuario
 WHERE email=?
"""
SQL_OBTER_SENHA_POR_EMAIL = """
 SELECT senha
 FROM usuario
 WHERE email=?
"""
SQL_EXISTE_EMAIL = """
 SELECT EXISTS (
 SELECT 1 FROM usuario
 WHERE email=?
 )
"""
