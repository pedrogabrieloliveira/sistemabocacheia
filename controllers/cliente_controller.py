from models.cliente_model import ClienteModel

class ClienteController:
    def __init__(self, db):
        self.model = ClienteModel(db)

    def cadastrar(self, nome: str, telefone: str = "", email: str = "", endereco: str = "") -> None:
        if not nome.strip():
            raise ValueError("O nome do cliente é obrigatório.")
        self.model.criar(nome.strip(), telefone.strip(), email.strip(), endereco.strip())

    def listar(self) -> list:
        return self.model.listar()

    def obter(self, id_cliente: int):
        return self.model.obter(id_cliente)