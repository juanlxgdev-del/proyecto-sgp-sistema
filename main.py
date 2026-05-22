# Credenciales del Sistema:
#   Administrador -> usuario: admin        | contrasenia: admin123
#   Trabajador    -> usuario: trabajador 1 | contrasenia: trabajador123

import sys
import os

# Asegurar que el directorio raiz este en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontend.login import VentanaLogin
from frontend.ventana_principal import VentanaPrincipal

def main():
    login = VentanaLogin()
    login.mainloop()

    usuario = login.obtener_usuario()
    if not usuario:
        return

    app = VentanaPrincipal(usuario)
    app.mainloop()

if __name__ == "__main__":
    main()
