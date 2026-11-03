# Error 03: Caracteres rotos (Mojibake) en comentarios y strings

## Qué me pasó
Al abrir scripts o mirar el código en GitHub, palabras comunes con tildes o eñes se veían totalmente deformadas:
- `Versión` aparecía como `VersiA3n`
- `pingüinos` aparecía como `pingAinos`
- `código` aparecía como `cA3digo`
- `mañana` aparecía como `maAana`

## Por qué pasó
En Windows los editores y la consola suelen usar por defecto codificaciones como CP1252 o Latin-1, mientras que Git y las herramientas modernas esperan UTF-8. Al abrir o guardar un archivo interpretando los bytes en una codificación distinta, los caracteres especiales se corrompen (lo que se conoce como *mojibake*).

## Cómo me di cuenta
Al leer los comentarios en GitHub y al ver que los títulos de los gráficos en Matplotlib salían con signos de interrogación o símbolos raros.

## Cómo lo arreglé
1. Guardar siempre los archivos de código (`.py`, `.R`, `.md`) en formato **UTF-8 sin BOM(Byte Order Mark)**.
2. Cuando cargo archivos externos con `pd.read_csv()`, poner de forma explícita `encoding='latin1'` si los datos crudos vienen en esa codificación.
3. Para limpiar nombres de columnas en scripts de calidad del aire, armé una función chica de reemplazo con diccionario para normalizar textos antes de graficar.
