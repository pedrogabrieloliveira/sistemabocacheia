from tkinter import ttk
from PIL import Image, ImageTk
import os

class TelaBoasVindas(ttk.Frame):
    def __init__(self, master, go_callback):
        super().__init__(master)
        self.go = go_callback

        # Caminho da imagem
        logo_path = os.path.join(os.path.dirname(__file__), "..", "imagens", "logo.png")

        # Carrega e redimensiona a imagem
        img = Image.open(logo_path)
        img = img.resize((200, 200))  # Ajuste o tamanho conforme necessário
        self.logo = ImageTk.PhotoImage(img)

        # Container central
        container = ttk.Frame(self)
        container.pack(expand=True)

        # Exibe a logo
        ttk.Label(container, image=self.logo).pack(pady=(40, 10))

        # Título principal
        ttk.Label(container, text="Bem-vindo ao Boca Cheia", style="Title.TLabel").pack(pady=(0, 10))

        # Subtítulo
        ttk.Label(container, text="Sistema de Gestão para Restaurantes", style="Subtitle.TLabel").pack(pady=(0, 30))

        # Botão de entrada
        ttk.Button(container, text="Entrar no sistema", style="Accent.TButton",
                   command=lambda: self.go("Login")).pack()