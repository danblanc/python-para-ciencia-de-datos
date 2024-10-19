#### Proyecto C.Rey y V.Fernandez

# **ANÁLISIS DE PERMISOS DE OBRA DE LA INTENDENCIA MUNICIPAL DE MONTEVIDEO Y REGISTRO EN LA DIRECCIÓN NACIONAL DE CATASTRO**


## **OBJETIVO:**

### En primera instancia el objetivo del proyecto era verificar la demora en la actualización de las mejoras realizadas en los padrones de Montevideo por parte de la Dirección Nacional de Catastro. 
### Con este objetivo se analizaron las bases de Padrones Urbanos a nivel nacional, con la fecha de la última declaración, que registra todas las superficies afectadas, publicado por la Dirección de Catastro y de los permisos de construcción solicitados publicado por la Intendencia Municipal de Montevideo. 



## **ANÁLISIS Y CONCLUSIONES:**

### Padrones Urbanos de la Dirección Nacional de Catastro tiene información de los padrones de todo el país. Tiene aproximadamente un millon y medio de registros, y 15 variables. Permisos de construcción tiene información de todos los permisos solicitados y aprobados por padrón y superficie afectada por el mismo publicado por la Intendencia Municipal de Montevideo. Tiene aproximadamente unos 39500 registros con informaciónd de 10 variables.

### Desarrollando un análisis descriptivo de las bases, la base de la IM con datos de catastro se encuentra un poco desactualizada ya que las variables de catastro para por ejemplo categoría en 2023  es "Desconocido" esto significa que no tiene información de catastro.

### En los tiempos de demora se nota una efectividad mayor a partir del los 2000 en la IM.

### Links de acceso a las bases:

#### 1. Padrones Urbanos a nivel nacional - Fuente: Dirección Nacional de Catastro - https://catalogodatos.gub.uy/dataset/direccion-nacional-de-catastro-padrones-urbanos-y-rurales/resource/14a3e2e5-a7c4-4795-8baf-f56691765d8e

####  2. Permisos solicitados y aprobados - Fuente: Intendencia Municipal de Montevideo - https://catalogodatos.gub.uy/dataset/permisos-de-construccion-aprobados

### Se procedió a analizar ambas bases, realizando los ajustes correspondientes en cada una de ellas para poder realizar el macheo de ambas (filtrados, eliminación de duplicados, recategoriaciones, conversiones de tipos de datos, etc). 

### Se procedió a machear ambas bases en ambos sentidos utilizando left join, y luego se analizaron las bases resultantes.
### Para realizar este análisis se procedió a realizar diferentes tablas, resultando que al ser diferente la información de las bases originales, el macheo de éstas no proporcionaba inforanción suficiente para poder concluir un resultado sobre el objetivo de la investigación. 

### Como consecuencia de ese problema se cambio el objetivo de la investigación. 

### Se procedió a analizar otra base proveniente de la Intendencia Municipal de Montevideo, Permisos solicitados y aprobados con información de catastro. Esta base cuenta con más de 40000 registros y 15 variables.

#### Permisos solicitados y aprobados con información de catastro - Fuente: Intendencia Municipal de Montevideo - https://intgis.montevideo.gub.uy/sit/php/common/datos/generar_zip2.php?nom_tab=v_mdg_parcelas_geom&tipo=gis

### Se realizaron los ajustes necesarios para analizar la información contenida en esta base (conversión de datos, recateorizaciones, cálculo de días de demora entre que se inicia el trámite y se aprueba, etc.)

### En el dashboard se presentan varios gráficos:


### 1. Cantidad de registros por año y régimen. Muestra la información de la cantidad de registros por año y régimen de propiedad (común, propiedad horizontal y sin código de régimen)

### 2. Área de edificación por tipo de construcción. Muestra el área de edificación por tipo de construcción (Obra nueva, reforma, regularización, demolición, incorporación a propiedad horizontal, sin tipo de obra definido y otros), pero a la vez muestra el destino de esa construcción, si es vivienda, industria, comercio, sin destino definido o varios destinos. 

### 3. Cantidad por Categoría.Muestra la cantidad de registros por categoría de la construcción, economico, , mediano, suntuoso y desconosido. Aquí se aprecia que a partir de 2023 no está actualizada esta información.  

### 4. Cantidad por año y destino. Muestra la cantidad de registros por destino de la construcción, pero por año, y la información es desde 1997 a la fecha. 

### 5. Promedio de tiempos de demora por año. Muestra la evolución del promedio de tiempo de demora entre que se solicita el permiso y se aprueba, desde 1997 a la fecha. Aqui observamos que los tiempos de demora en los primeros años es muy superior a la que hay hoy en día.

### Tanbién se muestra un cuadro comparativo con la cantidad de registros por año para las tres bases utilizadas. 

### Finalmente se presenta un mapa de la ciudad de Montevideo como imagen ya que al subir los shape pesaba mucho y se volvía muy largo el proceso.

### En la primera pestaña se presentan los links a las tres bases y diccionario de las variables donde se pueden seleccionar de a una. 

### Se adjuntan: 

* 1. Archivo Jupyter Notebook: ""
* 2. Archivo Python, para correr el dashboard: ""
* 3. Archivo txt, con listado de los paquetes utilizados.








