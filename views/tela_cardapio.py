from tkinter import ttk
from PIL import Image, ImageTk
import os

class TelaCardapio(ttk.Frame):
    def __init__(self, master, produto_controller, categoria_controller, go_callback):
        super().__init__(master)
        self.pc = produto_controller
        self.cc = categoria_controller
        self.go = go_callback
        self.imagens = []

        # Filtros
        filtros = ttk.Frame(self)
        filtros.pack(pady=(20, 0))

        ttk.Label(filtros, text="🔍 Buscar:", style="Card.TLabel").pack(side="left", padx=(0, 6))
        self.e_busca = ttk.Entry(filtros, width=30)
        self.e_busca.pack(side="left", padx=(0, 20))

        ttk.Label(filtros, text="📂 Categoria:", style="Card.TLabel").pack(side="left", padx=(0, 6))
        self.cb_categoria = ttk.Combobox(filtros, state="readonly", width=20)
        self.cb_categoria.pack(side="left")

        ttk.Button(filtros, text="Filtrar", style="Accent.TButton", command=self._filtrar).pack(side="left", padx=10)

        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "..", "imagens", "logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((180, 180))
            self.logo = ImageTk.PhotoImage(img)
            ttk.Label(self, image=self.logo).pack(pady=(10, 10))

        # Cabeçalho com título e botão voltar
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(10, 10), padx=20)

        ttk.Label(header, text="🍽️ Cardápio", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="← Voltar", style="Ghost.TButton",
                   command=lambda: self.go("Dashboard")).pack(side="right")

        # Área de produtos
        self.container = ttk.Frame(self)
        self.container.pack(padx=40, pady=10, fill="both", expand=True)

    def on_show(self, context=None):
        self._carregar_categorias()
        self.e_busca.delete(0, "end")
        self.cb_categoria.set("")
        self._exibir_produtos(self.pc.listar())

    def _carregar_categorias(self):
        categorias = self.cc.listar()
        nomes = [f"{c['id_categoria']} - {c['nome']}" for c in categorias]
        self.cb_categoria["values"] = [""] + nomes

    def _filtrar(self):
        nome = self.e_busca.get().strip().lower()
        cat_val = self.cb_categoria.get()
        id_categoria = None

        if cat_val:
            try:
                id_categoria = int(cat_val.split(" - ")[0])
            except:
                pass

        produtos = self.pc.listar()
        filtrados = []

        for p in produtos:
            if nome and nome not in p["nome"].lower():
                continue
            if id_categoria and p["id_categoria"] != id_categoria:
                continue
            filtrados.append(p)

        self._exibir_produtos(filtrados)

    def _exibir_produtos(self, produtos):
        for w in self.container.winfo_children():
            w.destroy()
        self.imagens.clear()

        if not produtos:
            ttk.Label(self.container, text="Nenhum produto encontrado.",
                      style="Subtitle.TLabel").pack(pady=20)
            return

        for p in produtos:
            frame = ttk.Frame(self.container, style="Card.TFrame")
            frame.pack(fill="x", pady=10)

            # Imagem
            img_path = p.get("imagem")
            if img_path and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    img = img.resize((100, 100))
                    photo = ImageTk.PhotoImage(img)
                    self.imagens.append(photo)
                    ttk.Label(frame, image=photo).pack(side="left", padx=10)
                except:
                    ttk.Label(frame, text="📷", style="Subtitle.TLabel").pack(side="left", padx=10)
            else:
                ttk.Label(frame, text="📷", style="Subtitle.TLabel").pack(side="left", padx=10)

            # Info
            info = ttk.Frame(frame)
            info.pack(side="left", padx=10)

            ttk.Label(info, text=p.get("nome", "Produto sem nome"), style="Subtitle.TLabel").pack(anchor="w")
            ttk.Label(info, text=f"R$ {p.get('preco', 0):.2f}", style="Card.TLabel").pack(anchor="w")
            if p.get("descricao"):
                ttk.Label(info, text=p["descricao"], style="Card.TLabel").pack(anchor="w")

            # Botão
            ttk.Button(frame, text="Adicionar ao pedido", style="Accent.TButton",
                       command=lambda pid=p["id_produto"]: self._adicionar(pid)).pack(side="right", padx=10)

    def _adicionar(self, produto_id):
        print(f"Produto {produto_id} adicionado ao pedido")