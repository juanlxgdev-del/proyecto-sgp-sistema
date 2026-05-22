"""
SGP - Ventana Principal
Navegación lateral adaptada por rol (Administrador / Trabajador)
"""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from frontend.styles import *
from frontend.modulo_ventas import ModuloVentas
from frontend.modulo_inventario import ModuloInventario
from frontend.modulo_caja_chica import ModuloCajaChica
from frontend.modulo_clientes import ModuloClienteControl
from frontend.modulo_usuarios import ModuloUsuarios
from frontend.modulo_reportes import ModuloReportes


class VentanaPrincipal(tk.Tk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.es_admin = usuario.rol == "Administrador"
        self.modulo_activo = None

        self.title(f"SGP — {usuario.nombre} ({usuario.rol})")
        self.geometry("1200x720")
        self.minsize(900, 600)
        self.configure(bg=NAVY)

        self._construir()
        self.state('zoomed') # Pantalla completa

        # Módulo inicial
        if self.es_admin:
            self._ir_a("reportes")
        else:
            self._ir_a("ventas")

    def _construir(self):
        # ── Sidebar ────────────────────────────────────────
        self.sidebar = tk.Frame(self, bg=NAVY_MED, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo en sidebar
        logo_frame = tk.Frame(self.sidebar, bg=BLUE, pady=16)
        logo_frame.pack(fill="x")
        # Obtener la ruta del logo de manera dinámica y portátil
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_logo_main = os.path.join(BASE_DIR, "Logotipos", "Logo menu.png")
        if os.path.exists(path_logo_main):
            try:
                img = Image.open(path_logo_main)
                w, h = img.size
                # Ajustar al ancho del sidebar (220px) con una escala de 190px de alta calidad
                new_w = 190
                new_h = int(h * (new_w / w))
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                self.photo_logo_main = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(logo_frame, image=self.photo_logo_main, bg=BLUE)
                lbl_img.pack(pady=(0, 6))
            except Exception as e:
                # Fallback en caso de error de lectura
                tk.Label(logo_frame, text="📋", bg=BLUE, fg=WHITE, font=("Arial", 24)).pack()
                tk.Label(logo_frame, text="SGP", bg=BLUE, fg=WHITE, font=("Georgia", 16, "bold")).pack()
        else:
            # Fallback en caso de que no exista el archivo de imagen
            tk.Label(logo_frame, text="📋", bg=BLUE, fg=WHITE, font=("Arial", 24)).pack()
            tk.Label(logo_frame, text="SGP", bg=BLUE, fg=WHITE, font=("Georgia", 16, "bold")).pack()
        tk.Label(logo_frame, text=self.usuario.nombre, bg=BLUE, fg=ICE,
                 font=FONT_SMALL, wraplength=180).pack(pady=(4, 0))
        tk.Label(logo_frame, text=f"● {self.usuario.rol}",
                 bg=BLUE, fg=GOLD, font=FONT_SMALL).pack()

        # Separador
        tk.Frame(self.sidebar, bg=NAVY_LIGHT, height=1).pack(fill="x", pady=8)

        # Menú adaptado al rol
        self.botones_nav = {}
        nav_items = self._obtener_items_nav()
        for key, icono, texto in nav_items:
            btn = tk.Button(
                self.sidebar, text=f"{icono}  {texto}",
                command=lambda k=key: self._ir_a(k),
                bg=NAVY_MED, fg=ICE, font=FONT_BTN,
                relief="flat", anchor="w", cursor="hand2",
                padx=16, pady=10, bd=0,
                activebackground=BLUE, activeforeground=WHITE
            )
            btn.pack(fill="x")
            self.botones_nav[key] = btn

        # Spacer + Cerrar sesión
        tk.Frame(self.sidebar, bg=NAVY_MED).pack(fill="both", expand=True)
        tk.Frame(self.sidebar, bg=NAVY_LIGHT, height=1).pack(fill="x")
        tk.Button(
            self.sidebar, text="⬅  Cerrar Sesión",
            command=self._cerrar_sesion,
            bg=NAVY_MED, fg=RED, font=FONT_BTN,
            relief="flat", anchor="w", cursor="hand2",
            padx=16, pady=12, bd=0,
            activebackground="#3D1010", activeforeground=RED
        ).pack(fill="x")

        # ── Área de contenido ─────────────────────────────
        self.area = tk.Frame(self, bg=NAVY)
        self.area.pack(side="left", fill="both", expand=True)

    def _obtener_items_nav(self) -> list:
        items_trabajador = [
            ("ventas",    "🛒", "Ventas"),
            ("inventario","📦", "Consultar Inventario"),
            ("caja_chica","💰", "Caja Chica"),
            ("clientes",  "🧑", "ClienteControl"),
        ]
        items_admin = [
            ("reportes",  "📊", "Dashboard / Reportes"),
            ("ventas",    "🛒", "Ventas"),
            ("inventario","📦", "Inventario"),
            ("caja_chica","💰", "Caja Chica"),
            ("clientes",  "🧑", "ClienteControl"),
            ("usuarios",  "👥", "Gestión de Usuarios"),
        ]
        return items_admin if self.es_admin else items_trabajador

    def _ir_a(self, key: str):
        # Limpiar área
        for w in self.area.winfo_children():
            w.destroy()

        # Resaltar botón activo
        for k, btn in self.botones_nav.items():
            if k == key:
                btn.config(bg=BLUE, fg=WHITE)
            else:
                btn.config(bg=NAVY_MED, fg=ICE)

        # Instanciar módulo
        modulos = {
            "ventas":     lambda: ModuloVentas(self.area, self.usuario),
            "inventario": lambda: ModuloInventario(self.area, self.usuario),
            "caja_chica": lambda: ModuloCajaChica(self.area, self.usuario),
            "clientes":   lambda: ModuloClienteControl(self.area, self.usuario),
            "usuarios":   lambda: ModuloUsuarios(self.area, self.usuario),
            "reportes":   lambda: ModuloReportes(self.area, self.usuario),
        }
        if key in modulos:
            modulo = modulos[key]()
            modulo.pack(fill="both", expand=True)
            self.modulo_activo = modulo

    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión",
                               "¿Deseas cerrar sesión?", parent=self):
            self.destroy()
            # Re-lanzar login
            import subprocess, sys
            subprocess.Popen([sys.executable, "main.py"])
