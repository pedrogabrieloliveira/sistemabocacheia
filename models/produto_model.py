class ProdutoModel:
    def __init__(self, db):
        self.conn = db.connection()

    def criar(self, nome, id_categoria, preco, estoque, descricao=""):
        with self.conn:
            self.conn.execute("""
                INSERT INTO produtos (nome, id_categoria, preco, estoque, descricao)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, id_categoria, preco, estoque, descricao))

    def listar(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id_produto, nome, preco, estoque, id_categoria
            FROM produtos
            ORDER BY nome
        """)
        return [dict(row) for row in cur.fetchall()]

    def obter(self, produto_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM produtos WHERE id_produto = ?", (produto_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def deletar(self, produto_id):
        with self.conn:
            self.conn.execute("DELETE FROM produtos WHERE id_produto = ?", (produto_id,))

    def atualizar_estoque(self, produto_id, novo_estoque):
        with self.conn:
            self.conn.execute("""
                UPDATE produtos SET estoque = ? WHERE id_produto = ?
            """, (novo_estoque, produto_id))