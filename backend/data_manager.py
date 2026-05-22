"""
SGP - Sistema de Gestión Papelera
Backend: Capa de persistencia JSON
"""

import json
import os
from typing import Optional
from backend.models import (
    Usuario, Administrador, Trabajador, Producto,
    Venta, DetalleVenta, CajaChica, ClienteControl
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _ruta(archivo: str) -> str:
    return os.path.join(DATA_DIR, archivo)


def resolver_ruta(ruta: str) -> str:
    if not ruta:
        return ""
    
    # Normalizar separadores de ruta
    normalized = ruta.replace("\\", "/")
    
    # 1. Si es una ruta absoluta o contiene directorios conocidos, busquemos el final
    for pattern in ["data/imagenes/", "data/tickets/", "Logotipos/", "Sistema_img/"]:
        if pattern in normalized:
            parts = normalized.split(pattern)
            relative_path = os.path.join(pattern.replace("/", os.sep), parts[-1])
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(base_dir, relative_path)
            if os.path.exists(full_path):
                return full_path

    # 2. Si ya es una ruta relativa o absoluta local que existe, la retornamos
    if os.path.isabs(ruta) and os.path.exists(ruta):
        return ruta
        
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, ruta)
    if os.path.exists(full_path):
        return full_path
        
    # 3. Fallback: Buscar solo por el nombre de archivo en data/imagenes o Logotipos
    filename = os.path.basename(ruta)
    for folder in [os.path.join("data", "imagenes"), "Logotipos", "Sistema_img"]:
        fallback_path = os.path.join(base_dir, folder, filename)
        if os.path.exists(fallback_path):
            return fallback_path
            
    return ruta


def _leer(archivo: str) -> list:
    ruta = _ruta(archivo)
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _escribir(archivo: str, datos: list) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_ruta(archivo), "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def obtener_nombre_tienda() -> str:
    ruta = os.path.join(DATA_DIR, "config.json")
    if not os.path.exists(ruta):
        return "MI PAPELERÍA"
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("nombre_tienda", "MI PAPELERÍA")
    except Exception:
        return "MI PAPELERÍA"


def guardar_nombre_tienda(nombre: str) -> None:
    ruta = os.path.join(DATA_DIR, "config.json")
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump({"nombre_tienda": nombre}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ─────────────────────────────────────────
# GESTIÓN DE USUARIOS
# ─────────────────────────────────────────
def cargar_usuarios() -> list:
    raw = _leer("usuarios.json")
    usuarios = []
    for d in raw:
        if d["rol"] == "Administrador":
            usuarios.append(Administrador.from_dict(d))
        else:
            usuarios.append(Trabajador.from_dict(d))
    return usuarios


def guardar_usuarios(usuarios: list) -> None:
    _escribir("usuarios.json", [u.to_dict() for u in usuarios])


def autenticar(nombre: str, contraseña: str) -> Optional[Usuario]:
    for u in cargar_usuarios():
        if u.nombre == nombre and u.login(contraseña):
            return u
    return None


def agregar_usuario(usuario: Usuario) -> bool:
    usuarios = cargar_usuarios()
    if any(u.id_usuario == usuario.id_usuario for u in usuarios):
        return False
    usuarios.append(usuario)
    guardar_usuarios(usuarios)
    return True


def eliminar_usuario(id_usuario: int) -> bool:
    usuarios = cargar_usuarios()
    nuevos = [u for u in usuarios if u.id_usuario != id_usuario]
    if len(nuevos) == len(usuarios):
        return False
    guardar_usuarios(nuevos)
    return True


def siguiente_id_usuario() -> int:
    usuarios = cargar_usuarios()
    return max((u.id_usuario for u in usuarios), default=0) + 1


# ─────────────────────────────────────────
# GESTIÓN DE PRODUCTOS
# ─────────────────────────────────────────
def cargar_productos() -> list[Producto]:
    return [Producto.from_dict(d) for d in _leer("productos.json")]


def guardar_productos(productos: list[Producto]) -> None:
    _escribir("productos.json", [p.to_dict() for p in productos])


def agregar_producto(producto: Producto) -> bool:
    productos = cargar_productos()
    if any(p.id_producto == producto.id_producto for p in productos):
        return False
    productos.append(producto)
    guardar_productos(productos)
    return True


def actualizar_producto(producto: Producto) -> bool:
    productos = cargar_productos()
    for i, p in enumerate(productos):
        if p.id_producto == producto.id_producto:
            productos[i] = producto
            guardar_productos(productos)
            return True
    return False


def eliminar_producto(id_producto: str) -> bool:
    productos = cargar_productos()
    nuevos = [p for p in productos if p.id_producto != id_producto]
    if len(nuevos) == len(productos):
        return False
    guardar_productos(nuevos)
    return True


def buscar_producto(termino: str) -> list[Producto]:
    termino = termino.lower()
    return [p for p in cargar_productos()
            if termino in p.id_producto.lower() or termino in p.nombre_prod.lower()]


def productos_bajo_stock() -> list[Producto]:
    return [p for p in cargar_productos() if p.emitir_alerta_stock()]


# ─────────────────────────────────────────
# GESTIÓN DE VENTAS
# ─────────────────────────────────────────
def cargar_ventas() -> list[dict]:
    return _leer("ventas.json")


def obtener_nombre_usuario(id_usuario: int) -> str:
    for u in cargar_usuarios():
        if u.id_usuario == id_usuario:
            return u.nombre
    return "Desconocido"


def guardar_venta(venta: Venta) -> None:
    ventas = cargar_ventas()
    d = venta.to_dict()
    ventas.append(d)
    _escribir("ventas.json", ventas)

    # Descontar stock
    productos = cargar_productos()
    for detalle in venta.lista_productos:
        for p in productos:
            if p.id_producto == detalle.producto.id_producto:
                p.actualizar_inventario(-detalle.cantidad)
    guardar_productos(productos)

    # Generar PDF del ticket automáticamente
    try:
        from fpdf import FPDF
        nombre_trabajador = obtener_nombre_usuario(venta.id_trabajador)
        
        pdf = FPDF(format=(105, 148))
        pdf.add_page()
        
        # Colores elegantes: Azul Marino y Gris
        pdf.set_text_color(20, 30, 55) # Navy
        pdf.set_font("Helvetica", "B", 14)
        
        # Nombre de la tienda dinámico decidido por el administrador
        nombre_tienda = obtener_nombre_tienda().upper()
        
        # Agregar TICKET LOGO si existe
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_ticket_logo = os.path.join(base_dir, "Logotipos", "TICKET LOGO.png")
        if os.path.exists(path_ticket_logo):
            # Centrar la imagen (ancho de página A6 = 105mm)
            # Con un ancho de 24mm: x = (105 - 24) / 2 = 40.5
            pdf.image(path_ticket_logo, x=40.5, y=6, w=24)
            # Colocar el cursor debajo de la imagen
            pdf.set_y(32)
            
        pdf.cell(0, 10, nombre_tienda, ln=True, align="C")
        
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 5, "="*40, ln=True, align="C")
        
        # Info venta
        pdf.set_text_color(50, 50, 50)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, f"TICKET #{venta.id_ticket}", ln=True, align="L")
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, f"Fecha/Hora: {venta.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}", ln=True)
        pdf.cell(0, 5, f"Vendedor: {nombre_trabajador}", ln=True)
        pdf.cell(0, 5, f"Pago: {venta.metodo_pago}", ln=True)
        pdf.cell(0, 5, "="*40, ln=True, align="C")
        
        # Detalle de productos con columnas corregidas y ensanchadas para mayor legibilidad
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(45, 6, "Producto", align="L")
        pdf.cell(10, 6, "Cant", align="C")
        pdf.cell(15, 6, "Precio", align="R")
        pdf.cell(20, 6, "Subtotal", align="R", ln=True)
        pdf.cell(0, 2, "-"*65, ln=True)
        
        pdf.set_font("Helvetica", "", 9)
        for d in venta.lista_productos:
            # Aumentado a 23 caracteres para evitar cortes como "Cuaderno Profesion"
            nombre = d.producto.nombre_prod[:23]
            pdf.cell(45, 6, nombre, align="L")
            pdf.cell(10, 6, str(d.cantidad), align="C")
            pdf.cell(15, 6, f"${d.precio_unitario:.2f}", align="R")
            pdf.cell(20, 6, f"${d.subtotal:.2f}", align="R", ln=True)
            
        pdf.cell(0, 2, "-"*65, ln=True)
        
        # Descuentos y Total
        if venta.descuento_aplicado > 0:
            pdf.cell(70, 6, f"Descuento ({venta.descuento_aplicado}%):", align="R")
            subt_total = sum(item.subtotal for item in venta.lista_productos)
            desct_monto = round(subt_total * (venta.descuento_aplicado / 100), 2)
            pdf.cell(20, 6, f"-${desct_monto:.2f}", align="R", ln=True)
            
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(180, 130, 20) # Gold
        pdf.cell(70, 8, "TOTAL:", align="R")
        pdf.cell(20, 8, f"${venta.total_pago:.2f}", align="R", ln=True)
        
        pdf.set_text_color(100, 100, 100)
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(0, 10, "¡Gracias por su compra!", ln=True, align="C")
        
        tickets_dir = os.path.join(DATA_DIR, "tickets")
        os.makedirs(tickets_dir, exist_ok=True)
        ruta_pdf = os.path.join(tickets_dir, f"ticket_{venta.id_ticket}.pdf")
        pdf.output(ruta_pdf)
        print(f"Ticket PDF generado en: {ruta_pdf}")
    except Exception as e:
        print(f"Error generando ticket PDF: {e}")


def siguiente_ticket() -> int:
    ventas = cargar_ventas()
    return max((v["id_ticket"] for v in ventas), default=0) + 1


def ventas_por_trabajador(id_trabajador: int) -> list[dict]:
    return [v for v in cargar_ventas() if v["id_trabajador"] == id_trabajador]


# ─────────────────────────────────────────
# GESTIÓN DE CAJA CHICA
# ─────────────────────────────────────────
def cargar_caja_chica() -> list[CajaChica]:
    return [CajaChica.from_dict(d) for d in _leer("caja_chica.json")]


def guardar_egreso(egreso: CajaChica) -> None:
    egresos = _leer("caja_chica.json")
    egresos.append(egreso.to_dict())
    _escribir("caja_chica.json", egresos)


def siguiente_id_egreso() -> int:
    egresos = cargar_caja_chica()
    return max((e.id_movimiento for e in egresos), default=0) + 1


# ─────────────────────────────────────────
# GESTIÓN DE CLIENTES / DEUDORES
# ─────────────────────────────────────────
def cargar_clientes() -> list[ClienteControl]:
    return [ClienteControl.from_dict(d) for d in _leer("clientes.json")]


def guardar_clientes(clientes: list[ClienteControl]) -> None:
    _escribir("clientes.json", [c.to_dict() for c in clientes])


def agregar_cliente(cliente: ClienteControl) -> bool:
    clientes = cargar_clientes()
    if any(c.id_cliente == cliente.id_cliente for c in clientes):
        return False
    clientes.append(cliente)
    guardar_clientes(clientes)
    return True


def actualizar_cliente(cliente: ClienteControl) -> bool:
    clientes = cargar_clientes()
    for i, c in enumerate(clientes):
        if c.id_cliente == cliente.id_cliente:
            clientes[i] = cliente
            guardar_clientes(clientes)
            return True
    return False


def siguiente_id_cliente() -> int:
    clientes = cargar_clientes()
    return max((c.id_cliente for c in clientes), default=0) + 1


# ─────────────────────────────────────────
# REPORTES
# ─────────────────────────────────────────
def reporte_ventas_por_empleado() -> dict:
    """Retorna dict {nombre_trabajador: total_ventas}"""
    usuarios = cargar_usuarios()
    ventas = cargar_ventas()
    resultado = {}
    for u in usuarios:
        if u.rol in ("Trabajador", "Administrador"):
            total = sum(v["total_pago"] for v in ventas if v["id_trabajador"] == u.id_usuario)
            resultado[u.nombre] = round(total, 2)
    return resultado


def productos_menos_vendidos(top_n: int = 5) -> list[dict]:
    ventas = cargar_ventas()
    conteo = {}
    for v in ventas:
        for item in v["lista_productos"]:
            pid = item["id_producto"]
            conteo[pid] = conteo.get(pid, 0) + item["cantidad"]
    productos = cargar_productos()
    resultado = []
    for p in productos:
        resultado.append({
            "id": p.id_producto,
            "nombre": p.nombre_prod,
            "vendidos": conteo.get(p.id_producto, 0),
            "stock": p.cantidad_stock
        })
    resultado.sort(key=lambda x: x["vendidos"])
    return resultado[:top_n]
