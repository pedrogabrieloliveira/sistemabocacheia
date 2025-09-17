from tkinter import ttk, messagebox

class TelaLogin(ttk.Frame):
    def __init__(self, master, usuario_controller, go_callback):
        super().__init__(master)
        self.uc = usuario_controller
        self.go = go_callback
        self._build_ui()

    def _build_ui(self):
        card = ttk.Frame(self, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=320)

        ttk.Label(card, text="Login - Boca Cheia", style="Title.TLabel").pack(pady=(20, 10))

        ttk.Label(card, text="Usuário").pack(anchor="w", padx=24)
        self.e_user = ttk.Entry(card, width=40)
        self.e_user.pack(padx=24, pady=4)

        ttk.Label(card, text="Senha").pack(anchor="w", padx=24)
        self.e_pass = ttk.Entry(card, show="*", width=40)
        self.e_pass.pack(padx=24, pady=4)

        btns = ttk.Frame(card)
        btns.pack(pady=16)
        ttk.Button(btns, text="Entrar", command=self._login).pack(side="left", padx=4)
        ttk.Button(btns, text="Cadastrar Usuário", style="Ghost.TButton",
                   command=lambda: self.go("CadastroUsuario")).pack(side="left", padx=4)

    def _login(self):
        usuario = self.e_user.get().strip()
        senha = self.e_pass.get().strip()
        if not usuario or not senha:
            messagebox.showwarning("Campos obrigatórios", "Preencha usuário e senha.")
            return
        try:
            if self.uc.login(usuario, senha):
                user_data = self.uc.get_by_username(usuario)
                # Guarda no App
                self.master.master.current_user = user_data
                messagebox.showinfo("Sucesso", f"Bem-vindo, {user_data['nome']}!")
                self.go("Dashboard")
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao tentar logar.\n{e}")