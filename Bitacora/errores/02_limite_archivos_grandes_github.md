# Error 02: GitHub me rebotó el push por archivos gigantes (>100 MB)

## Qué me pasó
Metí un commit con los datos de tránsito de Montevideo y cuando tiré `git push origin main` me salió este cartel rojo gigante:
```text
remote: error: GH001: Large files detected.
remote: error: File Bitacora/Data/autoscope_06_2024_volumen.csv is 317.30 MB; this exceeds GitHub's file size limit of 100.00 MB
To https://github.com/Fabricio552/Repositorio-Personal.git
 ! [remote rejected] main -> main (pre-receive hook declined)
```

## Por qué pasó
Los archivos de los sensores de Autoscope (`autoscope_04_2024_volumen.csv` y `autoscope_06_2024_volumen.csv`) pesan casi 300 y 330 MB. GitHub tiene un límite estricto de 100 MB por archivo en repositorios comunes.

## Cómo me di cuenta
Al momento de intentar sincronizar con el repositorio remoto.

## Cómo lo arreglé
1. Saqué los archivos pesados del commit con `git restore --staged`.
2. Actualicé el `.gitignore` para que ignore automáticamente cualquier archivo `.csv` o `.xlsx` pesado en `Data/`, dejando solo como excepción los datasets chicos de práctica:
   ```gitignore
   Bitacora/Data/*.csv
   !Bitacora/Data/12561_tasa_de_empleo_segun_nivel_educativo-_total_pais.csv
   !Bitacora/Data/transito_aire_junio2024.csv
   ```
3. Me quedó grabada la regla del curso: **en Git se versiona el código que procesa los datos, pero los datos crudos masivos no se suben al repositorio**.
