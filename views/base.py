# views/base.py
import tkinter as tk
from tkinter import ttk
from theme import apply_theme, TITLE

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        apply_theme(self)
        self.title(TITLE)
        self.geometry("1100x720")
        self.current_user = None

        self.frames = {}
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=14, pady=14)

    def register(self, name: str, frame: ttk.Frame):
        self.frames[name] = frame

    def show(self, name: str):
        # Esconde todos e mostra só o escolhido
        for child in self.container.winfo_children():
            child.pack_forget()
        frame = self.frames[name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.pack(fill="both", expand=True)

class BaseView(ttk.Frame):
    def __init__(self, parent, app: App, title: str):
        super().__init__(parent, style="TFrame")
        self.app = app
        self.title_text = title
        self._build_header()

    def _build_header(self):
        # Header usa pack
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))

        ttk.Label(header, text=self.title_text, style="Title.TLabel").pack(side="left")
        if self.app.current_user:
            ttk.Label(
                header,
                text=f"{self.app.current_user['nome']} ({self.app.current_user['perfil']})",
                style="Sub.TLabel"
            ).pack(side="right")

    def build_nav(self, parent=None):
        # Navbar usa pack
        parent = parent or self
        nav = ttk.Frame(parent)
        nav.pack(fill="x", pady=(0, 10))

        buttons = [
            ("Dashboard", "Dashboard"),
            ("Sair", "Logout"),
        ]
        for text, target in buttons:
            ttk.Button(nav, text=text, style="Ghost.TButton", command=lambda t=target: self.app.show(t)).pack(side="left", padx=4)

        return nav

    def refresh(self):
        pass