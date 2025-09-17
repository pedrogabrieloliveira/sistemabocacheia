import tkinter as tk
from tkinter import ttk

PRIMARY = "#FF6B35"
PRIMARY_DARK = "#E05324"
ACCENT = "#2FBF71"
BG = "#FFF8F3"
FG = "#2B2B2B"
MUTED = "#6B6B6B"
CARD = "#FFFFFF"
BORDER = "#EDE0DA"

TITLE = "Boca Cheia"

FONT_TITLE = ("Poppins", 20, "bold")
FONT_SUB = ("Poppins", 12)
FONT_BODY = ("Poppins", 11)

def apply_theme(root: tk.Tk):
    root.configure(bg=BG)
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=CARD, bordercolor=BORDER, relief="solid", borderwidth=1)

    style.configure("TLabel", background=BG, foreground=FG, font=FONT_BODY)
    style.configure("Title.TLabel", background=BG, foreground=FG, font=FONT_TITLE)
    style.configure("Sub.TLabel", background=BG, foreground=MUTED, font=FONT_SUB)
    style.configure("Card.TLabel", background=CARD, foreground=FG, font=FONT_BODY)
    style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=FONT_BODY)

    style.configure("TButton", font=FONT_BODY, padding=8, background=PRIMARY, foreground="white", borderwidth=0)
    style.map("TButton", background=[("active", PRIMARY_DARK)])

    style.configure("Accent.TButton", background=ACCENT, foreground="white")
    style.map("Accent.TButton", background=[("active", "#26A15E")])

    style.configure("Ghost.TButton", background=BG, foreground=PRIMARY, borderwidth=1, relief="solid")
    style.map("Ghost.TButton", background=[("active", "#FFE6DC")])

    style.configure("TEntry", padding=6, fieldbackground="white")
    style.configure("TCombobox", padding=6, fieldbackground="white")

    style.configure("Treeview",
        font=FONT_BODY,
        rowheight=28,
        background="white",
        fieldbackground="white",
        foreground=FG
    )
    style.configure("Treeview.Heading", font=("Poppins", 11, "bold"))
    style.map("Treeview", background=[("selected", "#FFE6DC")])