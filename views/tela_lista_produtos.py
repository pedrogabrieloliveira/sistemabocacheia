from tkinter import ttk, messagebox

class TelaListaProdutos(ttk.Frame):
    def __init__(self, master, produto_controller, go_callback):
        super().__init__(master)
        self.pc = produto_controller
        self.go = go_callback

        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(10,10))
        ttk.Label(header, text="Produtos", style="Title.TLabel").pack(side="left", padx=10)

        ttk.Button(header, text="Voltar", style="Ghost.TButton",
                   command=lambda: self.go("Dashboard")).pack(side="right", padx=10)
        ttk.Button(header, text="Novo", style="Accent.TButton",
                   command=lambda: self.go("CadastroProduto")).pack(side="right", padx=10)

        # Tabela
        cols = ("id","nome","preco","estoque","categoria")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        heads = ("ID","Nome","Preço","Estoque","CategoriaID")
        for c,h in zip(cols, heads):
            self.tree.heading(c, text=h)
            self.tree.column(c, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões de ação
        btns = ttk.Frame(self)
        btns.pack(anchor="e", pady=8)
        ttk.Button(btns, text="Excluir", command=self._excluir).pack(side="left", padx=4)
        ttk.Button(btns, text="Atualizar", command=self.on_show).pack(side="left", padx=4)

    def on_show(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            for p in self.pc.listar():
                self.tree.insert("", "end",
                                 values=(p["id_produto"], p["nome"], f"R$ {p['preco']:.2f}",
                                         p["estoque"], p["id_categoria"]))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os produtos.\n{e}")

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Selecione um produto para excluir.")
            return
        pid = int(self.tree.item(sel[0])["values"][0])
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este produto?"):
            try:
                self.pc.deletar(pid)
                self.on_show()
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir o produto.\n{e}")