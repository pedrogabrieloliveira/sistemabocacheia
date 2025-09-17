from models.pedido_model import PedidoModel
from models.produto_model import ProdutoModel

class PedidoController:
    def __init__(self, db):
        self.model = PedidoModel(db)
        self.produto_model = ProdutoModel(db)

    def criar_pedido(self, dados):
        return self.model.criar(dados["id_cliente"], dados["id_usuario"])

    def adicionar_item(self, id_pedido, id_produto, quantidade):
        produto = self.produto_model.obter(id_produto)
        if not produto:
            raise ValueError("Produto não encontrado.")

        preco_unit = produto["preco"]
        estoque_atual = produto["estoque"]

        if quantidade > estoque_atual:
            raise ValueError("Estoque insuficiente.")

        novo_estoque = estoque_atual - quantidade
        self.produto_model.atualizar_estoque(id_produto, novo_estoque)

        self.model.adicionar_item(id_pedido, id_produto, quantidade, preco_unit)

    def listar(self):
        return self.model.listar()

    def detalhes(self, id_pedido):
        return self.model.detalhes(id_pedido)

    def deletar(self, id_pedido):
        try:
            cur = self.model.conn.cursor()
            cur.execute("DELETE FROM pedido_itens WHERE id_pedido = ?", (id_pedido,))
            cur.execute("DELETE FROM pedidos WHERE id_pedido = ?", (id_pedido,))
            self.model.conn.commit()
        except Exception as e:
            raise Exception(f"Erro ao excluir pedido: {e}")