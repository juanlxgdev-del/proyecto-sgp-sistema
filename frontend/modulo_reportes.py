"""
SGP - Módulo de Reportes y Análisis (Administrador)
Usa Matplotlib para visualización
"""
import tkinter as tk
from tkinter import ttk, messagebox
from backend import data_manager as dm
from frontend.styles import *
from frontend.widgets import label_title, btn_primary, btn_success, btn_ghost, tabla_con_scroll, aplicar_tema_treeview, dialogo_simple

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.patches as mpatches
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False


class ModuloReportes(tk.Frame):
    def __init__(self, parent, usuario, **kw):
        super().__init__(parent, bg=NAVY, **kw)
        self.usuario = usuario
        self._canvas_fig = None
        self._construir()

    def _construir(self):
        style = ttk.Style()
        aplicar_tema_treeview(style)

        barra = tk.Frame(self, bg=BLUE, pady=8)
        barra.pack(fill="x")
        tk.Label(barra, text="📊  REPORTES Y ANÁLISIS",
                 bg=BLUE, fg=WHITE, font=FONT_TITLE).pack(side="left", padx=16)

        # Botones de tipo reporte
        btn_bar = tk.Frame(self, bg=NAVY_MED, pady=8, padx=10)
        btn_bar.pack(fill="x")
        btn_primary(btn_bar, "Ventas por Empleado",
                    self._reporte_empleados).pack(side="left", padx=4)
        btn_primary(btn_bar, "Productos Menos Vendidos",
                    self._reporte_productos).pack(side="left", padx=4)
        btn_success(btn_bar, "🟢 Exportar Excel",
                    self._exportar_excel).pack(side="left", padx=4)
        btn_ghost(btn_bar, "🗑 Limpiar", self._limpiar).pack(side="right")
        btn_ghost(btn_bar, "⚙️ Nombre Tienda", self._cambiar_nombre_tienda).pack(side="right", padx=4)

        # Área de gráfica
        self.area_grafica = tk.Frame(self, bg=NAVY)
        self.area_grafica.pack(fill="both", expand=True, padx=10, pady=8)

        if not MATPLOTLIB_OK:
            tk.Label(self.area_grafica,
                     text="⚠ Matplotlib no instalado.\nEjecuta: pip install matplotlib",
                     bg=NAVY, fg=ORANGE, font=FONT_HEADER).pack(expand=True)

        # Tabla resumen
        cols = ("Concepto", "Valor")
        self.tree, cont = tabla_con_scroll(self, cols, height=6)
        cont.pack(fill="x", padx=10, pady=(0, 8))
        for col, w in zip(cols, (300, 200)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

    def _limpiar(self):
        for w in self.area_grafica.winfo_children():
            w.destroy()
        self.tree.delete(*self.tree.get_children())
        self._canvas_fig = None

    def _mostrar_grafica(self, fig):
        self._limpiar()
        if not MATPLOTLIB_OK: return
        canvas = FigureCanvasTkAgg(fig, master=self.area_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self._canvas_fig = canvas
        plt.close(fig)

    def _estilo_figura(self):
        fig, ax = plt.subplots(figsize=(9, 4))
        fig.patch.set_facecolor("#1B2B3A")
        ax.set_facecolor("#0D1B2A")
        ax.tick_params(colors=ICE, labelsize=9)
        ax.spines["bottom"].set_color(NAVY_LIGHT)
        ax.spines["left"].set_color(NAVY_LIGHT)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.yaxis.label.set_color(ICE)
        ax.xaxis.label.set_color(ICE)
        ax.title.set_color(GOLD)
        return fig, ax

    def _reporte_empleados(self):
        datos = dm.reporte_ventas_por_empleado()
        if not datos:
            messagebox.showinfo("Reporte", "No hay datos de ventas.", parent=self)
            return

        if MATPLOTLIB_OK:
            fig, ax = self._estilo_figura()
            nombres = list(datos.keys())
            valores = list(datos.values())
            colores = [BLUE if v == max(valores) else NAVY_LIGHT for v in valores]
            bars = ax.bar(nombres, valores, color=colores, edgecolor=NAVY)
            ax.set_title("Ventas Totales por Empleado", pad=12)
            ax.set_ylabel("Total ($)")
            for bar, val in zip(bars, valores):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                        f"${val:.2f}", ha="center", va="bottom", color=GOLD, fontsize=8)
            self._mostrar_grafica(fig)

        self.tree.delete(*self.tree.get_children())
        for nombre, total in sorted(datos.items(), key=lambda x: -x[1]):
            self.tree.insert("", "end", values=(f"Empleado: {nombre}", f"${total:.2f}"))

    def _reporte_productos(self):
        datos = dm.productos_menos_vendidos(8)
        if not datos:
            messagebox.showinfo("Reporte", "No hay datos.", parent=self)
            return

        if MATPLOTLIB_OK:
            fig, ax = self._estilo_figura()
            nombres = [d["nombre"][:20] for d in datos]
            vendidos = [d["vendidos"] for d in datos]
            stocks = [d["stock"] for d in datos]
            x = range(len(nombres))
            width = 0.35
            ax.bar([i - width/2 for i in x], vendidos, width, label="Vendidos",
                   color=BLUE, edgecolor=NAVY)
            ax.bar([i + width/2 for i in x], stocks, width, label="Stock actual",
                   color=GOLD, edgecolor=NAVY)
            ax.set_xticks(list(x))
            ax.set_xticklabels(nombres, rotation=30, ha="right", fontsize=8)
            ax.set_title("Productos con Menor Rotación", pad=12)
            ax.legend(facecolor=NAVY_MED, edgecolor=NAVY_LIGHT,
                      labelcolor=ICE, fontsize=8)
            self._mostrar_grafica(fig)

        self.tree.delete(*self.tree.get_children())
        for d in datos:
            self.tree.insert("", "end", values=(
                d["nombre"], f"Vendidos: {d['vendidos']} | Stock: {d['stock']}"
            ))

    def _exportar_excel(self):
        import pandas as pd
        from tkinter import filedialog
        
        ventas_raw = dm.cargar_ventas()
        if not ventas_raw:
            messagebox.showinfo("Exportar", "No hay ventas registradas para exportar.", parent=self)
            return

        # Obtener nombres de trabajadores
        nombres_vendedores = {u.id_usuario: u.nombre for u in dm.cargar_usuarios()}
        
        filas = []
        for v in ventas_raw:
            id_ticket = v["id_ticket"]
            fecha_hora = v.get("fecha_hora", "")
            id_vendedor = v["id_trabajador"]
            vendedor = nombres_vendedores.get(id_vendedor, f"Usuario #{id_vendedor}")
            metodo = v["metodo_pago"]
            descuento = v["descuento_aplicado"]
            total_ticket = v["total_pago"]
            
            for p in v["lista_productos"]:
                filas.append({
                    "Ticket": id_ticket,
                    "Fecha/Hora": fecha_hora,
                    "Vendedor": vendedor,
                    "Método Pago": metodo,
                    "Descuento %": descuento,
                    "Producto": p["nombre"],
                    "Piezas": p["cantidad"],
                    "Precio Unitario": p["precio_unitario"],
                    "Subtotal": p["subtotal"],
                    "Total Ticket": total_ticket
                })
        
        df = pd.DataFrame(filas)
        
        # Diálogo para guardar archivo
        ruta_archivo = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            title="Guardar reporte de ventas",
            initialfile="Reporte_Ventas_SGP.xlsx"
        )
        
        if not ruta_archivo:
            return
            
        try:
            # Crear un Excel bonito usando openpyxl a través de pandas
            writer = pd.ExcelWriter(ruta_archivo, engine="openpyxl")
            df.to_excel(writer, sheet_name="Ventas", index=False)
            
            # Ajustar anchos de columnas automáticamente (detalle premium)
            workbook = writer.book
            worksheet = writer.sheets["Ventas"]
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 10)
                
            writer.close()
            messagebox.showinfo("Éxito", f"Reporte exportado exitosamente a:\n{ruta_archivo}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo: {e}", parent=self)

    def _cambiar_nombre_tienda(self):
        nombre_actual = dm.obtener_nombre_tienda()
        datos = dialogo_simple(self, "Configurar Tienda", [
            ("Nombre de la Tienda", "text", nombre_actual),
        ])
        if not datos:
            return
        nuevo_nombre = datos["Nombre de la Tienda"].strip()
        if not nuevo_nombre:
            messagebox.showerror("Error", "El nombre de la tienda no puede estar vacío.", parent=self)
            return
        dm.guardar_nombre_tienda(nuevo_nombre)
        messagebox.showinfo("Configuración Guardada", f"¡El nombre de la tienda se ha cambiado a:\n{nuevo_nombre.upper()}!\n\nEste nombre aparecerá en todos los futuros tickets generados.", parent=self)
