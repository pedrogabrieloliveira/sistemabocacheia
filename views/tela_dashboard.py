from tkinter import ttk

class TelaDashboard(ttk.Frame):
    def __init__(self, master, produto_controller, pedido_controller, go_callback):
        super().__init__(master)
        self.pc = produto_controller
        self.ped = pedido_controller
        self.go = go_callback

        # Título principal
        ttk.Label(self, text="Painel Principal", style="Title.TLabel").pack(pady=(30, 10))

        # Subtítulo
        ttk.Label(self, text="Escolha uma opção abaixo", style="Subtitle.TLabel").pack(pady=(0, 20))

        # Área de botões
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        # Linha 1
        linha1 = ttk.Frame(btn_frame)
        linha1.pack(pady=5)

        ttk.Button(linha1, text="👤 Usuários", style="TButton",
                   command=lambda: self.go("ListaUsuarios")).pack(side="left", padx=10)

        ttk.Button(linha1, text="📦 Produtos", style="TButton",
                   command=lambda: self.go("ListaProdutos")).pack(side="left", padx=10)

        ttk.Button(linha1, text="🧾 Pedidos", style="TButton",
                   command=lambda: self.go("Pedidos")).pack(side="left", padx=10)

        # Linha 2
        linha2 = ttk.Frame(btn_frame)
        linha2.pack(pady=5)

        ttk.Button(linha2, text="👥 Clientes", style="TButton",
                   command=lambda: self.go("NovoPedido")).pack(side="left", padx=10)

        ttk.Button(linha2, text="📊 Relatórios", style="TButton",
                   command=lambda: self.go("Relatorios")).pack(side="left", padx=10)

        ttk.Button(linha2, text="⚙ Configurações", style="TButton",
                   command=lambda: self.go("Configuracoes")).pack(side="left", padx=10)

        # Linha 3
        linha3 = ttk.Frame(btn_frame)
        linha3.pack(pady=5)

        ttk.Button(linha3, text="🍽️ Cardápio", style="TButton",
                   command=lambda: self.go("Cardapio")).pack(side="left", padx=10)

        ttk.Button(linha3, text="ℹ️ Sobre o sistema", style="TButton",
                   command=lambda: self.go("Sobre")).pack(side="left", padx=10)

        # Rodapé
        ttk.Button(self, text="❌ Sair do sistema", style="Ghost.TButton",
                   command=lambda: self.go("Saida")).pack(pady=30)

    def on_show(self, context=None):
        pass  # Se quiser atualizar algo ao entrar no painel, coloque aqui