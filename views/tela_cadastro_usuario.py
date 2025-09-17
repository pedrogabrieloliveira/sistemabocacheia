from tkinter import ttk, messagebox, filedialog
import os

class TelaCadastroUsuario(ttk.Frame):
    def __init__(self, master, usuario_controller, go_callback):
        super().__init__(master)
        self.uc = usuario_controller
        self.go = go_callback
        self.foto_path: str | None = None
        self._build_ui()

    def _build_ui(self):
        card = ttk.Frame(self, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center", width=580, height=420)

        ttk.Label(card, text="Cadastro de Usuário", style="Title.TLabel").pack(pady=(16, 10))

        form = ttk.Frame(card, style="Card.TFrame"); form.pack(padx=20, pady=4, fill="x")

        # Nome
        ttk.Label(form, text="Nome", style="Card.TLabel").grid(row=0, column=0, sticky="w")
        self.e_nome = ttk.Entry(form, width=40); self.e_nome.grid(row=1, column=0, padx=(0, 16), pady=4)

        # Cargo
        ttk.Label(form, text="Cargo (admin/operacional)", style="Card.TLabel").grid(row=0, column=1, sticky="w")
        self.e_cargo = ttk.Combobox(form, values=["admin", "operacional"], width=20, state="readonly")
        self.e_cargo.grid(row=1, column=1, pady=4)

        # Usuário
        ttk.Label(form, text="Usuário (login)", style="Card.TLabel").grid(row=2, column=0, sticky="w")
        self.e_user = ttk.Entry(form, width=40); self.e_user.grid(row=3, column=0, padx=(0, 16), pady=4)

        # Senha
        ttk.Label(form, text="Senha", style="Card.TLabel").grid(row=2, column=1, sticky="w")
        self.e_pass = ttk.Entry(form, show="*", width=20); self.e_pass.grid(row=3, column=1, pady=4)

        # Foto
        foto_frame = ttk.Frame(form, style="Card.TFrame")
        foto_frame.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))

        ttk.Label(foto_frame, text="Foto do usuário", style="Card.TLabel").pack(anchor="w")
        row2 = ttk.Frame(foto_frame, style="Card.TFrame"); row2.pack(fill="x", pady=4)
        ttk.Button(row2, text="Selecionar foto", style="Ghost.TButton", command=self._selecionar_foto).pack(side="left")
        self.lbl_foto = ttk.Label(row2, text="Nenhum arquivo selecionado", style="Muted.TLabel")
        self.lbl_foto.pack(side="left", padx=8)

        # Botões
        btns = ttk.Frame(card, style="Card.TFrame"); btns.pack(pady=14)
        ttk.Button(btns, text="Salvar", style="Accent.TButton", command=self._salvar).pack(side="left", padx=6)
        ttk.Button(btns, text="Voltar", style="Ghost.TButton", command=lambda: self.go("Login")).pack(side="left", padx=6)

    def _selecionar_foto(self):
        path = filedialog.askopenfilename(
            title="Selecione a foto do usuário",
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("Todos os arquivos", "*.*")]
        )
        if path:
            self.foto_path = path
            self.lbl_foto.config(text=os.path.basename(path))

    def _salvar(self):
        nome = self.e_nome.get().strip()
        cargo = self.e_cargo.get().strip()
        usuario = self.e_user.get().strip()
        senha = self.e_pass.get().strip()

        # Validações básicas
        if not all([nome, cargo, usuario, senha]):
            messagebox.showwarning("Campos obrigatórios", "Preencha nome, cargo, usuário e senha.")
            return

        try:
            self.uc.cadastrar(nome, cargo, usuario, senha, self.foto_path)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.go("Login")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível cadastrar o usuário.\n{e}")