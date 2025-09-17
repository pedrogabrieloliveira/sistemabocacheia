import tkinter as tk
from tkinter import ttk, messagebox

class TelaCadastroProduto(ttk.Frame):
    def __init__(self, master, produto_controller, categoria_controller, go_callback):
        super().__init__(master)
        self.pc = produto_controller
        self.cc = categoria_controller
        self.go = go_callback
        self.categorias = []
        self._build()

    def _build(self):
        card = ttk.Frame(self, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center", width=560, height=420)

        ttk.Label(card, text="Cadastro de Produto", style="Title.TLabel").pack(pady=(16, 10))
        form = ttk.Frame(card, style="Card.TFrame")
        form.pack(padx=20, pady=4, fill="x")

        ttk.Label(form, text="Nome", style="Card.TLabel").grid(row=0, column=0, sticky="w")
        self.e_nome = ttk.Entry(form, width=40)
        self.e_nome.grid(row=1, column=0, padx=(0, 16), pady=4)

        ttk.Label(form, text="Preço", style="Card.TLabel").grid(row=0, column=1, sticky="w")
        self.e_preco = ttk.Entry(form, width=20)
        self.e_preco.grid(row=1, column=1, pady=4)

        ttk.Label(form, text="Estoque", style="Card.TLabel").grid(row=2, column=1, sticky="w")
        self.e_estoque = ttk.Entry(form, width=20)
        self.e_estoque.grid(row=3, column=1, pady=4)

        ttk.Label(form, text="Descrição", style="Card.TLabel").grid(row=2, column=0, sticky="w")
        self.e_desc = ttk.Entry(form, width=40)
        self.e_desc.grid(row=3, column=0, padx=(0, 16), pady=4)

        ttk.Label(form, text="Categoria", style="Card.TLabel").grid(row=4, column=0, sticky="w")
        self.cb_cat = ttk.Combobox(form, state="readonly", width=37)
        self.cb_cat.grid(row=5, column=0, padx=(0, 16), pady=4)

        ttk.Button(form, text="+ Nova", style="Ghost.TButton", command=self._nova_categoria).grid(row=5, column=1, pady=4)

        btns = ttk.Frame(card, style="Card.TFrame")
        btns.pack(pady=10)
        ttk.Button(btns, text="Salvar", style="Accent.TButton", command=self._salvar).pack(side="left", padx=6)
        ttk.Button(btns, text="Voltar", style="Ghost.TButton", command=lambda: self.go("ListaProdutos")).pack(side="left", padx=6)

    def on_show(self):
        self.categorias = self.cc.listar()
        if not self.categorias:
            self.cb_cat["values"] = []
            self.cb_cat.set("")
            messagebox.showwarning("Categorias", "Nenhuma categoria cadastrada.")
        else:
            nomes = [f"{c['id_categoria']} - {c['nome']}" for c in self.categorias]
            self.cb_cat["values"] = nomes
            self.cb_cat.set(nomes[0])

        self.e_nome.delete(0, "end")
        self.e_preco.delete(0, "end")
        self.e_estoque.delete(0, "end")
        self.e_desc.delete(0, "end")

    def _salvar(self):
        try:
            nome = self.e_nome.get().strip()
            preco = float(self.e_preco.get())
            estoque = int(self.e_estoque.get() or "0")
            descricao = self.e_desc.get().strip()
            cat_val = self.cb_cat.get()

            if not nome or not cat_val:
                messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
                return

            id_categoria = int(cat_val.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores numéricos.")
            return

        self.pc.cadastrar(nome, id_categoria, preco, estoque, descricao)
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        self.go("ListaProdutos")

    def _nova_categoria(self):
        popup = tk.Toplevel(self)
        popup.title("Nova Categoria")
        popup.geometry("300x120")
        popup.transient(self)
        popup.grab_set()

        ttk.Label(popup, text="Nome da categoria:", style="Card.TLabel").pack(pady=(10, 4))
        e_nome = ttk.Entry(popup, width=30)
        e_nome.pack(pady=4)

        def salvar():
            nome = e_nome.get().strip()
            if nome:
                self.cc.criar(nome)
                popup.destroy()
                self.on_show()
            else:
                messagebox.showerror("Erro", "Digite um nome válido.")

        ttk.Button(popup, text="Salvar", style="Accent.TButton", command=salvar).pack(pady=10)