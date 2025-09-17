class ClienteModel:
    def __init__(self, db):
        self.conn = db.connection()

    def criar(self, nome: str, telefone: str = "", email: str = "", endereco: str = ""):
        with self.conn:
            self.conn.execute("""
                INSERT INTO clientes (nome, telefone, email, endereco)
                VALUES (?, ?, ?, ?)
            """, (nome, telefone, email, endereco))

    def listar(self) -> list:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id_cliente, nome, telefone, email, endereco
            FROM clientes
            ORDER BY nome
        """)
        return [dict(row) for row in cur.fetchall()]

    def obter(self, id_cliente: int):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id_cliente, nome, telefone, email, endereco
            FROM clientes
            WHERE id_cliente = ?
        """, (id_cliente,))
        row = cur.fetchone()
        return dict(row) if row else None