import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="boca_cheia.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  
        self._criar_tabelas()
        self._corrigir_estrutura()
        self._inserir_admin_inicial()

    def connection(self):
        return self.conn

    def _criar_tabelas(self):
        cur = self.conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                cargo TEXT NOT NULL,
                dt_login_usuario TEXT,
                senha TEXT NOT NULL,
                foto TEXT
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                id_categoria INTEGER NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER NOT NULL DEFAULT 0,
                descricao TEXT,
                imagem TEXT,
                FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
                dt_pedido TEXT NOT NULL,
                vl_total_pedido REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL,
                id_usuario INTEGER NOT NULL,
                id_cliente INTEGER NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS pedido_itens (
                id_item INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pedido INTEGER NOT NULL,
                id_produto INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unit REAL NOT NULL,
                vl_total_item REAL NOT NULL,
                FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
                FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
            );
        """)

        self.conn.commit()

    def _corrigir_estrutura(self):
        """Adiciona coluna 'endereco' em clientes se não existir."""
        cur = self.conn.cursor()
        cur.execute("PRAGMA table_info(clientes)")
        colunas = [col["name"] for col in cur.fetchall()]
        if "endereco" not in colunas:
            cur.execute("ALTER TABLE clientes ADD COLUMN endereco TEXT;")
            self.conn.commit()

    def _inserir_admin_inicial(self):
        """Insere usuário admin padrão se não houver nenhum."""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) as total FROM usuarios")
        total = cur.fetchone()["total"]
        if total == 0:
            cur.execute("""
                INSERT INTO usuarios (nome, usuario, cargo, dt_login_usuario, senha, foto)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                "Administrador",
                "admin",
                "admin",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "123",
                None
            ))
            self.conn.commit()

    def close(self):
        self.conn.close()