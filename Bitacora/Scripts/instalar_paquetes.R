# =============================================================================
# Script de instalación de paquetes necesarios en R
# Curso: Introducción a la Ciencia de Datos (FCEE - Universidad de Montevideo)
# =============================================================================

paquetes_necesarios <- c("dplyr", "readr", "lubridate", "ggplot2", "patchwork")

paquetes_faltantes <- paquetes_necesarios[!(paquetes_necesarios %in% installed.packages()[, "Package"])]

if (length(paquetes_faltantes) > 0) {
  message("Instalando paquetes faltantes: ", paste(paquetes_faltantes, collapse = ", "))
  install.packages(paquetes_faltantes, repos = "https://cloud.r-project.org")
} else {
  message("Todos los paquetes requeridos de R ya se encuentran instalados.")
}

