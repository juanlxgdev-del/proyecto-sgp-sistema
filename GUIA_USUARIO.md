# SGP - GUÍA DE USUARIO

Bienvenido a la guía oficial del **Sistema de Gestión Papelera (SGP)**. En este documento aprenderás paso a paso cómo poner en marcha el sistema, operar las ventas diarias, administrar el inventario y exportar reportes financieros.

---

## 1. CÓMO DESCARGAR Y ABRIR EL PROYECTO

SGP está optimizado para ejecutarse en cualquier sistema operativo (Windows, macOS o Linux) sin requerir pasos de configuración difíciles.

1.  **Clonar o Descargar el Repositorio:**
    *   Descarga el archivo `.zip` del repositorio de GitHub y extráelo en una carpeta local de tu computadora.
    *   *O alternativamente*, clónalo con Git desde tu consola:
        ```bash
        git clone https://github.com/tu-usuario/SGP.git
        ```
2.  **Abrir en tu Editor de Código:**
    *   Abre tu editor de código favorito (se recomienda encarecidamente **Visual Studio Code**).
    *   Selecciona la opción **Archivo -> Abrir Carpeta** y elige el directorio raíz del proyecto (`SGP`).

---

## 2. CÓMO INICIAR EL SISTEMA (PASO A PASO)

El proyecto incluye un entorno virtual de Python (`.venv`) preconfigurado con las librerías necesarias. Sigue estos sencillos pasos en la terminal de VS Code (abierta con `` Ctrl + ` `` o seleccionando **Terminal -> Nueva Terminal**):

### Paso 1: Activar el Entorno Virtual
Dependiendo de tu sistema operativo y consola, ejecuta el comando correspondiente:

*   **En Windows (PowerShell - Recomendado):**
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
    *(Nota: Si obtienes un error de políticas de ejecución en Windows, corre primero `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` en tu terminal).*
*   **En Windows (CMD / Símbolo del Sistema):**
    ```cmd
    .\.venv\Scripts\activate.bat
    ```
*   **En Linux o macOS (Bash/Zsh):**
    ```bash
    source .venv/bin/activate
    ```

### Paso 2: Inicializar / Sembrar la Base de Datos (Solo la primera vez)
Para cargar el catálogo inicial de productos de papelería, los clientes deudores de demostración y registrar a los usuarios autorizados en la base de datos JSON local, ejecuta:
```bash
python seed_data.py
```
*(Verás en consola una confirmación exitosa con la leyenda `Datos iniciales cargados correctamente!`)*.

### Paso 3: Iniciar la Aplicación
Para ejecutar el punto de venta gráfico de inmediato, corre el siguiente comando:
```bash
python main.py
```

---

## 3. CÓMO INICIAR SESIÓN (CREDENCIALES)

Al ejecutarse `main.py`, aparecerá la pantalla elegante de inicio de sesión de SGP. Las credenciales de demostración por defecto son:

### A) Rol Trabajador (Operación Diaria)
*   **Usuario:** `trabajador 1`
*   **Contraseña:** `trabajador123`
*   *Nota:* Este usuario no tiene acceso a los paneles confidenciales de Dashboard, Reportes Financieros, Cambios de precios ni Gestión de Usuarios.

### B) Rol Administrador (Control Total)
*   **Usuario:** `admin`
*   **Contraseña:** `admin123`
*   *Nota:* Este usuario tiene acceso irrestricto a todas las funcionalidades operativas y administrativas del sistema.

---

## 4. CÓMO REALIZAR UNA VENTA

Una vez dentro de la sesión con tu usuario (`trabajador 1` o `admin`), sigue estos pasos para procesar una compra:

1.  **Buscar el Producto:**
    *   En la pestaña **Ventas**, haz clic en el cuadro de búsqueda en la parte superior y escribe parte del nombre del producto (ej: "Cuaderno") o su código ID (ej: "P001").
    *   Haz clic en **Buscar**. Los productos coincidentes aparecerán en la lista izquierda.
2.  **Ver el Producto e Imagen:**
    *   Haz clic en el producto dentro de la lista. En el panel de visualización a la derecha verás los detalles y la **imagen real del producto** (por ejemplo, la foto del cuaderno profesional o del bolígrafo azul). Esto ayuda a verificar físicamente que cobras el artículo correcto.
3.  **Agregar al Carrito:**
    *   Haz clic en **Agregar al Carrito**. Se abrirá una ventana emergente preguntando la cantidad de piezas. Escribe el número y pulsa **Aceptar**.
4.  **Configurar Métodos de Pago y Descuentos:**
    *   En el panel de cobro derecho, introduce el porcentaje de **Descuento** si aplica (ej: `5` para 5%).
    *   Selecciona el **Método de Pago** en el menú desplegable:
        *   **Efectivo / Tarjeta:** Pagos de liquidación inmediata.
        *   **Deudor:** Si el cliente tiene cuenta de crédito. El sistema te pedirá asociar el cobro a un cliente registrado (ej. *Roberto Perez*). Si el cliente excede su límite de deuda ($500), el cobro será rechazado automáticamente por seguridad.
5.  **Cobrar:**
    *   Haz clic en el botón de acento azul **COBRAR Y GENERAR TICKET**. ¡La venta se guardará y descontará el inventario al instante!

---

## 5. CÓMO GENERAR Y GUARDAR EL PDF DEL TICKET

¡El sistema genera tus tickets automáticamente! No requiere que realices pasos manuales adicionales:

1.  **Generación Automática:** Al presionar **COBRAR Y GENERAR TICKET**, la venta queda consolidada y la librería backend `FPDF` genera instantáneamente un archivo PDF estilizado del recibo con la marca de tu tienda, detalles de los productos, desglose de subtotales, descuentos y totales.
2.  **Dónde encontrar el Ticket:**
    *   Todos los tickets se guardan de forma permanente dentro de la carpeta del proyecto en la ruta:
        `[Directorio del Proyecto SGP]/data/tickets/`
    *   Los archivos están ordenados por ID con el formato: `ticket_1.pdf`, `ticket_2.pdf`, etc.
    *   Puedes abrir estos archivos en tu navegador web o visor de PDF habitual e imprimirlos directamente en cualquier impresora de tickets de 58mm o de escritorio.

---

## 6. CÓMO AGREGAR PRODUCTOS CON IMÁGENES

Mantener tu catálogo de papelería al día es fundamental. Para dar de alta un producto nuevo con su foto:

1.  **Ingresar al Módulo:** Haz clic en la pestaña **Inventario** en el menú lateral. (Si iniciaste sesión como Administrador, verás botones para modificar, de lo contrario solo podrás consultar).
2.  **Nuevo Producto:** Haz clic en el botón verde **➕ Nuevo Producto**.
3.  **Llenar el Formulario:**
    *   Escribe el ID del producto (ej: `P011`), Nombre (ej: `Sacapuntas Metálico`), Precio de Menudeo, Precio de Mayoreo, Stock actual, Stock mínimo de alerta.
4.  **Seleccionar la Imagen del Producto:**
    *   Haz clic en el campo **Imagen** o el botón examinador adyacente en el diálogo.
    *   Se abrirá el explorador de archivos nativo de tu computadora. Selecciona la foto del producto (formatos recomendados: `.png` o `.jpg` optimizados).
    *   El sistema automáticamente registrará la ruta de forma portátil dentro de la carpeta `data/imagenes/` para que funcione en cualquier otra computadora.
5.  **Guardar:** Haz clic en **Guardar**. El producto aparecerá de inmediato en tu inventario con su fotografía vinculada.

---

## 7. CÓMO EXPORTAR EL EXCEL PARA EL ADMINISTRADOR

El administrador del negocio puede exportar todo el historial detallado de operaciones comerciales a Excel para auditorías o análisis fiscal:

1.  **Iniciar Sesión como Administrador:** Inicia sesión usando la cuenta de usuario `admin`.
2.  **Ir al Módulo de Reportes:** Selecciona la opción **Dashboard / Reportes** en la barra de navegación lateral.
3.  **Exportar:** Haz clic en el botón verde oliva **🟢 Exportar Excel**.
4.  **Elegir Ruta de Guardado:** Se abrirá el selector de archivos nativo de tu sistema operativo. Elige dónde guardar el archivo (por ejemplo, en tu Escritorio) y haz clic en **Guardar**.
5.  **Detalle Premium:** El sistema ajusta automáticamente el ancho de las columnas de Excel según el contenido para que el reporte sea legible, elegante y profesional inmediatamente al abrirlo.

---

## 8. SOLUCIÓN DE PROBLEMAS COMUNES

*   **Error: "Python was not found..." o "Python no se reconoce como un comando interno"**
    *   *Solución:* Asegúrate de haber activado el entorno virtual (`.venv`) ejecutando primero `.\.venv\Scripts\Activate.ps1`. Si Python sigue sin detectarse, asegúrate de tener instalado Python 3.10+ en tu sistema y haberlo agregado a las Variables de Entorno del sistema (PATH) durante su instalación.
*   **La visualización de reportes / gráficas da error de importación**
    *   *Solución:* Las gráficas avanzadas en el Dashboard del administrador requieren la librería `matplotlib`. Asegúrate de instalarla ingresando al entorno virtual y corriendo: `pip install matplotlib pandas openpyxl Pillow fpdf`.
*   **Las fotos de los productos no se ven en otras computadoras**
    *   *Solución:* Asegúrate de guardar las fotos de los productos directamente en la subcarpeta `data/imagenes/` dentro del directorio del proyecto antes de seleccionarlas. Esto garantiza que las rutas sean portátiles cuando copies o subas la carpeta a otra máquina o a GitHub.
*   **No se puede cobrar a crédito**
    *   *Solución:* El cliente seleccionado puede haber alcanzado su límite máximo de crédito ($500) o su conducta fue clasificada como de riesgo en el panel. Realiza un abono de saldo o modifica su estatus en la pestaña **ClienteControl** para restablecer sus privilegios de compra.
