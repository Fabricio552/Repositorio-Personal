# Receta 01: Leer CSVs con problemas de codificación (Encoding) y separador

## Cuándo usar esto
Cuando te pasan un CSV de acá (por ejemplo datos abiertos de intendencias o ministerios de Uruguay) y te pasa una de dos cosas:
1. Te tira `UnicodeDecodeError: 'utf-8' codec can't decode byte...` porque viene en **Latin-1** o **Windows CP1252** por las tildes y eñes.
2. Te abre el dataset pero te mete todas las columnas juntas en una sola porque viene separado por **punto y coma (`;`)** en vez de coma.

---

## Cómo lo resuelvo en Python (Pandas)

```python
import pandas as pd
from pathlib import Path

archivo = Path("Bitacora/Data/mi_archivo.csv")

# 1. Le paso el encoding y el separador correcto de una:
df = pd.read_csv(archivo, encoding="latin1", sep=";")

# 2. Si además los números vienen con coma decimal (ej. "25,4"):
df = pd.read_csv(archivo, encoding="latin1", sep=";", decimal=",")

# 3. Verifico que haya cargado bien:
print("Filas y columnas:", df.shape)
print(df.head(3))
```

---

## Cómo lo resuelvo en R (`readr`)

```r
library(readr)

# read_csv2 ya asume de entrada punto y coma y coma decimal:
df <- read_csv2("Bitacora/Data/mi_archivo.csv", 
                locale = locale(encoding = "Latin1"))
```

---

## Tip importante
Nunca abrir el archivo crudo en Excel y darle "Guardar como" para arreglarlo a mano. Excel suele cambiar el formato de las fechas y borrar los ceros a la izquierda (como en cédulas o códigos postales). El archivo original se deja intacto y se arregla desde el código.
