# Bitácora Semana 6 — 15/09 al 19/09
**Tema:** Series de tiempo y calidad del aire  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Empezar con el análisis de calidad del aire en Montevideo usando las mediciones minutales de Ozono ($O_3$) para sacar promedios y ver cómo variaba en el día.

## Qué falló
Cuando quise agrupar las fechas por hora con `pd.Grouper` me tiró error de tipo. Resulta que pandas me había cargado la columna de fecha como texto (`object`) en vez de `datetime`.

## Qué decidí
Agregar `parse_dates=["fecha"]` directamente al leer el CSV y verificar con `df.info()` que las fechas queden reconocidas antes de hacer cualquier filtro temporal.
