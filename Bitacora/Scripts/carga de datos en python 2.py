# %%
from pathlib import Path
import pandas as pd

# 1. Definir la ruta raíz del proyecto o del directorio de trabajo actual
BASE_DIR = Path.cwd()

# 2. Construir la ruta relativa de forma segura utilizando el operador /
# Estructura esperada: tu_proyecto/data/raw/datos.csv
archivo = "12561_tasa_de_empleo_segun_nivel_educativo-_total_pais.csv"
ruta_csv = BASE_DIR / "Repositorio-Personal" / "Bitacora" / "Data" / archivo

ruta_csv = BASE_DIR / "Repositorio-Personal" /"Bitacora" / "Data" / "12561_tasa_de_empleo_segun_nivel_educativo-_total_pais.csv"

# 3. Verificar que el archivo realmente existe antes de cargarlo
if not ruta_csv.exists():
    raise FileNotFoundError(f"No se encontró el archivo en: {ruta_csv}")

# 4. Cargar el archivo CSV
df = pd.read_csv(ruta_csv, encoding='latin1', sep=',')

# 5. Inspección inicial de los datos
print(f"--- Archivo cargado exitosamente desde: {ruta_csv.name} ---")
print(df.info())
print("\nPrimeras 5 filas:")
print(df.head())

## 5.1. Dimensiones y estructura de los datos (Equivalente a str(df))
df.info()
# Nota: df.shape te da exactamente las dimensiones (filas, columnas) -> (1222, 41)
df.shape

# 5.2. Filas únicas: detectando la columna que contiene el ID (Equivalente a length(unique(...)))
# 5.2. Filas únicas: analizando las variables principales
print("Cantidad de niveles educativos distintos:", df["nivel_educa"].nunique())
print("Cantidad de años registrados:", df["año"].nunique())

# Comprobamos si la combinación de "nivel_educa" y "año" funciona como un ID único
# Si el resultado es 0, significa que no hay registros repetidos para un mismo nivel en un mismo año
duplicados_id = df.duplicated(subset=['nivel_educa', 'año']).sum()
print(f"Filas duplicadas usando nivel_educa + año como ID: {duplicados_id}")
# Si df["columna"].nunique() es igual a len(df), esa columna es un ID único
print("\nValores únicos por columna (Buscar candidatos a ID):")
print(df.nunique())

# 5.3 Datos faltantes

df.isnull().sum()  # Conteo de NA por columna
(df == "").sum()   # Falsos nulos (cadenas vacías)

## 5.4 Duplicados
df.duplicated().sum() # Cantidad de filas exactamente iguales

## 5.5. Primeras filas
print("\nPrimeras 5 filas:")
print(df.head())
