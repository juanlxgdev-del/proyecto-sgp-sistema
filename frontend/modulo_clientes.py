"""
SGP - Módulo ClienteControl (Deudores)
"""
import tkinter as tk
from tkinter import ttk, messagebox
from backend import data_manager as dm
from backend.models import ClienteControl
from frontend.styles import *
from frontend.widgets import (
    label_title, entry_field, btn_primary, btn_danger, btn_success,
    btn_ghost, tabla_con_scroll, aplicar_tema_treeview, dialogo_simple
)


class ModuloClienteControl(tk.Frame):
    def __init__(self, parent, usuario, **kw):
        super().__init__(parent, bg=NAVY, **kw)
        self.usuario = usuario
        self.es_admin = usuario.rol == "Administrador"
        self._construir()

    def _construir(self):
        style = ttk.Style()
        aplicar_tema_treeview(style)

        barra = tk.Frame(self, bg=BLUE, pady=8)
        barra.pack(fill="x")
        tk.Label(barra, text="🧑  CLIENTECONTROL — Deudores",
                 bg=BLUE, fg=WHITE, font=FONT_TITLE).pack(side="left", padx=16)

        # Aviso ético
        aviso = tk.Frame(self, bg="#1A2F1A", pady=4, padx=12)
        aviso.pack(fill="x")
        tk.Label(aviso,
                 text="ℹ  Módulo ético: registro voluntario para control de adeudos y seguridad del personal.",
                 bg="#1A2F1A", fg="#6FCF97", font=FONT_SMALL).pack(anchor="w")

        # Toolbar
        toolbar = tk.Frame(self, bg=NAVY_MED, pady=6, padx=10)
        toolbar.pack(fill="x")
        btn_success(toolbar, "➕ Nuevo Cliente", self._nuevo_cliente).pack(side="left", padx=2)
        btn_primary(toolbar, "✏ Actualizar Deuda", self._actualizar_deuda).pack(side="left", padx=2)
        btn_danger(toolbar, "🚫 Bloquear Crédito", self._bloquear).pack(side="left", padx=2)
        btn_ghost(toolbar, "🔄 Actualizar", self._cargar).pack(side="right")

        # Tabla
        cols = ("ID", "Nombre", "Saldo Pendiente", "Conducta", "Estado")
        self.tree, cont = tabla_con_scroll(self, cols)
        cont.pack(fill="both", expand=True, padx=10, pady=8)
        for col, w in zip(cols, (50, 250, 130, 130, 100)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        self.tree.tag_configure("bloqueado", background="#3D0000", foreground=RED)
        self.tree.tag_configure("ok", background=NAVY_MED)

        # Panel detalle
        det = tk.Frame(self, bg=NAVY_MED, padx=12, pady=8)
        det.pack(fill="x", padx=10, pady=(0, 8))
        self.lbl_det = tk.Label(det, text="Selecciona un cliente",
                                 bg=NAVY_MED, fg=GRAY_MED, font=FONT_SMALL)
        self.lbl_det.pack(anchor="w")
        self.tree.bind("<<TreeviewSelect>>", self._mostrar_detalle)

        self._cargar()

    def _cargar(self):
        self.tree.delete(*self.tree.get_children())
        for c in dm.cargar_clientes():
            bloqueado = c.bloquear_venta_credito()
            estado = "🚫 BLOQUEADO" if bloqueado else "✔ Activo"
            tag = "bloqueado" if bloqueado else "ok"
            self.tree.insert("", "end", iid=str(c.id_cliente), values=(
                c.id_cliente, c.nombre_cliente,
                f"${c.saldo_pendiente:.2f}",
                c.estatus_conducta, estado
            ), tags=(tag,))

    def _mostrar_detalle(self, event=None):
        sel = self.tree.selection()
        if not sel: return
        clientes = dm.cargar_clientes()
        c = next((x for x in clientes if str(x.id_cliente) == sel[0]), None)
        if c:
            info = c.ver_historial_cliente()
            self.lbl_det.config(
                text=f"ID: {info['ID']}  |  {info['Nombre']}  |  "
                     f"Saldo: {info['Saldo']}  |  Conducta: {info['Conducta']}  |  "
                     f"Bloqueado: {'Sí' if info['Bloqueado'] else 'No'}",
                fg=RED if info["Bloqueado"] else ICE)

    def _nuevo_cliente(self):
        datos = dialogo_simple(self, "Nuevo Cliente", [
            ("Nombre",          "text",  ""),
            ("Saldo Inicial",   "number","0.0"),
            ("Conducta", "combo:Confiable,Grosero,Conflictivo,En evaluación", "Confiable"),
        ])
        if not datos: return
        try:
            c = ClienteControl(
                dm.siguiente_id_cliente(),
                datos["Nombre"].strip(),
                float(datos["Saldo Inicial"]),
                datos["Conducta"]
            )
            if not c.nombre_cliente: raise ValueError("Nombre vacío")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e), parent=self)
            return
        dm.agregar_cliente(c)
        self._cargar()

    def _actualizar_deuda(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un cliente.", parent=self)
            return
        clientes = dm.cargar_clientes()
        c = next((x for x in clientes if str(x.id_cliente) == sel[0]), None)
        if not c: return

        datos = dialogo_simple(self, f"Actualizar deuda: {c.nombre_cliente}", [
            ("Monto (+deuda / -abono)", "number", "0"),
        ])
        if not datos: return
        try:
            monto = float(datos["Monto (+deuda / -abono)"])
        except ValueError:
            messagebox.showerror("Error", "Monto inválido.", parent=self)
            return

        c.actualizar_deuda(monto)
        if c.bloquear_venta_credito():
            messagebox.showwarning("Crédito Bloqueado",
                                   f"⚠ {c.nombre_cliente} ha superado el límite de "
                                   f"${ClienteControl.LIMITE_CREDITO:.2f}.\n"
                                   f"Ventas a crédito bloqueadas.", parent=self)
        dm.actualizar_cliente(c)
        self._cargar()

    def _bloquear(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un cliente.", parent=self)
            return
        clientes = dm.cargar_clientes()
        c = next((x for x in clientes if str(x.id_cliente) == sel[0]), None)
        if not c: return
        # Forzar bloqueo seteando saldo al límite
        c.saldo_pendiente = ClienteControl.LIMITE_CREDITO
        dm.actualizar_cliente(c)
        messagebox.showinfo("Bloqueado",
                            f"Crédito de {c.nombre_cliente} bloqueado.", parent=self)
        self._cargar()
