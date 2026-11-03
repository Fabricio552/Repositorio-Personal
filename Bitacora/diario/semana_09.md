# Bitácora Semana 9 — 06/10 al 10/10
**Tema:** Percentiles y sensores descalibrados  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Graficar curvas de densidad y ver la distribución de contaminantes para comparar días hábiles contra fines de semana.

## Qué falló
Noté que en algunas horas los sensores marcaban valores negativos de $NO_2$. Si calculaba la media directo, esos números absurdos por descalibración me tiraban el promedio abajo.

## Qué decidí
Filtrar los valores negativos justificándolo en `decisiones.md`, y calcular también el percentil 95 ($P_{95}$) para no perder de vista los picos de contaminación que la media tiende a esconder.
