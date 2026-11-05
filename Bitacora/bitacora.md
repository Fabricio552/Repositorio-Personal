# Bitácora Personal — Fabricio De Souza
**Materia:** Introducción a la Ciencia de Datos  
**Facultad de Ciencias Empresariales y Economía (FCEE) — Universidad de Montevideo**  

Registro semanal de lo que fui trabajando en el curso, los problemas que me encontré en el camino y las decisiones que fui tomando con el código y los datos.  
*(Formato de la cátedra: una entrada por semana, máximo 150 palabras, con los tres campos obligatorios: Qué intentamos/intenté, Qué falló y Qué decidimos).*

---

## Semana 1 — 11/08 al 15/08: Primeros pasos, Git y pingüinos
- **Qué intenté:** Configurar mi entorno de trabajo en la compu con VS Code y Git, clonar el repo de la materia y probar el primer script de exploración (`ejemplo_pinguinos.py`) con el dataset de los pingüinos de Palmer.
- **Qué falló:** Al querer ejecutar el script desde PowerShell me decía que el comando `python` no se reconocía. Tenía instalado Python pero no había marcado la casilla de agregar al PATH en el instalador de Windows.
- **Qué decidí:** Agregué Python a las variables de entorno a mano, elegí el intérprete correcto en VS Code y verifiqué que funcionara en la terminal antes de armar mi primer commit.

---

## Semana 2 — 18/08 al 22/08: Muestreo, sesgos y encuestas
- **Qué intenté:** Resolver el cuestionario de múltiple opción sobre diseño de encuestas, representatividad y tipos de muestreo que subió la profe (`Ejercicio de multiple opción.pdf`).
- **Qué falló:** Me entreveré en un par de preguntas entre lo que es error de cobertura y sesgo por no respuesta, sobre todo pensando en encuestas que se contestan de forma voluntaria por internet o redes.
- **Qué decidí:** Repasar las diapositivas de clase teórica, anotar bien la diferencia (marco muestral vs quién responde efectivamente) y dejar el PDF resuelto guardado en la carpeta de documentos de la bitácora.

---

## Semana 3 — 25/08 al 29/08: Carga de datos y formatos en Python
- **Qué intenté:** Cargar con pandas y pathlib los primeros datasets reales de empleo (`12561_tasa_de_empleo_segun_nivel_educativo-_total_pais.csv`) y la planilla de Excel `Trabajos_Objetos.xlsx`.
- **Qué falló:** Al hacer `pd.read_csv()` me saltó de una `UnicodeDecodeError`. El archivo tenía caracteres en español (tildes, eñes) guardados en formato Latin-1 y Python por defecto intentaba leerlo en UTF-8.
- **Qué decidí:** No tocar el archivo crudo a mano para no romper la reproducibilidad. Le pasé `encoding='latin1'` a pandas y me anoté una receta con los parámetros para que no me vuelva a pasar.

---

## Semana 4 — 01/09 al 05/09: Libros de códigos y datos faltantes
- **Qué intenté:** Cruzar la tabla simulada de respuestas con el libro de códigos (`libro de código.csv`), chequear si había filas duplicadas y buscar si teníamos una columna que sirviera de ID único.
- **Qué falló:** Al cargar el archivo las columnas me quedaron todas pegadas en una sola porque el separador era `;` y no `,`. Además, `isnull()` no me contaba celdas que parecían vacías pero en realidad tenían espacios en blanco (`""`).
- **Qué decidí:** Usar `sep=';'` y agregar una línea con `(df == "").sum()` para pescar esos falsos nulos antes de ponerme a transformar nada.

---

## Semana 5 — 08/09 al 12/09: Relación de variables y curvas ROC
- **Qué intenté:** Armar el notebook `Analisis_del_csv.ipynb` para ver cómo se relacionaban las variables, calcular la matriz de confusión y graficar la curva ROC para evaluar clasificadores.
- **Qué falló:** El notebook me quedó pesadísimo (más de 10 MB) porque guardó todos los gráficos renderizados adentro del archivo. Cuando quise hacer `git status` y diff andaba lentísimo.
- **Qué decidí:** Exportar los gráficos finales como imágenes livianas (`.png`) a la carpeta Documentos y limpiar las salidas de las celdas del Jupyter notebook antes de commitear en Git.

---

## Semana 6 — 15/09 al 19/09: Series de tiempo y calidad del aire
- **Qué intenté:** Empezar con el análisis de calidad del aire en Montevideo usando las mediciones minutales de Ozono ($O_3$) para sacar promedios y ver cómo variaba en el día.
- **Qué falló:** Cuando quise agrupar las fechas por hora con `pd.Grouper` me tiró error de tipo. Resulta que pandas me había cargado la columna de fecha como texto (`object`) en vez de `datetime`.
- **Qué decidí:** Agregar `parse_dates=["fecha"]` directamente al leer el CSV y verificar con `df.info()` que las fechas queden reconocidas antes de hacer cualquier filtro temporal.

---

## Semana 7 — 22/09 al 26/09: Unir tránsito vehicular con sensores de aire
- **Qué intenté:** Cruzar los datos de tránsito de los detectores Autoscope de Tres Cruces con las estaciones de aire para ver si a más autos subía el $NO_2$ o el $PM_{2.5}$.
- **Qué falló:** Quise hacer un `merge` directo y casi me explota la memoria de la compu. Los detectores miden minuto a minuto por carril y los datos de aire estaban a nivel horario, así que las marcas de tiempo no coincidían.
- **Qué decidí:** Agregar primero todo el tránsito a nivel de promedio horario y por estación, y recién ahí hacer el join con la tabla de aire para trabajar con una base limpia y manejable.

---

## Semana 8 — 29/09 al 03/10: Datos de panel y gráficos en R
- **Qué intenté:** Pasar parte del análisis a R usando tidyverse (`dplyr` y `ggplot2`) para replicar los gráficos que vimos en la clase 10 y calcular los percentiles 95.
- **Qué falló:** En R me daba error al filtrar por franjas horarias porque en Windows los nombres con tildes (`mañana`) se me rompían con caracteres raros al importar el script.
- **Qué decidí:** Escribir una función simple para limpiar nombres y caracteres especiales, y usar `facet_wrap` en ggplot2 para comparar las tres estaciones de monitoreo en un solo gráfico.

---

## Semana 9 — 06/10 al 10/10: Percentiles y sensores descalibrados
- **Qué intenté:** Graficar curvas de densidad y ver la distribución de contaminantes para comparar días hábiles contra fines de semana.
- **Qué falló:** Noté que en algunas horas los sensores marcaban valores negativos de $NO_2$. Si calculaba la media directo, esos números absurdos por descalibración me tiraban el promedio abajo.
- **Qué decidí:** Filtrar los valores negativos justificándolo en `decisiones.md`, y calcular también el percentil 95 ($P_{95}$) para no perder de vista los picos de contaminación que la media tiende a esconder.

---

## Semana 10 — 13/10 al 17/10: Rebotado por GitHub y el `.gitignore`
- **Qué intenté:** Subir los scripts actualizados de visualización y tener el repositorio al día para que el profe pudiera revisar los avances.
- **Qué falló:** Al hacer `git push` GitHub me rebotó el commit porque tenía los CSVs grandes de tránsito (de casi 300 y 330 MB) y el límite por archivo es de 100 MB.
- **Qué decidí:** Armar un `.gitignore` en serio para que ningún CSV pesado vuelva a entrar al repositorio, recordando lo que dijo la profe en clase: los datos crudos gigantes se descargan o procesan con scripts, pero no se suben a Git.

---

## Semana 11 — 20/10 al 24/10: Inferencia causal y Diferencias en Diferencias
- **Qué intenté:** Plantear un esquema de Diferencias en Diferencias (DiD) para ver si los cambios de tránsito en ciertas fechas cambiaban la contaminación en Tres Cruces respecto a otra zona de la ciudad.
- **Qué falló:** El supuesto de tendencias paralelas no se cumplía bien porque las estaciones están en lugares urbanos re distintos (una en zona céntrica encerrada y otra cerca de la costa con más viento).
- **Qué decidí:** Explicar honestamente esa limitación en las conclusiones del análisis: no se puede asegurar causalidad directa sin controlar por variables meteorológicas como viento y lluvia.

---

## Semana 12 — 27/10 al 31/10: Limpieza final y armado del portfolio
- **Qué intenté:** Hacer una pasada general por todo el repositorio para verificar que cualquier persona pueda clonarlo y correr los scripts sin que se le rompa nada.
- **Qué falló:** Me di cuenta de que si corría los scripts desde otra carpeta me saltaba `FileNotFoundError` porque había usado `Path.cwd() / "Repositorio-Personal/..."` hardcodeado.
- **Qué decidí:** Corregir las rutas en todos los archivos de Python usando `Path(__file__).resolve()`, armar un `requirements.txt` con las librerías necesarias y dejar la bitácora ordenada con las recetas y errores que me fueron pasando.

---

## Semana 13 — 03/11 al 07/11: Revisión por pares del proyecto "datos-espaciales"
- **Qué intenté:** Clonar y auditar el repositorio del equipo asignado (`datos-espaciales`) para evaluar su reproducibilidad y darles una devolución técnica y metodológica según la consigna de la clase.
- **Qué falló:** El repo tenía salidas pesadas versionadas (HTML de 38 MB y GeoPackage de 5 MB), carpetas desordenadas con duplicados y un `requirements.txt` vacío. En lo metodológico, el script definía la necesidad de transporte usando solo edades <14 y >80 (dependencia demográfica), omitiendo a estudiantes y trabajadores sin auto, que son los usuarios cautivos reales del ómnibus.
- **Qué decidí:** Armarles un feedback constructivo sugiriendo regenerar salidas por script usando `.gitignore`, ordenar la estructura de carpetas y corregir el supuesto conceptual del índice de transporte; y registrar la revisión en mi bitácora como aprendizaje de auditoría de código.

