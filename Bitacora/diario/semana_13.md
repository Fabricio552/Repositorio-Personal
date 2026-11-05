# Bitácora Semana 13 — 03/11 al 07/11
**Tema:** Revisión por pares del proyecto "datos-espaciales"  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Clonar y auditar el repositorio del equipo asignado (`datos-espaciales`) para evaluar su reproducibilidad y darles una devolución técnica y metodológica según la consigna de la clase.

## Qué falló
El repo tenía salidas pesadas versionadas (un mapa HTML de 38 MB y capas GeoPackage), carpetas desordenadas con archivos duplicados y un `requirements.txt` vacío. En lo metodológico, el script de transporte definía la población dependiente usando solo edades <14 y >80 (dependencia demográfica), dejando afuera a estudiantes de secundaria/universidad y trabajadores sin auto, que son los usuarios cautivos reales del ómnibus en Montevideo.

## Qué decidí
Armarles un feedback constructivo recomendando excluir salidas con `.gitignore` y regenerarlas con scripts, ordenar la estructura del proyecto y ajustar la definición del índice de necesidad de transporte; y registrar esta revisión en mi bitácora como aprendizaje para no cometer los mismos errores en nuestro código.

