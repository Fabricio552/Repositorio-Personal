"""Módulo para resolución robusta y portable de rutas del proyecto.

Inspirado en la librería `here` de R. Permite obtener rutas absolutas
confiables independientemente de la carpeta desde la que se ejecute el script.
"""

from pathlib import Path
from typing import Sequence


def buscar_raiz(
    marcadores: Sequence[str] = (".git", "_quarto.yml", ".here"),
    inicio: Path | None = None,
) -> Path:
    """Busca hacia arriba en el árbol de directorios hasta encontrar un marcador de la raíz.

    Parameters
    ----------
    marcadores : Sequence[str]
        Archivos o carpetas que identifican la raíz del proyecto (ej. .git).
    inicio : Path, optional
        Punto de partida de la búsqueda. Por defecto usa la ubicación de este archivo.

    Returns
    -------
    Path
        Ruta absoluta al directorio raíz del proyecto.
    """
    if inicio is None:
        try:
            actual = Path(__file__).resolve().parent
        except NameError:
            actual = Path.cwd().resolve()
    else:
        actual = Path(inicio).resolve()

    for carpeta in [actual, *actual.parents]:
        if any((carpeta / m).exists() for m in marcadores):
            return carpeta

    for carpeta in [actual, *actual.parents]:
        if carpeta.name == "Bitacora":
            return carpeta.parent

    return actual


def ruta_datos(nombre_archivo: str = "") -> Path:
    """Retorna la ruta absoluta hacia la carpeta Data de la Bitácora.

    Parameters
    ----------
    nombre_archivo : str, optional
        Nombre de un archivo dentro de Data. Si se omite, retorna la carpeta Data.
    """
    raiz = buscar_raiz()
    candidatos = [
        raiz / "Bitacora" / "Data",
        raiz / "Data",
    ]
    for c in candidatos:
        if c.exists():
            return (c / nombre_archivo) if nombre_archivo else c

    data_dir = raiz / "Bitacora" / "Data"
    return (data_dir / nombre_archivo) if nombre_archivo else data_dir


# =============================================================================
# Caso de prueba
# =============================================================================
if __name__ == "__main__":
    print("=== Test de funciones/raiz_proyecto.py ===")
    raiz = buscar_raiz()
    print(f"Raiz detectada: {raiz}")
    assert (raiz / ".git").exists(), "La raiz detectada debe contener .git"

    data_dir = ruta_datos()
    print(f"Carpeta de datos: {data_dir}")
    assert data_dir.exists(), "La carpeta de datos debe existir"

    print("[OK] Caso de prueba superado exitosamente.")
