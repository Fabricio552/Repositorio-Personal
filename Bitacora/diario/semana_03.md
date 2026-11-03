# Bitácora Semana 3 — 25/08 al 29/08
**Tema:** Carga de datos y formatos en Python  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Cargar con pandas y pathlib los primeros datasets reales de empleo (`12561_tasa_de_empleo_segun_nivel_educativo-_total_pais.csv`) y la planilla de Excel `Trabajos_Objetos.xlsx`.

## Qué falló
Al hacer `pd.read_csv()` me saltó de una `UnicodeDecodeError`. El archivo tenía caracteres en español (tildes, eñes) guardados en formato Latin-1 y Python por defecto intentaba leerlo en UTF-8.

## Qué decidí
No tocar el archivo crudo a mano para no romper la reproducibilidad. Le pasé `encoding='latin1'` a pandas y me anoté una receta con los parámetros para que no me vuelva a pasar.
