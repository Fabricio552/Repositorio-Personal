"""Módulo para el diagnóstico y perfilado rápido de valores faltantes y nulos falsos."""

from typing import Any
import pandas as pd


def diagnosticar_faltantes(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula un perfil detallado de datos ausentes y cadenas vacías por columna.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a diagnosticar.

    Returns
    -------
    pd.DataFrame
        Tabla resumen con conteos y porcentajes de nulos, falsos nulos y tipo de dato.
    """
    total_filas = len(df)
    registros: list[dict[str, Any]] = []

    for col in df.columns:
        n_nulos = int(df[col].isnull().sum())
        pct_nulos = (n_nulos / total_filas) * 100 if total_filas > 0 else 0.0

        # Cadenas vacías excluyendo valores ya nulos (NaN / None)
        validos = df[col].dropna()
        if pd.api.types.is_string_dtype(validos.dtype) or validos.dtype == "object":
            n_vacios = int((validos.astype(str).str.strip() == "").sum())
        else:
            n_vacios = 0

        n_unicos = int(df[col].nunique(dropna=True))

        registros.append({
            "columna": col,
            "tipo": str(df[col].dtype),
            "n_nulos": n_nulos,
            "pct_nulos": round(pct_nulos, 2),
            "cadenas_vacias": n_vacios,
            "valores_unicos": n_unicos,
        })

    resumen = pd.DataFrame(registros)
    return resumen.sort_values(by="pct_nulos", ascending=False).reset_index(drop=True)



# Caso de prueba

if __name__ == "__main__":
    import numpy as np

    print("=== Test de funciones/resumen_faltantes.py ===")

    df_ejemplo = pd.DataFrame({
        "id": [1, 2, 3, 4],
        "estacion": ["Tres Cruces", "Colon", "", None],
        "valor": [15.2, np.nan, 22.0, np.nan],
    })

    diagnostico = diagnosticar_faltantes(df_ejemplo)
    print(diagnostico)

    assert diagnostico.loc[diagnostico["columna"] == "valor", "n_nulos"].values[0] == 2
    assert diagnostico.loc[diagnostico["columna"] == "estacion", "cadenas_vacias"].values[0] == 1

    print("[OK] Caso de prueba superado exitosamente.")
