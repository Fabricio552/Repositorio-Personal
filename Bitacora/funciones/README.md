# Funciones útiles propias — Bitácora

En esta carpeta guardé tres funciones sencillas que me sirvieron durante el semestre para resolver problemas comunes con los datos y no tener que andar copiando y pegando el mismo código en cada script nuevo.

Cada archivo está pensado para poder importarse o correrse directo, y abajo del todo tiene una prueba chica (`if __name__ == "__main__":`) para verificar que ande bien.

---

## Qué hace cada archivo

1. **[`raiz_proyecto.py`](raiz_proyecto.py)**:
   - Resuelve el problema de las rutas relativas. Busca hacia arriba hasta encontrar el archivo `.git` o la carpeta `Bitacora`, funcionando igual que la librería `here` de R.
   - Tiene `ruta_datos("nombre_archivo.csv")` para apuntar a la carpeta `Bitacora/Data/` sin importar desde dónde corras el script en la terminal.

2. **[`carga_robusta.py`](carga_robusta.py)**:
   - Resuelve los líos de codificación y delimitadores al leer CSVs en Uruguay. Prueba automáticamente `latin1`, `utf-8` y `cp1252` con coma o punto y coma hasta encontrar la combinación que no se rompe.
   - Te devuelve el DataFrame listo y un diccionario con qué codificación y separador detectó.

3. **[`resumen_faltantes.py`](resumen_faltantes.py)**:
   - Hace un diagnóstico rápido de la tabla: te muestra columna por columna el tipo de dato, cuántos `NaN` hay, qué porcentaje representan y cuántas celdas tienen textos vacíos `""` que pandas a veces no cuenta como nulos.

---

## Cómo probarlas
Podés correr cada una directo desde la terminal para verificar que los tests pasen:

```bash
python "Bitacora/funciones/raiz_proyecto.py"
python "Bitacora/funciones/carga_robusta.py"
python "Bitacora/funciones/resumen_faltantes.py"
```
