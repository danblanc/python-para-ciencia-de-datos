# Proyecto:

# Transformación de datos y generación de Dashboard de Farmacias

Integrantes del equipo: __Ana Inés López, Luis Vázquez, Carlos Chabay__

__Antecedentes:__

	
    Para la habilitación de las farmacias de primera categoría, los emprendedores deben presentar
	ante el MSP, entre otros documentos, una constancia expedida por el INE con la población
	que vive en un radio de 1 km a la redonda de la ubicación prevista
	(https://www.gub.uy/tramites/habilitacion-apertura-farmacia-primera-categoria).
	Por otra parte, el MSP rechaza la instalación si la población anteriormente descrita es
	menor a 3.000 habitantes.
	A los efectos de evitar inconvenientes y pérdidas de tiempo y recursos, se entiende
	pertinente que el MSP pueda contar con esta herramienta y evitar que los emprendedores tengan
	que recurrir al INE para lograr que se apruebe el trámite.

__Objetivos:__

	Los objetivos de este trabajo son:

		- Calcular la cantidad de farmacias por departamento, pudiéndose filtrar la información
			por uno o mas departamentos.
		- Desplegar sobre un mapa del Uruguay las farmacias georreferenciadas, pudiéndose
			filtrar las farmacias por uno o mas departamentos
			y por el nombre o parte del nombre de la farmacia.
		- Presentar dos cuadros con casos atípicos de farmacias por localidades:
			- Localidades con mas de 3.000 habitantes que no tienen farmacias dentro de su
				área de influencia de 1 km
			- Localidades con menos de 3.000 habitantes que tienen una o mas farmacias dentro
				de su área de influencia de 1 km


__NOTAS:__
 • Podría haber farmacias que no figuran en la capa usada para este trabajo.
 • Los datos de población corresponden al Censo 2011 dado que no están disponibles los
 	del Censo 2023.
 • Este ejercicio es sólo un esbozo de lo que podría ser un servicio en la página
 	del INE, que incluyera un mapa de las zonas censales con la cantidad de personas
	y que los usuarios pudieran procesar en línea la población para sus áreas de interés.

__Datos originales:__

Archivo | Datos que contiene | Formato | Ubicación |
-------- | -------- | ------- | ------- |
Marco_2011 | Marco censo 2011  | dbf | https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/estadisticas/marcos-censales |
Ine_zonas_11 | Capa de zonas censo 2011 | shp | https://www.gub.uy/instituto-nacional-estadistica/datos-y-estadisticas/estadisticas/mapas-vectoriales-ano-2011 |
Farmacias | Farmacias habilitadas de primera categoría | gpck | Base de datos de Geomática |

• __Procedimiento:__

	En QGIS:

		1. Incorporar las dos capas y el marco

		2. Asociar marco a capa de zonas (resultado: Geopackage zonas_con_pob)

		3. Generar área de influencia de las farmacias de radio 1 km
			(resultado: Geopackage buffer_1_km)

		4. Asignar datos de área de influencia a zonas_con_pob
			(resultado: Geopackage buffer_1_km)

		5. Exportar la tabla de zonas a nivel país con los datos asociados de cantidad
			de población y del área de influencia de farmacia a la que pertenece si
			correspondiera (resultado: csv intersección_zonas_buffer)

	Procesamiento python:

		1. Calcular la cantidad de farmacias por departamento
			(resultado: csv farmacias_departamento).
			Procedimiento:
				• en tabla intersección_zonas_buffer group by NOMBDEPTO y suma farmacias
					(NOMBRE y DIRECCIÓN) concatenadas
				• Crea archivo farmacias_departamento.csv con cantidad de farmacias
					por departamento

		2. Calcular la cantidad de farmacias en las localidades del interior y analizar si
			hay localidades de más de 3.000 habitantes que no tienen farmacias y localidades
			de menos de 3.000 habitantes que tienen al menos una farmacia

			Procedimiento:
				• En tabla intersección_zonas_buffer group by CODLOC y sum POBLACION
				• En tabla intersección_zonas_buffer group by CODLOC y count farmacias
				• Crea archivo loc_pob_farm.csv con población y cantidad de farmacias
					por localidad
				• Crea archivo loc_grandes_sin_farm.csv con localidades de más de 3.000
					habitantes sin farmacias
				• Crea archivo loc_chicas_con_farm.csv con localidades de menos de 3.000
					habitantes con al menos una farmacia
