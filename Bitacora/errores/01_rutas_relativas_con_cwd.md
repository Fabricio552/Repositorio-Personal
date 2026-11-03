# Error 01: Rutas rotas al usar `Path.cwd()`

## Qué me pasó
Quise correr un script desde la terminal (`python Bitacora/Scripts/transito_aire.py`) y me saltó este error de la nada:
```text
FileNotFoundError: [Errno 2] No such file or directory: 
'C:\...\Repositorio-Personal\Repositorio-Personal\Bitacora\Data\...'
```

## Por qué pasó
En el script tenía escrito esto:
```python
# CÓDIGO CON ERROR
BASE_DIR = Path.cwd()
SUBCARPETA = BASE_DIR / "Repositorio-Personal/Bitacora/Data"
```
`Path.cwd()` agarra la carpeta donde tenés abierta la terminal en ese momento. Como yo ya estaba parado adentro de `Repositorio-Personal`, me duplicó el nombre de la carpeta y buscaba en una ruta que no existía. Solo andaba si corría el script parado un nivel arriba.

## Cómo me di cuenta
Al probar correr los scripts por fuera del botón de play de VS Code, navegando con `cd` en la consola de PowerShell.

## Cómo lo arreglé
Cambié la lógica para anclar la búsqueda al archivo que se está ejecutando (`Path(__file__).resolve()`) y no a la consola:
```python
# CÓDIGO CORREGIDO
from pathlib import Path

# Subo dos niveles desde la carpeta Scripts hasta la raíz del repo
RAIZ = Path(__file__).resolve().parents[2]
DATA_DIR = RAIZ / "Bitacora" / "Data"
```
Además, armé la función `buscar_raiz()` en `Bitacora/funciones/raiz_proyecto.py` que sube carpetas buscando el `.git` para que ande siempre.
