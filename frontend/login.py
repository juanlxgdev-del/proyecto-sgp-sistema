"""
SGP - Ventana de Login
"""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from frontend.styles import *
from backend import data_manager as dm


class VentanaLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SGP – Sistema de Gestión Papelera")
        self.geometry("440x520")
        self.resizable(False, False)
        self.configure(bg=NAVY)
        self.usuario_autenticado = None
        self._construir()
        self.state('zoomed') # Pantalla completa

    def _construir(self):
        # Header decorativo
        header = tk.Frame(self, bg=BLUE, height=6)
        header.pack(fill="x")

        # Logo / Título
        logo_frame = tk.Frame(self, bg=NAVY, pady=20)
        logo_frame.pack(fill="x")

        # Obtener la ruta del logo de manera dinámica y portátil
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_logo = os.path.join(BASE_DIR, "Logotipos", "Logo principal.png")
        if os.path.exists(path_logo):
            try:
                img = Image.open(path_logo)
                w, h = img.size
                # Escalar de forma nítida y amplia para la pantalla de Login (incluso más grande)
                new_w = 440
                new_h = int(h * (new_w / w))
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                self.photo_logo = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(logo_frame, image=self.photo_logo, bg=NAVY)
                lbl_img.pack()
            except Exception as e:
                # Fallback si ocurre algún error de carga
                tk.Label(logo_frame, text="📋", bg=NAVY, fg=GOLD, font=("Arial", 38)).pack()
                tk.Label(logo_frame, text="SGP", bg=NAVY, fg=WHITE, font=("Georgia", 28, "bold")).pack()
        else:
            # Fallback si el archivo no existe
            tk.Label(logo_frame, text="📋", bg=NAVY, fg=GOLD, font=("Arial", 38)).pack()
            tk.Label(logo_frame, text="SGP", bg=NAVY, fg=WHITE, font=("Georgia", 28, "bold")).pack()

        # Separador
        tk.Frame(self, bg=NAVY_LIGHT, height=1).pack(fill="x", padx=30, pady=5)

        # Formulario
        form = tk.Frame(self, bg=NAVY, padx=50)
        form.pack(fill="both", expand=True)

        # Usuario
        tk.Label(form, text="Usuario", bg=NAVY, fg=ICE,
                 font=("Consolas", 10), anchor="w").pack(fill="x", pady=(18, 2))
        self.entry_usuario = tk.Entry(form, **{**ENTRY_STYLE, "font": ("Consolas", 12)})
        self.entry_usuario.pack(fill="x", ipady=8)

        # Contraseña
        tk.Label(form, text="Contraseña", bg=NAVY, fg=ICE,
                 font=("Consolas", 10), anchor="w").pack(fill="x", pady=(14, 2))
        self.entry_pass = tk.Entry(form, show="●",
                                    **{**ENTRY_STYLE, "font": ("Consolas", 12)})
        self.entry_pass.pack(fill="x", ipady=8)

        # Botón ingresar
        self.entry_pass.bind("<Return>", lambda e: self._login())
        self.entry_usuario.bind("<Return>", lambda e: self.entry_pass.focus())

        btn = tk.Button(form, text="INGRESAR →",
                        command=self._login,
                        bg=BLUE, fg=WHITE, font=("Consolas", 12, "bold"),
                        relief="flat", cursor="hand2",
                        pady=10, bd=0, activebackground=BLUE_LIGHT,
                        activeforeground=WHITE)
        btn.pack(fill="x", pady=(24, 0))

        self.lbl_error = tk.Label(form, text="", bg=NAVY, fg=RED,
                                   font=("Consolas", 9))
        self.lbl_error.pack(pady=6)

        # Footer
        tk.Frame(self, bg=BLUE, height=3).pack(fill="x", side="bottom")

    def _login(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_pass.get()

        if not usuario or not password:
            self.lbl_error.config(text="⚠ Ingresa usuario y contraseña")
            return

        u = dm.autenticar(usuario, password)
        if u:
            self.usuario_autenticado = u
            self.destroy()
        else:
            self.lbl_error.config(text="✖ Credenciales incorrectas")
            self.entry_pass.delete(0, "end")

    def obtener_usuario(self):
        return self.usuario_autenticado
