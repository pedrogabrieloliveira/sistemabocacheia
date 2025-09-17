from tkinter import ttk
from PIL import Image, ImageTk
import os
from theme import TITLE

class TelaSobre(ttk.Frame):
    def __init__(self, master, go_callback):
        super().__init__(master)
        self.go = go_callback

        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(10, 10))

        ttk.Label(header, text="Sobre", style="Title.TLabel").pack(side="left", padx=10)

        ttk.Button(header, text="Voltar", style="Ghost.TButton",
                   command=lambda: self.go("Dashboard")).pack(side="right", padx=10)

        # Logo centralizada
        logo_path = os.path.join(os.path.dirname(__file__), "..", "imagens", "logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((180, 180))  # Ajuste o tamanho conforme necessário
            self.logo = ImageTk.PhotoImage(img)
            ttk.Label(self, image=self.logo).pack(pady=(20, 10))

        # Caixa de informações
        box = ttk.Frame(self, style="Card.TFrame")
        box.pack(fill="x", padx=20, pady=10)

        ttk.Label(box, text=f"{TITLE} — Sistema de gestão para empreendimento alimentício.",
                  style="Card.TLabel").pack(anchor="w", padx=12, pady=10)

        ttk.Label(box, text="Versão 1.0.0", style="Muted.TLabel").pack(anchor="w", padx=12, pady=4)

        ttk.Label(box, text="Desenvolvido por alunos do Senac.", style="Muted.TLabel").pack(anchor="w", padx=12, pady=4)

        ttk.Label(box, text="© 2025 Boca Cheia Software", style="Muted.TLabel").pack(anchor="w", padx=12, pady=4)