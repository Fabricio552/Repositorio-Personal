# Bitácora Semana 8 — 29/09 al 03/10
**Tema:** Datos de panel y gráficos en R  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Pasar parte del análisis a R usando tidyverse (`dplyr` y `ggplot2`) para replicar los gráficos que vimos en la clase 10 y calcular los percentiles 95.

## Qué falló
En R me daba error al filtrar por franjas horarias porque en Windows los nombres con tildes (`mañana`) se me rompían con caracteres raros al importar el script.

## Qué decidí
Escribir una función simple para limpiar nombres y caracteres especiales, y usar `facet_wrap` en ggplot2 para comparar las tres estaciones de monitoreo en un solo gráfico.
