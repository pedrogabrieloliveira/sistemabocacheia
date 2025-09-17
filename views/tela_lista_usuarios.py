from tkinter import ttk, messagebox
import os

class TelaListaUsuarios(ttk.Frame):
    def __init__(self, master, usuario_controller, go_callback):
        super().__init__(master)
        self.uc = usuario_controller
        self.go = go_callback

        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(10,10))

        ttk.Label(header, text="Usuários", style="Title.TLabel").pack(side="left", padx=10)

        ttk.Button(header, text="Voltar", style="Ghost.TButton",
                   command=lambda: self.go("Dashboard")).pack(side="right", padx=10)

        ttk.Button(header, text="Novo", style="Accent.TButton",
                   command=lambda: self.go("CadastroUsuario")).pack(side="right", padx=10)

        # Tabela
        cols = ("id","nome","usuario","cargo","foto")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)

        heads = ("ID", "Nome", "Usuário", "Cargo", "Foto")
        for c, h in zip(cols, heads):
            self.tree.heading(c, text=h)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões de ação
        btns = ttk.Frame(self)
        btns.pack(anchor="e", pady=8)

        ttk.Button(btns, text="Excluir", command=self._excluir).pack(side="left", padx=4)
        ttk.Button(btns, text="Atualizar", command=self.on_show).pack(side="left", padx=4)

    def on_show(self, context=None):
        """Atualiza a lista de usuários"""
        for i in self.tree.get_children():
            self.tree.delete(i)

        for u in self.uc.listar():
            # Garante que não quebra se a coluna 'foto' estiver vazia ou None
            foto_name = ""
            if "foto" in u.keys() and u["foto"]:
                foto_name = os.path.basename(u["foto"])

            self.tree.insert(
                "",
                "end",
                values=(u["id_usuario"], u["nome"], u["usuario"], u["cargo"], foto_name)
            )

    def _excluir(self):
        """Exclui o usuário selecionado"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Selecione um usuário.")
            return

        uid = int(self.tree.item(sel[0])["values"][0])
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este usuário?"):
            try:
                self.uc.deletar(uid)
                self.on_show()
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir o usuário.\n{e}")