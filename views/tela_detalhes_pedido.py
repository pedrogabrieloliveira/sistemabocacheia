from tkinter import ttk, messagebox

class TelaDetalhesPedido(ttk.Frame):
    def __init__(self, master, pedido_controller, produto_controller, go_callback):
        super().__init__(master)
        self.pc = pedido_controller
        self.prod = produto_controller
        self.go = go_callback
        self._build_ui()

    def _build_ui(self):
        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(10, 10))
        ttk.Label(header, text="Detalhes do Pedido", style="Title.TLabel").pack(side="left", padx=10)
        ttk.Button(header, text="← Voltar", style="Ghost.TButton",
                   command=lambda: self.go("Pedidos")).pack(side="right", padx=10)

        # Tabela de itens
        self.tree = ttk.Treeview(self, columns=("produto", "qtd", "preco", "total"), show="headings", height=15)
        self.tree.heading("produto", text="Produto")
        self.tree.heading("qtd", text="Qtd")
        self.tree.heading("preco", text="Preço Unit.")
        self.tree.heading("total", text="Total Item")

        for col in ("produto", "qtd", "preco", "total"):
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def on_show(self, pedido_id):
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)

            itens = self.pc.detalhes(pedido_id)
            if not itens:
                messagebox.showinfo("Aviso", "Este pedido não possui itens.")
                return

            for item in itens:
                self.tree.insert("", "end", values=(
                    item.get("produto", "Desconhecido"),
                    item.get("quantidade", 0),
                    f"R$ {item.get('preco_unit', 0):.2f}",
                    f"R$ {item.get('vl_total_item', 0):.2f}"
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os detalhes.\n{e}")