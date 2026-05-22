# Sistema de Gestion Papelera (SGP)

Bienvenido al **Sistema de Gestion Papelera (SGP)**. Esta es una aplicacion de escritorio premium, responsiva y robusta desarrollada en Python utilizando Tkinter para la interfaz grafica y una arquitectura local agil basada en almacenamiento JSON. El software ha sido disenado con un enfoque visual de vanguardia ("Elegant Midnight & Indigo"), optimizado para su ejecucion en pantalla completa y con un rendimiento comercial sobresaliente.

---

## Lanzamiento Rápido

El SGP es una solución integral para papelerías que incluye punto de venta con catálogo visual, facturación automática en PDF, control de inventario con alertas, gestión de créditos a clientes, auditoría de caja chica y análisis de rendimiento con reportes en Excel.

---

## Estructura del Proyecto

A continuación se detalla la función de cada directorio y archivo en la raíz del proyecto para comprender su arquitectura:

```plaintext
SGP/
├── .venv/                  # Entorno virtual con las dependencias locales de Python.
├── backend/                # Lógica de negocio y persistencia de datos.
│   ├── __init__.py
│   ├── data_manager.py     # Manejo de persistencia JSON, generación de tickets PDF y reportes.
│   └── models.py           # Esquemas de datos y lógica orientada a objetos (Usuario, Producto, Venta, etc.).
├── data/                   # Carpeta de almacenamiento de datos locales y multimedia.
│   ├── imagenes/           # Catálogo de imágenes oficiales de los productos en formato PNG.
│   ├── tickets/            # Recibos PDF generados por las transacciones de venta.
│   ├── clientes.json       # Datos locales de control de deudores y saldo de clientes.
│   ├── productos.json      # Listado maestro de productos en inventario.
│   ├── usuarios.json       # Plantilla de credenciales y perfiles de usuarios.
│   ├── ventas.json         # Historial transaccional de ventas realizadas.
│   └── caja_chica.json     # Flujo de egresos y control de caja chica.
├── frontend/               # Módulos de la interfaz gráfica de usuario (GUI) en Tkinter.
│   ├── __init__.py
│   ├── login.py            # Ventana de control de acceso de personal.
│   ├── modulo_caja_chica.py# Panel de control de flujo de efectivo.
│   ├── modulo_clientes.py  # Panel de gestión de créditos y cuentas.
│   ├── modulo_inventario.py# Panel de control y actualización de existencias de productos.
│   ├── modulo_reportes.py  # Dashboard con analíticas gráficas y exportador a Excel.
│   ├── modulo_usuarios.py  # Administración de credenciales de trabajadores.
│   ├── modulo_ventas.py    # Terminal de punto de venta (TPV) ágil e interactiva.
│   ├── styles.py           # Estilos unificados, tipografía y paleta "Elegant Midnight".
│   ├── widgets.py          # Componentes visuales reutilizables de Tkinter.
│   └── ventana_principal.py# Enrutador visual principal con barra de navegación lateral.
├── main.py                 # Script ejecutable principal de entrada al sistema.
├── requirements.txt        # Especificación detallada de todas las dependencias externas necesarias.
├── seed_data.py            # Script semilla para poblar y reiniciar datos de prueba.
├── Sistema_img/            # Recursos gráficos de identidad de la aplicación (Logotipos).
│   ├── Logo principal.png  # Logotipo principal del Login.
│   └── Logo menu.png       # Logotipo de la barra lateral del menú.
└── .gitignore              # Archivo de exclusión que mantiene el repositorio limpio.
```

---

## Compatibilidad del Sistema

El **SGP** está diseñado para ser altamente compatible y multiplataforma, lo que significa que **puede correr sin problemas en cualquier computadora o laptop (Windows, macOS o Linux)**. 

### Requisitos del Sistema:
1. **Python 3.10 o superior**: El lenguaje de programación base.
2. **Bibliotecas Requeridas**: Se listan por completo en `requirements.txt`.
   * **Tkinter**: Interfaz gráfica nativa (viene preinstalado en la mayoría de sistemas Windows/Mac).
   * **Pillow**: Renderizado y redimensionamiento de las imágenes del catálogo en la interfaz.
   * **Matplotlib**: Generación interactiva de gráficos y analíticas de negocio en el dashboard.
   * **Pandas**: Estructuración y cálculo de métricas financieras de ventas.
   * **openpyxl**: Motor necesario para exportar informes detallados directamente a Microsoft Excel (`.xlsx`).
   * **fpdf2**: Motor de generación instantánea de tickets de venta formateados en PDF.

> [!NOTE]
> **Compatibilidad en Linux (Ubuntu/Debian)**:
> La mayoría de distribuciones Linux no incluyen la interfaz nativa `tkinter` por defecto. Si corres el sistema en Linux, ejecuta lo siguiente en la terminal antes de iniciar el programa:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## Instalacion y Configuracion Local

Sigue estos pasos en cualquier laptop o computadora para poner en marcha el sistema:

### 1. Clonar el repositorio
Abre una terminal y clona el proyecto en tu carpeta local de preferencia:
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd SGP
```

### 2. Crear y activar el entorno virtual
* **En Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **En macOS y Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar dependencias
Instala todas las librerías necesarias compiladas en el archivo de requerimientos:
```bash
pip install -r requirements.txt
```

### 4. Inicializar Base de Datos Semilla con Catálogo de Imágenes
El sistema cuenta con un catálogo inicial de **10 productos oficiales** precargados con imágenes premium de alta calidad (AI e ilustraciones fotorrealistas de estudio). Para poblar tu base de datos local y enlazar las imágenes automáticamente, ejecuta:
```bash
python seed_data.py
```

---

## Ejecucion del Sistema

Para iniciar el sistema de gestión papelera en pantalla completa, asegúrate de tener el entorno virtual activado y ejecuta:
```bash
python main.py
```

### Credenciales de Acceso por Defecto:
* **Administrador**:
  * **Usuario**: `admin`
  * **Contraseña**: `admin123`
* **Trabajadores**:
  * **Usuario**: `trabajador 1` | **Contraseña**: `trabajador123`

¡Disfruta del uso del Sistema de Gestión Papelera! El software está listo para ser desplegado en producción local.
