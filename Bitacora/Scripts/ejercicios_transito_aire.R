# =============================================================================
# Tránsito y calidad del aire, junio de 2024 — Ejercicios
# Describir una tabla: una variable, grupos, dos variables y una recta
# =============================================================================
#
# LA TABLA (transito_aire_junio2024.csv): una fila por estación y hora
#   estacion   estación de calidad de aire (tres estaciones)
#   hora       fecha y hora de la medición
#   transito   vehículos por hora cerca de la estación
#   no2        dióxido de nitrógeno, promedio de la hora (µg/m³)
#   pm25       material particulado fino, promedio de la hora (µg/m³)
#
# CÓMO SE LEE ESTE ARCHIVO
#   Cada ejercicio tiene un encabezado con cinco rótulos:
#     Qué se busca      el propósito del ejercicio
#     Ya está escrito   el código que viene hecho; no hay que tocarlo
#     Se pide           lo único que hay que escribir, numerado
#     Se verifica       los resultados que tienen que dar
#     En la bitácora    la pregunta que se responde por escrito
#   Los lugares donde hay que escribir están marcados así:
#     # --- COMPLETAR 1 ---
#   La numeración de «Se pide» y la de los COMPLETAR es la misma.
#
#   El archivo se corre de arriba hacia abajo, línea por línea (Ctrl + Enter).
#   Los ejercicios se apoyan en los anteriores: las columnas que se crean en
#   el 2 y el 3 se usan después.
#
# Paquetes (instalar una sola vez):
#   install.packages(c("dplyr", "readr", "lubridate", "ggplot2"))
# =============================================================================

library(dplyr)
library(readr)
library(lubridate)
library(ggplot2)

RUTA <- "clases/clase10/transito_aire_junio2024.csv"
# Si la ruta no existe desde el directorio actual de trabajo, buscarla relativamente:
if (!file.exists(RUTA)) {
  if (file.exists("../clase10/transito_aire_junio2024.csv")) {
    RUTA <- "../clase10/transito_aire_junio2024.csv"
  } else if (file.exists(file.path("..", "..", RUTA))) {
    RUTA <- file.path("..", "..", RUTA)
  }
}

theme_set(theme_minimal(base_size = 12))

# Colores utilizados en los gráficos
COL_TRANSITO <- "#2E86AB"
COL_NO2      <- "#7B4B2A"
COL_PM25     <- "#D4A373"
COL_OSCURO   <- "#5C3A21"

# -----------------------------------------------------------------------------
# Carga e inicialización de la tabla 'datos' (base del análisis)
# -----------------------------------------------------------------------------
aire <- read_csv(RUTA, show_col_types = FALSE)

datos <- aire |>
  mutate(h         = hour(hora),
         dia       = as_date(hora),
         tipo_dia  = ifelse(wday(hora, week_start = 1) >= 6,
                            "fin de semana", "lunes a viernes"),
         franja    = case_when(h <= 5  ~ "madrugada",
                               h <= 11 ~ "mañana",
                               h <= 17 ~ "tarde",
                               TRUE    ~ "noche"),
         hora_pico = ifelse(h %in% c(7, 8, 9, 17, 18, 19), "hora pico", "resto")) |>
  mutate(franja = factor(franja,
                         levels = c("madrugada", "mañana", "tarde", "noche"))) |>
  group_by(estacion) |>
  mutate(transito_rel   = transito / mean(transito),
         nivel_transito = ntile(transito, 3)) |>
  ungroup() |>
  mutate(nivel_transito = factor(nivel_transito, levels = 1:3,
                                 labels = c("bajo", "medio", "alto")),
         transito_miles = transito / 1000,
         log_pm25       = log(pm25))

# Subconjuntos y tablas resumen auxiliares
tc <- datos |> filter(estacion == "Tres Cruces", !is.na(no2))

por_franja <- datos |>
  group_by(estacion, franja) |>
  summarise(transito     = mean(transito),
            transito_rel = mean(transito_rel),
            no2          = mean(no2, na.rm = TRUE),
            pm25         = mean(pm25, na.rm = TRUE),
            .groups      = "drop")



# =============================================================================
# EJERCICIO 1. FALTANTES
# =============================================================================
# En la Parte 1 se contaron los faltantes de la tabla aire:
#
# faltantes <- aire |>
#   group_by(estacion) |>
#   summarise(filas        = n(),
#             sin_transito = sum(is.na(transito)),
#             sin_no2      = sum(is.na(no2)),
#             sin_pm25     = sum(is.na(pm25)))
#
# Contar los faltantes de la tabla datos, agregando las variables nuevas:
# franja, tipo_dia, transito_rel y log_pm25.
# -----------------------------------------------------------------------------

faltantes_datos <- datos |>
  group_by(estacion) |>
  summarise(filas            = n(),
            sin_transito     = sum(is.na(transito)),
            sin_no2          = sum(is.na(no2)),
            sin_pm25         = sum(is.na(pm25)),
            sin_franja       = sum(is.na(franja)),
            sin_tipo_dia     = sum(is.na(tipo_dia)),
            sin_transito_rel = sum(is.na(transito_rel)),
            sin_log_pm25     = sum(is.na(log_pm25)))

print(faltantes_datos)


# =============================================================================
# EJERCICIO 2. ¿ESTÁ BIEN DEFINIDA LA HORA PICO?
# =============================================================================
# En la Parte 2 se creó hora_pico: las horas 7, 8, 9, 17, 18 y 19.
# El gráfico muestra el tránsito promedio de cada hora del día en Tres Cruces,
# de lunes a viernes, con las horas pico en color.

por_hora <- datos |>
  filter(estacion == "Tres Cruces", tipo_dia == "lunes a viernes") |>
  group_by(h, hora_pico) |>
  summarise(transito = mean(transito), .groups = "drop")

ggplot(por_hora, aes(h, transito, fill = hora_pico)) +
  geom_col() +
  scale_fill_manual(values = c("hora pico" = "#5C3A21", "resto" = "grey75")) +
  labs(title = "Tránsito promedio por hora del día, Tres Cruces, lunes a viernes",
       x = "Hora del día", y = "Vehículos por hora", fill = NULL)

# 1. Mirar el gráfico: ¿las horas en color son las de más tránsito?
#    Anotar qué horas están mal clasificadas.
# 2. Crear en datos una variable nueva, con el nombre que elijan, que marque
#    las horas que según el gráfico tienen más tránsito.
# 3. Repetir el gráfico usando la variable nueva en lugar de hora_pico.
# -----------------------------------------------------------------------------
# --- COMPLETAR 2 ---
# Creamos la variable 'alto_transito' para horas de mayor tránsito continuo (8 a 18 h):
datos <- datos |>
  mutate(alto_transito = ifelse(h >= 8 & h <= 18, "alto tránsito", "resto"))

# Actualizamos también en tc si existe:
if (exists("tc")) {
  tc <- tc |>
    mutate(alto_transito = ifelse(h >= 8 & h <= 18, "alto tránsito", "resto"))
}

# --- COMPLETAR 3 ---
por_hora_corregido <- datos |>
  filter(estacion == "Tres Cruces", tipo_dia == "lunes a viernes") |>
  group_by(h, alto_transito) |>
  summarise(transito = mean(transito), .groups = "drop")

g_hora_corregido <- ggplot(por_hora_corregido, aes(h, transito, fill = alto_transito)) +
  geom_col() +
  scale_fill_manual(values = c("alto tránsito" = "#5C3A21", "resto" = "grey75")) +
  labs(title = "Tránsito promedio por hora del día, Tres Cruces, lunes a viernes",
       subtitle = "Definición corregida: alto tránsito continuo (8 a 18 h)",
       x = "Hora del día", y = "Vehículos por hora", fill = NULL)
print(g_hora_corregido)

# =============================================================================
# EJERCICIO 3. PM2.5 POR FRANJA HORARIA
# =============================================================================
# El gráfico g9 muestra el tránsito relativo por franja horaria.
# La tabla por_franja también tiene el promedio de pm25.
#
# 1. Copiar el código de g9 y cambiarlo para graficar pm25 en lugar de
#    transito_rel. Cambiar también el título, el nombre del eje y el color
#    (COL_PM25).
# 2. La línea punteada en 1 ya no tiene sentido: sacarla.
# 3. ¿En qué franja es máximo el PM2.5? ¿Coincide con la del tránsito?
# -----------------------------------------------------------------------------
# --- COMPLETAR 1 y 2 ---
g_pm25_franja <- ggplot(por_franja, aes(franja, pm25)) +
  geom_col(fill = COL_PM25) +
  facet_wrap(~ estacion) +
  labs(title = "PM2.5 promedio por franja horaria",
       x = "Franja horaria", y = "PM2.5 (µg/m³)")
print(g_pm25_franja)


# =============================================================================
# EJERCICIO 4. AGREGAR UNA VARIABLE AL MODELO
# =============================================================================
# El modelo modelo_tc3 explica el NO2 con el tránsito y el PM2.5:
#
# modelo_tc3 <- lm(no2 ~ transito_miles + pm25, data = tc)
# coef(modelo_tc3)
# summary(modelo_tc3)$r.squared
#
# 1. Copiar el código y agregar la variable franja al modelo.
#    Guardarlo como modelo_tc4.
# 2. Mostrar los coeficientes y el R².
# 3. ¿Mejoró el R²? ¿Mucho o poco?
# -----------------------------------------------------------------------------
modelo_tc3 <- lm(no2 ~ transito_miles + pm25, data = tc)

# --- COMPLETAR 1 ---
modelo_tc4 <- lm(no2 ~ transito_miles + pm25 + franja, data = tc)

# --- COMPLETAR 2 ---
cat("--- Coeficientes de modelo_tc4 ---\n")
print(coef(modelo_tc4))

cat("\nR² de modelo_tc3:", summary(modelo_tc3)$r.squared, "\n")
cat("R² de modelo_tc4:", summary(modelo_tc4)$r.squared, "\n")
summary(modelo_tc4)


# =============================================================================
# EJERCICIO 5. UNA VARIABLE BINARIA A PARTIR DEL RESULTADO
# =============================================================================
# En summary(modelo_tc4), de las tres franjas solo la noche tiene un
# coeficiente que se distingue de cero.
#
# 1. Crear en tc la variable noche: vale 1 si la franja es "noche" y 0 si no.
# 2. Ajustar modelo_tc5 con transito_miles, pm25 y noche (sin franja).
# 3. Mostrar los coeficientes y el R². ¿Cuánto suma la noche?
# -----------------------------------------------------------------------------
# --- COMPLETAR 1 ---
tc <- tc |>
  mutate(noche = ifelse(franja == "noche", 1, 0))

# --- COMPLETAR 2 ---
modelo_tc5 <- lm(no2 ~ transito_miles + pm25 + noche, data = tc)

# --- COMPLETAR 3 ---
cat("--- Coeficientes de modelo_tc5 ---\n")
print(coef(modelo_tc5))

cat("\nR² de modelo_tc5:", summary(modelo_tc5)$r.squared, "\n")
summary(modelo_tc5)


# =============================================================================
# EJERCICIO 6. Interacciones
# =============================================================================

COL_FRANJA <- c("madrugada" = "#0072B2", "mañana" = "#E69F00",
                "tarde" = "#009E73", "noche" = "#CC79A7")

g17 <- ggplot(tc, aes(transito_miles, no2, color = franja)) +
  geom_point(size = 2.5, alpha = 0.6) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 1.2) +
  scale_color_manual(values = COL_FRANJA) +
  labs(title = "Tránsito y NO2 en Tres Cruces, por franja horaria",
       x = "Miles de vehículos por hora", y = "NO2 (µg/m³)", color = NULL)
print(g17)
# Qué vemos: cada franja tiene su recta, y no son paralelas. En la madrugada
#   el NO2 sube mucho más rápido con el tránsito que en el resto del día.

# En el gráfico g17 una de las cuatro rectas tiene una pendiente distinta
# de las demás. El modelo con interacción se escribió así:
#
# modelo_tc6 <- lm(no2 ~ transito_miles * franja, data = tc)
#
# 1. Mirar el gráfico: ¿qué franja tiene la recta más empinada?
# 2. Crear en tc una variable binaria para esa franja (1 si la hora
#    pertenece a esa franja, 0 si no).
# 3. Ajustar modelo_tc7 con la interacción entre transito_miles y la
#    variable nueva. Mostrar los coeficientes y el R²
# --- COMPLETAR 2 ---
tc <- tc |>
  mutate(madrugada = ifelse(franja == "madrugada", 1, 0))

# --- COMPLETAR 3 ---
modelo_tc7 <- lm(no2 ~ transito_miles * madrugada, data = tc)

cat("--- Coeficientes de modelo_tc7 ---\n")
print(coef(modelo_tc7))

cat("\nR² de modelo_tc7:", summary(modelo_tc7)$r.squared, "\n")
summary(modelo_tc7)

# =============================================================================
# EJERCICIO 7. ¿QUÉ PASA EN LA TARDE?
# =============================================================================
# En el gráfico g17 los puntos de la tarde forman dos grupos separados.
#
# 1. Crear la tabla tarde con las filas de tc cuya franja es "tarde".
# 2. Copiar el código de g17 y cambiarlo para usar la tabla tarde y
#    colorear por tipo_dia en lugar de franja.
# 3. ¿Qué son los dos grupos?
# -----------------------------------------------------------------------------
# --- COMPLETAR 1 ---
tarde <- tc |>
  filter(franja == "tarde")

# --- COMPLETAR 2 ---
g_tarde <- ggplot(tarde, aes(transito_miles, no2, color = tipo_dia)) +
  geom_point(size = 2.5, alpha = 0.6) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 1.2) +
  scale_color_manual(values = c("fin de semana" = "#D4A373", "lunes a viernes" = "#2E86AB")) +
  labs(title = "Tránsito y NO2 en Tres Cruces (Tarde)",
       subtitle = "Separado según tipo de día",
       x = "Miles de vehículos por hora", y = "NO2 (µg/m³)", color = NULL)
print(g_tarde)
