from tkinter import ttk, messagebox

class TelaConfiguracoes(ttk.Frame):
    def __init__(self, master, go_callback):
        super().__init__(master)
        self.go = go_callback

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(10,10))

        ttk.Label(header, text="Configurações", style="Title.TLabel").pack(side="left", padx=10)

        # Botão Voltar
        ttk.Button(header, text="Voltar", style="Ghost.TButton",
                   command=lambda: self.go("Dashboard")).pack(side="right", padx=10)

        box = ttk.Frame(self, style="Card.TFrame")
        box.pack(fill="x", padx=10, pady=10)

        ttk.Label(box, text="Preferências do sistema", style="Card.TLabel").pack(anchor="w", padx=12, pady=10)
        ttk.Button(box, text="Limpar cache (demo)", style="Accent.TButton",
                   command=lambda: messagebox.showinfo("OK", "Cache limpo com sucesso!")).pack(anchor="w", padx=12, pady=8)