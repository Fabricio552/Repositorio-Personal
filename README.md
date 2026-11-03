# Repositorio Personal — Introducción a la Ciencia de Datos

**Estudiante:** Fabricio De Souza  
**Facultad:** Ciencias Empresariales y Economía (FCEE) — Universidad de Montevideo  
**Docente:** Joselina Beatriz DAVYT COLO

---

## 👋 Sobre este repositorio

¡Buenas! Este es mi repositorio personal para la materia. Acá voy guardando:
- La **Bitácora personal** semanal, donde anoto qué intenté en cada clase, qué cosas se me rompieron en el camino y qué decisiones tomé para solucionarlo.
- El **Registro de decisiones** de limpieza y análisis de datos.
- Las **recetas y errores comunes** que me fueron pasando (problemas con encodings en Windows, rutas de archivos, librerías, etc.) para tenerlos a mano.
- Los **scripts de práctica** en Python y en R donde trabajamos con datos de empleo, encuestas y el caso de calidad del aire y tránsito vehicular en Montevideo (zona Tres Cruces y estaciones de monitoreo).

---

## 📁 Cómo está organizada la carpeta

Seguí la estructura que nos pidió la cátedra en el programa:

```text
Repositorio-Personal/
├── .gitignore                      # Para no subir datos pesados (>100 MB) ni archivos temporales
├── README.md                       # Esta guía del repositorio
├── requirements.txt                # Paquetes de Python necesarios para correr los scripts
│
└── Bitacora/                       # Carpeta principal de la bitácora
    ├── bitacora.md                 # Resumen semanal completo (Qué intenté, Qué falló, Qué decidí)
    ├── decisiones.md               # Tabla con el registro de decisiones y alternativas descartadas
    │
    ├── diario/                     # Las 12 entradas semanales separadas archivo por archivo
    │   ├── semana_01.md            # Entorno, Git, GitHub y pingüinos de Palmer
    │   ├── semana_02.md            # Muestreo, sesgos y encuestas
    │   ├── semana_03.md            # Carga de datos, codificación Latin-1 y estructura
    │   ├── semana_04.md            # Libros de códigos y detección de falsos nulos
    │   ├── semana_05.md            # Matrices de confusión, curva ROC y notebooks
    │   ├── semana_06.md            # Series temporales y calidad de aire minutal
    │   ├── semana_07.md            # Agregaciones horarias e integración de tránsito
    │   ├── semana_08.md            # Análisis de paneles en R (tidyverse / ggplot2)
    │   ├── semana_09.md            # Distribuciones, percentil 95 y valores inválidos
    │   ├── semana_10.md            # Gestión de datasets pesados y gitignore
    │   ├── semana_11.md            # Inferencia causal y diferencias en diferencias
    │   └── semana_12.md            # Auditoría, portabilidad y consolidación final
    │
    ├── funciones/                  # Pequeñas funciones auxiliares que armé con sus casos de prueba
    │   ├── raiz_proyecto.py        # Para que las rutas no fallen sin importar dónde estés parado
    │   ├── carga_robusta.py        # Para leer CSVs mañosos probando encodings y separadores
    │   └── resumen_faltantes.py    # Para ver rápido cuántos nulos y textos vacíos hay por columna
    │
    ├── recetas/                    # Guías cortas paso a paso de cosas que me sirvieron
    │   ├── 01_leer_csv_con_problemas_de_encoding_y_separador.md
    │   ├── 02_unir_tablas_por_fecha_y_estacion.md
    │   ├── 03_perfilado_rapido_de_datos.md
    │   └── 04_leer_planillas_excel_con_encabezados_complejos.md
    │
    ├── errores/                    # Registro de metidas de pata reales, cómo saltaron y cómo arreglarlas
    │   ├── 01_rutas_relativas_con_cwd.md
    │   ├── 02_limite_archivos_grandes_github.md
    │   ├── 03_mojibake_y_codificacion_caracteres.md
    │   └── 04_notebook_outputs_pesados.md
    │
    ├── Data/                       # Datasets de ejemplo livianos para probar los scripts
    │   ├── 12561_tasa_de_empleo_segun_nivel_educativo-_total_pais.csv
    │   ├── Trabajos_Objetos.xlsx
    │   ├── transito_aire_junio2024.csv
    │   └── Tabla simulada de respuestas.csv
    │
    ├── Documentos/                 # Gráficos exportados y ejercicios entregados
    │   ├── Curva ROC.png
    │   ├── Matriz de confusión.png
    │   ├── Grafico del paso 2_1.png
    │   ├── grafico del paso 1_1.png
    │   ├── Rplots.pdf
    │   └── Ejercicio de multiple opción.pdf
    │
    └── Scripts/                    # Los scripts de código de las clases
        ├── Analisis_del_csv.ipynb  # Notebook de análisis con las salidas limpias para Git
        ├── carga de datos en python 2.py
        ├── carga_y_transformacion.py
        ├── carga_transformacion_visualizacionV3.py
        ├── transito_aire.py
        ├── ejemplo_pinguinos.py
        ├── Ejercicio de clase de 08.09.2026.py
        ├── estadistica_basica.R
        ├── ejercicios_transito_aire.R
        └── instalar_paquetes.R
```

---

## ⚙️ Cómo correr el código en tu máquina

### En Python:
Usé Python 3.11. Para instalar las librerías que pide el curso:
```bash
# 1. Crear el entorno virtual (opcional pero recomendado)
python -m venv .venv

# 2. Activarlo (en Windows PowerShell):
.venv\Scripts\Activate.ps1

# 3. Instalar dependencias:
pip install -r requirements.txt
```

Para probar que las rutas y funciones anden bien:
```bash
python "Bitacora/funciones/raiz_proyecto.py"
python "Bitacora/funciones/carga_robusta.py"
python "Bitacora/funciones/resumen_faltantes.py"
```

Los scripts de Python los dejé preparados con rutas relativas dinámicas para que se puedan ejecutar parados en la raíz del repo o adentro de `Bitacora/Scripts/` sin que tiren error de archivo no encontrado.

### En R:
Para los scripts en R (`estadistica_basica.R`, `ejercicios_transito_aire.R`), armé un script que instala los paquetes necesarios (`dplyr`, `readr`, `lubridate`, `ggplot2`, `patchwork`):
```r
source("Bitacora/Scripts/instalar_paquetes.R")
```

---

## 📝 Notas sobre los datos y buenas prácticas de Git
- **Archivos grandes:** Los CSVs pesados de conteo vehicular de la Intendencia (`autoscope_04_2024_volumen.csv` y `autoscope_06_2024_volumen.csv`) pesan alrededor de 300 MB cada uno, así que los dejé afuera con `.gitignore` para no romper el límite de 100 MB de GitHub. El script que los procesa está acá, pero los datos crudos gigantes no se suben a Git.
- **Notebooks de Jupyter:** Limpié las salidas de las celdas del notebook antes de subirlo para que no pese 10 megas en binarios y el diff de Git sea legible.
- **Uso de IA:** Como está permitido en el curso siempre que se declare, usé asistencia de IA para consultar dudas de sintaxis, depurar errores de rutas y darle formato ordenado a la documentación, habiendo probado y verificado yo mismo cada script en mi computadora.
