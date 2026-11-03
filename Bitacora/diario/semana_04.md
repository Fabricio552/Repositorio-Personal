# Bitácora Semana 4 — 01/09 al 05/09
**Tema:** Libros de códigos y datos faltantes  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Cruzar la tabla simulada de respuestas con el libro de códigos (`libro de código.csv`), chequear si había filas duplicadas y buscar si teníamos una columna que sirviera de ID único.

## Qué falló
Al cargar el archivo las columnas me quedaron todas pegadas en una sola porque el separador era `;` y no `,`. Además, `isnull()` no me contaba celdas que parecían vacías pero en realidad tenían espacios en blanco (`""`).

## Qué decidí
Usar `sep=';'` y agregar una línea con `(df == "").sum()` para pescar esos falsos nulos antes de ponerme a transformar nada.
