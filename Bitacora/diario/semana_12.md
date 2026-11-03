# Bitácora Semana 12 — 27/10 al 31/10
**Tema:** Limpieza final y armado del portfolio  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Hacer una pasada general por todo el repositorio para verificar que cualquier persona pueda clonarlo y correr los scripts sin que se le rompa nada.

## Qué falló
Me di cuenta de que si corría los scripts desde otra carpeta me saltaba `FileNotFoundError` porque había usado `Path.cwd() / "Repositorio-Personal/..."` hardcodeado.

## Qué decidí
Corregir las rutas en todos los archivos de Python usando `Path(__file__).resolve()`, armar un `requirements.txt` con las librerías necesarias y dejar la bitácora ordenada con las recetas y errores que me fueron pasando.
