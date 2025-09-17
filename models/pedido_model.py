from datetime import datetime

class PedidoModel:
    def __init__(self, db):
        self.conn = db.connection()

    def criar(self, id_cliente, id_usuario):
        dt_pedido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Aberto"
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO pedidos (dt_pedido, vl_total_pedido, status, id_usuario, id_cliente)
                VALUES (?, ?, ?, ?, ?)
            """, (dt_pedido, 0.0, status, id_usuario, id_cliente))
            return cur.lastrowid

    def adicionar_item(self, id_pedido, id_produto, quantidade, preco_unit):
        vl_total_item = quantidade * preco_unit
        with self.conn:
            self.conn.execute("""
                INSERT INTO pedido_itens (id_pedido, id_produto, quantidade, preco_unit, vl_total_item)
                VALUES (?, ?, ?, ?, ?)
            """, (id_pedido, id_produto, quantidade, preco_unit, vl_total_item))

            # Atualiza total do pedido
            cur = self.conn.cursor()
            cur.execute("""
                SELECT vl_total_pedido FROM pedidos WHERE id_pedido = ?
            """, (id_pedido,))
            atual = cur.fetchone()["vl_total_pedido"]
            novo_total = atual + vl_total_item

            self.conn.execute("""
                UPDATE pedidos SET vl_total_pedido = ? WHERE id_pedido = ?
            """, (novo_total, id_pedido))

    def listar(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT p.id_pedido, p.dt_pedido, p.vl_total_pedido, p.status,
                   u.nome AS usuario, c.nome AS cliente
            FROM pedidos p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            JOIN clientes c ON p.id_cliente = c.id_cliente
            ORDER BY p.dt_pedido DESC
        """)
        return [dict(row) for row in cur.fetchall()]

    def detalhes(self, id_pedido):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT pi.id_item, pr.nome AS produto, pi.quantidade, pi.preco_unit, pi.vl_total_item
            FROM pedido_itens pi
            JOIN produtos pr ON pi.id_produto = pr.id_produto
            WHERE pi.id_pedido = ?
        """, (id_pedido,))
        return [dict(row) for row in cur.fetchall()]