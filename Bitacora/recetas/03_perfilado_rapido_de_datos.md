# Receta 03: Perfilado rápido de datos crudos (Paso 2 del flujo)

## Cuándo usar esto
Antes de ponerte a limpiar, filtrar o cambiar tipos de datos. La profe nos remarcó que limpiar a ciegas es el peor error: primero hay que diagnosticar qué tenemos entre manos (cuántas filas, cuántas columnas, qué tipos tomó pandas, cuántos nulos hay y cuál puede ser la clave primaria).

---

## Cómo lo resuelvo en Python (Pandas)

Armé esta función simple para que me imprima un resumen completo:

```python
import pandas as pd

def perfilar(df: pd.DataFrame, nombre: str = "Tabla") -> None:
    print(f"\n--- PERFILADO: {nombre} ---")
    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"Filas duplicadas exactas: {df.duplicated().sum()}")
    
    resumen = pd.DataFrame({
        "Tipo": df.dtypes,
        "Nulos (NaN)": df.isnull().sum(),
        "% Nulos": (df.isnull().sum() / len(df) * 100).round(2),
        "Textos vacíos": [(df[c].astype(str).str.strip() == '').sum() if df[c].dtype == 'object' else 0 for c in df.columns],
        "Valores únicos": df.nunique()
    })
    print("\nResumen por columna:")
    print(resumen)

    # Buscar columnas que puedan ser clave primaria (sin repetidos)
    claves = [col for col in df.columns if df[col].nunique() == len(df)]
    if claves:
        print(f"\nPosible clave primaria única: {claves}")
    else:
        print("\nOjo: Ninguna columna sola tiene valores únicos para todas las filas.")

# Ejemplo de uso:
# perfilar(mi_df, "Encuesta de clase")
```

---

## Cómo lo miro en R

```r
library(dplyr)

glimpse(datos)
summary(datos)
sum(duplicated(datos))
```

---

## Qué anotar para el informe
- Cantidad de filas y columnas de partida.
- Cuál es la clave candidata a identificador.
- Si los nulos parecen ser al azar (MCAR/MAR) o si faltan por un motivo concreto (MNAR).
