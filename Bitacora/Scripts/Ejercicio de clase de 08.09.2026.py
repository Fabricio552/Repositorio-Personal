from pathlib import Path
import pandas as pd

# 1. Definir la ruta raíz del proyecto o del directorio de trabajo actual
BASE_DIR = Path.cwd()

# 2. Construir las rutas de forma segura para ambos archivos
archivo_respuestas = "Tabla simulada de respuestas.csv"
archivo_codigos = "libro de código.csv"

ruta_respuestas = BASE_DIR / "Repositorio-Personal" / "Bitacora" / "Data" / archivo_respuestas
ruta_codigos = BASE_DIR / "Repositorio-Personal" / "Bitacora" / "Data" / archivo_codigos

# 3. Verificar que los archivos realmente existen antes de cargarlos
if not ruta_respuestas.exists():
    raise FileNotFoundError(f"No se encontró el archivo en: {ruta_respuestas}")
if not ruta_codigos.exists():
    raise FileNotFoundError(f"No se encontró el archivo en: {ruta_codigos}")

# 4. Cargar los archivos CSV
# Nota: Si te da error de lectura por los acentos, cambia encoding='utf-8' a encoding='latin1'
# Si los datos aparecen en una sola columna, cambia sep=',' por sep=';'

df_respuestas = pd.read_csv(ruta_respuestas, encoding='latin1', sep=';')
df_codigos = pd.read_csv(ruta_codigos, encoding='latin1', sep=';')

# 5. Inspección inicial de la tabla de respuestas
print(f"--- Archivo cargado exitosamente: {ruta_respuestas.name} ---")
print(df_respuestas.info())
print("\nPrimeras 5 filas:")
print(df_respuestas.head())

## 5.1. Dimensiones y estructura de los datos
print("\nDimensiones de la tabla de respuestas:", df_respuestas.shape)

# 5.2. Filas únicas: detectando la columna que contiene el ID
# En este caso, asumimos que la columna se llama 'id'
if 'id' in df_respuestas.columns:
    duplicados_id = df_respuestas.duplicated(subset=['id']).sum()
    print(f"\nFilas duplicadas usando 'id': {duplicados_id}")
    
    # Validar si el id es realmente único
    if df_respuestas['id'].nunique() == len(df_respuestas):
        print("La columna 'id' funciona correctamente como identificador único.")
else:
    print("\nAdvertencia: No se encontró la columna 'id' en el DataFrame.")

print("\nValores únicos por columna:")
print(df_respuestas.nunique())

# 5.3 Datos faltantes
print("\nConteo de datos nulos (NA) por columna:")
print(df_respuestas.isnull().sum())

print("\nConteo de cadenas vacías (falsos nulos) por columna:")
print((df_respuestas == "").sum())

## 5.4 Duplicados generales
print(f"\nCantidad de filas exactamente iguales en todas sus columnas: {df_respuestas.duplicated().sum()}")

# Opcional: Echar un vistazo rápido al libro de códigos
print("\n--- Libro de Códigos ---")
print(df_codigos.head())