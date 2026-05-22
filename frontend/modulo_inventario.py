"""
SGP - Módulo de Inventario
Gestión completa de productos con soporte para imágenes
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
from backend import data_manager as dm
from backend.models import Producto
from frontend.styles import *
from frontend.widgets import (
    label_title, label_body, entry_field, btn_primary, btn_danger,
    btn_success, btn_ghost, tabla_con_scroll, separador,
    aplicar_tema_treeview, dialogo_simple
)

try:
    from PIL import Image, ImageTk
    PILLOW_OK = True
except ImportError:
    PILLOW_OK = False


class ModuloInventario(tk.Frame):
    def __init__(self, parent, usuario, **kw):
        super().__init__(parent, bg=NAVY, **kw)
        self.usuario = usuario
        self.es_admin = usuario.rol == "Administrador"
        self.img_placeholder = None
        self._construir()

    def _construir(self):
        style = ttk.Style()
        aplicar_tema_treeview(style)

        # Título
        barra = tk.Frame(self, bg=BLUE, pady=8)
        barra.pack(fill="x")
        tk.Label(barra, text="📦  INVENTARIO",
                 bg=BLUE, fg=WHITE, font=FONT_TITLE).pack(side="left", padx=16)

        # Barra de herramientas
        toolbar = tk.Frame(self, bg=NAVY_MED, pady=6, padx=10)
        toolbar.pack(fill="x")

        self.entry_busqueda = entry_field(toolbar, width=30)
        self.entry_busqueda.pack(side="left", ipady=5, padx=(0, 6))
        self.entry_busqueda.bind("<KeyRelease>", self._buscar)
        btn_ghost(toolbar, "🔍 Buscar", self._buscar).pack(side="left")

        separador(toolbar, NAVY_LIGHT).pack(side="left", fill="y", padx=10)

        if self.es_admin:
            btn_success(toolbar, "➕ Nuevo Producto", self._nuevo_producto).pack(side="left", padx=2)
            btn_primary(toolbar, "✏ Editar", self._editar_producto).pack(side="left", padx=2)
            btn_danger(toolbar, "🗑 Eliminar", self._eliminar_producto).pack(side="left", padx=2)

        btn_ghost(toolbar, "🔄 Actualizar", self._cargar).pack(side="right")

        # Alerta de stock bajo
        self.lbl_alerta = tk.Label(self, text="", bg=ORANGE, fg=WHITE,
                                    font=FONT_LABEL, pady=4)

        # Contenedor central (Tabla + Imagen)
        main_cont = tk.Frame(self, bg=NAVY)
        main_cont.pack(fill="both", expand=True)

        # Tabla
        cols = ("ID", "Nombre", "P.Menudeo", "P.Mayoreo", "Stock", "Mín", "Surtido", "Estado")
        self.tree, cont = tabla_con_scroll(main_cont, cols)
        cont.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        anchos = (80, 220, 90, 90, 70, 60, 70, 80)
        for col, w in zip(cols, anchos):
            self.tree.heading(col, text=col,
                                command=lambda c=col: self._ordenar(c))
            self.tree.column(col, width=w, anchor="center")

        self.tree.tag_configure("alerta", background="#3D1C00", foreground=ORANGE)
        self.tree.tag_configure("normal", background=NAVY_MED)

        # Panel de Imagen (Derecha)
        self.img_frame = tk.Frame(main_cont, bg=NAVY_MED, width=200, padx=10, pady=10)
        self.img_frame.pack(side="right", fill="y", padx=(0, 10), pady=8)
        self.img_frame.pack_propagate(False)
        
        label_title(self.img_frame, "Imagen").pack(pady=(0, 10))

        # Contenedor de pixel fijo para la imagen de inventario para evitar agrandamientos si no hay imagen
        self.lbl_img_container = tk.Frame(self.img_frame, bg=NAVY, width=180, height=180)
        self.lbl_img_container.pack()
        self.lbl_img_container.pack_propagate(False)

        self.lbl_img = tk.Label(self.lbl_img_container, text="Sin imagen", bg=NAVY, fg=GRAY_MED, font=FONT_SMALL)
        self.lbl_img.pack(fill="both", expand=True)

        # Panel detalle (abajo)
        detalle_frame = tk.Frame(self, bg=NAVY_MED, pady=8, padx=12)
        detalle_frame.pack(fill="x", padx=10, pady=(0, 8))
        self.lbl_detalle = tk.Label(detalle_frame, text="Selecciona un producto para ver detalles",
                                     bg=NAVY_MED, fg=GRAY_MED, font=FONT_SMALL)
        self.lbl_detalle.pack(anchor="w")
        
        self.tree.bind("<<TreeviewSelect>>", self._mostrar_detalle)

        self._cargar()

    def _cargar(self, productos=None):
        self.tree.delete(*self.tree.get_children())
        lista = productos or dm.cargar_productos()
        bajos = 0
        for p in lista:
            bajo_stock = p.emitir_alerta_stock()
            if bajo_stock: bajos += 1
            estado = "⚠ BAJO" if bajo_stock else "✔ OK"
            tag = "alerta" if bajo_stock else "normal"
            self.tree.insert("", "end", iid=p.id_producto, values=(
                p.id_producto, p.nombre_prod,
                f"${p.precio_menudeo:.2f}", f"${p.precio_mayoreo:.2f}",
                p.cantidad_stock, p.stock_minimo,
                "Sí" if p.es_surtido else "No", estado
            ), tags=(tag,))

        if bajos > 0:
            self.lbl_alerta.config(
                text=f"  ⚠  {bajos} producto(s) con stock bajo — requieren resurtido")
            self.lbl_alerta.pack(fill="x", padx=10, before=self.tree.master)
        else:
            self.lbl_alerta.pack_forget()

    def _buscar(self, event=None):
        termino = self.entry_busqueda.get().strip()
        self._cargar(dm.buscar_producto(termino) if termino else None)

    def _mostrar_detalle(self, event=None):
        sel = self.tree.selection()
        if not sel: return
        iid = sel[0]
        productos = dm.cargar_productos()
        p = next((x for x in productos if x.id_producto == iid), None)
        if p:
            self.lbl_detalle.config(
                text=f"ID: {p.id_producto}  |  {p.nombre_prod}  |  "
                     f"Menudeo: ${p.precio_menudeo:.2f}  |  Mayoreo: ${p.precio_mayoreo:.2f} (Mín. Mayoreo: {p.cant_minima_mayoreo})  |  "
                     f"Stock: {p.cantidad_stock}  |  Mín: {p.stock_minimo}",
                fg=ICE)
            self._cargar_imagen(p.foto_ruta)

    def _cargar_imagen(self, ruta):
        ruta_res = dm.resolver_ruta(ruta)
        if not ruta_res or not os.path.exists(ruta_res):
            self.lbl_img.config(image="", text="Sin imagen")
            return
        
        try:
            if PILLOW_OK:
                img = Image.open(ruta_res)
                img.thumbnail((180, 180))
                self.img_placeholder = ImageTk.PhotoImage(img)
                self.lbl_img.config(image=self.img_placeholder, text="")
            else:
                # Fallback básico para GIF/PNG/PGM/PPM
                self.img_placeholder = tk.PhotoImage(file=ruta_res)
                self.lbl_img.config(image=self.img_placeholder, text="")
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            self.lbl_img.config(image="", text="Error al cargar")

    def _guardar_imagen_local(self, ruta_orig, id_prod):
        """Copia la imagen a una carpeta local del proyecto."""
        if not ruta_orig or not os.path.exists(ruta_orig):
            return ""
        
        # Carpeta local
        dest_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "imagenes")
        os.makedirs(dest_dir, exist_ok=True)
        
        ext = os.path.splitext(ruta_orig)[1]
        nombre_dest = f"prod_{id_prod}{ext}"
        ruta_dest = os.path.join(dest_dir, nombre_dest)
        
        try:
            shutil.copy2(ruta_orig, ruta_dest)
            # Retornar ruta relativa para mayor portabilidad
            return os.path.join("data", "imagenes", nombre_dest)
        except Exception as e:
            print(f"Error copiando imagen: {e}")
            return ruta_orig

    def _nuevo_producto(self):
        # ── [FRAGMENTO PREPARADO PARA IMÁGENES] ───────────────────────────
        # Aquí puedes decidir qué campos mostrar u ocultar en el diálogo.
        # El tipo 'image' abre automáticamente el explorador de archivos.
        datos = dialogo_simple(self, "Nuevo Producto", [
            ("ID / Código",     "text",   ""),
            ("Nombre",          "text",   ""),
            ("Precio Menudeo",  "number", "0.0"),
            ("Precio Mayoreo",  "number", "0.0"),
            ("Mínimo Mayoreo",  "number", "3"),
            ("Stock Inicial",   "number", "0"),
            ("Stock Mínimo",    "number", "5"),
            ("Es Surtido",      "bool",   False),
            ("Imagen",          "image",  ""), # <--- ESPACIO PARA ADJUNTAR IMAGEN
        ])
        # ──────────────────────────────────────────────────────────────────
        if not datos: return
        try:
            id_p = datos["ID / Código"].strip()
            
            # ── [LÓGICA DE PROCESAMIENTO DE IMAGEN] ───────────────────────
            # Puedes editar cómo se guardan o renombran las imágenes aquí:
            foto = self._guardar_imagen_local(datos["Imagen"], id_p)
            # ──────────────────────────────────────────────────────────────
            
            p = Producto(
                id_producto=id_p,
                nombre_prod=datos["Nombre"].strip(),
                precio_menudeo=float(datos["Precio Menudeo"]),
                precio_mayoreo=float(datos["Precio Mayoreo"]),
                cantidad_stock=int(datos["Stock Inicial"]),
                stock_minimo=int(datos["Stock Mínimo"]),
                es_surtido=bool(datos["Es Surtido"]),
                foto_ruta=foto,
                cant_minima_mayoreo=int(datos["Mínimo Mayoreo"])
            )
            if not p.id_producto or not p.nombre_prod:
                raise ValueError("Campos vacíos")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}", parent=self)
            return

        if dm.agregar_producto(p):
            messagebox.showinfo("Éxito", f"Producto '{p.nombre_prod}' agregado.", parent=self)
            self._cargar()
        else:
            messagebox.showerror("Error", "El ID de producto ya existe.", parent=self)

    def _editar_producto(self):
        if not self.es_admin:
            messagebox.showwarning("Sin permiso", "Solo el administrador puede editar.", parent=self)
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un producto.", parent=self)
            return
        iid = sel[0]
        productos = dm.cargar_productos()
        p = next((x for x in productos if x.id_producto == iid), None)
        if not p: return

        # ── [FRAGMENTO PREPARADO PARA IMÁGENES] ───────────────────────────
        # Diálogo editado para incluir el campo de imagen existente.
        datos = dialogo_simple(self, f"Editar: {p.nombre_prod}", [
            ("Nombre",          "text",   p.nombre_prod),
            ("Precio Menudeo",  "number", str(p.precio_menudeo)),
            ("Precio Mayoreo",  "number", str(p.precio_mayoreo)),
            ("Mínimo Mayoreo",  "number", str(p.cant_minima_mayoreo)),
            ("Stock Actual",    "number", str(p.cantidad_stock)),
            ("Stock Mínimo",    "number", str(p.stock_minimo)),
            ("Es Surtido",      "bool",   p.es_surtido),
            ("Imagen",          "image",  p.foto_ruta), # <--- ESPACIO PARA EDITAR IMAGEN
        ])
        # ──────────────────────────────────────────────────────────────────
        if not datos: return
        try:
            p.nombre_prod = datos["Nombre"].strip()
            p.precio_menudeo = float(datos["Precio Menudeo"])
            p.precio_mayoreo = float(datos["Precio Mayoreo"])
            p.cant_minima_mayoreo = int(datos["Mínimo Mayoreo"])
            p.cantidad_stock = int(datos["Stock Actual"])
            p.stock_minimo = int(datos["Stock Mínimo"])
            p.es_surtido = bool(datos["Es Surtido"])
            
            # ── [LÓGICA DE ACTUALIZACIÓN DE IMAGEN] ───────────────────────
            # Si el usuario seleccionó una imagen diferente, se procesa:
            if datos["Imagen"] != p.foto_ruta:
                p.foto_ruta = self._guardar_imagen_local(datos["Imagen"], p.id_producto)
            # ──────────────────────────────────────────────────────────────
                
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}", parent=self)
            return

        dm.actualizar_producto(p)
        messagebox.showinfo("Éxito", "Producto actualizado.", parent=self)
        self._cargar()
        self._cargar_imagen(p.foto_ruta)

    def _eliminar_producto(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un producto.", parent=self)
            return
        iid = sel[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar producto '{iid}'?", parent=self):
            dm.eliminar_producto(iid)
            self._cargar()
            self.lbl_img.config(image="", text="Sin imagen")

    def _ordenar(self, columna):
        items = [(self.tree.set(k, columna), k) for k in self.tree.get_children("")]
        try:
            items.sort(key=lambda t: float(t[0].replace("$", "")))
        except ValueError:
            items.sort()
        for idx, (_, k) in enumerate(items):
            self.tree.move(k, "", idx)
