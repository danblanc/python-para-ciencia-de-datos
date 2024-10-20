# Proyecto:

# Detección de edificaciones en imágenes satelitales o de vuelos

Integrantes del equipo: __Carlos Chabay__

__Antecedentes:__

	Dentro de las tareas del área de Geomática se encuentra la detección de nuevas edificaciones
	en el territorio nacional. Dicha tarea en el INE se realiza manualmente por operadores GIS y
	se le dedica mucho tiempo.

__Objetivos:__

	Esta tarea se puede realizar automáticamente con la asistencia de herramientas como YOLO que
	permiten detectar objetos (edificaciones en este caso) en imágenes satelitales o vuelos.
	Estas herramientas requieren workstations muy potentes con tarjeta aceleradora gráfica que el
	INE actualmente no tiene pero que está en proceso de adquirirlas.
	
	El objetivo de este proyecto es identificar las imágenes del territorio nacional que contengan
	edificaciones. Esta clasificación la realiza el jupyter notebook proyecto_img_ia.ipynb utilizando
	GPT-4o de OpenAI. Itera sobre todas las imágenes de la carpeta data y genera un archivo
	result_edific.csv con el resultado de la identificación de edificaciones para cada imágen.
	Las imágenes catalogadas con edificios van a ser el input del futuro entrenar proceso de
	identificación de cambios entre períodos utilizando YOLOv8.

__Datos originales:__

	Se utilizaron 37 imágenes urbanas y rurales en escala 1:2029 generadas por el área de Geomática

__Nota:__

	Se suprimió el valor de la variable api_key para poder publicar este notebook
	en forma segura en git, se deberá agregar el valor para ejecutarlo.
