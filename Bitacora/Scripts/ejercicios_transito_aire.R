# =============================================================================
# TrÃ¡nsito y calidad del aire, junio de 2024 â Ejercicios
# Describir una tabla: una variable, grupos, dos variables y una recta
# =============================================================================
#
# LA TABLA (transito_aire_junio2024.csv): una fila por estaciÃ³n y hora
#   estacion   estaciÃ³n de calidad de aire (tres estaciones)
#   hora       fecha y hora de la mediciÃ³n
#   transito   vehÃ­culos por hora cerca de la estaciÃ³n
#   no2        diÃ³xido de nitrÃ³geno, promedio de la hora (Âµg/mÂ³)
#   pm25       material particulado fino, promedio de la hora (Âµg/mÂ³)
#
# CÃMO SE LEE ESTE ARCHIVO
#   Cada ejercicio tiene un encabezado con cinco rÃ³tulos:
#     QuÃ© se busca      el propÃ³sito del ejercicio
#     Ya estÃ¡ escrito   el cÃ³digo que viene hecho; no hay que tocarlo
#     Se pide           lo Ãºnico que hay que escribir, numerado
#     Se verifica       los resultados que tienen que dar
#     En la bitÃ¡cora    la pregunta que se responde por escrito
#   Los lugares donde hay que escribir estÃ¡n marcados asÃ­:
#     # --- COMPLETAR 1 ---
#   La numeraciÃ³n de Â«Se pideÂ» y la de los COMPLETAR es la misma.
#
#   El archivo se corre de arriba hacia abajo, lÃ­nea por lÃ­nea (Ctrl + Enter).
#   Los ejercicios se apoyan en los anteriores: las columnas que se crean en
#   el 2 y el 3 se usan despuÃ©s.
#
# Paquetes (instalar una sola vez):
#   install.packages(c("dplyr", "readr", "lubridate", "ggplot2"))
# =============================================================================

library(dplyr)
library(readr)
library(lubridate)
library(ggplot2)

RUTA <- file.path("Bitacora", "Data", "transito_aire_junio2024.csv")
# Búsqueda robusta en distintas ubicaciones relativas
candidatos_ruta <- c(
  RUTA,
  file.path("..", "Data", "transito_aire_junio2024.csv"),
  file.path("Data", "transito_aire_junio2024.csv"),
  file.path("..", "..", "Bitacora", "Data", "transito_aire_junio2024.csv"),
  "clases/clase10/transito_aire_junio2024.csv",
  "../clase10/transito_aire_junio2024.csv"
)
for (cand in candidatos_ruta) {
  if (file.exists(cand)) {
    RUTA <- cand
    break
  }
}

theme_set(theme_minimal(base_size = 12))

# Colores utilizados en los grÃ¡ficos
COL_TRANSITO <- "#2E86AB"
COL_NO2      <- "#7B4B2A"
COL_PM25     <- "#D4A373"
COL_OSCURO   <- "#5C3A21"

# -----------------------------------------------------------------------------
# Carga e inicializaciÃ³n de la tabla 'datos' (base del anÃ¡lisis)
# -----------------------------------------------------------------------------
aire <- read_csv(RUTA, show_col_types = FALSE)

datos <- aire |>
  mutate(h         = hour(hora),
         dia       = as_date(hora),
         tipo_dia  = ifelse(wday(hora, week_start = 1) >= 6,
                            "fin de semana", "lunes a viernes"),
         franja    = case_when(h <= 5  ~ "madrugada",
                               h <= 11 ~ "maÃ±ana",
                               h <= 17 ~ "tarde",
                               TRUE    ~ "noche"),
         hora_pico = ifelse(h %in% c(7, 8, 9, 17, 18, 19), "hora pico", "resto")) |>
  mutate(franja = factor(franja,
                         levels = c("madrugada", "maÃ±ana", "tarde", "noche"))) |>
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
# EJERCICIO 2. Â¿ESTÃ BIEN DEFINIDA LA HORA PICO?
# =============================================================================
# En la Parte 2 se creÃ³ hora_pico: las horas 7, 8, 9, 17, 18 y 19.
# El grÃ¡fico muestra el trÃ¡nsito promedio de cada hora del dÃ­a en Tres Cruces,
# de lunes a viernes, con las horas pico en color.

por_hora <- datos |>
  filter(estacion == "Tres Cruces", tipo_dia == "lunes a viernes") |>
  group_by(h, hora_pico) |>
  summarise(transito = mean(transito), .groups = "drop")

ggplot(por_hora, aes(h, transito, fill = hora_pico)) +
  geom_col() +
  scale_fill_manual(values = c("hora pico" = "#5C3A21", "resto" = "grey75")) +
  labs(title = "TrÃ¡nsito promedio por hora del dÃ­a, Tres Cruces, lunes a viernes",
       x = "Hora del dÃ­a", y = "VehÃ­culos por hora", fill = NULL)

# 1. Mirar el grÃ¡fico: Â¿las horas en color son las de mÃ¡s trÃ¡nsito?
#    Anotar quÃ© horas estÃ¡n mal clasificadas.
# 2. Crear en datos una variable nueva, con el nombre que elijan, que marque
#    las horas que segÃºn el grÃ¡fico tienen mÃ¡s trÃ¡nsito.
# 3. Repetir el grÃ¡fico usando la variable nueva en lugar de hora_pico.
# -----------------------------------------------------------------------------
# --- COMPLETAR 2 ---
# Creamos la variable 'alto_transito' para horas de mayor trÃ¡nsito continuo (8 a 18 h):
datos <- datos |>
  mutate(alto_transito = ifelse(h >= 8 & h <= 18, "alto trÃ¡nsito", "resto"))

# Actualizamos tambiÃ©n en tc si existe:
if (exists("tc")) {
  tc <- tc |>
    mutate(alto_transito = ifelse(h >= 8 & h <= 18, "alto trÃ¡nsito", "resto"))
}

# --- COMPLETAR 3 ---
por_hora_corregido <- datos |>
  filter(estacion == "Tres Cruces", tipo_dia == "lunes a viernes") |>
  group_by(h, alto_transito) |>
  summarise(transito = mean(transito), .groups = "drop")

g_hora_corregido <- ggplot(por_hora_corregido, aes(h, transito, fill = alto_transito)) +
  geom_col() +
  scale_fill_manual(values = c("alto trÃ¡nsito" = "#5C3A21", "resto" = "grey75")) +
  labs(title = "TrÃ¡nsito promedio por hora del dÃ­a, Tres Cruces, lunes a viernes",
       subtitle = "DefiniciÃ³n corregida: alto trÃ¡nsito continuo (8 a 18 h)",
       x = "Hora del dÃ­a", y = "VehÃ­culos por hora", fill = NULL)
print(g_hora_corregido)

# =============================================================================
# EJERCICIO 3. PM2.5 POR FRANJA HORARIA
# =============================================================================
# El grÃ¡fico g9 muestra el trÃ¡nsito relativo por franja horaria.
# La tabla por_franja tambiÃ©n tiene el promedio de pm25.
#
# 1. Copiar el cÃ³digo de g9 y cambiarlo para graficar pm25 en lugar de
#    transito_rel. Cambiar tambiÃ©n el tÃ­tulo, el nombre del eje y el color
#    (COL_PM25).
# 2. La lÃ­nea punteada en 1 ya no tiene sentido: sacarla.
# 3. Â¿En quÃ© franja es mÃ¡ximo el PM2.5? Â¿Coincide con la del trÃ¡nsito?
# -----------------------------------------------------------------------------
# --- COMPLETAR 1 y 2 ---
g_pm25_franja <- ggplot(por_franja, aes(franja, pm25)) +
  geom_col(fill = COL_PM25) +
  facet_wrap(~ estacion) +
  labs(title = "PM2.5 promedio por franja horaria",
       x = "Franja horaria", y = "PM2.5 (Âµg/mÂ³)")
print(g_pm25_franja)


# =============================================================================
# EJERCICIO 4. AGREGAR UNA VARIABLE AL MODELO
# =============================================================================
# El modelo modelo_tc3 explica el NO2 con el trÃ¡nsito y el PM2.5:
#
# modelo_tc3 <- lm(no2 ~ transito_miles + pm25, data = tc)
# coef(modelo_tc3)
# summary(modelo_tc3)$r.squared
#
# 1. Copiar el cÃ³digo y agregar la variable franja al modelo.
#    Guardarlo como modelo_tc4.
# 2. Mostrar los coeficientes y el RÂ².
# 3. Â¿MejorÃ³ el RÂ²? Â¿Mucho o poco?
# -----------------------------------------------------------------------------
modelo_tc3 <- lm(no2 ~ transito_miles + pm25, data = tc)

# --- COMPLETAR 1 ---
modelo_tc4 <- lm(no2 ~ transito_miles + pm25 + franja, data = tc)

# --- COMPLETAR 2 ---
cat("--- Coeficientes de modelo_tc4 ---\n")
print(coef(modelo_tc4))

cat("\nRÂ² de modelo_tc3:", summary(modelo_tc3)$r.squared, "\n")
cat("RÂ² de modelo_tc4:", summary(modelo_tc4)$r.squared, "\n")
summary(modelo_tc4)


# =============================================================================
# EJERCICIO 5. UNA VARIABLE BINARIA A PARTIR DEL RESULTADO
# =============================================================================
# En summary(modelo_tc4), de las tres franjas solo la noche tiene un
# coeficiente que se distingue de cero.
#
# 1. Crear en tc la variable noche: vale 1 si la franja es "noche" y 0 si no.
# 2. Ajustar modelo_tc5 con transito_miles, pm25 y noche (sin franja).
# 3. Mostrar los coeficientes y el RÂ². Â¿CuÃ¡nto suma la noche?
# -----------------------------------------------------------------------------
# --- COMPLETAR 1 ---
tc <- tc |>
  mutate(noche = ifelse(franja == "noche", 1, 0))

# --- COMPLETAR 2 ---
modelo_tc5 <- lm(no2 ~ transito_miles + pm25 + noche, data = tc)

# --- COMPLETAR 3 ---
cat("--- Coeficientes de modelo_tc5 ---\n")
print(coef(modelo_tc5))

cat("\nRÂ² de modelo_tc5:", summary(modelo_tc5)$r.squared, "\n")
summary(modelo_tc5)


# =============================================================================
# EJERCICIO 6. Interacciones
# =============================================================================

COL_FRANJA <- c("madrugada" = "#0072B2", "maÃ±ana" = "#E69F00",
                "tarde" = "#009E73", "noche" = "#CC79A7")

g17 <- ggplot(tc, aes(transito_miles, no2, color = franja)) +
  geom_point(size = 2.5, alpha = 0.6) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 1.2) +
  scale_color_manual(values = COL_FRANJA) +
  labs(title = "TrÃ¡nsito y NO2 en Tres Cruces, por franja horaria",
       x = "Miles de vehÃ­culos por hora", y = "NO2 (Âµg/mÂ³)", color = NULL)
print(g17)
# QuÃ© vemos: cada franja tiene su recta, y no son paralelas. En la madrugada
#   el NO2 sube mucho mÃ¡s rÃ¡pido con el trÃ¡nsito que en el resto del dÃ­a.

# En el grÃ¡fico g17 una de las cuatro rectas tiene una pendiente distinta
# de las demÃ¡s. El modelo con interacciÃ³n se escribiÃ³ asÃ­:
#
# modelo_tc6 <- lm(no2 ~ transito_miles * franja, data = tc)
#
# 1. Mirar el grÃ¡fico: Â¿quÃ© franja tiene la recta mÃ¡s empinada?
# 2. Crear en tc una variable binaria para esa franja (1 si la hora
#    pertenece a esa franja, 0 si no).
# 3. Ajustar modelo_tc7 con la interacciÃ³n entre transito_miles y la
#    variable nueva. Mostrar los coeficientes y el RÂ²
# --- COMPLETAR 2 ---
tc <- tc |>
  mutate(madrugada = ifelse(franja == "madrugada", 1, 0))

# --- COMPLETAR 3 ---
modelo_tc7 <- lm(no2 ~ transito_miles * madrugada, data = tc)

cat("--- Coeficientes de modelo_tc7 ---\n")
print(coef(modelo_tc7))

cat("\nRÂ² de modelo_tc7:", summary(modelo_tc7)$r.squared, "\n")
summary(modelo_tc7)

# =============================================================================
# EJERCICIO 7. Â¿QUÃ PASA EN LA TARDE?
# =============================================================================
# En el grÃ¡fico g17 los puntos de la tarde forman dos grupos separados.
#
# 1. Crear la tabla tarde con las filas de tc cuya franja es "tarde".
# 2. Copiar el cÃ³digo de g17 y cambiarlo para usar la tabla tarde y
#    colorear por tipo_dia en lugar de franja.
# 3. Â¿QuÃ© son los dos grupos?
# -----------------------------------------------------------------------------
# --- COMPLETAR 1 ---
tarde <- tc |>
  filter(franja == "tarde")

# --- COMPLETAR 2 ---
g_tarde <- ggplot(tarde, aes(transito_miles, no2, color = tipo_dia)) +
  geom_point(size = 2.5, alpha = 0.6) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 1.2) +
  scale_color_manual(values = c("fin de semana" = "#D4A373", "lunes a viernes" = "#2E86AB")) +
  labs(title = "TrÃ¡nsito y NO2 en Tres Cruces (Tarde)",
       subtitle = "Separado segÃºn tipo de dÃ­a",
       x = "Miles de vehÃ­culos por hora", y = "NO2 (Âµg/mÂ³)", color = NULL)
print(g_tarde)
