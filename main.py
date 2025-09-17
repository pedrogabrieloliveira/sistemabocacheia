import tkinter as tk
from tkinter import ttk, messagebox

# Models e Controllers
from models.database import Database
from controllers.usuario_controller import UsuarioController
from controllers.produto_controller import ProdutoController
from controllers.pedido_controller import PedidoController
from controllers.categoria_controller import CategoriaController
from controllers.cliente_controller import ClienteController

# Tema e Telas
from theme import apply_theme
from views.tela_boasvindas import TelaBoasVindas
from views.tela_login import TelaLogin
from views.tela_dashboard import TelaDashboard
from views.tela_lista_produtos import TelaListaProdutos
from views.tela_cadastro_produto import TelaCadastroProduto
from views.tela_lista_usuarios import TelaListaUsuarios
from views.tela_cadastro_usuario import TelaCadastroUsuario
from views.tela_pedidos import TelaPedidos
from views.tela_novo_pedido import TelaNovoPedido
from views.tela_detalhes_pedido import TelaDetalhesPedido
from views.tela_relatorios import TelaRelatorios
from views.tela_configuracoes import TelaConfiguracoes
from views.tela_sobre import TelaSobre
from views.tela_saida import TelaSaida
from views.tela_cardapio import TelaCardapio

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Boca Cheia - Sistema de Gestão")
        self.geometry("1024x720")
        self.minsize(960, 640)
        apply_theme(self)

        self.current_user = None

        # Instância do banco e controllers
        db = Database()
        self.uc = UsuarioController(db)
        self.cc = CategoriaController(db)
        self.cli = ClienteController(db)
        self.ped = PedidoController(db)
        self.pc = ProdutoController(db)

        # Container principal
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        def go(nome, context=None):
            self.show(nome, context)

        # Telas
        self.frames["BoasVindas"] = TelaBoasVindas(container, go)
        self.frames["Login"] = TelaLogin(container, self.uc, go)
        self.frames["Dashboard"] = TelaDashboard(container, self.pc, self.ped, go)
        self.frames["Cardapio"] = TelaCardapio(container, self.pc, self.cc, go)
        self.frames["ListaProdutos"] = TelaListaProdutos(container, self.pc, go)
        self.frames["CadastroProduto"] = TelaCadastroProduto(container, self.pc, self.cc, go)
        self.frames["ListaUsuarios"] = TelaListaUsuarios(container, self.uc, go)
        self.frames["CadastroUsuario"] = TelaCadastroUsuario(container, self.uc, go)
        self.frames["Pedidos"] = TelaPedidos(container, self.ped, go)
        self.frames["NovoPedido"] = TelaNovoPedido(container, self.cli, self.pc, self.ped, go)  # ✅ CORRIGIDO
        self.frames["DetalhesPedido"] = TelaDetalhesPedido(container, self.ped, self.pc, go)
        self.frames["Relatorios"] = TelaRelatorios(container, self.ped, go)
        self.frames["Configuracoes"] = TelaConfiguracoes(container, go)
        self.frames["Sobre"] = TelaSobre(container, go)
        self.frames["Saida"] = TelaSaida(container, go)

        # Posiciona todas as telas
        for f in self.frames.values():
            f.grid(row=0, column=0, sticky="nsew")

        # Tela inicial
        self.show("BoasVindas")

    def show(self, nome, context=None):
        restritas = {
            "ListaUsuarios": "admin",
            "CadastroUsuario": "admin",
            "Relatorios": "admin",
            "Configuracoes": "admin"
        }

        if nome in restritas:
            if not self.current_user or self.current_user["cargo"] != restritas[nome]:
                messagebox.showwarning("Acesso negado", "Você não tem permissão para acessar esta tela.")
                return

        frame = self.frames.get(nome)
        if not frame:
            frame = self.frames.get("Dashboard", next(iter(self.frames.values())))

        on_show = getattr(frame, "on_show", None)
        if callable(on_show):
            try:
                if context is None:
                    on_show()
                else:
                    on_show(context)
            except TypeError:
                on_show()

        frame.tkraise()

if __name__ == "__main__":
    App().mainloop()