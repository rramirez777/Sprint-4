import ctypes
import os
import sys

def cargar_sdl3():
    raiz = os.path.dirname(os.path.abspath(sys.argv[0]))
    ruta_sdl = os.path.join(raiz, "Core", "SDL3.dll")

    print("Intentando cargar SDL3 desde:", ruta_sdl)

    if not os.path.exists(ruta_sdl):
        print("❌ SDL3.dll no encontrado.")
        return False

    try:
        ctypes.WinDLL(ruta_sdl)
        print("✅SDL3 cargado correctamente")
        return True

    except OSError as e:
        print(f"⚠ Error al cargar SDL3: {e}")
        return False
