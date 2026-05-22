# SGP - Inicializacion de datos de demostracion
# Ejecutar una vez para poblar el sistema con datos iniciales.
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from backend.models import Administrador, Trabajador, Producto, ClienteControl
from backend import data_manager as dm


def sembrar():
    print("Inicializando datos SGP (Modo Local + Imagenes)...")

    # Limpiar archivos de base de datos JSON antiguos para evitar duplicados
    for db_file in ["usuarios.json", "productos.json", "clientes.json", "ventas.json", "caja_chica.json"]:
        path_file = os.path.join("data", db_file)
        if os.path.exists(path_file):
            try:
                os.remove(path_file)
            except Exception as e:
                print(f"Advertencia: No se pudo eliminar {db_file}: {e}")

    # Limpiar tickets PDF antiguos para iniciar sin historial
    tickets_dir = os.path.join("data", "tickets")
    if os.path.exists(tickets_dir):
        for f in os.listdir(tickets_dir):
            if f.endswith(".pdf"):
                try:
                    os.remove(os.path.join(tickets_dir, f))
                except Exception as e:
                    print(f"Advertencia: No se pudo eliminar ticket {f}: {e}")

    # Ruta base para imagenes
    img_dir = os.path.join("data", "imagenes")
    
    # Configuracion de usuarios
    admin = Administrador(1, "admin", "admin123")
    t1 = Trabajador(2, "trabajador 1", "trabajador123")
    
    if dm.agregar_usuario(admin): print("  [OK] Administrador creado  (usuario: admin / pass: admin123)")
    if dm.agregar_usuario(t1):    print("  [OK] Trabajador creado (usuario: trabajador 1 / pass: trabajador123)")

    # Productos con imagenes por defecto
    productos = [
        Producto("P001", "Cuaderno Profesional 100h", 35.0, 30.0, 50, 10, 
                 foto_ruta=os.path.join(img_dir, "cuaderno.png"), cant_minima_mayoreo=5),
        Producto("P002", "Boligrafo Azul (caja)",     110.0, 95.0, 200, 20, True,
                 foto_ruta=os.path.join(img_dir, "boligrafo.png"), cant_minima_mayoreo=12),
        Producto("P003", "Lapiz #2 (caja 12 pzas)",   18.0, 15.0, 8,  10, False,
                 foto_ruta=os.path.join(img_dir, "lapiz.png"), cant_minima_mayoreo=6),
        Producto("P004", "Goma de Borrar",              5.0,  4.0, 80, 15, 
                 foto_ruta=os.path.join(img_dir, "goma.png"), cant_minima_mayoreo=10),
        Producto("P005", "Tijeras Escolar",            25.0, 22.0, 30, 5, 
                 foto_ruta=os.path.join(img_dir, "tijeras.png"), cant_minima_mayoreo=5),
        Producto("P006", "Pegamento Barra",            15.0, 13.0, 45, 8, 
                 foto_ruta=os.path.join(img_dir, "pegamento.png"), cant_minima_mayoreo=5),
        Producto("P007", "Regla 30cm",                 12.0, 10.0, 60, 10, 
                 foto_ruta=os.path.join(img_dir, "regla.png"), cant_minima_mayoreo=10),
        Producto("P008", "Folder Manila",               4.0,  3.5, 150, 20, 
                 foto_ruta=os.path.join(img_dir, "folder.png"), cant_minima_mayoreo=25),
        Producto("P009", "Cinta Adhesiva",             10.0,  8.0, 3,   5, 
                 foto_ruta=os.path.join(img_dir, "cinta.png"), cant_minima_mayoreo=3),
        Producto("P010", "Marcador Permanente",        18.0, 16.0, 25, 5, 
                 foto_ruta=os.path.join(img_dir, "marcador.png"), cant_minima_mayoreo=5),
        Producto("P011", "Sacapuntas Plastico",          6.0,  5.0, 120, 15, cant_minima_mayoreo=15),
        Producto("P012", "Colores (caja 12 pzas)",     45.0, 38.0, 40, 8, cant_minima_mayoreo=8),
        Producto("P013", "Plastilina Barra",            8.0,  6.5, 90, 10, cant_minima_mayoreo=10),
        Producto("P014", "Sacapuntas Metalico",        10.0,  8.0, 75, 10, cant_minima_mayoreo=10),
        Producto("P015", "Calculadora Cientifica",    220.0, 195.0, 15, 3, cant_minima_mayoreo=3),
        Producto("P016", "Marcatextos Amarillo",       14.0, 12.0, 50, 8, cant_minima_mayoreo=8),
        Producto("P017", "Juego de Geometria",         38.0, 32.0, 35, 5, cant_minima_mayoreo=5),
        Producto("P018", "Papel Bond (pliego)",         5.0,  4.0, 200, 20, cant_minima_mayoreo=20),
        Producto("P019", "Cartulina Blanca",            6.0,  5.0, 150, 20, cant_minima_mayoreo=20),
        Producto("P020", "Compas de Precision",        45.0, 39.0, 20, 5, cant_minima_mayoreo=5),
        Producto("P021", "Engrapadora Standard",       85.0, 75.0, 12, 3, cant_minima_mayoreo=3),
        Producto("P022", "Grapas (caja 5000 pzas)",    25.0, 21.0, 30, 5, cant_minima_mayoreo=5),
        Producto("P023", "Clips Standard (caja)",      15.0, 12.5, 80, 10, cant_minima_mayoreo=10),
        Producto("P024", "Libreta de Tareas",          18.0, 15.0, 60, 10, cant_minima_mayoreo=10),
        Producto("P025", "Folder Plastico Oficio",     12.0, 10.0, 100, 15, cant_minima_mayoreo=15),
        Producto("P026", "Hojas Blancas (paq 500h)",   95.0, 85.0, 25, 5, cant_minima_mayoreo=5),
        Producto("P027", "Pintura Acrilica 100ml",     28.0, 24.0, 40, 8, cant_minima_mayoreo=8),
        Producto("P028", "Pincel Redondo #6",          12.0,  9.5, 60, 10, cant_minima_mayoreo=10),
        Producto("P029", "Cutter Mediano",             18.0, 15.0, 50, 8, cant_minima_mayoreo=8),
        Producto("P030", "Diurex Chico (rollo)",        4.0,  3.2, 180, 20, cant_minima_mayoreo=20),
    ]

    for p in productos:
        if dm.agregar_producto(p):
            print(f"  [OK] Producto: {p.nombre_prod} (Imagen: {'Si' if p.foto_ruta else 'No'})")

    # Clientes deudores demo
    c1 = ClienteControl(1, "Roberto Perez", 120.0, "Confiable")
    c2 = ClienteControl(2, "Ana Gonzalez",  550.0, "Malo")
    if dm.agregar_cliente(c1): print("  [OK] Cliente Roberto Perez agregado")
    if dm.agregar_cliente(c2): print("  [OK] Cliente Ana Gonzalez agregado (bloqueado por deuda)")

    print("\nDatos iniciales cargados correctamente!")
    print("Inicia el sistema con:  python main.py")

if __name__ == "__main__":
    sembrar()