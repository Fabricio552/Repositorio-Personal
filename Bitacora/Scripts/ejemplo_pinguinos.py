"""
EJEMPLO — Un conjunto de datos famoso: los pingüinos de Palmer
Diez filas reales del dataset "penguins" (Horst, Hill y Gorman, 2020),
escritas a mano para no depender de la red.
"""
# %%         
import pandas as pd
pinguinos = pd.DataFrame({
    "especie":          ["Adelia", "Adelia", "Adelia", "Adelia", "Barbijo",
                         "Barbijo", "Barbijo", "Juanito", "Juanito", "Juanito"],
    "isla":             ["Torgersen", "Torgersen", "Biscoe", "Dream", "Dream",
                         "Dream", "Dream", "Biscoe", "Biscoe", "Biscoe"],
    "largo_pico_mm":    [39.1, 39.5, 37.8, 39.5, 46.5, 50.0, 51.3, 46.1, 50.0, 48.7],
    "alto_pico_mm":     [18.7, 17.4, 18.3, 16.7, 17.9, 19.5, 19.2, 13.2, 16.3, 14.1],
    "largo_aleta_mm":   [181, 186, 174, 178, 192, 196, 193, 211, 230, 210],
    "masa_corporal_g":  [3750, 3800, 3400, 3250, 3500, 3900, 3650, 4500, 5700, 4450],
})

print(pinguinos.to_string(index=False))

print("-" *50)
# Ver las primeras filas
print(pinguinos.head())

print("-" *50)
# Ver las últimas filas
print(pinguinos.tail())

print("-" *50)
# Información general del DataFrame
print(pinguinos.info())

print("-" *50)
# Estadísticas descriptivas
print(pinguinos.describe())

print("-" *50)
# Ver columnas
print(pinguinos.columns)

print("-" *50)
print("masa corporal mayor a 3990")
# Filtrar filas por condición
filtro = pinguinos[pinguinos["masa_corporal_g"] > 3990]
print(filtro)

print("-" *50)
# Seleccionar columnas específicas
print(pinguinos[["alto_pico_mm", "largo_pico_mm"]])

print("-" *50)
# Contar valores únicos
print(pinguinos["isla"].value_counts())

print("-" *50)
# Eliminar valores nulos
pinguinos = pinguinos.dropna()

print("-" *50)
# Rellenar valores nulos
pinguinos["largo_pico_mm"] = pinguinos["largo_pico_mm"].fillna(pinguinos["largo_pico_mm"].mean())

# %%
