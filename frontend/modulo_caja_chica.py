import tkinter as tk
from tkinter import ttk, messagebox
from backend import data_manager as dm
from backend.models import CajaChica
from frontend.styles import *
from frontend.widgets import (
    label_title, label_body, entry_field, btn_primary, btn_danger,
    btn_success, btn_ghost, tabla_con_scroll, separador,
    aplicar_tema_treeview
)


class ModuloCajaChica(tk.Frame):
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
        tk.Label(barra, text="💰  CAJA CHICA",
                 bg=BLUE, fg=WHITE, font=FONT_TITLE).pack(side="left", padx=16)

        # Formulario de egreso
        form_card = tk.Frame(self, bg=NAVY_MED, padx=16, pady=14)
        form_card.pack(fill="x", padx=10, pady=10)
        label_title(form_card, "Registrar Egreso").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        campos = [
            ("Monto ($)", 1, 0),
            ("Proveedor / Destino", 1, 2),
            ("Justificación / Nota", 2, 0),
        ]
        labels = ["Monto ($)", "Proveedor / Destino", "Justificación / Nota"]
        for txt, row, col in campos:
            tk.Label(form_card, text=txt + ":", bg=NAVY_MED, fg=ICE,
                     font=FONT_LABEL, anchor="w").grid(row=row, column=col,
                                                        sticky="w", padx=(0, 8), pady=4)

        self.entry_monto = entry_field(form_card, width=14)
        self.entry_monto.grid(row=1, column=1, ipady=6, pady=4)

        self.entry_proveedor = entry_field(form_card, width=22)
        self.entry_proveedor.grid(row=1, column=3, ipady=6, pady=4)

        self.entry_justif = entry_field(form_card, width=50)
        self.entry_justif.grid(row=2, column=1, columnspan=3, sticky="ew",
                                ipady=6, pady=4)

        btn_success(form_card, "💸 Registrar Salida",
                    self._registrar_egreso).grid(row=3, column=0, columnspan=4,
                                                  pady=(10, 0), sticky="w")

        separador(self).pack(fill="x", padx=10)

        # Tabla historial
        lbl_frame = tk.Frame(self, bg=NAVY, pady=6, padx=10)
        lbl_frame.pack(fill="x")
        label_title(lbl_frame, "Historial de Egresos").pack(side="left")
        if self.es_admin:
            tk.Label(lbl_frame, text="  ← Vista completa (Administrador)",
                     bg=NAVY, fg=GOLD, font=FONT_SMALL).pack(side="left")

        cols = ("ID", "Trabajador", "Monto", "Proveedor", "Justificación", "Fecha/Hora")
        self.tree, cont = tabla_con_scroll(self, cols)
        cont.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for col, w in zip(cols, (50, 120, 90, 130, 220, 150)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        # Totalizador
        self.lbl_total = tk.Label(self, text="Total egresos: $0.00",
                                   bg=NAVY_MED, fg=ORANGE, font=FONT_HEADER,
                                   pady=6)
        self.lbl_total.pack(fill="x", padx=10)

        self._cargar()

    def _registrar_egreso(self):
        try:
            monto = float(self.entry_monto.get())
            if monto <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Monto inválido.", parent=self)
            return

        proveedor = self.entry_proveedor.get().strip()
        justif = self.entry_justif.get().strip()
        if not proveedor:
            messagebox.showerror("Error", "Indica el proveedor/destino.", parent=self)
            return

        egreso = CajaChica(
            dm.siguiente_id_egreso(),
            self.usuario.id_usuario,
            monto, proveedor, justif
        )
        dm.guardar_egreso(egreso)

        self.entry_monto.delete(0, "end")
        self.entry_proveedor.delete(0, "end")
        self.entry_justif.delete(0, "end")

        messagebox.showinfo("Registrado",
                            f"Egreso de ${monto:.2f} registrado.", parent=self)
        self._cargar()

    def _cargar(self):
        self.tree.delete(*self.tree.get_children())
        egresos = dm.cargar_caja_chica()
        usuarios = {u.id_usuario: u.nombre for u in dm.cargar_usuarios()}
        total = 0.0

        # Si es trabajador, solo ve los suyos
        filtrado = egresos if self.es_admin else [
            e for e in egresos if e.id_trabajador == self.usuario.id_usuario
        ]

        for e in filtrado:
            nombre_trab = usuarios.get(e.id_trabajador, f"ID:{e.id_trabajador}")
            self.tree.insert("", "end", values=(
                e.id_movimiento, nombre_trab,
                f"${e.monto_retirado:.2f}", e.proveedor_destino,
                e.justificacion,
                e.fecha_hora.strftime("%d/%m/%Y %H:%M")
            ))
            total += e.monto_retirado

        self.lbl_total.config(text=f"Total egresos: ${total:.2f}")
