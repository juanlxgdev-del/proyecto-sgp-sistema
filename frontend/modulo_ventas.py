"""
SGP - Módulo de Ventas
Operación de cobro para Trabajadores
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from backend import data_manager as dm
from backend.models import Venta, DetalleVenta
from frontend.styles import *
from frontend.widgets import (
    label_title, label_body, entry_field, btn_primary,
    btn_danger, btn_success, btn_ghost, tabla_con_scroll,
    separador, aplicar_tema_treeview
)

try:
    from PIL import Image, ImageTk
    PILLOW_OK = True
except ImportError:
    PILLOW_OK = False


class ModuloVentas(tk.Frame):
    def __init__(self, parent, usuario, **kw):
        super().__init__(parent, bg=NAVY, **kw)
        self.usuario = usuario
        self.carrito: list[DetalleVenta] = []
        self.descuento = 0.0
        self._construir()

    def _construir(self):
        style = ttk.Style()
        aplicar_tema_treeview(style)

        # ── Título ──
        titulo_bar = tk.Frame(self, bg=BLUE, pady=8)
        titulo_bar.pack(fill="x")
        tk.Label(titulo_bar, text="🛒  MÓDULO DE VENTAS",
                 bg=BLUE, fg=WHITE, font=FONT_TITLE).pack(side="left", padx=16)
        tk.Label(titulo_bar, text=f"Trabajador: {self.usuario.nombre}",
                 bg=BLUE, fg=ICE, font=FONT_SMALL).pack(side="right", padx=16)

        # ── Cuerpo principal (2 columnas) ──
        cuerpo = tk.Frame(self, bg=NAVY)
        cuerpo.pack(fill="both", expand=True, padx=10, pady=10)
        cuerpo.columnconfigure(0, weight=2)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        # ── Panel izquierdo: búsqueda + tabla de productos ──
        panel_izq = tk.Frame(cuerpo, bg=NAVY_MED, padx=10, pady=10)
        panel_izq.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        panel_izq.rowconfigure(2, weight=1)
        panel_izq.columnconfigure(0, weight=1)

        label_title(panel_izq, "🔍 Buscar Producto").grid(
            row=0, column=0, columnspan=2, sticky="w")

        busq_frame = tk.Frame(panel_izq, bg=NAVY_MED)
        busq_frame.grid(row=1, column=0, sticky="ew", pady=6)
        busq_frame.columnconfigure(0, weight=1)

        self.entry_busqueda = entry_field(busq_frame)
        self.entry_busqueda.grid(row=0, column=0, sticky="ew", ipady=6)
        self.entry_busqueda.bind("<KeyRelease>", self._buscar)
        btn_ghost(busq_frame, "Buscar", self._buscar).grid(row=0, column=1, padx=(6, 0))

        # Contenedor para tabla y detalle al lado
        cont_catalogo = tk.Frame(panel_izq, bg=NAVY_MED)
        cont_catalogo.grid(row=2, column=0, sticky="nsew", pady=4)
        cont_catalogo.rowconfigure(0, weight=1)
        cont_catalogo.columnconfigure(0, weight=3) # Tabla
        cont_catalogo.columnconfigure(1, weight=2) # Detalle

        cols = ("ID", "Nombre", "Menudeo", "Mayoreo", "Stock", "Surtido")
        self.tree_productos, cont = tabla_con_scroll(cont_catalogo, cols)
        cont.grid(row=0, column=0, sticky="nsew")
        for col, w in zip(cols, (70, 180, 80, 80, 60, 60)):
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, width=w, anchor="center")

        # Bind para mostrar detalle de producto seleccionado
        self.tree_productos.bind("<<TreeviewSelect>>", self._mostrar_detalle_producto)

        # Panel de detalle del producto (derecha de la tabla)
        self.panel_detalle = tk.Frame(cont_catalogo, bg=NAVY, padx=8, pady=8)
        self.panel_detalle.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        label_title(self.panel_detalle, "Detalle de Producto").pack(anchor="w", pady=(0, 6))

        # Contenedor de pixel fijo para la imagen para evitar agrandamiento si no hay imagen
        self.img_prod_container = tk.Frame(self.panel_detalle, bg=NAVY_MED, width=250, height=250)
        self.img_prod_container.pack(pady=4)
        self.img_prod_container.pack_propagate(False)

        self.lbl_img_prod = tk.Label(self.img_prod_container, text="Sin imagen", bg=NAVY_MED, fg=GRAY_MED, font=FONT_SMALL)
        self.lbl_img_prod.pack(fill="both", expand=True)

        self.lbl_detalles_prod = tk.Label(self.panel_detalle, text="Selecciona un producto\npara ver detalles.",
                                           bg=NAVY, fg=ICE, font=FONT_SMALL, justify="left", anchor="nw")
        self.lbl_detalles_prod.pack(fill="both", expand=True, pady=4)

        # Botón agregar al carrito
        btn_primary(panel_izq, "➕ Agregar al Carrito",
                    self._agregar_al_carrito).grid(row=3, column=0, pady=8, sticky="ew")

        # ── Panel derecho: carrito + cobro ──
        panel_der = tk.Frame(cuerpo, bg=NAVY_MED, padx=10, pady=10)
        panel_der.grid(row=0, column=1, sticky="nsew")
        panel_der.rowconfigure(2, weight=1)
        panel_der.columnconfigure(0, weight=1)

        label_title(panel_der, "🧾 Carrito").grid(row=0, column=0, sticky="w")

        cols_carr = ("Producto", "Cant", "P.Unit", "Subtotal")
        self.tree_carrito, cont2 = tabla_con_scroll(panel_der, cols_carr)
        cont2.grid(row=2, column=0, sticky="nsew", pady=4)
        for col, w in zip(cols_carr, (160, 50, 70, 80)):
            self.tree_carrito.heading(col, text=col)
            self.tree_carrito.column(col, width=w, anchor="center")

        # Controles descuento
        desc_frame = tk.Frame(panel_der, bg=NAVY_MED)
        desc_frame.grid(row=3, column=0, sticky="ew", pady=4)
        label_body(desc_frame, "Descuento %:").pack(side="left")
        self.entry_desc = entry_field(desc_frame, width=6)
        self.entry_desc.insert(0, "0")
        self.entry_desc.pack(side="left", padx=6, ipady=4)
        btn_ghost(desc_frame, "Aplicar", self._aplicar_descuento).pack(side="left")

        # Método de pago
        metodo_frame = tk.Frame(panel_der, bg=NAVY_MED)
        metodo_frame.grid(row=4, column=0, sticky="ew", pady=4)
        label_body(metodo_frame, "Pago:").pack(side="left")
        self.var_metodo = tk.StringVar(value="Efectivo")
        for opcion in ("Efectivo", "Tarjeta", "Crédito/Deudor"):
            tk.Radiobutton(metodo_frame, text=opcion, variable=self.var_metodo,
                           value=opcion, bg=NAVY_MED, fg=ICE, font=FONT_SMALL,
                           selectcolor=BLUE, activebackground=NAVY_MED).pack(side="left", padx=4)

        # Total
        self.lbl_total = tk.Label(panel_der, text="TOTAL: $0.00",
                                   bg=NAVY_MED, fg=GOLD, font=("Georgia", 16, "bold"))
        self.lbl_total.grid(row=5, column=0, pady=8)

        # Botones acción
        acciones = tk.Frame(panel_der, bg=NAVY_MED)
        acciones.grid(row=6, column=0, sticky="ew")
        btn_success(acciones, "✔ COBRAR", self._cobrar).pack(side="left", fill="x", expand=True, padx=(0, 4))
        btn_danger(acciones, "✖ Vaciar", self._vaciar_carrito).pack(side="left")
        btn_ghost(acciones, "🗑 Quitar", self._quitar_seleccion).pack(side="left", padx=(4, 0))

        # Comprobante
        self.txt_comprobante = tk.Text(panel_der, height=8, bg=NAVY,
                                        fg=ICE, font=FONT_MONO,
                                        relief="flat", state="disabled")
        self.txt_comprobante.grid(row=7, column=0, sticky="ew", pady=(8, 0))

        # Leyenda sobre la ubicación de los tickets PDF generados
        self.lbl_tickets_path = tk.Label(panel_der, text="📁 Tickets PDF: data/tickets/",
                                          bg=NAVY_MED, fg=GREEN, font=FONT_SMALL)
        self.lbl_tickets_path.grid(row=8, column=0, pady=(4, 0), sticky="w")

        # Cargar catálogo inicial
        self._cargar_catalogo()

    def _cargar_catalogo(self, productos=None):
        self.tree_productos.delete(*self.tree_productos.get_children())
        lista = productos if productos is not None else dm.cargar_productos()
        for p in lista:
            alerta = "⚠" if p.emitir_alerta_stock() else ""
            self.tree_productos.insert("", "end", iid=p.id_producto, values=(
                p.id_producto, p.nombre_prod + alerta,
                f"${p.precio_menudeo:.2f}", f"${p.precio_mayoreo:.2f}",
                p.cantidad_stock, "Sí" if p.es_surtido else "No"
            ))

    def _buscar(self, event=None):
        termino = self.entry_busqueda.get().strip()
        if termino:
            self._cargar_catalogo(dm.buscar_producto(termino))
        else:
            self._cargar_catalogo()

    def _mostrar_detalle_producto(self, event=None):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            self.lbl_img_prod.config(image="", text="Sin imagen")
            self.lbl_detalles_prod.config(text="Selecciona un producto\npara ver detalles.")
            return

        iid = seleccion[0]
        productos = dm.cargar_productos()
        producto = next((p for p in productos if p.id_producto == iid), None)
        if not producto:
            return

        # Actualizar detalles del producto
        detalles_text = (
            f"ID: {producto.id_producto}\n"
            f"Producto: {producto.nombre_prod}\n"
            f"Precio Menudeo: ${producto.precio_menudeo:.2f}\n"
            f"Precio Mayoreo: ${producto.precio_mayoreo:.2f}\n"
            f"Mín. Mayoreo: {producto.cant_minima_mayoreo} pzas\n"
            f"Stock Disponible: {producto.cantidad_stock} pzas\n"
            f"Surtido: {'Sí' if producto.es_surtido else 'No'}"
        )
        self.lbl_detalles_prod.config(text=detalles_text)

        # Cargar imagen
        self._cargar_imagen_producto(producto.foto_ruta)

    def _cargar_imagen_producto(self, ruta, target_label=None):
        label = target_label if target_label else self.lbl_img_prod
        ruta_res = dm.resolver_ruta(ruta)
        if not ruta_res or not os.path.exists(ruta_res):
            label.config(image="", text="Sin imagen")
            return
        
        try:
            if PILLOW_OK:
                img = Image.open(ruta_res)
                # Escalar de forma nítida y grande en proporción al contenedor (250x250)
                ancho, alto = 250, 250
                img.thumbnail((ancho, alto))
                if target_label:
                    self.img_placeholder_popup = ImageTk.PhotoImage(img)
                    label.config(image=self.img_placeholder_popup, text="")
                else:
                    self.img_placeholder_panel = ImageTk.PhotoImage(img)
                    label.config(image=self.img_placeholder_panel, text="")
            else:
                if target_label:
                    self.img_placeholder_popup = tk.PhotoImage(file=ruta_res)
                    label.config(image=self.img_placeholder_popup, text="")
                else:
                    self.img_placeholder_panel = tk.PhotoImage(file=ruta_res)
                    label.config(image=self.img_placeholder_panel, text="")
        except Exception as e:
            print(f"Error cargando imagen en modulo_ventas: {e}")
            label.config(image="", text="Error")

    def _agregar_al_carrito(self):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un producto del catálogo.", parent=self)
            return

        iid = seleccion[0]
        productos = dm.cargar_productos()
        producto = next((p for p in productos if p.id_producto == iid), None)
        if not producto:
            return

        if producto.cantidad_stock <= 0:
            messagebox.showerror("Sin stock", f"'{producto.nombre_prod}' no tiene existencias.", parent=self)
            return

        # Preguntar cantidad y tipo de precio
        win = tk.Toplevel(self)
        win.title("Agregar al carrito")
        win.configure(bg=NAVY)
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text=producto.nombre_prod, bg=NAVY, fg=GOLD,
                 font=FONT_HEADER, pady=8, padx=20).pack()

        main_form = tk.Frame(win, bg=NAVY, padx=20, pady=10)
        main_form.pack()

        # Parte izquierda: imagen e info del producto
        panel_izq_pop = tk.Frame(main_form, bg=NAVY, padx=10)
        panel_izq_pop.pack(side="left", fill="both", expand=True)

        # Contenedor de pixel fijo para la imagen en el popup para evitar que se agrande si no hay imagen
        img_pop_container = tk.Frame(panel_izq_pop, bg=NAVY_MED, width=250, height=250)
        img_pop_container.pack(pady=4)
        img_pop_container.pack_propagate(False)

        lbl_img_pop = tk.Label(img_pop_container, text="Sin imagen", bg=NAVY_MED, fg=GRAY_MED, font=FONT_SMALL)
        lbl_img_pop.pack(fill="both", expand=True)
        self._cargar_imagen_producto(producto.foto_ruta, lbl_img_pop)

        info_pop = (
            f"Menudeo: ${producto.precio_menudeo:.2f}\n"
            f"Mayoreo: ${producto.precio_mayoreo:.2f}\n"
            f"Mayoreo desde: {producto.cant_minima_mayoreo} pzas"
        )
        tk.Label(panel_izq_pop, text=info_pop, bg=NAVY, fg=ICE, font=FONT_SMALL, justify="left").pack(pady=4)

        # Parte derecha: formulario para escoger cantidad y precio
        form = tk.Frame(main_form, bg=NAVY, padx=10)
        form.pack(side="right", fill="both", expand=True)

        tk.Label(form, text="Cantidad:", bg=NAVY, fg=ICE, font=FONT_LABEL).grid(
            row=0, column=0, sticky="w", pady=4)
        e_cant_var = tk.StringVar(value="1")
        e_cant = tk.Entry(form, textvariable=e_cant_var, **{**ENTRY_STYLE, "width": 10})
        e_cant.grid(row=0, column=1, pady=4, padx=(8, 0))

        # Auto-selección de precio según la cantidad
        var_precio = tk.StringVar(value="menudeo")
        
        tk.Label(form, text="Precio:", bg=NAVY, fg=ICE, font=FONT_LABEL).grid(
            row=1, column=0, sticky="w", pady=4)
        f_precio = tk.Frame(form, bg=NAVY)
        f_precio.grid(row=1, column=1, pady=4)
        
        rb_menudeo = tk.Radiobutton(f_precio, text=f"Menudeo (${producto.precio_menudeo:.2f})",
                       variable=var_precio, value="menudeo",
                       bg=NAVY, fg=ICE, font=FONT_SMALL, selectcolor=BLUE)
        rb_menudeo.pack(anchor="w")
        rb_mayoreo = tk.Radiobutton(f_precio, text=f"Mayoreo (${producto.precio_mayoreo:.2f})",
                       variable=var_precio, value="mayoreo",
                       bg=NAVY, fg=ICE, font=FONT_SMALL, selectcolor=BLUE)
        rb_mayoreo.pack(anchor="w")

        # Trace para cambiar automáticamente a mayoreo si la cantidad supera el mínimo
        def on_cant_change(*args):
            try:
                cant = int(e_cant_var.get())
                if cant >= producto.cant_minima_mayoreo:
                    var_precio.set("mayoreo")
                else:
                    var_precio.set("menudeo")
            except ValueError:
                pass
        
        # Enlazar evento para actualizar radiobutton automáticamente
        e_cant_var.trace_add("write", on_cant_change)

        def agregar():
            try:
                cant = int(e_cant.get())
                if cant <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida.", parent=win)
                return
            if cant > producto.cantidad_stock:
                messagebox.showerror("Error",
                    f"Solo hay {producto.cantidad_stock} en stock.", parent=win)
                return

            precio = (producto.precio_menudeo if var_precio.get() == "menudeo"
                      else producto.precio_mayoreo)
            detalle = DetalleVenta(producto, cant, precio)
            self.carrito.append(detalle)
            self._actualizar_carrito()
            win.destroy()

        btn_success(win, "Agregar", agregar).pack(pady=10)
        win.wait_window()

    def _actualizar_carrito(self):
        self.tree_carrito.delete(*self.tree_carrito.get_children())
        total = 0.0
        for d in self.carrito:
            self.tree_carrito.insert("", "end", values=(
                d.producto.nombre_prod[:22], d.cantidad,
                f"${d.precio_unitario:.2f}", f"${d.subtotal:.2f}"
            ))
            total += d.subtotal
        total_desc = round(total * (1 - self.descuento / 100), 2)
        self.lbl_total.config(text=f"TOTAL: ${total_desc:.2f}")

    def _aplicar_descuento(self):
        try:
            self.descuento = float(self.entry_desc.get())
            if not (0 <= self.descuento <= 100): raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Descuento debe ser entre 0 y 100.", parent=self)
            return
        self._actualizar_carrito()

    def _quitar_seleccion(self):
        sel = self.tree_carrito.selection()
        if not sel: return
        idx = self.tree_carrito.index(sel[0])
        if 0 <= idx < len(self.carrito):
            self.carrito.pop(idx)
            self._actualizar_carrito()

    def _vaciar_carrito(self):
        self.carrito.clear()
        self.descuento = 0.0
        self.entry_desc.delete(0, "end")
        self.entry_desc.insert(0, "0")
        self._actualizar_carrito()
        self.txt_comprobante.config(state="normal")
        self.txt_comprobante.delete("1.0", "end")
        self.txt_comprobante.config(state="disabled")

    def _cobrar(self):
        if not self.carrito:
            messagebox.showwarning("Aviso", "El carrito está vacío.", parent=self)
            return

        metodo = self.var_metodo.get()
        id_ticket = dm.siguiente_ticket()
        venta = Venta(id_ticket, self.usuario.id_usuario, metodo, self.descuento)
        for d in self.carrito:
            venta.agregar_detalle(d)

        # Verificar si es crédito y el cliente está bloqueado
        if metodo == "Crédito/Deudor":
            clientes = dm.cargar_clientes()
            # Informar al trabajador que puede registrar el deudor
            messagebox.showinfo("Crédito", "Registra el deudor en el módulo ClienteControl.", parent=self)

        dm.guardar_venta(venta)

        # Mostrar comprobante
        comprobante = venta.generar_comprobante()
        self.txt_comprobante.config(state="normal")
        self.txt_comprobante.delete("1.0", "end")
        self.txt_comprobante.insert("end", comprobante)
        self.txt_comprobante.config(state="disabled")

        # Ruta donde se generó el PDF
        ruta_pdf = f"data/tickets/ticket_{id_ticket}.pdf"
        messagebox.showinfo("Venta Registrada",
                            f"✔ Ticket #{id_ticket} | Total: ${venta.total_pago:.2f}\n\n"
                            f"📝 PDF generado automáticamente en:\n{ruta_pdf}", parent=self)

        # Actualizar trabajador (si el rol posee ventas_del_dia)
        if hasattr(self.usuario, "ventas_del_dia"):
            self.usuario.ventas_del_dia = round(
                self.usuario.ventas_del_dia + venta.total_pago, 2)

        self._vaciar_carrito()
        self._cargar_catalogo()

        # Alertas de stock
        bajos = dm.productos_bajo_stock()
        if bajos:
            nombres = "\n".join(f"  ⚠ {p.nombre_prod} (stock: {p.cantidad_stock})" for p in bajos)
            messagebox.showwarning("Alerta de Stock",
                                   f"Los siguientes productos están bajos:\n{nombres}", parent=self)
