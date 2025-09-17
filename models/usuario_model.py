from datetime import datetime

class UsuarioModel:
    def __init__(self, db):
        self.conn = db.connection()

    def criar(self, nome: str, usuario: str, cargo: str, senha: str, foto: str | None = None):
        dt_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO usuarios (nome, usuario, cargo, dt_login_usuario, senha, foto)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, usuario, cargo, dt_login, senha, foto))

    def listar(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM usuarios ORDER BY id_usuario DESC")
        return cur.fetchall()

    def autenticar(self, usuario: str, senha: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        return cur.fetchone()

    def deletar(self, usuario_id: int):
        with self.conn:
            self.conn.execute("DELETE FROM usuarios WHERE id_usuario = ?", (usuario_id,))