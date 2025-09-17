class CategoriaModel:
    def __init__(self, db):
        self.conn = db.connection()

    def listar(self) -> list:
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM categorias ORDER BY nome ASC")
            return cur.fetchall()

    def criar(self, nome: str) -> None:
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))

    def excluir(self, id_categoria: int) -> None:
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM categorias WHERE id_categoria = ?", (id_categoria,))

    def inicializar_padrao(self):
        categorias = [
            "Entrada",
            "Prato Principal",
            "Sobremesa",
            "Bebida"
        ]
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM categorias")
        total = cur.fetchone()[0]

        if total == 0:
            for nome in categorias:
                cur.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
            self.conn.commit()