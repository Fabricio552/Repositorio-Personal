# Error 04: El notebook de Jupyter se infló a más de 10 MB

## Qué me pasó
El archivo `Bitacora/Scripts/Analisis_del_csv.ipynb` terminó pesando **10.6 MB**. Cada vez que quería hacer un `git diff` la terminal se me colgaba, y clonar el repo tardaba una eternidad.

## Por qué pasó
Jupyter guarda dentro del archivo JSON no solo el código que escribís, sino también todas las salidas de las celdas: tablas HTML con miles de filas y los gráficos de Matplotlib convertidos en cadenas de texto larguísimas en base64. El notebook tenía más de 10 millones de caracteres de puro dibujo embebido.

## Cómo me di cuenta
Al revisar el peso de los archivos del repo con Git y notar que el notebook era casi tan pesado como una base de datos entera.

## Cómo lo arreglé
1. Borré las salidas de las celdas antes de commitear (en VS Code se puede hacer con el botón "Clear All Outputs" o con un script chico de Python).
2. Con eso el notebook bajó de **10.6 MB a 142 KB** (más del 98% menos) sin perder una sola línea de código ni explicación.
3. Los gráficos importantes los exporté como `.png` a la carpeta `Bitacora/Documentos/` para poder verlos fácil en el repositorio sin engordar el notebook.
