# Bitácora Semana 10 — 13/10 al 17/10
**Tema:** Rebotado por GitHub y el .gitignore  
**Estudiante:** Fabricio De Souza

---

## Qué intenté
Subir los scripts actualizados de visualización y tener el repositorio al día para que el profe pudiera revisar los avances.

## Qué falló
Al hacer `git push` GitHub me rebotó el commit porque tenía los CSVs grandes de tránsito (de casi 300 y 330 MB) y el límite por archivo es de 100 MB.

## Qué decidí
Armar un `.gitignore` en serio para que ningún CSV pesado vuelva a entrar al repositorio, recordando lo que dijo la profe en clase: los datos crudos gigantes se descargan o procesan con scripts, pero no se suben a Git.
