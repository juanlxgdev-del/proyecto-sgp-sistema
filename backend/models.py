"""
Backend: Modelos de dominio (POO)
"""
from datetime import datetime
from typing import Optional
import hashlib

# USUARIO
class Usuario:
    def __init__(self, id_usuario: int, nombre: str, contraseña: str,
                 rol: str):
        self.id_usuario: int = id_usuario
        self.nombre: str = nombre
        self.contraseña_hash: str = self._hashear(contraseña)
        self.rol: str = rol # Roles: Administrador o Trabajador

    @staticmethod
    def _hashear(texto: str) -> str:
        return hashlib.sha256(texto.encode()).hexdigest()

    def login(self, contraseña: str) -> bool:
        return self.contraseña_hash == self._hashear(contraseña)

    def cambiar_contraseña(self, nueva: str) -> None:
        self.contraseña_hash = self._hashear(nueva)

    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "contraseña_hash": self.contraseña_hash,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, d: dict):
        obj = cls.__new__(cls)
        obj.id_usuario = d["id_usuario"]
        obj.nombre = d["nombre"]
        obj.contraseña_hash = d["contraseña_hash"]
        obj.rol = d["rol"]
        return obj

# ADMINISTRADOR
class Administrador(Usuario):
    def __init__(self, id_usuario: int, nombre: str, contraseña: str):
        super().__init__(id_usuario, nombre, contraseña, "Administrador")
        self.permisos_globales: list = [
            "inventario", "usuarios", "reportes",
            "caja_chica", "deudores", "precios"
        ]

    def gestionar_usuarios(self) -> str:
        return "Módulo de gestión de usuarios activo"

    def modificar_precios(self) -> str:
        return "Módulo de modificación de precios activo"

    def auditar_caja_chica(self) -> str:
        return "Módulo de auditoría de caja chica activo"

    def ver_reporte_rendimiento(self) -> str:
        return "Módulo de reportes activo"

    def gestionar_deudores(self) -> str:
        return "Módulo de gestión de deudores activo"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["permisos_globales"] = self.permisos_globales
        return d

    @classmethod
    def from_dict(cls, d: dict):
        obj = cls.__new__(cls)
        obj.id_usuario = d["id_usuario"]
        obj.nombre = d["nombre"]
        obj.contraseña_hash = d["contraseña_hash"]
        obj.rol = d["rol"]
        obj.permisos_globales = d.get("permisos_globales", [])
        return obj

# TRABAJADOR (hereda Usuario)
class Trabajador(Usuario):
    def __init__(self, id_usuario: int, nombre: str, contraseña: str):
        super().__init__(id_usuario, nombre, contraseña, "Trabajador")
        self.ventas_del_dia: float = 0.0
        self.hora_entrada: Optional[datetime] = None

    def registrar_entrada(self) -> None:
        self.hora_entrada = datetime.now()

    def registrar_venta(self) -> str:
        return "Procesando cobro..."

    def consultar_stock(self) -> str:
        return "Consultando inventario..."

    def notificar_egreso(self) -> str:
        return "Registrando salida de caja chica..."

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["ventas_del_dia"] = self.ventas_del_dia
        d["hora_entrada"] = self.hora_entrada.isoformat() if self.hora_entrada else None
        return d

    @classmethod
    def from_dict(cls, d: dict):
        obj = cls.__new__(cls)
        obj.id_usuario = d["id_usuario"]
        obj.nombre = d["nombre"]
        obj.contraseña_hash = d["contraseña_hash"]
        obj.rol = d["rol"]
        obj.ventas_del_dia = d.get("ventas_del_dia", 0.0)
        entrada = d.get("hora_entrada")
        obj.hora_entrada = datetime.fromisoformat(entrada) if entrada else None
        return obj

# PRODUCTO
class Producto:
    def __init__(self, id_producto: str, nombre_prod: str,
                 precio_menudeo: float, precio_mayoreo: float,
                 cantidad_stock: int, stock_minimo: int,
                 es_surtido: bool = False, foto_ruta: str = "",
                 cant_minima_mayoreo: int = 3):
        self.id_producto: str = id_producto
        self.nombre_prod: str = nombre_prod
        self.precio_menudeo: float = precio_menudeo
        self.precio_mayoreo: float = precio_mayoreo
        self.cantidad_stock: int = cantidad_stock
        self.stock_minimo: int = stock_minimo
        self.es_surtido: bool = es_surtido
        self.foto_ruta: str = foto_ruta
        self.cant_minima_mayoreo: int = cant_minima_mayoreo

    def actualizar_inventario(self, cantidad: int) -> None:
        """Suma o resta existencias. cantidad negativa = venta."""
        self.cantidad_stock += cantidad
        if self.cantidad_stock < 0:
            self.cantidad_stock = 0

    #Guardamos todo lo que tenga que ver con el producto al JSON
    def ver_detalles(self) -> dict:
        return {
            "ID": self.id_producto,
            "Nombre": self.nombre_prod,
            "Precio Menudeo": f"${self.precio_menudeo:.2f}",
            "Precio Mayoreo": f"${self.precio_mayoreo:.2f}",
            "Stock Actual": self.cantidad_stock,
            "Stock Mínimo": self.stock_minimo,
            "Es Surtido": self.es_surtido,
            "Foto": self.foto_ruta,
            "Mínimo Mayoreo": self.cant_minima_mayoreo
        }

    def emitir_alerta_stock(self) -> bool:
        return self.cantidad_stock <= self.stock_minimo

    def to_dict(self) -> dict:
        return {
            "id_producto": self.id_producto,
            "nombre_prod": self.nombre_prod,
            "precio_menudeo": self.precio_menudeo,
            "precio_mayoreo": self.precio_mayoreo,
            "cantidad_stock": self.cantidad_stock,
            "stock_minimo": self.stock_minimo,
            "es_surtido": self.es_surtido,
            "foto_ruta": self.foto_ruta,
            "cant_minima_mayoreo": self.cant_minima_mayoreo
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            d["id_producto"], d["nombre_prod"],
            d["precio_menudeo"], d["precio_mayoreo"],
            d["cantidad_stock"], d["stock_minimo"],
            d.get("es_surtido", False), d.get("foto_ruta", ""),
            d.get("cant_minima_mayoreo", 3)
        )

# DETALLE VENTA
class DetalleVenta:
    def __init__(self, producto: Producto, cantidad: int, precio_unitario: float):
        self.producto: Producto = producto
        self.cantidad: int = cantidad
        self.precio_unitario: float = precio_unitario
        self.subtotal: float = self.calcular_subtotal()

    def calcular_subtotal(self) -> float:
        return round(self.cantidad * self.precio_unitario, 2)

    def to_dict(self) -> dict:
        return {
            "id_producto": self.producto.id_producto,
            "nombre": self.producto.nombre_prod,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal
        }

# VENTA
class Venta:
    def __init__(self, id_ticket: int, id_trabajador: int,
                 metodo_pago: str = "Efectivo", descuento: float = 0.0):
        self.id_ticket: int = id_ticket
        self.id_trabajador: int = id_trabajador
        self.lista_productos: list[DetalleVenta] = []
        self.total_pago: float = 0.0
        self.metodo_pago: str = metodo_pago # Metodos: Efectivo, Tarjeta o Deudor
        self.fecha_hora: datetime = datetime.now()
        self.descuento_aplicado: float = descuento

    def agregar_detalle(self, detalle: DetalleVenta) -> None:
        self.lista_productos.append(detalle)
        self.calcular_total()

    def calcular_total(self) -> float:
        subtotal = sum(d.subtotal for d in self.lista_productos)
        self.total_pago = round(subtotal * (1 - self.descuento_aplicado / 100), 2)
        return self.total_pago

    def aplicar_descuento(self, porcentaje: float) -> None:
        self.descuento_aplicado = porcentaje
        self.calcular_total()

    def generar_comprobante(self) -> str:
        lineas = [
            "=" * 40,
            f"  TICKET #{self.id_ticket}",
            f"  {self.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}",
            "=" * 40,
        ]
        for d in self.lista_productos:
            lineas.append(f"  {d.producto.nombre_prod[:20]:<20} x{d.cantidad}")
            lineas.append(f"  ${d.precio_unitario:.2f} c/u  = ${d.subtotal:.2f}")
        lineas.append("-" * 40)
        if self.descuento_aplicado > 0:
            lineas.append(f"  Descuento: {self.descuento_aplicado}%")
        lineas.append(f"  TOTAL: ${self.total_pago:.2f}")
        lineas.append(f"  Pago: {self.metodo_pago}")
        lineas.append("=" * 40)
        return "\n".join(lineas)

    def to_dict(self) -> dict:
        return {
            "id_ticket": self.id_ticket,
            "id_trabajador": self.id_trabajador,
            "lista_productos": [d.to_dict() for d in self.lista_productos],
            "total_pago": self.total_pago,
            "metodo_pago": self.metodo_pago,
            "fecha_hora": self.fecha_hora.isoformat(),
            "descuento_aplicado": self.descuento_aplicado
        }

# CAJA CHICA
class CajaChica:
    def __init__(self, id_movimiento: int, id_trabajador: int,
                 monto_retirado: float, proveedor_destino: str,
                 justificacion: str):
        self.id_movimiento: int = id_movimiento
        self.id_trabajador: int = id_trabajador
        self.monto_retirado: float = monto_retirado
        self.proveedor_destino: str = proveedor_destino
        self.justificacion: str = justificacion
        self.fecha_hora: datetime = datetime.now()

    def registrar_salida(self) -> dict:
        return self.to_dict()

    def ver_historial(self) -> str:
        return (f"[{self.fecha_hora.strftime('%d/%m/%Y %H:%M')}] "
                f"${self.monto_retirado:.2f} → {self.proveedor_destino}: {self.justificacion}")

    def to_dict(self) -> dict:
        return {
            "id_movimiento": self.id_movimiento,
            "id_trabajador": self.id_trabajador,
            "monto_retirado": self.monto_retirado,
            "proveedor_destino": self.proveedor_destino,
            "justificacion": self.justificacion,
            "fecha_hora": self.fecha_hora.isoformat()
        }

    @classmethod
    def from_dict(cls, d: dict):
        obj = cls(
            d["id_movimiento"], d["id_trabajador"],
            d["monto_retirado"], d["proveedor_destino"], d["justificacion"]
        )
        obj.fecha_hora = datetime.fromisoformat(d["fecha_hora"])
        return obj

# CLIENTE CONTROL
class ClienteControl:
    LIMITE_CREDITO: float = 500.0 # Limite de credito para deudores

    def __init__(self, id_cliente: int, nombre_cliente: str,
                 saldo_pendiente: float = 0.0,
                 estatus_conducta: str = "Confiable"):
        self.id_cliente: int = id_cliente
        self.nombre_cliente: str = nombre_cliente
        self.saldo_pendiente: float = saldo_pendiente
        self.estatus_conducta: str = estatus_conducta

    def actualizar_deuda(self, monto: float) -> None:
        """Positivo = nueva deuda, Negativo = abono."""
        self.saldo_pendiente = round(self.saldo_pendiente + monto, 2)

    def bloquear_venta_credito(self) -> bool:
        return self.saldo_pendiente >= self.LIMITE_CREDITO

    def ver_historial_cliente(self) -> dict:
        return {
            "ID": self.id_cliente,
            "Nombre": self.nombre_cliente,
            "Saldo": f"${self.saldo_pendiente:.2f}",
            "Conducta": self.estatus_conducta,
            "Bloqueado": self.bloquear_venta_credito()
        }

    def to_dict(self) -> dict:
        return {
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "saldo_pendiente": self.saldo_pendiente,
            "estatus_conducta": self.estatus_conducta
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            d["id_cliente"], d["nombre_cliente"],
            d.get("saldo_pendiente", 0.0),
            d.get("estatus_conducta", "Confiable")
        )
