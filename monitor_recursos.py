import ctypes
import os
import shutil
import tempfile
import threading
import tkinter as tk
from tkinter import ttk
from pathlib import Path


APP_BG = "#0f172a"
CARD_BG = "#1e293b"
TEXT = "#f8fafc"
MUTED = "#94a3b8"
ACCENT = "#38bdf8"
GREEN = "#4ade80"
ORANGE = "#fb923c"


def format_bytes(value):
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(max(0, value))
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:,.2f} {unit}".replace(",", "X").replace(".", ",").replace("X", ".")
        value /= 1024
    return "0 B"


def memory_info():
    class MemoryStatus(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    status = MemoryStatus()
    status.dwLength = ctypes.sizeof(status)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
    total = status.ullTotalPhys
    free = status.ullAvailPhys
    return total, total - free, free, status.dwMemoryLoad


def folder_size(path):
    total = 0
    try:
        for root, dirs, files in os.walk(path, onerror=lambda e: None):
            dirs[:] = [d for d in dirs if d not in {"System Volume Information", "$Recycle.Bin"}]
            for name in files:
                try:
                    total += os.path.getsize(os.path.join(root, name))
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    return total


def disk_info(path):
    usage = shutil.disk_usage(path)
    return usage.total, usage.used, usage.free


class ResourceMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitor de Recursos do PC")
        self.geometry("700x540")
        self.minsize(620, 470)
        self.configure(bg=APP_BG)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.cards = {}
        self.value_labels = {}
        self.progress_bars = {}
        self.create_styles()
        self.create_ui()
        self.update_data()

    def create_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Resource.Horizontal.TProgressbar", troughcolor="#334155", background=ACCENT, bordercolor="#334155", lightcolor=ACCENT, darkcolor=ACCENT, thickness=10)
        style.configure("Temp.Horizontal.TProgressbar", troughcolor="#334155", background=ORANGE, bordercolor="#334155", lightcolor=ORANGE, darkcolor=ORANGE, thickness=10)

    def create_ui(self):
        header = tk.Frame(self, bg=APP_BG)
        header.pack(fill="x", padx=28, pady=(24, 14))
        tk.Label(header, text="Monitor de Recursos", font=("Segoe UI", 24, "bold"), fg=TEXT, bg=APP_BG).pack(anchor="w")
        tk.Label(header, text="Acompanhe a memória e o armazenamento do computador em tempo real", font=("Segoe UI", 10), fg=MUTED, bg=APP_BG).pack(anchor="w", pady=(5, 0))

        body = tk.Frame(self, bg=APP_BG)
        body.pack(fill="both", expand=True, padx=28)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)

        self.add_card(body, 0, 0, "MEMÓRIA RAM", "ram", ACCENT)
        self.add_card(body, 0, 1, "ARMAZENAMENTO PRINCIPAL", "disk", GREEN)
        self.add_card(body, 1, 0, "ARMAZENAMENTO TEMPORÁRIO", "temp", ORANGE)

        info = tk.Frame(body, bg=CARD_BG, padx=20, pady=18)
        info.grid(row=1, column=1, padx=(8, 0), pady=(8, 8), sticky="nsew")
        tk.Label(info, text="ATUALIZAÇÃO", font=("Segoe UI", 10, "bold"), fg=MUTED, bg=CARD_BG).pack(anchor="w")
        self.update_label = tk.Label(info, text="Calculando...", font=("Segoe UI", 16, "bold"), fg=TEXT, bg=CARD_BG)
        self.update_label.pack(anchor="w", pady=(18, 4))
        tk.Label(info, text="Os dados são atualizados automaticamente a cada 2 segundos.", font=("Segoe UI", 9), fg=MUTED, bg=CARD_BG, wraplength=250, justify="left").pack(anchor="w")
        tk.Label(info, text="Aplicativo local — nenhuma informação é enviada.", font=("Segoe UI", 9), fg=MUTED, bg=CARD_BG, wraplength=250, justify="left").pack(anchor="w", pady=(14, 0))

        footer = tk.Frame(self, bg=APP_BG)
        footer.pack(fill="x", padx=28, pady=(8, 20))
        self.status_label = tk.Label(footer, text="Pronto", font=("Segoe UI", 9), fg=MUTED, bg=APP_BG)
        self.status_label.pack(anchor="w")

    def add_card(self, parent, row, column, title, key, color):
        card = tk.Frame(parent, bg=CARD_BG, padx=20, pady=18)
        card.grid(row=row, column=column, padx=(0 if column == 0 else 8, 8 if column == 0 else 0), pady=(0 if row == 0 else 8, 8), sticky="nsew")
        tk.Label(card, text=title, font=("Segoe UI", 10, "bold"), fg=MUTED, bg=CARD_BG).pack(anchor="w")
        value = tk.Label(card, text="Calculando...", font=("Segoe UI", 18, "bold"), fg=color, bg=CARD_BG)
        value.pack(anchor="w", pady=(14, 2))
        detail = tk.Label(card, text="", font=("Segoe UI", 9), fg=TEXT, bg=CARD_BG)
        detail.pack(anchor="w")
        bar = ttk.Progressbar(card, style="Temp.Horizontal.TProgressbar" if key == "temp" else "Resource.Horizontal.TProgressbar", maximum=100, value=0)
        bar.pack(fill="x", pady=(16, 0))
        self.cards[key] = card
        self.value_labels[key] = (value, detail)
        self.progress_bars[key] = bar

    def update_data(self):
        try:
            ram_total, ram_used, ram_free, ram_percent = memory_info()
            disk_path = os.environ.get("SystemDrive", "C:") + "\\"
            disk_total, disk_used, disk_free = disk_info(disk_path)
            temp_path = tempfile.gettempdir()
            temp_total, temp_used, temp_free = disk_info(temp_path)
            temp_size = folder_size(temp_path)

            self.value_labels["ram"][0].config(text=f"{format_bytes(ram_used)} em uso")
            self.value_labels["ram"][1].config(text=f"Total: {format_bytes(ram_total)}  •  Livre: {format_bytes(ram_free)}")
            self.progress_bars["ram"]["value"] = ram_percent

            disk_percent = (disk_used / disk_total * 100) if disk_total else 0
            self.value_labels["disk"][0].config(text=f"{format_bytes(disk_free)} livres")
            self.value_labels["disk"][1].config(text=f"Total: {format_bytes(disk_total)}  •  Usado: {format_bytes(disk_used)}")
            self.progress_bars["disk"]["value"] = disk_percent

            temp_percent = (temp_used / temp_total * 100) if temp_total else 0
            self.value_labels["temp"][0].config(text=f"{format_bytes(temp_size)} em arquivos")
            self.value_labels["temp"][1].config(text=f"Livre no volume temporário: {format_bytes(temp_free)}")
            self.progress_bars["temp"]["value"] = temp_percent

            self.update_label.config(text="Atualizado agora")
            self.status_label.config(text=f"Pasta temporária: {temp_path}")
        except Exception as error:
            self.update_label.config(text="Não foi possível ler os dados")
            self.status_label.config(text=f"Erro: {error}")
        finally:
            self.after(2000, self.update_data)


if __name__ == "__main__":
    ResourceMonitor().mainloop()
