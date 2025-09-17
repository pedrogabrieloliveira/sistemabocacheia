from models.usuario_model import UsuarioModel

class UsuarioController:
    def __init__(self, db):
        self.model = UsuarioModel(db)

    def cadastrar(self, nome: str, cargo: str, usuario: str, senha: str, foto: str | None = None):
        self.model.criar(nome, usuario, cargo, senha, foto)

    def listar(self):
        return self.model.listar()

    def login(self, usuario: str, senha: str):
        return self.model.autenticar(usuario, senha) is not None

    def get_by_username(self, usuario: str):
        for u in self.model.listar():
            if u["usuario"] == usuario:
                return u
        return None

    def deletar(self, usuario_id: int):
        self.model.deletar(usuario_id)