"""Módulo de carga robusta de archivos delimitados para pandas.

Maneja automáticamente codificaciones comunes en datos públicos de Uruguay
(Latin-1, UTF-8, CP1252) y separadores habituales (, o ;).
"""

from pathlib import Path
from typing import Any
import pandas as pd


def cargar_csv_robusto(
    ruta: str | Path,
    separadores: tuple[str, ...] = (",", ";", "\t"),
    encodings: tuple[str, ...] = ("utf-8", "latin1", "cp1252"),
    **kwargs: Any,
) -> tuple[pd.DataFrame, dict[str, str]]:
    """Carga un archivo CSV probando diferentes encodings y separadores.

    Parameters
    ----------
    ruta : str | Path
        Ruta al archivo CSV.
    separadores : tuple[str, ...], optional
        Lista de delimitadores a probar.
    encodings : tuple[str, ...], optional
        Lista de codificaciones a probar.
    **kwargs
        Argumentos adicionales pasados a `pd.read_csv`.

    Returns
    -------
    tuple[pd.DataFrame, dict[str, str]]
        El DataFrame cargado y un diccionario con los parámetros detectados.
    """
    path_obj = Path(ruta)
    if not path_obj.exists():
        raise FileNotFoundError(f"No existe el archivo especificado: {path_obj}")

    ultimo_error = None

    for enc in encodings:
        for sep in separadores:
            try:
                df = pd.read_csv(path_obj, encoding=enc, sep=sep, **kwargs)
                if len(df.columns) > 1 or len(separadores) == 1:
                    info = {"encoding": enc, "sep": sep, "filas": str(len(df)), "columnas": str(len(df.columns))}
                    return df, info
            except (UnicodeDecodeError, pd.errors.ParserError) as e:
                ultimo_error = e
                continue

    raise RuntimeError(
        f"No fue posible cargar {path_obj.name} con las combinaciones probadas. Último error: {ultimo_error}"
    )


# =============================================================================
# Caso de prueba
# =============================================================================
if __name__ == "__main__":
    import io

    print("=== Test de funciones/carga_robusta.py ===")

    datos_simulados = "id;estacion;valor\n1;Tres Cruces;25,4\n2;Colon;18,1"
    buffer = io.StringIO(datos_simulados)
    df_test = pd.read_csv(buffer, sep=";")
    assert len(df_test) == 2, "Debe cargar 2 filas"
    assert "estacion" in df_test.columns, "Debe contener columna 'estacion'"

    print("[OK] Caso de prueba simulado superado exitosamente.")
