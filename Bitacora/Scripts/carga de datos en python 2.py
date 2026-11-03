# %%
from pathlib import Path
import pandas as pd

# 1. Definir la ruta raíz del proyecto de forma dinámica y portable
try:
    BASE_DIR = Path(__file__).resolve().parents[2]
except NameError:
    BASE_DIR = Path.cwd().resolve()

candidatos_data = [
    BASE_DIR / "Bitacora" / "Data",
    BASE_DIR / "Repositorio-Personal" / "Bitacora" / "Data",
    Path.cwd() / "Bitacora" / "Data",
    Path.cwd() / "Data",
]
DATA_DIR = next((p for p in candidatos_data if p.exists()), BASE_DIR / "Bitacora" / "Data")

archivo = "12561_tasa_de_empleo_segun_nivel_educativo-_total_pais.csv"
ruta_csv = DATA_DIR / archivo

# 2. Verificar que el archivo realmente existe antes de cargarlo
if not ruta_csv.exists():
    raise FileNotFoundError(f"No se encontró el archivo en: {ruta_csv}")

# 3. Cargar el archivo CSV
df = pd.read_csv(ruta_csv, encoding="latin1", sep=",")

# 4. Inspección inicial de los datos
print(f"--- Archivo cargado exitosamente desde: {ruta_csv.name} ---")
print(df.info())
print("\nPrimeras 5 filas:")
print(df.head())

## 4.1. Dimensiones y estructura de los datos (Equivalente a str(df))
print("\nDimensiones:", df.shape)

# 4.2. Filas únicas: analizando las variables principales
print("Cantidad de niveles educativos distintos:", df["nivel_educa"].nunique())
print("Cantidad de años registrados:", df["año"].nunique())

# Comprobamos si la combinación de "nivel_educa" y "año" funciona como un ID único
duplicados_id = df.duplicated(subset=["nivel_educa", "año"]).sum()
print(f"Filas duplicadas usando nivel_educa + año como ID: {duplicados_id}")

print("\nValores únicos por columna (Buscar candidatos a ID):")
print(df.nunique())

# 4.3. Datos faltantes
print("\nConteo de nulos por columna:")
print(df.isnull().sum())
print("\nFalsos nulos (cadenas vacías):")
print((df == "").sum())

## 4.4. Duplicados exactos
print("\nFilas duplicadas exactas:", df.duplicated().sum())

# %%
