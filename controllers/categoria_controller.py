from models.categoria_model import CategoriaModel

class CategoriaController:
    def __init__(self, db):
        self.model = CategoriaModel(db)
        self.model.inicializar_padrao()  # ← insere categorias padrão se estiver vazio

    def listar(self) -> list:
        return self.model.listar()

    def criar(self, nome: str) -> None:
        self.model.criar(nome)

    def excluir(self, id_categoria: int) -> None:
        self.model.excluir(id_categoria)