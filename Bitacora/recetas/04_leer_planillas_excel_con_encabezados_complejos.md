# Receta 04: Leer planillas Excel (.xlsx) con títulos o celdas combinadas

## Cuándo usar esto
Cuando tenés que cargar un Excel institucional (como `Trabajos_Objetos.xlsx` o informes del Estado) que no arranca prolijo en la primera celda: trae títulos grandes arriba, logos, notas al pie o varias pestañas. Si tirás `pd.read_excel()` sin parámetros, pandas te toma los títulos como nombres de columna (`Unnamed: 0`, `Unnamed: 1`).

---

## Cómo lo resuelvo en Python (Pandas)

```python
import pandas as pd
from pathlib import Path

archivo = Path("Bitacora/Data/Trabajos_Objetos.xlsx")

# 1. Mirar qué hojas tiene el archivo antes de abrirlo todo
excel = pd.ExcelFile(archivo)
print("Hojas que trae:", excel.sheet_names)

# 2. Cargar salteando las filas de adorno iniciales y eligiendo columnas
df = pd.read_excel(
    archivo,
    sheet_name=0,          # primera hoja, o el nombre: sheet_name="Datos"
    skiprows=2,            # saltea las 2 primeras filas de títulos
    usecols="A:F",         # agarra solo el rango de columnas que importan
    engine="openpyxl"
)

# 3. Limpiar filas de notas al pie que no tengan ID
df = df.dropna(subset=["id"]).reset_index(drop=True)

print("Datos limpios:")
print(df.head())
```

---

## Ojo con esto
- Requiere tener instalado `openpyxl` (`pip install openpyxl`).
- Si en el Excel había categorías combinadas hacia abajo (celdas combinadas), se puede usar `df.ffill()` (*forward fill*) para rellenar los huecos vacíos con el valor de la fila de arriba.
