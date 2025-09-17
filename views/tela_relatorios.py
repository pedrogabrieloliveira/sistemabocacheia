from tkinter import ttk
from datetime import datetime

class TelaRelatorios(ttk.Frame):
    def __init__(self, master, pedido_controller, go_callback):
        super().__init__(master)
        self.ped = pedido_controller
        self.go = go_callback

        # Cabeçalho
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(40, 20), padx=40)

        ttk.Label(header, text="📊 Relatórios de Vendas", style="Title.TLabel").pack(side="left")

        ttk.Button(header, text="← Voltar ao Dashboard", style="Ghost.TButton",
                   command=lambda: self.go("Dashboard")).pack(side="right")

        # Área de conteúdo centralizada
        self.box = ttk.Frame(self, style="Card.TFrame")
        self.box.pack(padx=80, pady=30, fill="x")

        # Rodapé com data
        self.footer = ttk.Label(self, text="", style="Subtitle.TLabel")
        self.footer.pack(pady=(10, 30))

    def on_show(self):
        for w in self.box.winfo_children():
            w.destroy()

        pedidos = self.ped.listar()
        total = sum(p["vl_total_pedido"] for p in pedidos) if pedidos else 0
        ticket_medio = total / len(pedidos) if pedidos else 0

        status_map = {"aberto": 0, "finalizado": 0, "cancelado": 0}
        for p in pedidos:
            status = p["status"]
            if status in status_map:
                status_map[status] += 1

        # Bloco de resumo
        resumo = ttk.Frame(self.box)
        resumo.pack(anchor="center", pady=(0, 30))

        ttk.Label(resumo, text=f"📦 Total de pedidos: {len(pedidos)}", style="Card.TLabel").pack(pady=8)
        ttk.Label(resumo, text=f"💰 Receita total: R$ {total:.2f}", style="Card.TLabel").pack(pady=8)
        ttk.Label(resumo, text=f"📈 Ticket médio: R$ {ticket_medio:.2f}", style="Card.TLabel").pack(pady=8)

        # Separador visual
        ttk.Separator(self.box, orient="horizontal").pack(fill="x", pady=10)

        # Bloco de status
        status_frame = ttk.Frame(self.box)
        status_frame.pack(anchor="center", pady=(10, 20))

        ttk.Label(status_frame, text="📌 Status dos pedidos:", style="Subtitle.TLabel").pack(pady=(0, 10))
        ttk.Label(status_frame, text=f"🟡 Abertos: {status_map['aberto']}", style="Card.TLabel").pack(pady=6)
        ttk.Label(status_frame, text=f"✅ Finalizados: {status_map['finalizado']}", style="Card.TLabel").pack(pady=6)
        ttk.Label(status_frame, text=f"❌ Cancelados: {status_map['cancelado']}", style="Card.TLabel").pack(pady=6)

        # Rodapé com data
        hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.footer.config(text=f"Última atualização: {hoje}")