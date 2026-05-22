"""
SGP - Módulo de Usuarios (solo Administrador)
"""
import tkinter as tk
from tkinter import ttk, messagebox
from backend import data_manager as dm
from backend.models import Administrador, Trabajador
from frontend.styles import *
from frontend.widgets import (
    label_title, entry_field, btn_primary, btn_danger, btn_success,
    btn_ghost, tabla_con_scroll, aplicar_tema_treeview, dialogo_simple
)


class ModuloUsuarios(tk.Frame):
    def __init__(self, parent, usuario, **kw):
        super().__init__(parent, bg=NAVY, **kw)
        self.usuario = usuario
        self._construir()

    def _construir(self):
        style = ttk.Style()
        aplicar_tema_treeview(style)

        barra = tk.Frame(self, bg=BLUE, pady=8)
        barra.pack(fill="x")
        tk.Label(barra, text="👥  GESTIÓN DE USUARIOS",
                 bg=BLUE, fg=WHITE, font=FONT_TITLE).pack(side="left", padx=16)

        toolbar = tk.Frame(self, bg=NAVY_MED, pady=6, padx=10)
        toolbar.pack(fill="x")
        btn_success(toolbar, "➕ Nuevo Usuario", self._nuevo_usuario).pack(side="left", padx=2)
        btn_danger(toolbar, "🗑 Eliminar", self._eliminar_usuario).pack(side="left", padx=2)
        btn_primary(toolbar, "🔑 Cambiar Contraseña", self._cambiar_pass).pack(side="left", padx=2)
        btn_ghost(toolbar, "🔄 Actualizar", self._cargar_usuarios).pack(side="right")

        cols = ("ID", "Nombre", "Rol")
        self.tree_usuarios, cont = tabla_con_scroll(self, cols)
        cont.pack(fill="both", expand=True, padx=10, pady=8)
        for col, w in zip(cols, (50, 250, 150)):
            self.tree_usuarios.heading(col, text=col)
            self.tree_usuarios.column(col, width=w, anchor="center")
        self.tree_usuarios.tag_configure("admin", foreground=GOLD)

        self._cargar_usuarios()

    def _cargar_usuarios(self):
        self.tree_usuarios.delete(*self.tree_usuarios.get_children())
        for u in dm.cargar_usuarios():
            tag = "admin" if u.rol == "Administrador" else ""
            self.tree_usuarios.insert("", "end", iid=str(u.id_usuario), values=(
                u.id_usuario, u.nombre, u.rol
            ), tags=(tag,))

    def _nuevo_usuario(self):
        datos = dialogo_simple(self, "Nuevo Usuario", [
            ("Nombre de usuario",  "text",     ""),
            ("Contraseña",         "password", ""),
            ("Rol", "combo:Trabajador,Administrador", "Trabajador"),
        ])
        if not datos: return
        try:
            nombre = datos["Nombre de usuario"].strip()
            passwd = datos["Contraseña"]
            rol = datos["Rol"]
            if not nombre or not passwd: raise ValueError("Campos vacíos")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e), parent=self)
            return

        nid = dm.siguiente_id_usuario()
        if rol == "Administrador":
            u = Administrador(nid, nombre, passwd)
        else:
            u = Trabajador(nid, nombre, passwd)

        if dm.agregar_usuario(u):
            messagebox.showinfo("Éxito", f"Usuario '{nombre}' creado.", parent=self)
            self._cargar_usuarios()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario.", parent=self)

    def _eliminar_usuario(self):
        sel = self.tree_usuarios.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un usuario.", parent=self)
            return
        uid = int(sel[0])
        if uid == self.usuario.id_usuario:
            messagebox.showerror("Error", "No puedes eliminarte a ti mismo.", parent=self)
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar usuario ID {uid}?", parent=self):
            dm.eliminar_usuario(uid)
            self._cargar_usuarios()

    def _cambiar_pass(self):
        sel = self.tree_usuarios.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un usuario.", parent=self)
            return
        uid = int(sel[0])
        datos = dialogo_simple(self, "Nueva Contraseña", [
            ("Nueva Contraseña", "password", ""),
        ])
        if not datos: return
        nueva = datos["Nueva Contraseña"]
        if not nueva:
            messagebox.showerror("Error", "Contraseña vacía.", parent=self)
            return
        usuarios = dm.cargar_usuarios()
        for u in usuarios:
            if u.id_usuario == uid:
                u.cambiar_contraseña(nueva)
        dm.guardar_usuarios(usuarios)
        messagebox.showinfo("Éxito", "Contraseña actualizada.", parent=self)
