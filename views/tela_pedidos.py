from tkinter import ttk, messagebox

class TelaPedidos(ttk.Frame):
    def __init__(self, master, pedido_controller, go_callback):
        super().__init__(master)
        self.pc = pedido_controller
        self.go = go_callback
        self._build_ui()

    def _build_ui(self):
        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(10, 10))
        ttk.Label(header, text="Pedidos", style="Title.TLabel").pack(side="left", padx=10)

        ttk.Button(header, text="Voltar", style="Ghost.TButton",
                   command=lambda: self.go("Dashboard")).pack(side="right", padx=10)
        ttk.Button(header, text="+ Novo Pedido", style="Accent.TButton",
                   command=lambda: self.go("NovoPedido")).pack(side="right", padx=10)

        # Tabela
        cols = ("id", "cliente", "total", "status", "data")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        heads = ("ID", "Cliente", "Total", "Status", "Data")
        for c, h in zip(cols, heads):
            self.tree.heading(c, text=h)
            self.tree.column(c, anchor="center", width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões de ação
        btns = ttk.Frame(self)
        btns.pack(anchor="e", pady=8, padx=10)
        ttk.Button(btns, text="Detalhes", command=self._detalhes).pack(side="left", padx=4)
        ttk.Button(btns, text="Excluir", command=self._excluir).pack(side="left", padx=4)
        ttk.Button(btns, text="Atualizar", command=self.on_show).pack(side="left", padx=4)

    def on_show(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            for p in self.pc.listar():
                self.tree.insert("", "end", values=(
                    p["id_pedido"],
                    p["cliente"],
                    f"R$ {p['vl_total_pedido']:.2f}",
                    p["status"],
                    p["dt_pedido"]
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os pedidos.\n{e}")

    def _detalhes(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Selecione um pedido para ver os detalhes.")
            return
        pid = int(self.tree.item(sel[0])["values"][0])
        self.go("DetalhesPedido", pid)

    def _excluir(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Selecione um pedido para excluir.")
            return
        pid = int(self.tree.item(sel[0])["values"][0])
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este pedido?"):
            try:
                self.pc.deletar(pid)
                self.on_show()
                messagebox.showinfo("Sucesso", "Pedido excluído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir o pedido.\n{e}")