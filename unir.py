import os

# Carpetas y archivos a ignorar
IGNORAR = {"migrations", "staticfiles", ".git", ".gitignore", "__pycache__", "venv", "node_modules"}
EXPORT_DIR = "__export__"

# === FUNCIONES ===

def recorrer_archivos(base, extension):
    """Devuelve rutas de archivos con una extensión específica, ignorando carpetas filtradas."""
    for carpeta, subcarpetas, archivos in os.walk(base):
        subcarpetas[:] = [c for c in subcarpetas if c not in IGNORAR]
        for archivo in archivos:
            if archivo.endswith(extension):
                yield os.path.join(carpeta, archivo)


def escribir_contenidos(base, extension, salida_nombre):
    """Crea un .txt con el contenido de todos los archivos de una extensión."""
    salida_dir = os.path.join(base, EXPORT_DIR)
    os.makedirs(salida_dir, exist_ok=True)
    salida = os.path.join(salida_dir, salida_nombre)

    nombre_base = os.path.basename(base)
    with open(salida, "w", encoding="utf-8") as out:
        for ruta in recorrer_archivos(base, extension):
            ruta_relativa = os.path.relpath(ruta, base)
            ruta_final = os.path.join(nombre_base, ruta_relativa).replace("\\", "/")
            out.write(f"------{ruta_final}------\n")
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"[Error leyendo {ruta_relativa}: {e}]")
            out.write("\n\n")
    print(f"✅ {salida_nombre} creado en {EXPORT_DIR}/")


def dibujar_arbol(ruta_base, prefijo="", archivo=None):
    """Escribe la estructura de carpetas en formato árbol."""
    try:
        items = sorted(os.listdir(ruta_base))
    except PermissionError:
        return
    items = [i for i in items if i not in IGNORAR and i != EXPORT_DIR]
    total = len(items)
    for i, item in enumerate(items):
        ruta = os.path.join(ruta_base, item)
        es_ultimo = (i == total - 1)
        conector = "└── " if es_ultimo else "├── "
        archivo.write(prefijo + conector + item + "\n")
        if os.path.isdir(ruta):
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            dibujar_arbol(ruta, nuevo_prefijo, archivo)


def escribir_estructura(base):
    """Genera el archivo estructura.txt"""
    salida_dir = os.path.join(base, EXPORT_DIR)
    os.makedirs(salida_dir, exist_ok=True)
    salida = os.path.join(salida_dir, "estructura.txt")

    nombre_base = os.path.basename(base)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(f"{nombre_base}/\n")
        dibujar_arbol(base, archivo=f)
    print(f"✅ estructura.txt creado en {EXPORT_DIR}/")


# === EJECUCIÓN ===

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))

    escribir_contenidos(base, ".py", "todo_py.txt")
    escribir_contenidos(base, ".html", "todo_html.txt")
    escribir_contenidos(base, ".js", "todo_js.txt")
    escribir_contenidos(base, ".css", "todo_css.txt")
    escribir_estructura(base)

    print("\n🎉 Todos los archivos fueron generados en la carpeta '__export__'.")
