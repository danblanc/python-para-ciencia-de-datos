# Proyectos finales del curso

En la presente carpeta se recibirán los proyectos finales del curso. Los mismos serán evaluados por los siguientes criterios:

Num| Concepto | Puntos |
-------- | -------- | ------- |
1 | Utiliza una fuente de datos vinculada al INE  | 10 |
2 | Obtiene, manipula y transforma datos utilizando Pandas | 20 |
3 | Genera un dashboard interactivo con visualizaciones y filtros    | 30 |
4 | Utiliza buenas prácticas de programación y documentación en el código | 10 |

**El total de puntos será de 70 y el mínimo para aprobar será de 50**

## Requerimientos del proyecto final

El proyecto final será una carpeta que se entregará mediante un `pull request` a este repositorio, a través de alguna cuenta de Github de los integrantes de los equipos. 

La carpeta del proyecto final deberá contener:

1. Un archivo `README.md` en donde se deberá detallar en código markdown lo realizado por el equipo:
    - El problema que busca resolver.
    - El origen y razón de los datos que maneja
    - La solución planteada
2. Un archivo `script.ipynb`, que será una jupyter notebook que combinará el uso de Python para analizar y transformar la data, junto con bloques de markdown que detallarán el procedimiento utilizado. 
3. Un archivo `app.py` que será el dashboard interactivo que se desarrolle.
4. Un archivo `requeriments.txt` que contendrá un listado de los paquetes utilizados y sus versiones.
5. Una carpeta `data` con toda la data que se utilice en caso que se haga.
6. Si se utilizan contraseñas o claves en el código, no deberán enviarse en el `pull request`, sino que se enviarán por un método seguro al docente para que pueda reproducir el resultado.

> El dashboard se evaluará creando un entorno virtual e instalando dentro los paquetes del archivo `requirements.txt`. Luego, se ejecutará el comando ´streamlit run app.py` y el dashboard deberá aparecer. Si no aparece, se considerará que no funciona. Se recomienda testear este procedimiento en otra PC antes de enviar. 

### Procedimiento para hacer el `pull request`

1. Descargue el repositorio localmente

```bash
git clone https://github.com/danblanc/python-para-ciencia-de-datos.git
```

2. Cree una nueva rama para trabajar

```bash
cd python-para-ciencia-de-datos
git checkout -b mi_proyecto_algo_nombre_coso
```

3. Desarrolle su solución y cuando termine de trabajar agregue sus cambios a git

```bash
git add la_carpeta_de_mi_proyecto
git commit -m "Mensaje para que mis compas sepan qué hice hoy"
```

4. Pushee sus cambios a la nube de modo que sus compañeros al trabajar en su rama puedan acceder a sus cambios.

```bash
git push origin
```

5. Cuando al siguiente día comience a trabajar, recuerde obtener la última versión de la rama en donde estén trabajando.

```bash
git pull
```

6. Al terminar, hacer un `compare and pull request` con la rama main del repositorio


### Procedimiento para generar el archivo `requirements.txt`

1. Cree un entorno virtual local. 

```bash
pip install virtualenv
python -m venv mi_entorno_virtual
```

2. Instale los paquetes que necesita y desarrolle su trabajo. 

3. Al terminar, exporte sus paquetes y versiones a un archivo `requirements.txt`

```bash
pip freeze > requirements.txt
```

4. Si está comenzando a trabajar a partir de algo que hizo otro compañero, puede instalar los paquetes en su entorno virtual de la siguiente manera:

```bash
pip install -r requirements.txt
```