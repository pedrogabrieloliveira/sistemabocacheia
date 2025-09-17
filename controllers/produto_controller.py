from models.produto_model import ProdutoModel

class ProdutoController:
    def __init__(self, db):
        self.model = ProdutoModel(db)

    def cadastrar(self, nome, id_categoria, preco, estoque, descricao=""):
        self.model.criar(nome, id_categoria, preco, estoque, descricao)

    def listar(self):
        return self.model.listar()

    def obter(self, produto_id):
        return self.model.obter(produto_id)

    def deletar(self, produto_id):
        self.model.deletar(produto_id)

    def atualizar_estoque(self, produto_id, novo_estoque):
        self.model.atualizar_estoque(produto_id, novo_estoque)