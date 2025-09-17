from tkinter import ttk

class TelaSaida(ttk.Frame):
    def __init__(self, master, go_callback):
        super().__init__(master)
        self.go = go_callback
        ttk.Label(self, text="Você saiu do sistema.", style="Sub.TLabel").pack(pady=20)

    def on_show(self):
        self.go("Login")