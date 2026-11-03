# Bitácora Semana 7 — 22/09 al 26/09
**Tema:** Unir tránsito vehicular con sensores de aire  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Cruzar los datos de tránsito de los detectores Autoscope de Tres Cruces con las estaciones de aire para ver si a más autos subía el $NO_2$ o el $PM_{2.5}$.

## Qué falló
Quise hacer un `merge` directo y casi me explota la memoria de la compu. Los detectores miden minuto a minuto por carril y los datos de aire estaban a nivel horario, así que las marcas de tiempo no coincidían.

## Qué decidí
Agregar primero todo el tránsito a nivel de promedio horario y por estación, y recién ahí hacer el join con la tabla de aire para trabajar con una base limpia y manejable.
