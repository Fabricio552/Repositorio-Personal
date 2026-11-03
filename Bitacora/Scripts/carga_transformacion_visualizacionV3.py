# =============================================================================
# Carga y transformaciÃ³n
# Ejemplo: medioambiente y aire (ozono, PM2.5, conteo vehicular) â Montevideo
# VersiÃ³n Python (pandas + matplotlib) â equivalente de carga_y_transformacion.R
# =============================================================================
# InstalaciÃ³n (una sola vez):  pip install pandas numpy matplotlib
# Para el mapa ademÃ¡s:         pip install geopandas folium
# =============================================================================
#%%
from pathlib import Path

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

archivo = "o3_01_2024_04_2024.csv"
try:
    BASE_DIR = Path(__file__).resolve().parents[2]
except NameError:
    BASE_DIR = Path.cwd().resolve()

candidatos_data = [
    BASE_DIR / "Bitacora" / "Data",
    BASE_DIR / "Repositorio-Personal" / "Bitacora" / "Data",
    Path.cwd() / "Bitacora" / "Data",
    Path.cwd() / "Data",
]
SUBCARPETA = next((p for p in candidatos_data if p.exists()), BASE_DIR / "Bitacora" / "Data")
RUTA = SUBCARPETA / archivo

# =============================================================================
# 1. Carga de datos: ejemplo medioambiente y aire
# =============================================================================
# read_csv de R detecta fechas automÃ¡ticamente; pandas necesita parse_dates.

## Ozono â datos minutales de concentraciÃ³n de O3 en aire ambiente
ozono = pd.read_csv(SUBCARPETA / "o3_01_2024_04_2024.csv",
                    encoding="latin1", parse_dates=["fecha"])

#InspecciÃ³n inicial de los datos
print(ozono.info())
print("\nPrimeras 5 filas:")
print(ozono.head())                   

## Material particulado menor de 2,5 micras, estaciones automÃ¡ticas
pm = pd.read_csv(SUBCARPETA / "pm_2_5_01_2024_04_2024.csv",
                 encoding="latin1", parse_dates=["fecha"])

## Conteo vehicular en las principales avenidas de Montevideo
# El sistema del Centro de GestiÃ³n de Movilidad (CGM) usa analÃ­ticas de video
# para medir volÃºmenes vehiculares. Los detectores miden el total de vehÃ­culos
# y su clasificaciÃ³n por largo, por sentido de circulaciÃ³n, y pueden
# discriminarse por carril dentro de cada sentido.
auto = pd.read_csv(SUBCARPETA / "autoscope_04_2024_volumen.csv",
                   encoding="latin1", parse_dates=["fecha"])


# =============================================================================
# 2. Data profiling: id, nulos y duplicados
# =============================================================================

## 2.1 InformaciÃ³n bÃ¡sica del dataset  (equivale a str())
ozono.info()
print(ozono.head())

## 2.2 Identificador
# Los datos se toman por estaciÃ³n (que tiene una ubicaciÃ³n geogrÃ¡fica, es decir,
# es una caracterÃ­stica de la estaciÃ³n) y por fecha.
# El identificador podrÃ­a ser la fecha: sirve para unir con otros datos.
# TambiÃ©n podrÃ­a ser la combinaciÃ³n de fecha y estaciÃ³n.

# 1- Tenemos problemas con los valores de las estaciones
print(ozono.iloc[0:10, 2])          # filas 1-10, tercera columna (Ã­ndice 2)

print(ozono["estacion"].unique())

# Creamos el diccionario de traducciÃ³n (Busca -> Reemplaza)
pauta_limpieza = {
    "ÃÂ³": "o",
    "ÃÂ±": "ni",
    "ÃÂ¡": "Ã¡",
    "ÃÂ©": "Ã©",
    "ÃÂ­": "Ã­",
    "ÃÂº": "Ãº",
    "Ãâ": "Ã",
    "Ãâ": "NI",
    "Ã":  "Ã­",   # a veces la 'Ã­' sola se rompe asÃ­; dejarla al final del dict
}

# Aplicamos la limpieza a la columna. El dict conserva el orden de inserciÃ³n,
# asÃ­ que las reglas se aplican en el mismo orden que el vector de R.
ozono_limpio = ozono.copy()
for buscar, reemplazar in pauta_limpieza.items():
    ozono_limpio["estacion"] = ozono_limpio["estacion"].str.replace(
        buscar, reemplazar, regex=False)

## 2.3 Valores faltantes  (equivale a colSums(is.na()))
print(ozono.isna().sum())

# La Ãºnica variable con valores faltantes es la mediciÃ³n, por lo tanto se pueden
# eliminar, ya que no eliminamos identificador (podrÃ­a discutirse si hay que
# eliminar fechas sin registro).

# Quito los NaN de todo el dataset:
ozono_sinna = ozono_limpio.dropna()

# Quito los NaN de columnas especÃ­ficas:
ozono_sinna = ozono_limpio.dropna(subset=["o3"]).copy()

## 2.4 Duplicados
# NÃºmero total de filas repetidas en todo el dataset
print(ozono_sinna.duplicated().sum())

# Mostrar TODAS las filas involucradas en un duplicado (la primera y sus copias)
ozono_repetidas = ozono_sinna[ozono_sinna.duplicated(keep=False)]

## 2.5 Eliminar duplicados
# Conserva solo la primera apariciÃ³n de cada fila Ãºnica
dataset_sindup = ozono_sinna.drop_duplicates()

# Duplicados segÃºn una sola columna, conservando el resto del primer registro
dataset_sindup_columna = ozono_sinna.drop_duplicates(subset=["estacion"])

# otra manera de cargar los datos
def cargar(archivo):
    datos = pd.read_csv(SUBCARPETA / archivo, encoding="latin1", parse_dates=["fecha"])
    for buscar, reemplazar in pauta_limpieza.items():
        datos["estacion"] = datos["estacion"].str.replace(buscar, reemplazar, regex=False)
    return datos.drop_duplicates()

ozono_limpio = cargar("o3_01_2024_04_2024.csv")
pm_limpio = cargar("pm_2_5_01_2024_04_2024.csv")

# =============================================================================
# 3. Tipos de datos y transformaciÃ³n de datos
# =============================================================================

## 3.1 Fechas
# El equivalente de POSIXct en pandas es datetime64[ns]: internamente un entero
# de 64 bits (nanosegundos desde el 1 de enero de 1970), lo que hace muy rÃ¡pidas
# las operaciones aritmÃ©ticas entre fechas.
print(ozono["fecha"].dtype)

# Si la columna no se hubiera parseado al leer:
# ozono["fecha"] = pd.to_datetime(ozono["fecha"])

## 3.2 Crear variables  (el accesor .dt cumple el rol de lubridate)
ozono_new = ozono_sinna.assign(
    anio=lambda d: d["fecha"].dt.year,
    mes=lambda d: d["fecha"].dt.month,
    hora=lambda d: d["fecha"].dt.hour,
)


# =============================================================================
# 4. GeneraciÃ³n de informaciÃ³n
# =============================================================================

## 4.1 AgregaciÃ³n mensual
ozono_mes = (
    ozono_new.groupby("mes")
    .agg(o3_medio_mes=("o3", "mean"), n_registros_mes=("o3", "size"))
    .reset_index()
)
print(ozono_mes)

## 4.2 VisualizaciÃ³n
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(ozono_mes["mes"], ozono_mes["o3_medio_mes"],
        color="blue", linewidth=2)                        # lÃ­nea
ax.scatter(ozono_mes["mes"], ozono_mes["o3_medio_mes"],
           color="red", s=60, zorder=3)                   # puntos
ax.set(title="ConcentraciÃ³n de Ozono en el ambiente, por mes, 2024",
       xlabel="Fecha", ylabel="Valores")
ax.grid(alpha=0.3)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
plt.tight_layout()
fig.savefig("ozono_2024.png", dpi=300, bbox_inches="tight")
plt.show()

# Partes bÃ¡sicas de un grÃ¡fico:
#   - dataset
#   - variable eje x
#   - variable eje y
#   - tipo de grÃ¡fico
#   - tÃ­tulos: del grÃ¡fico y nombres de los ejes

def grafico_ozono(datos, color_puntos="red", color_linea="blue", ylim=(0, 40)):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(datos["mes"], datos["o3_medio_mes"], color=color_linea, linewidth=2)
    ax.scatter(datos["mes"], datos["o3_medio_mes"], color=color_puntos, s=60, zorder=3)
    ax.set_xticks(datos["mes"])
    ax.set_xticklabels(["Ene", "Feb", "Mar", "Abr"])
    ax.set(title="Ozono troposfÃ©rico: media mensual, enero a abril de 2024",
           xlabel="Mes (2024)", ylabel="Ozono (Âµg/mÂ³)")
    ax.set_ylim(*ylim)
    ax.grid(alpha=0.3)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    fig.tight_layout()
    return fig, ax

plt.close("all")

fig, ax = grafico_ozono(ozono_mes, color_puntos="green")
fig.savefig("ozono_verde.png", dpi=300, bbox_inches="tight")
plt.show()
# =============================================================================
# 5. AnÃ¡lisis profundo: agregaciÃ³n temporal minutal -> horario -> diario
# =============================================================================
# Pregunta central: al agregar, Â¿quÃ© estadÃ­stico representa el fenÃ³meno?
#   - media: nivel tÃ­pico
#   - mÃ¡ximo: episodios puntuales (sensible a errores del sensor)
#   - percentil 95: episodios altos pero robusto a picos aislados
#   - n: cuÃ¡ntos minutos respaldan el valor agregado (cobertura)


def p95(x):
    return x.quantile(0.95)


## 5.1 Horario
# pd.Grouper(freq=...) cumple el rol de floor_date() + group_by()
ozono_hora = (
    ozono_sinna
    .groupby(["estacion", pd.Grouper(key="fecha", freq="h")])["o3"]
    .agg(media="mean", maximo="max", p95=p95, n_min="size")   # n_min: mÃ¡x 60
    .reset_index()
    .rename(columns={"fecha": "fecha_hora"})
)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ozono_hora["fecha_hora"], ozono_hora["media"], color="blue", linewidth=1)
ax.scatter(ozono_hora["fecha_hora"], ozono_hora["media"], color="red", s=4, zorder=3)
ax.set(title="ConcentraciÃ³n de Ozono en el ambiente, por hora, 2024",
       xlabel="Fecha", ylabel="Valores")
ax.grid(alpha=0.3)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
plt.tight_layout()
plt.show()

# =============================================================================
# 6. Diario
# =============================================================================
ozono_dia = (
    ozono_sinna
    .groupby(["estacion", pd.Grouper(key="fecha", freq="D")])["o3"]
    .agg(media="mean", maximo="max", p95=p95, n_min="size")   # n_min: mÃ¡x 1440
    .reset_index()
    .rename(columns={"fecha": "dia"})
)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ozono_dia["dia"], ozono_dia["media"], color="blue", linewidth=1)
ax.scatter(ozono_dia["dia"], ozono_dia["media"], color="red", s=4, zorder=3)
ax.set(title="ConcentraciÃ³n de Ozono en el ambiente, por hora, 2024",
       xlabel="Fecha", ylabel="Valores")
ax.grid(alpha=0.3)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
plt.tight_layout()
plt.show()

# Las tres curvas cuentan historias distintas sobre el mismo dÃ­a
estaciones = ozono_dia["estacion"].unique()
fig, axes = plt.subplots(len(estaciones), 1, figsize=(9, 3 * len(estaciones)),
                         sharex=True, squeeze=False)
for ax, est in zip(axes[:, 0], estaciones):
    d = ozono_dia[ozono_dia["estacion"] == est]
    for col in ("media", "p95", "maximo"):
        ax.plot(d["dia"], d[col], label=col)
    ax.set_title(est)
    ax.set_ylabel("O3 (Âµg/mÂ³)")
    ax.grid(alpha=0.3)
axes[0, 0].legend()
fig.suptitle("AgregaciÃ³n diaria: media, p95 y mÃ¡ximo por estaciÃ³n")
plt.tight_layout()
plt.show()


# =============================================================================
# 7. Avanzado: mÃ¡ximo diario de la media mÃ³vil de 8 horas
# =============================================================================
# Las guÃ­as OMS (2021) para O3 usan el mÃ¡ximo diario de la media mÃ³vil de 8 h.
# Una media mÃ³vil requiere una grilla horaria COMPLETA: si faltan horas, la
# ventana de 8 posiciones deja de ser una ventana de 8 horas.

grilla_horaria = pd.date_range(ozono_hora["fecha_hora"].min(),
                               ozono_hora["fecha_hora"].max(), freq="h")

# reindex sobre la grilla completa por estaciÃ³n = tidyr::complete()
ozono_8h = (
    ozono_hora
    .set_index("fecha_hora")
    .groupby("estacion")["media"]
    .apply(lambda s: s.reindex(grilla_horaria))     # inserta NaN en horas ausentes
    .rename_axis(["estacion", "fecha_hora"])
    .reset_index()
)
# rolling(8, min_periods=8): si falta alguna de las 8 horas, el resultado es NaN,
# igual que stats::filter con NA en la ventana.
ozono_8h["media_8h"] = (
    ozono_8h.groupby("estacion")["media"]
    .transform(lambda s: s.rolling(8, min_periods=8).mean())
)

max_8h_dia = (
    ozono_8h
    .assign(dia=lambda d: d["fecha_hora"].dt.floor("D"))
    .groupby(["estacion", "dia"])["media_8h"]
    .agg(max_8h="max", horas_validas="count")   # max ignora NaN; count no los cuenta
    .reset_index()
)

fig, ax = plt.subplots(figsize=(9, 5))
for est, d in max_8h_dia.groupby("estacion"):
    ax.plot(d["dia"], d["max_8h"], label=est)
ax.axhline(100, linestyle="--", color="black")   # guÃ­a OMS 2021: 100 Âµg/mÂ³
ax.set(title="MÃ¡ximo diario de la media mÃ³vil de 8 h", ylabel="O3 (Âµg/mÂ³)")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# 8. Patrones de faltantes
# =============================================================================
# Tres tipos de faltante en una serie de sensor:
#   a) explÃ­cito: la fila existe, o3 es NaN
#   b) en rachas: muchos NaN consecutivos -> sensor caÃ­do o en mantenimiento
#   c) implÃ­cito: la fila no existe (el minuto no estÃ¡ en el archivo)
# Eliminar NaN sin mirar esto borra evidencia sobre el proceso de mediciÃ³n.

## 8.1 Faltantes explÃ­citos por estaciÃ³n
resumen_na = (
    ozono_limpio.groupby("estacion")["o3"]
    .agg(n_filas="size",
         n_na=lambda s: s.isna().sum(),
         prop_na=lambda s: s.isna().mean())
    .reset_index()
)
print(resumen_na)

## 8.2 Â¿CuÃ¡ndo faltan? ProporciÃ³n de NaN por dÃ­a
na_dia = (
    ozono_limpio
    .assign(es_na=lambda d: d["o3"].isna())
    .groupby(["estacion", pd.Grouper(key="fecha", freq="D")])["es_na"]
    .mean()
    .rename("prop_na").reset_index()
    .rename(columns={"fecha": "dia"})
)

estaciones = na_dia["estacion"].unique()
fig, axes = plt.subplots(len(estaciones), 1, figsize=(9, 2.5 * len(estaciones)),
                         sharex=True, squeeze=False)
for ax, est in zip(axes[:, 0], estaciones):
    d = na_dia[na_dia["estacion"] == est]
    ax.bar(d["dia"], d["prop_na"], color="grey", width=1)
    ax.set_title(est)
    ax.set_ylabel("ProporciÃ³n de NaN")
fig.suptitle("ProporciÃ³n de minutos sin dato, por dÃ­a y estaciÃ³n")
plt.tight_layout()
plt.show()


## 8.3 Rachas de NaN consecutivos (equivalente de rle())
def rachas_na(s: pd.Series) -> pd.DataFrame:
    es_na = s.isna().to_numpy()
    # cada cambio de valor abre una racha nueva
    id_racha = np.concatenate([[0], np.cumsum(es_na[1:] != es_na[:-1])])
    return (pd.DataFrame({"faltante": es_na, "id_racha": id_racha})
            .groupby("id_racha")
            .agg(faltante=("faltante", "first"), largo=("faltante", "size"))
            .reset_index(drop=True))


rachas = (
    ozono_limpio.sort_values(["estacion", "fecha"])
    .groupby("estacion")["o3"]
    .apply(rachas_na)
    .reset_index(level=0)
    .reset_index(drop=True)
)

tabla_rachas = (
    rachas[rachas["faltante"]]
    .assign(tipo=lambda d: pd.cut(
        d["largo"], bins=[0, 1, 10, 60, 1440, np.inf],
        labels=["1 min", "2-10 min", "11 min-1 h", "1 h-1 dÃ­a", "> 1 dÃ­a"]))
    .groupby(["estacion", "tipo"], observed=True).size()
    .rename("n_rachas").reset_index()
)
print(tabla_rachas)

## 8.4 Faltantes implÃ­citos: minutos que no estÃ¡n en el archivo
implicitos = (
    ozono_limpio.groupby("estacion")["fecha"]
    .agg(primero="min", ultimo="max", presentes="nunique")
    .assign(
        esperados=lambda d: ((d["ultimo"] - d["primero"])
                             / pd.Timedelta(minutes=1)).astype(int) + 1,
        implicitos=lambda d: d["esperados"] - d["presentes"],
        prop_implicitos=lambda d: d["implicitos"] / d["esperados"],
    )
    .reset_index()
)
print(implicitos)

## 10.5 Cobertura contra la grilla del perÃ­odo pedido
INICIO = pd.Timestamp("2024-01-01 00:00:00")
FIN    = pd.Timestamp("2024-04-30 23:59:00")
ESPERADOS = int((FIN - INICIO) / pd.Timedelta(minutes=1)) + 1

cobertura = (
    ozono_limpio.groupby("estacion")
    .agg(presentes=("fecha", "nunique"),
         validos=("o3", "count"))          # count no cuenta los NaN
    .assign(
        esperados=ESPERADOS,
        sin_fila=lambda d: d["esperados"] - d["presentes"],
        fila_sin_medicion=lambda d: d["presentes"] - d["validos"],
        cobertura=lambda d: 100 * (d["validos"] / d["esperados"]).round(3),
    )
    .reset_index()
)
print(cobertura)

#######
#6 Guardar dataset limpio
#####
ozono_limpio.to_csv(SUBCARPETA / "ozono_2024_limpio.csv", index=False, encoding="latin1")

########################################
#7 UNIR datasets: ozono + pm + autoscope
########################################

# 7.1 El archivo de PM limpio
print(pm.info())
print("\nPrimeras 5 filas:")
print(pm.head())

pm_limpio = pm.drop_duplicates().copy()   # el archivo trae 3 filas repetidas
for buscar, reemplazar in pauta_limpieza.items():
    pm_limpio["estacion"] = pm_limpio["estacion"].str.replace(
        buscar, reemplazar, regex=False)

print(pm_limpio.head())

# 7.2 Unir datasets: ozono + pm
aire = pd.merge(ozono_limpio, pm_limpio, on=["fecha", "estacion"], how="inner")

print(aire.info())
print("\nPrimeras 5 filas:")
print(aire.head()) #Â¿son los datos que queremos?

# 7.3 
# Resumir cada tabla a una fila por hora y estaciÃ³n,
#    despuÃ©s unir. La agregaciÃ³n no es un capricho, es lo que hace que la
#    clave sea Ãºnica de cada lado.
o3_h = ozono_limpio.groupby(["estacion", ozono_limpio["fecha"].dt.floor("h")])["o3"].mean().reset_index()
pm_h = pm_limpio.groupby(["estacion", pm_limpio["fecha"].dt.floor("h")])["pm2_5"].mean().reset_index()
aire = pd.merge(o3_h, pm_h, on=["estacion", "fecha"], how="inner", validate="one_to_one")
print(len(o3_h), len(pm_h), len(aire))

print(aire.info())
print("\nPrimeras 5 filas:")
print(aire.head()) #Â¿son los datos que queremos?

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

for est, d in aire.groupby("estacion"):
    ax1.plot(d["fecha"], d["o3"], label=est, linewidth=0.6)
    ax2.plot(d["fecha"], d["pm2_5"], label=est, linewidth=0.6)

ax1.set(title="Ozono y PM2.5 por hora, enero a abril de 2024", ylabel="O3 (Âµg/mÂ³)")
ax2.set(xlabel="Fecha", ylabel="PM2.5 (Âµg/mÂ³)")
ax1.legend(title="EstaciÃ³n")
for ax in (ax1, ax2):
    ax.grid(alpha=0.3)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
fig.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(7, 6))
for est, d in aire.groupby("estacion"):
    r = d["o3"].corr(d["pm2_5"])
    ax.scatter(d["pm2_5"], d["o3"], s=6, alpha=0.3, label=f"{est} (r = {r:.2f})")
ax.set(title="Ozono vs PM2.5, medias horarias", xlabel="PM2.5 (Âµg/mÂ³)", ylabel="O3 (Âµg/mÂ³)")
ax.legend(title="EstaciÃ³n")
ax.grid(alpha=0.3)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
fig.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(7, 6))
r = aire["o3"].corr(aire["pm2_5"])
ax.scatter(aire["pm2_5"], aire["o3"], s=6, alpha=0.3)
ax.set(title=f"Ozono vs PM2.5, medias horarias, {aire['estacion'].iloc[0]} (r = {r:.2f})",
       xlabel="PM2.5 (Âµg/mÂ³)", ylabel="O3 (Âµg/mÂ³)")
ax.grid(alpha=0.3)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
fig.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(8, 6))
sc = ax.scatter(aire["pm2_5"], aire["o3"], c=aire["fecha"].dt.hour,
                cmap="twilight", s=6, alpha=0.5)
fig.colorbar(sc, ax=ax, label="Hora del dÃ­a")
ax.set(title="Ozono vs PM2.5, medias horarias, Curva de MaroÃ±as",
       xlabel="PM2.5 (Âµg/mÂ³)", ylabel="O3 (Âµg/mÂ³)")
ax.set_xscale("log")
ax.grid(alpha=0.3)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
fig.tight_layout()
plt.show()

franjas = pd.cut(aire["fecha"].dt.hour, bins=[-1, 5, 11, 17, 23],
                 labels=["madrugada (0â5)", "maÃ±ana (6â11)", "tarde (12â17)", "noche (18â23)"])

fig, ax = plt.subplots(figsize=(8, 6))
for franja, d in aire.groupby(franjas, observed=True):
    ax.scatter(d["pm2_5"], d["o3"], s=8, alpha=0.5, label=franja)
ax.set(title="Ozono vs PM2.5, medias horarias, Curva de MaroÃ±as",
       xlabel="PM2.5 (Âµg/mÂ³)", ylabel="O3 (Âµg/mÂ³)")
ax.set_xscale("log")
ax.set_xticks([3, 5, 10, 20, 30, 50])
ax.set_xticklabels(["3", "5", "10", "20", "30", "50"])
ax.minorticks_off()
ax.legend(title="Franja horaria")
ax.grid(alpha=0.3)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
fig.tight_layout()
plt.show()

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)

for ax, (franja, d) in zip(axes.flat, aire.groupby(franjas, observed=True)):
    r = d["o3"].corr(d["pm2_5"])
    ax.scatter(d["pm2_5"], d["o3"], s=8, alpha=0.4)
    ax.set_title(f"{franja}   r = {r:.2f}   n = {len(d)}")
    ax.set_xscale("log")
    ax.set_xticks([3, 5, 10, 20, 30, 50])
    ax.set_xticklabels(["3", "5", "10", "20", "30", "50"])
    ax.minorticks_off()
    ax.grid(alpha=0.3)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)

for ax in axes[1, :]:
    ax.set_xlabel("PM2.5 (Âµg/mÂ³)")
for ax in axes[:, 0]:
    ax.set_ylabel("O3 (Âµg/mÂ³)")
fig.suptitle("Ozono vs PM2.5 dentro de cada franja horaria, Curva de MaroÃ±as")
fig.tight_layout()
plt.show()

# Buscando correlaciones

aire["hora"] = aire["fecha"].dt.hour
aire["o3_res"]  = aire["o3"]    - aire.groupby("hora")["o3"].transform("mean")
aire["pm_res"]  = aire["pm2_5"] - aire.groupby("hora")["pm2_5"].transform("mean")
print(aire["o3_res"].corr(aire["pm_res"]))

tabla = (aire.groupby(franjas, observed=True)
             .apply(lambda d: pd.Series({
                 "r_crudo":    d["o3"].corr(d["pm2_5"]),
                 "r_residuos": d["o3_res"].corr(d["pm_res"]),
                 "n": len(d)}), include_groups=False)
             .round(2))
print(tabla)

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)

for ax, (franja, d) in zip(axes.flat, aire.groupby(franjas, observed=True)):
    r = d["o3_res"].corr(d["pm_res"])
    ax.scatter(d["pm_res"], d["o3_res"], s=8, alpha=0.4)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.axvline(0, color="grey", linewidth=0.8)
    ax.set_title(f"{franja}   r = {r:.2f}   n = {len(d)}")
    ax.grid(alpha=0.3)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)

for ax in axes[1, :]:
    ax.set_xlabel("PM2.5, apartamiento de la media de su hora (Âµg/mÂ³)")
for ax in axes[:, 0]:
    ax.set_ylabel("O3, apartamiento de la media de su hora (Âµg/mÂ³)")
fig.suptitle("Residuos por franja horaria, Curva de MaroÃ±as")
fig.tight_layout()
plt.show()

# =============================================================================
# 9. Serie temporal: grilla al minuto, autocorrelaciÃ³n y correlaciÃ³n cruzada
# =============================================================================
# Una serie de tiempo es una columna cuyo Ã­ndice es el tiempo, a paso fijo.
# Lo nuevo: reindex a una grilla completa (como grilla_horaria en la secciÃ³n 7),
# shift (la serie corrida k pasos) y autocorrelaciÃ³n (la serie correlacionada
# consigo misma a distintos rezagos).
import matplotlib.dates as mdates

ESTACION = "Curva de Maronias"
o3_s = ozono_limpio[ozono_limpio["estacion"] == ESTACION].set_index("fecha")["o3"].sort_index()
pm_s = pm_limpio[pm_limpio["estacion"] == ESTACION].set_index("fecha")["pm2_5"].sort_index()

## 9.1 Sellos repetidos: reindex exige Ã­ndice Ãºnico (resample los promediarÃ­a)
for nombre, s in [("O3", o3_s), ("PM2.5", pm_s)]:
    dup = s.index.duplicated(keep=False)
    print(nombre, "sellos repetidos:", dup.sum())
# PM2.5 traÃ­a 3 pares de filas idÃ©nticas; drop_duplicates en la carga los saca.

## 9.2 Grilla completa al minuto
grilla = pd.date_range(INICIO, FIN, freq="min")
serie = pd.DataFrame({"o3": o3_s.reindex(grilla), "pm25": pm_s.reindex(grilla)})
serie.index.name = "fecha"
print("Filas:", len(serie), "(121 dÃ­as Ã 1440 min)")
print(serie.isna().sum())
print(serie.describe().round(1))

## 9.3 Huecos: rachas de NaN con fecha de inicio y fin
falta = serie["o3"].isna()
bloque = (falta != falta.shift()).cumsum()
huecos = (serie[falta].groupby(bloque[falta])
          .apply(lambda g: pd.Series({"desde": g.index[0], "hasta": g.index[-1],
                                      "horas": len(g) / 60}))
          .reset_index(drop=True))
print(huecos.sort_values("horas", ascending=False).head(10))
# Un corte de 14 dÃ­as (20/3 al 2/4) y cortes de horas en abril. corr() descarta
# los pares con NaN, asÃ­ que los huecos no rompen lo que sigue.

## 9.4 Las dos series en el tiempo
# Para graficar y correlacionar usamos promedios de 10 min: el dato al minuto es
# entero y parpadea entre dos niveles vecinos (resoluciÃ³n del sensor, no aire).
suave = serie.resample("10min").mean()
POR_HORA = 6
semana = suave["2024-03-04":"2024-03-10"]
print("Cajas sin dato en la semana:")
print(semana.isna().sum())            # hay un corte corto el 5â6 de marzo

fig, axes = plt.subplots(2, 2, figsize=(13, 7))
for fila, (col, nombre) in enumerate([("o3", "O3"), ("pm25", "PM2.5")]):
    axes[fila, 0].plot(suave.index, suave[col], linewidth=0.4)
    axes[fila, 1].plot(semana.index, semana[col], linewidth=0.8)
    axes[fila, 0].set_ylabel(f"{nombre} (Âµg/mÂ³)")
axes[0, 0].set_title("Enero a abril, promedios de 10 min")
axes[0, 1].set_title("Una semana (4 a 10 de marzo)")
axes[1, 0].set_ylim(0, 250)           # queda fuera un valor de 600 a mediados de enero
for ax in axes[:, 0]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
for ax in axes[:, 1]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %d"))
for ax in axes.flat:
    ax.grid(alpha=0.3)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
fig.suptitle(f"Ozono y PM2.5, {ESTACION}")
fig.tight_layout()
plt.show()
# Se ve: el corte de marzo, el ciclo diario del O3 en la semana, y PM2.5 como
# base plana con picos de minutos (fuente local intermitente, sin ciclo diario).

## 9.5 GrÃ¡fico de rezago: shift(k) deja en cada fila el valor de hace k pasos
rezagos_horas = [1/6, 1, 12, 24]      # 10 min, 1 h, 12 h, 24 h
fig, axes = plt.subplots(1, 4, figsize=(14, 3.8), sharey=True)
for ax, h in zip(axes, rezagos_horas):
    k = int(h * POR_HORA)
    r = semana["o3"].corr(semana["o3"].shift(k))
    ax.scatter(semana["o3"].shift(k), semana["o3"], s=4, alpha=0.4)
    ax.set_title(f"rezago {h:g} h   r = {r:.2f}")
    ax.set_xlabel(f"O3 hace {h:g} h")
    ax.grid(alpha=0.3)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
axes[0].set_ylabel("O3 ahora")
fig.suptitle("Ozono contra sÃ­ mismo a distintos rezagos, una semana")
fig.tight_layout()
plt.show()

## 9.6 Autocorrelograma: el r de arriba para cada rezago, hasta 48 h
rezagos = range(0, 48 * POR_HORA + 1)
horas = [k / POR_HORA for k in rezagos]
acf_o3 = [suave["o3"].corr(suave["o3"].shift(k)) for k in rezagos]
acf_pm = [suave["pm25"].corr(suave["pm25"].shift(k)) for k in rezagos]

fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
for ax, acf, nombre in [(axes[0], acf_o3, "O3"), (axes[1], acf_pm, "PM2.5")]:
    ax.vlines(horas, 0, acf, linewidth=1.5)
    ax.plot(horas, acf, "o", markersize=2.5)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set_ylabel("AutocorrelaciÃ³n")
    ax.set_title(nombre)
    ax.grid(alpha=0.3)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
axes[1].set(xlabel="Rezago (horas)", xticks=range(0, 49, 6))
fig.suptitle("Autocorrelograma, enero a abril")
fig.tight_layout()
plt.show()

# Lectura: arranca en 1 (rezago 0). Lo esperable para ozono era un mÃ­nimo a
# 12 h y un mÃ¡ximo a 24 h (ciclo diario). Aparece otra cosa: picos regulares
# cada ~2.4 h, iguales en las dos series. Dos contaminantes con procesos
# distintos no comparten un perÃ­odo asÃ­: es del instrumento, no de la
# atmÃ³sfera. Afinamos el perÃ­odo sobre la serie al minuto:
fino = pd.Series({k: serie["o3"].corr(serie["o3"].shift(k)) for k in range(120, 170)})
print("Primer pico de autocorrelaciÃ³n en", fino.idxmax(), "min")
# 143 min no divide a 1440: el ciclo no va con el reloj, cada dÃ­a arranca en
# otra fase. Queda como pregunta abierta: quÃ© hace el equipo cada 143 minutos.

## 9.7 CorrelaciÃ³n cruzada: PM2.5 de hace k pasos contra O3 de ahora
rezagos_c = range(-24 * POR_HORA, 24 * POR_HORA + 1)
horas_c = [k / POR_HORA for k in rezagos_c]
ccf = [suave["o3"].corr(suave["pm25"].shift(k)) for k in rezagos_c]

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(horas_c, ccf)
ax.axhline(0, color="grey", linewidth=0.8)
ax.axvline(0, color="grey", linewidth=0.8, linestyle="--")
ax.set(title="CorrelaciÃ³n entre O3 y PM2.5 segÃºn el rezago",
       xlabel="Rezago de PM2.5 respecto de O3 (horas; > 0 es PM del pasado)",
       ylabel="CorrelaciÃ³n", xticks=range(-24, 25, 6))
ax.grid(alpha=0.3)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)
fig.tight_layout()
plt.show()
# En rezago 0 es el r de la secciÃ³n anterior. La onda de ~2.4 h reaparece: es
# el mismo ciclo del instrumento, y hay que descontarlo antes de leer cualquier
# relaciÃ³n entre los dos contaminantes.

