import tkinter as tk
from tkinter import ttk, messagebox

class TelaNovoPedido(ttk.Frame):
    def __init__(self, master, cliente_controller, produto_controller, pedido_controller, go_callback):
        super().__init__(master)
        self.cc = cliente_controller
        self.pc = produto_controller
        self.ped = pedido_controller
        self.go = go_callback
        self.itens = []
        self._build_ui()

    def _build_ui(self):
        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(10, 10))
        ttk.Label(header, text="Novo Pedido", style="Title.TLabel").pack(side="left", padx=10)
        ttk.Button(header, text="← Voltar", style="Ghost.TButton",
                   command=lambda: self.go("Pedidos")).pack(side="right", padx=10)

        # Cliente (sem fundo cinza)
        cliente_box = ttk.Frame(self)
        cliente_box.pack(fill="x", padx=20, pady=10)
        ttk.Label(cliente_box, text="Cliente", style="Subtitle.TLabel").pack(anchor="w", padx=10, pady=(0, 4))

        cliente_row = ttk.Frame(cliente_box)
        cliente_row.pack(fill="x")
        self.cb_cliente = ttk.Combobox(cliente_row, width=40, state="readonly")
        self.cb_cliente.pack(side="left", padx=10, pady=6)
        ttk.Button(cliente_row, text="Cadastrar Novo Cliente", style="Ghost.TButton",
                   command=self._novo_cliente).pack(side="left", padx=10)

        # Produto (sem fundo cinza)
        produto_box = ttk.Frame(self)
        produto_box.pack(fill="x", padx=20, pady=10)
        ttk.Label(produto_box, text="Adicionar Produto", style="Subtitle.TLabel").pack(anchor="w", padx=10, pady=(0, 4))

        produto_row = ttk.Frame(produto_box)
        produto_row.pack(fill="x")
        self.cb_produto = ttk.Combobox(produto_row, state="readonly", width=40)
        self.cb_produto.pack(side="left", padx=10, pady=6)
        self.e_qtd = ttk.Entry(produto_row, width=5)
        self.e_qtd.pack(side="left", padx=10)
        ttk.Button(produto_row, text="Adicionar Produto", style="Accent.TButton",
                   command=self._adicionar_produto).pack(side="left", padx=10)

        # Tabela de itens
        self.tree = ttk.Treeview(self, columns=("produto", "quantidade"), show="headings", height=8)
        self.tree.heading("produto", text="Produto")
        self.tree.heading("quantidade", text="Quantidade")
        self.tree.column("produto", anchor="center", width=300)
        self.tree.column("quantidade", anchor="center", width=100)
        self.tree.pack(fill="x", padx=20, pady=10)

        # Botão de criar pedido
        ttk.Button(self, text="Criar Pedido", style="Accent.TButton",
                   command=self._criar_pedido).pack(pady=20)

    def on_show(self):
        self.itens.clear()
        for i in self.tree.get_children():
            self.tree.delete(i)

        clientes = self.cc.listar()
        self.cb_cliente["values"] = [f"{c['id_cliente']} - {c['nome']}" for c in clientes]
        if clientes:
            self.cb_cliente.set(f"{clientes[0]['id_cliente']} - {clientes[0]['nome']}")

        produtos = self.pc.listar()
        self.cb_produto["values"] = [f"{p['id_produto']} - {p['nome']}" for p in produtos]
        self.cb_produto.set("")
        self.e_qtd.delete(0, "end")

    def _novo_cliente(self):
        def salvar():
            nome = self.e_nome.get().strip()
            tel = self.e_tel.get().strip()
            email = self.e_email.get().strip()
            end = self.e_end.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Informe o nome do cliente.")
                return
            try:
                self.cc.cadastrar(nome, tel, email, end)
                top.destroy()
                self.on_show()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível cadastrar o cliente.\n{e}")

        top = tk.Toplevel(self)
        top.title("Novo Cliente")
        top.resizable(False, False)

        ttk.Label(top, text="Nome:").pack(padx=12, pady=(12, 4))
        self.e_nome = ttk.Entry(top, width=32)
        self.e_nome.pack(padx=12, pady=4)

        ttk.Label(top, text="Telefone:").pack(padx=12, pady=4)
        self.e_tel = ttk.Entry(top, width=32)
        self.e_tel.pack(padx=12, pady=4)

        ttk.Label(top, text="Email:").pack(padx=12, pady=4)
        self.e_email = ttk.Entry(top, width=32)
        self.e_email.pack(padx=12, pady=4)

        ttk.Label(top, text="Endereço:").pack(padx=12, pady=4)
        self.e_end = ttk.Entry(top, width=32)
        self.e_end.pack(padx=12, pady=4)

        ttk.Button(top, text="Salvar", style="Accent.TButton", command=salvar).pack(pady=12)

    def _adicionar_produto(self):
        val = self.cb_produto.get()
        qtd = self.e_qtd.get()

        if not val or not qtd.isdigit():
            messagebox.showwarning("Validação", "Selecione um produto e informe a quantidade.")
            return

        id_produto = int(val.split(" - ")[0])
        nome = val.split(" - ")[1]
        quantidade = int(qtd)

        self.itens.append((id_produto, quantidade))
        self.tree.insert("", "end", values=(nome, quantidade))

        self.cb_produto.set("")
        self.e_qtd.delete(0, "end")

    def _criar_pedido(self):
        try:
            sel = self.cb_cliente.get()
            if not sel:
                raise ValueError("Selecione um cliente.")
            if not self.itens:
                raise ValueError("Adicione pelo menos um produto ao pedido.")

            id_cliente = int(sel.split(" - ")[0])
            pedido_id = self.ped.criar_pedido({
                "id_cliente": id_cliente,
                "id_usuario": 1  # fixo para teste
            })

            for id_produto, qtd in self.itens:
                self.ped.adicionar_item(pedido_id, id_produto, qtd)

            messagebox.showinfo("Sucesso", "Pedido criado com sucesso.")
            self.go("Pedidos")

        except ValueError as ve:
            messagebox.showwarning("Validação", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar o pedido.\n{e}")