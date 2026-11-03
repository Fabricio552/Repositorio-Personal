# Receta 02: Unir tablas por fecha y estación (Merge temporal y espacial)

## Cuándo usar esto
Cuando tenés dos tablas que miden cosas distintas pero querés cruzarlas en el tiempo y el espacio. En nuestro caso:
- Los detectores de tránsito de Autoscope miden por minuto y por carril.
- Las estaciones de calidad de aire de Montevideo miden concentraciones promedio por hora de $NO_2$ y $PM_{2.5}$.

Si intentás hacer un `merge` directo al minuto exacto, la máquina se cuelga por la cantidad de filas y casi nada coincide al segundo.

---

## Cómo lo resuelvo en Python (Pandas)

Hay que llevar las dos tablas a la misma unidad (promedio o suma por hora y por estación) antes de hacer el join:

```python
import pandas as pd

# 1. Asegurarme de que las columnas de fecha sean datetime
transito["fecha"] = pd.to_datetime(transito["fecha"])
aire["fecha"] = pd.to_datetime(aire["fecha"])

# 2. Agrupar el tránsito a nivel horario y por estación
transito_horario = (
    transito
    .groupby(["estacion", pd.Grouper(key="fecha", freq="h")])["volumen"]
    .sum()
    .reset_index()
)

# 3. Agrupar la calidad del aire a nivel horario por estación
aire_horario = (
    aire
    .groupby(["estacion", pd.Grouper(key="fecha", freq="h")])[["no2", "pm25"]]
    .mean()
    .reset_index()
)

# 4. Hacer el merge (Paso 4 del flujo de clase: Unir tablas)
df_combinado = pd.merge(
    transito_horario,
    aire_horario,
    on=["estacion", "fecha"],
    how="inner"
)

# 5. Reportar siempre cuántas filas quedaron de cada lado
print(f"Filas tránsito horario: {len(transito_horario)}")
print(f"Filas aire horario:     {len(aire_horario)}")
print(f"Filas resultantes join: {len(df_combinado)}")
```

---

## Lo que pide la cátedra
En el informe del trabajo siempre hay que decir cuántas filas quedaron sin coincidir de cada lado y por qué (sensores apagados, días sin mediciones, etc.), aunque el número sea cero.
